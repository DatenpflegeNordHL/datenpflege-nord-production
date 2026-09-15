# Runbook: browser QA

For changed user-facing output, verify the affected page in a real Chromium-family browser at:

- 1440 px desktop;
- 390 px mobile;
- 320 px narrow mobile.

Check document-level overflow, heading hierarchy, visible keyboard focus, interactive controls, reload/reset persistence when relevant, `prefers-reduced-motion`, and readable core content with JavaScript disabled. Inspect screenshots at all required widths.

Tables may scroll inside their own labelled container; they must not widen the document.
