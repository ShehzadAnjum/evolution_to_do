#!/bin/bash
# Copy Essential Files Package
# Preserves all project knowledge for portability

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if destination provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Destination directory required${NC}"
    echo "Usage: $0 <destination_directory>"
    echo "Example: $0 ../new_project"
    exit 1
fi

DEST_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${GREEN}📦 Copying Essential Files Package${NC}"
echo "Source: $PROJECT_ROOT"
echo "Destination: $DEST_DIR"
echo ""

# Create directory structure
echo -e "${YELLOW}Creating directory structure...${NC}"
mkdir -p "$DEST_DIR/.specify/memory"
mkdir -p "$DEST_DIR/.specify/templates"
mkdir -p "$DEST_DIR/specs/001-phase1-console-todo/contracts"
mkdir -p "$DEST_DIR/specs/001-phase1-console-todo/checklists"
mkdir -p "$DEST_DIR/docs"
mkdir -p "$DEST_DIR/scripts"

# Copy SpecKit framework
echo -e "${YELLOW}Copying SpecKit framework...${NC}"
cp "$PROJECT_ROOT/.specify/config.yaml" "$DEST_DIR/.specify/" 2>/dev/null || echo "⚠️  config.yaml not found"
cp "$PROJECT_ROOT/.specify/memory/constitution.md" "$DEST_DIR/.specify/memory/" 2>/dev/null || echo "⚠️  constitution.md not found"
cp "$PROJECT_ROOT/.specify/templates/"*.md "$DEST_DIR/.specify/templates/" 2>/dev/null || echo "⚠️  Templates not found"

# Copy Phase I specifications
echo -e "${YELLOW}Copying Phase I specifications...${NC}"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/spec.md" "$DEST_DIR/specs/001-phase1-console-todo/" 2>/dev/null || echo "⚠️  spec.md not found"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/plan.md" "$DEST_DIR/specs/001-phase1-console-todo/" 2>/dev/null || echo "⚠️  plan.md not found"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/data-model.md" "$DEST_DIR/specs/001-phase1-console-todo/" 2>/dev/null || echo "⚠️  data-model.md not found"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/research.md" "$DEST_DIR/specs/001-phase1-console-todo/" 2>/dev/null || echo "⚠️  research.md not found"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/quickstart.md" "$DEST_DIR/specs/001-phase1-console-todo/" 2>/dev/null || echo "⚠️  quickstart.md not found"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/contracts/cli-interface.md" "$DEST_DIR/specs/001-phase1-console-todo/contracts/" 2>/dev/null || echo "⚠️  cli-interface.md not found"
cp "$PROJECT_ROOT/specs/001-phase1-console-todo/checklists/requirements.md" "$DEST_DIR/specs/001-phase1-console-todo/checklists/" 2>/dev/null || echo "⚠️  requirements.md not found"

# Copy project documentation
echo -e "${YELLOW}Copying project documentation...${NC}"
cp "$PROJECT_ROOT/docs/SESSION_HANDOFF.md" "$DEST_DIR/docs/" 2>/dev/null || echo "⚠️  SESSION_HANDOFF.md not found"
cp "$PROJECT_ROOT/docs/PROJECT_STATUS.md" "$DEST_DIR/docs/" 2>/dev/null || echo "⚠️  PROJECT_STATUS.md not found"
cp "$PROJECT_ROOT/docs/ESSENTIAL_FILES_PACKAGE.md" "$DEST_DIR/docs/" 2>/dev/null || echo "⚠️  ESSENTIAL_FILES_PACKAGE.md not found"
cp "$PROJECT_ROOT/docs/MARKDOWN_EVALUATION.md" "$DEST_DIR/docs/" 2>/dev/null || echo "⚠️  MARKDOWN_EVALUATION.md not found"
cp "$PROJECT_ROOT/docs/DAILY_CHECKLIST.md" "$DEST_DIR/docs/" 2>/dev/null || echo "⚠️  DAILY_CHECKLIST.md not found"
cp "$PROJECT_ROOT/docs/BEFORE_NEW_TOOL.md" "$DEST_DIR/docs/" 2>/dev/null || echo "⚠️  BEFORE_NEW_TOOL.md not found"

# Copy root documentation
echo -e "${YELLOW}Copying root documentation...${NC}"
cp "$PROJECT_ROOT/README.md" "$DEST_DIR/" 2>/dev/null || echo "⚠️  README.md not found"
cp "$PROJECT_ROOT/QUICK_REFERENCE.md" "$DEST_DIR/" 2>/dev/null || echo "⚠️  QUICK_REFERENCE.md not found"
cp "$PROJECT_ROOT/CLAUDE.md" "$DEST_DIR/" 2>/dev/null || echo "⚠️  CLAUDE.md not found (optional)"

# Copy this script
cp "$0" "$DEST_DIR/scripts/" 2>/dev/null || true

# Count copied files
FILE_COUNT=$(find "$DEST_DIR" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.sh" \) | wc -l)

echo ""
echo -e "${GREEN}✅ Essential files copied successfully!${NC}"
echo ""
echo "📊 Summary:"
echo "   Files copied: $FILE_COUNT"
echo "   Destination: $DEST_DIR"
echo ""
echo "📋 Next steps:"
echo "   1. Review docs/ESSENTIAL_FILES_PACKAGE.md"
echo "   2. Verify checklist in that file"
echo "   3. Read .specify/memory/constitution.md first"
echo "   4. Check docs/SESSION_HANDOFF.md for current state"
echo ""
echo -e "${YELLOW}Note: This preserves all research and specifications.${NC}"
echo -e "${YELLOW}You can start the project immediately without re-research.${NC}"

