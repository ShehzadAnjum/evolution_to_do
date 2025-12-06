---
id: "{{ID}}"
title: "{{TITLE}}"
stage: "{{STAGE}}"
date: "{{DATE_ISO}}"
surface: "agent"
model: "{{MODEL}}"
feature: "{{FEATURE}}"
branch: "{{BRANCH}}"
user: "{{USER}}"
command: "{{COMMAND}}"
labels: {{LABELS_YAML}}
links:
  spec: {{SPEC_URL}}
  ticket: {{TICKET_URL}}
  adr: {{ADR_URL}}
  pr: {{PR_URL}}
files_created_or_modified: {{FILES_YAML}}
tests_run_or_added: {{TESTS_YAML}}
---

# Prompt History Record: {{TITLE}}

**ID**: {{ID}}
**Stage**: {{STAGE}}
**Date**: {{DATE_ISO}}
**Feature**: {{FEATURE}}

---

## User Prompt

```
{{PROMPT_TEXT}}
```

---

## Agent Response Summary

{{RESPONSE_TEXT}}

---

## Context

**Branch**: {{BRANCH}}
**Command**: {{COMMAND}}
**Model**: {{MODEL}}
**Surface**: agent (Claude Code)

---

## Files Modified

{{FILES_YAML}}

---

## Tests

{{TESTS_YAML}}

---

## Links

- **Spec**: {{SPEC_URL}}
- **Ticket**: {{TICKET_URL}}
- **ADR**: {{ADR_URL}}
- **PR**: {{PR_URL}}

---

## Outcome

**Status**: {{OUTCOME_STATUS}}
**Result**: {{OUTCOME_RESULT}}

---

## Evaluation

**Success**: {{EVALUATION_SUCCESS}}
**Lessons**: {{EVALUATION_LESSONS}}

---

**Created**: {{DATE_ISO}}
**PHR Version**: 1.0.0
