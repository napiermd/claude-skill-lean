---
name: lean
description: The one command for context hygiene. Looks at the current session and does the right thing — mid-task, it names what's wasting the context window (idle tools, wide reads); on a task switch, it saves durable facts to memory and hands you `/clear`. Use when the user runs /lean, says the session feels bloated/heavy/slow, asks "should I clear or compact?", or is switching to an unrelated task. North star: fewer tokens WASTED, not fewer used.
---

# Lean — the one context command

There is **one** thing to remember: `/lean`. It reads the session and picks the situation itself; you
never choose a mode. The only follow-up is `/clear`, Claude Code's built-in — a skill cannot wipe the
window, so that keystroke always stays with you.

**North star: fewer tokens _wasted_, not fewer _used_.** Wasted = stale task history, full-file reads
where a slice was needed, idle MCP tool schemas, re-read files.

## Step 1 — which situation?

Decide from the session whether the user is **switching tasks** (current task differs from how the
session started, or they said they're moving on / starting something unrelated) or **still mid-task**.

## Step 2a — SWITCHING TASKS → save, then hand off `/clear`

The fresh session is the right call, but a bare `/clear` drops anything unsaved. Do the reversible
prep first:

1. Find **durable facts** from this session — who the user is / how they work, a correction or
   approach they confirmed (with the *why*), in-flight work state or a decision not recoverable from
   code/git, a useful URL/reference, and — if work is unfinished — a one-line where-we-left-off + next
   step.
2. **Filter hard:** skip anything the repo, git, or filesystem already records; skip ephemera; if a
   note already covers it, update it rather than duplicate. Nothing clears the bar → save nothing.
3. **Persist it.** If this install has file-based memory (a `# Memory` section in your system context),
   write the facts there following that system's conventions. Otherwise, put the where-we-left-off +
   next step in your reply so the user can paste it somewhere before clearing.
4. Output the summary, then tell the user to run `/clear`. **Never run `/clear` yourself.**

```
Saved:
- <where> — <one-line hook>

Run `/clear` to start fresh.
```
(or, if nothing met the bar:)
```
Nothing durable to persist. Run `/clear` to start fresh.
```

## Step 2b — STILL MID-TASK → diagnose the waste

Scan for the trims that **don't** cost the user their place, then emit a 1-line verdict, a ≤2-line
read of the top consumers, and **up to 3 moves** (two real beats three padded — a "nothing to fix"
line is not a move). Stop at the last move; nothing trails it.

| Trim | When | Command |
| --- | --- | --- |
| **Disconnect tools** | MCP servers connected but unused this session | `/mcp` → disconnect the idle ones |
| **Narrow reads** | A file was read whole, or re-read | `Read` with `offset`/`limit`; `Grep`/`Glob` to locate; hand fan-out to a subagent so the dump stays out of your window |
| **Compact (not clear)** | Same task, just long | `/compact` — keeps continuity. Don't `/compact` a *finished* task to shave the count; that's a switch, use Step 2a. |

```
## Context: <one-line verdict>

<≤2 lines on the top consumers this session>

1. **<action>** — <why, ties to a real consumer> → `<exact command>`
2. **<action>** — <why> → `<exact command>`
```

## Anti-patterns
- Asking the user which mode — Step 1 decides.
- Recommending a bare `/clear` without saving durable facts first.
- Inventing a fact to look productive, or dumping the whole session into one note.
- A generic essay / 40-line audit; padding to three moves; trailing caveats after the last move.
- Inventing a token number — there's no API for live window size; reason qualitatively.
