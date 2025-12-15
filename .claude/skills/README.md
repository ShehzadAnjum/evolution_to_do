# Skills Directory

Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge and workflows.

## Structure (Anthropic Official Format)

Each skill is a folder containing:
```
skill-name/
├── SKILL.md        # Required: YAML frontmatter + instructions
├── scripts/        # Optional: Executable code
├── references/     # Optional: Detailed documentation
└── assets/         # Optional: Templates, images
```

## SKILL.md Format

```markdown
---
name: skill-name
description: What it does and when to use it. Include trigger phrases.
---

# Skill Name

[Concise instructions - Claude is already smart, only add what's needed]
```

## Available Skills

| Skill | Purpose |
|-------|---------|
| `chatkit-integration` | ChatKit UI for chat interfaces |
| `mcp-crud-design` | MCP tools for CRUD operations |
| `cloud-native-blueprint` | K8s, CI/CD, Dapr patterns |
| `neon-sqlmodel` | SQLModel with Neon PostgreSQL |
| `better-auth-jwt` | Authentication with Better Auth |
| `voice-chat-bilingual` | STT/TTS with bilingual support |
| `github-actions-cicd` | GitHub Actions workflows |
| `azure-aks-deployment` | Azure AKS deployment |
| `docker-minikube` | Docker and local K8s |
| `kafka-dapr-patterns` | Event-driven with Dapr |
| `browser-notifications` | Web notifications + sounds |
| `webapp-testing` | Playwright testing |
| `git-workflow` | Git commit patterns |
| `vercel-deployment` | Vercel deployment |
| `python-cli-tui` | Python CLI/TUI patterns |
| `spec-kit-monorepo` | SpecKit configuration |

## Usage

Skills are automatically loaded when relevant. You can also explicitly request:

```
📋 USING: chatkit-integration skill

I'm implementing the chat UI...
```

## Creating New Skills

Follow the [Anthropic skill-creator guide](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

Key principles:
1. **Concise is key** - Claude is smart, only add what's needed
2. **Progressive disclosure** - Keep SKILL.md <5k words, use references/ for details
3. **Include triggers** - Description should say "Use when..."

## Archived Skills

Previous skill versions are in `history/archived/skills-v1/`.

---

**Format**: Anthropic Official Skills Format
**Reference**: https://github.com/anthropics/skills
