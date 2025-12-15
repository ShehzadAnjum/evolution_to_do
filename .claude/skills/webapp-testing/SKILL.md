---
name: webapp-testing
description: Web application testing using Playwright. Use when testing frontend functionality, debugging UI behavior, capturing screenshots, or viewing browser logs. Adapted from Anthropic's official webapp-testing skill.
---

# Web Application Testing

## Core Workflow

1. **Static HTML?** → Read file directly to find selectors
2. **Dynamic webapp?** → Check if server is running
3. **Need server?** → Start it first, then test
4. **Pattern:** Wait for load → Capture state → Identify selectors → Execute actions

## Playwright Setup

```python
from playwright.sync_api import sync_playwright

def test_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")  # Critical for SPAs!

        # Find elements
        page.click("text=Login")
        page.fill('input[name="email"]', "test@example.com")
        page.screenshot(path="screenshot.png")

        browser.close()
```

## Critical Pattern for SPAs

```python
# ALWAYS wait for network idle before interacting
page.wait_for_load_state("networkidle")

# Wait for specific elements
page.wait_for_selector(".dashboard-loaded")
```

## Capture Console Logs

```python
page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}"))
```

## Testing with Server

```bash
# Start server in background, run tests, cleanup
npm run dev &
sleep 5
python test_script.py
kill %1
```

## Best Practices

- Use descriptive selectors (text, role, data-testid)
- Always wait for dynamic content
- Capture screenshots on failure
- Check console for errors
