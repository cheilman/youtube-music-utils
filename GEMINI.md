# Gemini Project Configuration

This file helps Gemini understand your project and how you'd like it to behave.

## CRITICAL

**Do not use "git add ." or "git commit -a" EVER!**
**ALWAYS use "git add <filename>" to specifically add the files that you created or modified.**

## Project Information

- **Project Name:** YouTube Music Utilities
- **Description:** A set of utilities to interface with YouTubeMusic.
- **Key Technologies:**
    - Python 3.14+
    - uv for managing python project dependencies, environments, and tools
    - ruff for code formatting and linting
    - ytmusicapi for interfacing with YouTube Music
    - sqlite for database management

## Gemini's Role

- **Primary Goal:**
    - Gemini will be managing and coding this project.  You are an expert senior developer, comfortable writing clean, readable, testable code.
    - All code must be written with readability and test-ability in mind.  This is primary over performance.
- **Coding Style:**
    - Use four spaces for code indentation.
    - All code must be formatted with `ruff format` before committing.
    - All code must cleanly lint with `ruff check` before committing.
    - All code must typecheck cleajnly with `mypy` before committing.
    - You can try to autofix format and lint issues with the `--fix` arg to `ruff`.
    - Prefer making small, self contained changes and fully testing them before moving on to the next task.
    - Any time you add a TODO comment, create a corresponding beads issue and have the comment read "TODO(issue id): blah"
- **Testing:** [Describe your testing preferences. For example, "Write unit tests for all new features. Use the Jest testing framework."]
    - All code must have accompanying unit tests.
    - Tests much be executed and pass before code can be committed.
    - Tests may not be deleted without human approval.

## Interaction Preferences

- **Communication Style:**
    - Ask for clarification if you are unsure about anything.
- **Tool Usage:**
    - Always ask for confirmation before running any destructive commands.
    - Any time you run a command and try to pass backticks, you need to either escape them or enclose the string in single quotes.

## Other Rules
- ABSOLUTELY NEVER run destructive git operations (e.g., git reset --hard, rm, git checkout/git restore to an older commit) unless the user gives an explicit, written instruction in this conversation. Treat these commands as catastrophic; if you are even slightly unsure, stop and ask before touching them. (When working within Cursor or Codex Web, these git limitations do not apply; use the tooling's capabilities as needed.)
- NEVER use `git add .` or `git commit -a`, ALWAYS specify the files you touched and list each path explicitly.
- Delete unused or obsolete files when your changes make them irrelevant (refactors, feature removals, etc.), and revert files only when the change is yours or explicitly requested. If a git operation leaves you unsure about other agents' in-flight work, stop and coordinate instead of deleting.
- Before attempting to delete a file to resolve a local type/lint failure, stop and ask the user. Other agents are often editing adjacent files; deleting their work to silence an error is never acceptable without explicit approval.
- Moving/renaming and restoring files is allowed.
- Always double-check git status before any commit
- Keep commits atomic: commit only the files you touched and list each path explicitly. For tracked files run git commit -m "<scoped message>" -- path/to/file1 path/to/file2. For brand-new files, use the one-liner git restore --staged :/ && git add "path/to/file1" "path/to/file2" && git commit -m "<scoped message>" -- path/to/file1 path/to/file2.
- Quote any git paths containing brackets or parentheses (e.g., src/app/[candidate]/**) when staging or committing so the shell does not treat them as globs or subshells.
- Never amend commits unless you have explicit written approval in the task thread.

## Beads

**We track work in Beads instead of Markdown. Run `bd quickstart` to see how.**

Quick reference for agent workflows:

```
# Find ready work
bd ready --json | jq '.[0]'

# Create issues during work
bd create "Discovered bug" -t bug -p 0 --json

# Link discovered work back to parent
bd dep add <new-id> <parent-id> --type discovered-from

# Update status
bd update <issue-id> --status in_progress --json

# Complete work
bd close <issue-id> --reason "Implemented" --json
```

### Workflow
1. Check for ready work: Run bd ready to see what's unblocked
2. Claim your task: bd update <id> --status in_progress
3. Work on it: Implement, test, document
4. Discover new work: If you find bugs or TODOs, create issues:
    1. bd create "Found bug in auth" -t bug -p 1 --deps discovered-from:<current-id> --json
5. Complete: bd close <id> --reason "Implemented"
6. When your issue is complete, commit your changes (including the .beads directory) with a clear and concise commit message describing what you accomplished and how.

### Issue Types
- `bug` - Something broken that needs fixing
- `feature` - New functionality
- `task` - Work item (tests, docs, refactoring)
- `epic` - Large feature composed of multiple issues
- `chore` - Maintenance work (dependencies, tooling)

### Priorities
- `0` - Critical (security, data loss, broken builds)
- `1` - High (major features, important bugs)
- `2` - Medium (nice-to-have features, minor bugs)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

### Dependency Types
- `blocks` - Hard dependency (issue X blocks issue Y)
- `related` - Soft relationship (issues are connected)
- `parent-child` - Epic/subtask relationship
- `discovered-from` - Track issues discovered during work

Only blocks dependencies affect the ready work queue.

