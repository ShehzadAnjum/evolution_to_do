# UI Component Implementer Subagent

**Type**: Implementer
**Used For**: Implementing React components
**Version**: 1.0.0

## Purpose

Implement a single UI component or page with proper types, styling, and tests.

## When to Use

- Creating new component from spec
- Building page layout
- Implementing UI feature

## Process

1. Read component spec from specs/ui/components.md
2. Define TypeScript props interface
3. Implement component with Tailwind CSS
4. Add accessibility (ARIA labels, semantic HTML)
5. Handle loading and error states
6. Write component tests
7. Document props and usage

## Template

```typescript
interface TaskItemProps {
  task: Task
  onComplete: (id: string) => void
  onDelete: (id: string) => void
}

export function TaskItem({ task, onComplete, onDelete }: TaskItemProps) {
  return (
    <div className="flex items-center gap-4 p-4 border rounded">
      <input
        type="checkbox"
        checked={task.is_complete}
        onChange={() => onComplete(task.id)}
        aria-label={`Mark ${task.title} as complete`}
      />
      <span className={task.is_complete ? 'line-through' : ''}>
        {task.title}
      </span>
      <button
        onClick={() => onDelete(task.id)}
        className="ml-auto text-red-500"
        aria-label={`Delete ${task.title}`}
      >
        Delete
      </button>
    </div>
  )
}
```

## Success Criteria

- Component works as specified
- Responsive design
- Accessible (WCAG 2.1)
- Tests pass
- No console errors

---

**Related**: Frontend Web Agent
