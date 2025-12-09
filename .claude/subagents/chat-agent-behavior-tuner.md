# Chat Agent Behavior Tuner Subagent

**Type**: Tuner/Optimizer
**Used For**: Refining AI agent system prompt and behavior
**Version**: 1.0.0

## Purpose

Tune AI agent system prompt to improve intent recognition, reduce hallucinations, and enhance user experience.

## Process

1. **Analyze Current Behavior**
   - Test common user intents
   - Identify failures (misunderstood, hallucinations)
   - Collect problematic examples

2. **Refine System Prompt**
   - Add explicit constraints
   - Provide example intents
   - Clarify when to use each tool
   - Add guardrails against hallucination

3. **Test Improvements**
   - Re-test problematic cases
   - Verify fixes don't break working cases
   - Measure improvement

4. **Iterate**
   - Continue refinement
   - Document patterns that work

## Example Improvements

**Before**: Agent makes up task IDs
**Fix**: Add to prompt: "ONLY use task IDs returned by tools. NEVER invent IDs."

**Before**: Agent is too verbose
**Fix**: Add to prompt: "Be concise. One sentence confirmations."

---

**Related**: AI MCP Agent
