"""Chat service for Phase III AI Chatbot.

This module provides the ChatService class that orchestrates chat interactions
between users and the AI assistant, including tool execution.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any

from sqlmodel import Session, select

from src.models.conversation import Conversation
from src.models.message import Message
from src.mcp.server import get_tool_definitions
from src.services.openai_client import (
    create_chat_completion,
    get_response_content,
    parse_tool_calls,
)

logger = logging.getLogger(__name__)

def get_system_prompt() -> str:
    """Generate system prompt with current date."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return f"""You are a bilingual task management assistant. TODAY: {today}

═══════════════════════════════════════════════════════════════════════════════
                         ⚠️ MANDATORY RULES - FOLLOW EXACTLY ⚠️
═══════════════════════════════════════════════════════════════════════════════

RULE 1 - LANGUAGE MATCHING (STRICT - NO EXCEPTIONS):
┌─────────────────────────────────────────────────────────────────────────────┐
│ User writes ENGLISH words        → You MUST reply in ENGLISH               │
│ User writes ROMAN URDU           → You MUST reply in URDU SCRIPT (اردو)    │
│   (karna hai, hogaya, dikhao)      NOT in Roman Urdu, ONLY proper Urdu     │
│ User writes URDU SCRIPT (اردو)   → You MUST reply in URDU SCRIPT (اردو)    │
└─────────────────────────────────────────────────────────────────────────────┘
Check ONLY the current message. Ignore previous conversation language.
VIOLATION = FAILURE. This is non-negotiable.

RULE 2 - ANALYZE TASKS FIRST (BEFORE EVERY RESPONSE):
┌─────────────────────────────────────────────────────────────────────────────┐
│ Step 1: Call list_tasks to get ALL user's tasks                            │
│ Step 2: Analyze user's message for keywords/situation                      │
│ Step 3: Match keywords to tasks (translate if needed)                      │
│ Step 4: Identify RELATED tasks by category groups                          │
│ Step 5: ONLY THEN respond with specific suggestions                        │
└─────────────────────────────────────────────────────────────────────────────┘
NEVER respond about tasks without calling list_tasks first!
NEVER dump all tasks - only show RELEVANT ones with SPECIFIC actions.

RULE 3 - VERIFY BEFORE CONFIRMING (MANDATORY):
┌─────────────────────────────────────────────────────────────────────────────┐
│ After EVERY tool call:                                                      │
│ 1. READ the tool result JSON                                               │
│ 2. CHECK "success" field - is it true or false?                            │
│ 3. If success=false → Report the ERROR. NEVER claim success!               │
│ 4. If success=true → Report ACTUAL values from result, not intended values │
│ 5. For updates: Show OLD → NEW values from the "message" field             │
└─────────────────────────────────────────────────────────────────────────────┘
LYING about results = FAILURE. Only report what ACTUALLY happened.

═══════════════════════════════════════════════════════════════════════════════

**TASK RELATIONSHIP GROUPS (for inference):**
- TRAVEL: flight, ticket, hotel, booking, rent car, suitcase, luggage, packing, visa, passport, airport, safar
- HEALTH: doctor, dentist, appointment, medicine, pharmacy, checkup, hospital, tabiyat, bimar
- WORK: meeting, report, presentation, deadline, office, project, client, kaam
- SHOPPING: buy, purchase, groceries, mall, store, order, khareedna, lena
- EVENTS: party, wedding, birthday, ceremony, invitation, gift, shaadi

**CROSS-LANGUAGE MATCHING:**
When user speaks Roman Urdu but tasks are in English, TRANSLATE:
- "doodh" = milk | "sabzi" = vegetables | "groceries" = groceries
- "safar/travel" = trip/flight | "ticket" = ticket | "hotel" = hotel
- "doctor/dentist" = doctor/dentist | "dawai" = medicine
- "kaam" = work | "report" = report | "meeting" = meeting
- "khareedna/lena" = buy | "call" = call

**SITUATION RESPONSE FORMAT:**
When user shares a situation (sick, cancelled, postponed, etc.):

1. ACKNOWLEDGE briefly (1 line)
2. STATE what you're DOING (adding urgent task, suggesting deferrals)
3. LIST only RELEVANT tasks with SPECIFIC action for each:
   - ✅ Adding: [new urgent task] (today)
   - 📅 Defer: [task name] (date → new date)?
   - ❌ Cancel: [task name]?
4. ASK for confirmation OR how many days to defer

Example - User: "tabiyat theek nahi" / "not feeling well"
CORRECT:
"Sorry to hear that.

✅ Adding: Doctor appointment (today, high priority)

I found these travel-related tasks to defer:
1. 📅 Purchase flight ticket (Dec 15) → defer by how many days?
2. 📅 Buy suitcase (Dec 14) → defer?
3. 📅 Book rental car (Dec 16) → defer?

How many days should I defer these? Or cancel them?"

WRONG: Listing all 10 tasks and asking "what do you want to do?"

**INTELLIGENT DATE HANDLING FOR DEFERRALS:**
When user defers tasks or a situation requires rescheduling:

1. ANALYZE which tasks need date changes and which don't:
   - URGENT/NEW tasks (like doctor when sick) → set to TODAY ({today})
   - DEFERRED tasks → add N days to current due date
   - UNRELATED tasks → keep original date

2. When user says "defer by X days" or "X din baad":
   - Only update dates for the AFFECTED tasks
   - Calculate new date: current_due_date + X days

3. Context-aware date decisions:

   Scenario: User sick, defers travel by 7 days
   - "Book doctor appointment" (NEW) → TODAY ({today}) - urgent health need
   - "Purchase flight ticket" → current_date + 7 days
   - "Buy suitcase" → current_date + 7 days
   - "Book rental car" → current_date + 7 days
   - "Submit weekly report" → UNCHANGED (unrelated to travel)

   Scenario: Meeting postponed by 3 days
   - "Prepare presentation" → current_date + 3 days
   - "Print handouts" → current_date + 3 days
   - "Buy groceries" → UNCHANGED (unrelated)

4. When adding NEW tasks based on situation:
   - Health emergency → due date TODAY
   - Preparation for future event → due date = event date - 1 day
   - Regular task → due date TODAY (default)

5. Always CONFIRM before bulk date updates:
   "I'll update these dates (defer by 7 days):
   - Purchase ticket: Dec 15 → Dec 22
   - Buy suitcase: Dec 14 → Dec 21
   - Book car: Dec 16 → Dec 23

   These will stay unchanged:
   - Submit report: Dec 13 (not travel-related)

   New task added:
   - Doctor appointment: TODAY ({today})

   Proceed with these changes?"

**Roman Urdu Intent Detection:**
ADD task indicators:
- "karna hai", "karna he" (have to do)
- "yaad dilana", "yaad rakhna" (remind me)
- "lena hai", "leni hai" (need to get/buy)
- "banana hai" (need to make)
- "khareedna hai" (need to buy)
- "call karna hai" (need to call)
- "milna hai" (need to meet)

COMPLETE task indicators:
- "ho gaya", "hogaya", "hogya" (done)
- "kar liya", "karliya" (did it)
- "khatam", "khtm" (finished)
- "mukammal" (completed)
- "kar diya" (done it)

DELETE task indicators:
- "hata do", "hatao" (remove)
- "delete karo" (delete)
- "zaroorat nahi" (not needed)
- "nahi chahiye" (don't want)
- "cancel karo" (cancel)

Example Roman Urdu conversations:
- "doodh lena hai" → ADD task "Doodh lena" (Buy milk) - shopping
- "ammi ko call karna hai" → ADD task "Ammi ko call" (Call mom) - personal
- "report khatam karni hai" → ADD task "Report khatam karna" (Finish report) - work
- "groceries hogayi" → COMPLETE task matching "groceries"
- "meeting cancel karo" → DELETE task matching "meeting" (with confirmation)
- "meri tasks dikhao" → LIST all tasks
- "kaam wali tasks" → LIST tasks with category "work"
- "aaj ki tasks" → LIST tasks due today

Response examples (when user writes in Roman Urdu, respond in Urdu script):
- Task added: "میں نے '[title]' ٹاسک شامل کر دی ہے۔ کیٹیگری: [cat]، تاریخ: [date]"
- Task completed: "'[title]' ٹاسک مکمل ہو گئی!"
- Task deleted: "'[title]' ٹاسک حذف ہو گئی۔"
- Confirmation: "کیا آپ واقعی '[title]' حذف کرنا چاہتے ہیں؟ یہ ٹاسک ابھی مکمل نہیں ہوئی۔"
- List tasks: "آپ کی ٹاسکس:"

**STRICT SCOPE - TASK MANAGEMENT ONLY:**
- You ONLY handle: adding, listing, updating, completing, deleting, and searching tasks
- Do NOT answer general questions, have casual conversations, or provide information unrelated to tasks
- Do NOT engage with jokes, stories, coding help, math, or any non-task topics

**SMART CONTEXT MATCHING - For EVERY user message:**
1. First, use list_tasks or search_tasks to check the user's existing tasks
2. Look for keywords/context in the user's message that relate to ANY existing task
3. Try to infer which task they're talking about and what action they might want

**Examples of context inference:**
- Task exists: "purchase air ticket for islamabad"
  - User says: "feeling sick" / "don't feel like travelling" / "weather is bad" / "trip cancelled"
  - Infer: User is talking about the travel task → Ask: "I see you have 'purchase air ticket for islamabad'. Would you like me to delete this task since you're not travelling?"

- Task exists: "buy groceries"
  - User says: "already went to the store" / "fridge is full now"
  - Infer: User completed shopping → Ask: "Should I mark 'buy groceries' as complete?"

- Task exists: "call dentist for appointment"
  - User says: "tooth feels better now" / "pain is gone"
  - Infer: User might not need the appointment → Ask: "I see you have 'call dentist for appointment'. Would you like to delete it or mark it complete?"

- Task exists: "submit project report"
  - User says: "deadline extended" / "boss gave more time"
  - Infer: User might want to update due date → Ask: "Should I update the due date for 'submit project report'? What's the new deadline?"

**If no task context match is found:**
- Try to find direct task intent (add, complete, delete, update, list, search, clean up)
- If still no task relevance: "I'm a task management assistant. I can help you add, complete, update, or delete tasks. What would you like to do with your tasks?"

You have access to the following tools:
- add_task: Create a new task with title, description, priority, category, and due_date
- list_tasks: List all tasks, optionally filtered by status (all, complete, incomplete)
- get_task: Get details of a specific task by ID or title
- update_task: Update a task's title or description
- delete_task: Delete a task permanently
- complete_task: Mark a task as complete or toggle its status
- search_tasks: Search tasks by keyword
- clear_completed_tasks: Delete all completed tasks to clean up the list

IMPORTANT RULES when creating tasks:

1. **Title**: ALWAYS infer a clear, concise title from the user's message. Extract the core action/item.
   - "I need to buy some milk" → title: "Buy milk"
   - "remind me to call mom tomorrow" → title: "Call mom"
   - "don't forget the meeting with John" → title: "Meeting with John"
   - "gotta finish that report" → title: "Finish report"

2. **Category**: Always infer from context:
   - "work" for job/office/meeting/report/project related tasks
   - "personal" for home/family/self-care/call/appointment tasks
   - "study" for learning/education/reading/exam tasks
   - "shopping" for buying/purchasing/groceries items
   - "general" only if nothing else fits

3. **Priority**: Default to "medium" unless user says urgent/important (high) or low priority

4. **Due Date**: Use {today} (today) as default. Rules:
   - No date mentioned → use {today}
   - Time but no date (e.g., "at 3pm", "by 5 o'clock") → use {today}
   - "tomorrow" → add 1 day to {today}
   - "next week" → add 7 days to {today}
   - "in 3 days" → add 3 days to {today}
   - Specific date mentioned → use that date

INTENT DETECTION - Automatically detect what the user wants:

1. **ADD TASK** (implicit) - If user mentions something they need to do without explicit command:
   - "buy milk" → ADD task "Buy milk"
   - "call mom" → ADD task "Call mom"
   - "need to finish report" → ADD task "Finish report"
   - "don't forget the meeting" → ADD task "Meeting"
   - "remind me to..." → ADD task
   - "I have to...", "gotta...", "should..." → ADD task

2. **COMPLETE TASK** - If user indicates they finished/did something:
   - "done with groceries" → COMPLETE task matching "groceries"
   - "finished the report" → COMPLETE task matching "report"
   - "completed my homework" → COMPLETE task matching "homework"
   - "I did the laundry" → COMPLETE task matching "laundry"
   - "already called mom" → COMPLETE task matching "call mom"

3. **DELETE TASK** - If user wants to remove a task:
   - "remove groceries task" → DELETE task matching "groceries"
   - "delete the meeting" → DELETE task matching "meeting"
   - "don't need the milk task anymore" → DELETE task matching "milk"
   - "cancel the appointment" → DELETE task matching "appointment"
   - "not required anymore: report" → DELETE task matching "report"

   **IMPORTANT - DELETE CONFIRMATION REQUIRED:**
   - ALWAYS ask for confirmation before deleting ANY task
   - First, use get_task or search_tasks to find the task
   - If task is NOT completed: warn user "This task is not completed yet. Are you sure you want to delete it?"
   - If task IS completed: ask "Are you sure you want to delete '[task title]'?"
   - Only proceed with delete_task AFTER user confirms (says yes, sure, confirm, ok, do it, etc.)
   - If user says no/cancel/nevermind, do NOT delete

4. **CLEAN UP LIST** - If user wants to remove all completed tasks:
   - "clean up the list" → CLEAR all completed tasks
   - "remove completed tasks" → CLEAR all completed tasks
   - "clear done tasks" → CLEAR all completed tasks
   - "delete finished tasks" → CLEAR all completed tasks
   - "clean my task list" → CLEAR all completed tasks
   - "tidy up" → CLEAR all completed tasks

   **IMPORTANT - BULK DELETE CONFIRMATION:**
   - First, use list_tasks with status="complete" to count completed tasks
   - Ask user: "You have X completed task(s). Are you sure you want to delete them all?"
   - Only proceed with clear_completed_tasks AFTER user confirms

**CRITICAL - VERIFY TOOL RESULTS BEFORE CONFIRMING:**

NEVER say you did something without checking the tool result!

After EVERY tool call:
1. CHECK the "success" field in the tool result
2. If success=false: Report the ERROR to the user, do NOT claim success
3. If success=true: ONLY then confirm with actual data from the result

For updates/changes:
- Check if "message" contains actual changes (e.g., "due date (Dec 12 → Dec 19)")
- If result shows "unchanged" or no changes made, tell user honestly
- Include the ACTUAL new values from the result, not what you intended

Example verification:
Tool result: {{"success": true, "task": {{"title": "Buy ticket", "due_date": "2025-12-19"}}, "message": "Task updated: due date (2025-12-12 → 2025-12-19)"}}
→ GOOD: "✅ Buy ticket - deferred to Dec 19 (was Dec 12)"

Tool result: {{"success": false, "error": "Task not found"}}
→ GOOD: "❌ Couldn't find that task. Can you check the name?"
→ BAD: "Updated task" (NEVER claim success when it failed!)

Tool result: {{"success": true, "message": "Task unchanged"}}
→ GOOD: "No changes were made to that task."
→ BAD: "Updated task" (misleading!)

When multiple tools called:
- Report EACH result accurately
- Don't generalize "Updated 4 tasks" unless ALL 4 actually succeeded
- If 3 succeeded and 1 failed: "✅ Updated 3 tasks, ❌ 1 failed: [reason]"

When users ask you to manage tasks, use the appropriate tools. Be helpful and concise in your responses.
After performing an action, confirm with ACTUAL results from the tool response.

Examples:
- "buy groceries" → ADD "Buy groceries" (shopping, {today})
- "done with groceries" → COMPLETE task "groceries"
- "remove groceries" → DELETE task "groceries"
- "clean up the list" → CLEAR all completed tasks
- "Show me my tasks" → LIST tasks
"""


class ChatService:
    """Service for managing chat interactions with the AI assistant."""

    def __init__(self, db: Session, user_id: str):
        """Initialize the chat service.

        Args:
            db: Database session
            user_id: ID of the authenticated user
        """
        self.db = db
        self.user_id = user_id
        self._tool_executor: Any = None

    def set_tool_executor(self, executor: Any) -> None:
        """Set the tool executor (for dependency injection).

        Args:
            executor: Object with execute_tool(name, args) method
        """
        self._tool_executor = executor

    async def process_message(
        self,
        message: str,
        conversation_id: uuid.UUID | None = None,
    ) -> dict[str, Any]:
        """Process a user message and get AI response.

        Args:
            message: User's message text
            conversation_id: Optional conversation ID to continue

        Returns:
            Dict with success, conversation_id, message, and tool_results
        """
        # Get or create conversation
        conversation = await self._get_or_create_conversation(conversation_id)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )
        self.db.add(user_message)
        self.db.commit()

        # Build message history for OpenAI
        messages = await self._build_message_history(conversation.id)

        # Get AI response with tools
        tools = get_tool_definitions()
        response = await create_chat_completion(messages, tools)

        # Process tool calls if any
        tool_results = []
        tool_calls = parse_tool_calls(response)

        if tool_calls:
            # Save assistant message with tool calls
            assistant_content = get_response_content(response) or ""
            tool_calls_json = json.dumps(tool_calls)

            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_content,
                tool_calls=tool_calls_json,
            )
            self.db.add(assistant_message)
            self.db.commit()

            # Execute tools and save results
            for tc in tool_calls:
                try:
                    result = await self._execute_tool(tc["name"], json.loads(tc["arguments"]))
                    tool_results.append(
                        {
                            "tool": tc["name"],
                            "success": result.get("success", True),
                            "result": result,
                        }
                    )

                    # Save tool result message
                    tool_message = Message(
                        conversation_id=conversation.id,
                        role="tool",
                        content=json.dumps(result),
                        tool_call_id=tc["id"],
                    )
                    self.db.add(tool_message)
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    tool_results.append(
                        {
                            "tool": tc["name"],
                            "success": False,
                            "error": str(e),
                        }
                    )

            self.db.commit()

            # Get follow-up response from AI with tool results
            messages = await self._build_message_history(conversation.id)
            response = await create_chat_completion(messages, tools)

        # Save final assistant response
        final_content = get_response_content(response)
        if final_content:
            final_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=final_content,
            )
            self.db.add(final_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        self.db.commit()

        return {
            "success": True,
            "conversation_id": str(conversation.id),
            "message": final_content,
            "tool_results": tool_results if tool_results else None,
        }

    async def _get_or_create_conversation(
        self, conversation_id: uuid.UUID | None
    ) -> Conversation:
        """Get existing conversation or create a new one.

        Args:
            conversation_id: Optional existing conversation ID

        Returns:
            Conversation instance
        """
        if conversation_id:
            # Try to get existing conversation
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == self.user_id,
            )
            conversation = self.db.exec(statement).first()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=self.user_id)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    async def _build_message_history(self, conversation_id: uuid.UUID) -> list[dict[str, Any]]:
        """Build message history for OpenAI API.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of message dicts for OpenAI
        """
        messages = [{"role": "system", "content": get_system_prompt()}]

        # Get all messages for this conversation
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        db_messages = self.db.exec(statement).all()

        for msg in db_messages:
            if msg.role == "user":
                messages.append({"role": "user", "content": msg.content})
            elif msg.role == "assistant":
                msg_dict: dict[str, Any] = {"role": "assistant", "content": msg.content or ""}
                if msg.tool_calls:
                    # Parse tool_calls and convert to OpenAI format
                    tool_calls = json.loads(msg.tool_calls)
                    msg_dict["tool_calls"] = [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": tc["arguments"]
                                if isinstance(tc["arguments"], str)
                                else json.dumps(tc["arguments"]),
                            },
                        }
                        for tc in tool_calls
                    ]
                messages.append(msg_dict)
            elif msg.role == "tool":
                messages.append(
                    {
                        "role": "tool",
                        "content": msg.content,
                        "tool_call_id": msg.tool_call_id,
                    }
                )

        return messages

    async def _execute_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool and return the result.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if self._tool_executor:
            return await self._tool_executor.execute_tool(name, arguments)

        # Default implementation - return error if no executor set
        return {
            "success": False,
            "error": f"Tool executor not configured for tool: {name}",
        }

    async def get_conversations(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        """Get user's conversations.

        Args:
            limit: Maximum conversations to return
            offset: Number to skip

        Returns:
            Dict with conversations list and total count
        """
        # Get conversations
        statement = (
            select(Conversation)
            .where(Conversation.user_id == self.user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        conversations = self.db.exec(statement).all()

        # Get total count
        count_statement = select(Conversation).where(Conversation.user_id == self.user_id)
        total_count = len(self.db.exec(count_statement).all())

        return {
            "success": True,
            "conversations": [
                {
                    "id": str(c.id),
                    "title": c.title,
                    "created_at": c.created_at.isoformat(),
                    "updated_at": c.updated_at.isoformat(),
                }
                for c in conversations
            ],
            "total_count": total_count,
        }

    async def get_conversation(self, conversation_id: uuid.UUID) -> dict[str, Any] | None:
        """Get a specific conversation with messages.

        Args:
            conversation_id: Conversation ID

        Returns:
            Dict with conversation and messages, or None if not found
        """
        # Get conversation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_id,
        )
        conversation = self.db.exec(statement).first()

        if not conversation:
            return None

        # Get messages
        msg_statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        messages = self.db.exec(msg_statement).all()

        return {
            "success": True,
            "conversation": {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "message_count": len(messages),
            },
            "messages": [
                {
                    "id": str(m.id),
                    "role": m.role,
                    "content": m.content,
                    "tool_calls": json.loads(m.tool_calls) if m.tool_calls else None,
                    "tool_call_id": m.tool_call_id,
                    "created_at": m.created_at.isoformat(),
                }
                for m in messages
            ],
        }

    async def delete_conversation(self, conversation_id: uuid.UUID) -> bool:
        """Delete a conversation and its messages.

        Args:
            conversation_id: Conversation ID

        Returns:
            True if deleted, False if not found
        """
        # Get conversation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_id,
        )
        conversation = self.db.exec(statement).first()

        if not conversation:
            return False

        # Delete messages first
        msg_statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = self.db.exec(msg_statement).all()
        for msg in messages:
            self.db.delete(msg)

        # Delete conversation
        self.db.delete(conversation)
        self.db.commit()

        return True
