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
4. **Compact as you save.** Keep the auto-loaded memory index at most 60 lines and 6 KB total,
   whichever limit hits first. Use one line per entry: pointer + retrieval hook, never memory content.
   Clean in this order: delete wrong, obsolete, or duplicated memories; supersede dated session-log
   entries by collapsing them into per-topic files and deleting the redundant entries; then, if still over
   budget, evict only still-valid overflow — oldest still-valid dated entries first — to a non-auto-loaded
   archive file, creating it if absent. Never archive wrong, obsolete, or duplicated memories.
5. **Commit learnings to GBrain too, when it's wired up** (gbrain MCP connected, or the `gbrain` CLI
   works). File memory is the auto-loaded index; GBrain is the semantically searchable store — the
   thing that answers `gbrain search "<terms>" --source default` next month, from any repo. Write the
   SAME distilled facts (never a session dump): one page via `mcp__gbrain__put_page` (or
   `gbrain put-page`) titled by topic, plus `add_timeline_entry` for a dated decision/retro. Same
   filter bar as step 2 — if it didn't clear the bar for file memory, it doesn't go to GBrain. If
   GBrain isn't set up, skip silently; don't nag about installing it.
   For superseded facts, `mcp__gbrain__put_page` with the same title updates the existing page.
6. Output the summary, then tell the user to run `/clear`. **Never run `/clear` yourself.**

```
Saved:
- <where> — <one-line hook>
- gbrain: <page-title> — <one-line hook>   (only when GBrain is wired up)
- Pruned: <n merged / evicted / deleted>   (only when compaction touched anything)

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
- Inventing a fact to look productive, or dumping the whole session into one note (file memory OR GBrain).
- Writing to GBrain what you skipped for file memory — one filter bar, two destinations.
- Append-only memory — saving without pruning.
- A generic essay / 40-line audit; padding to three moves; trailing caveats after the last move.
- Inventing a token number — there's no API for live window size; reason qualitatively.
