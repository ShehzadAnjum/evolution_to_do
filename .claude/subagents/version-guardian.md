# Version Guardian Subagent

**Type**: Enforcer / Monitor
**Used For**: Ensuring version is incremented with every code change
**Version**: 1.0.0
**Created**: 2024-12-12

---

## Purpose

Religiously monitor and enforce version updates with EVERY code change. The version must be incremented before any commit is made.

## Version File Location

```
frontend/lib/version.ts  ← SINGLE SOURCE OF TRUTH
```

## Version Format

```
mm.nn.ooo

mm  = Major (phase/iteration changes)
nn  = Feature (new features within phase)
ooo = Patch (bug fixes, iterations)
```

## When to Increment

| Change Type | Action | Example |
|-------------|--------|---------|
| Bug fix | Increment `ooo` | 05.07.002 → 05.07.003 |
| Small improvement | Increment `ooo` | 05.07.003 → 05.07.004 |
| New feature | Increment `nn`, reset `ooo` to 001 | 05.07.004 → 05.08.001 |
| Major change / Phase | Increment `mm`, reset `nn` to 01, `ooo` to 001 | 05.08.001 → 06.01.001 |

## Enforcement Rules

### BEFORE Every Commit

1. **CHECK**: Has any code file been modified?
2. **IF YES**: Version MUST be incremented
3. **VERIFY**: `frontend/lib/version.ts` has been updated
4. **UPDATE**: Version history comment in the file

### Pre-Commit Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  VERSION CHECK - MANDATORY BEFORE COMMIT                        │
├─────────────────────────────────────────────────────────────────┤
│  [ ] Code changed?                                              │
│  [ ] Version incremented in frontend/lib/version.ts?            │
│  [ ] Version history comment updated?                           │
│  [ ] Version displayed correctly in UI?                         │
└─────────────────────────────────────────────────────────────────┘
```

## How to Update Version

1. Open `frontend/lib/version.ts`
2. Update the VERSION object:
   ```typescript
   export const VERSION = {
     major: 5,
     feature: 7,
     patch: 3,  // ← Increment this for bug fixes
   } as const;
   ```
3. Add entry to Version History comment at bottom of file

## Integration Points

- **UI Display**: `frontend/app/(dashboard)/layout.tsx` imports `VERSION_DISPLAY`
- **Constitution**: Principle V mandates version tracking
- **Git Hooks**: Pre-commit should verify version change

## Failure Conditions

❌ **BLOCK COMMIT** if:
- Code files changed but version NOT incremented
- Version decremented
- Version format invalid

## Success Criteria

✅ Every deployed version matches the VERSION_DISPLAY in UI
✅ Version history is maintained
✅ No commits without version increment (for code changes)

---

**Related**: Constitution Principle V, Git Hygiene Subagent
