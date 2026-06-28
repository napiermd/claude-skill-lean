# `/lean`

**Keep your Claude Code context lean. One command. No babysitting.**

---

## TL;DR

By hour two, your Claude Code session is hauling a task you already finished, MCP servers you never
called, and the same file read three times. You're paying for all of it, every turn.

`/lean` finds the dead weight and tells you exactly what to cut. One word. On a task switch it saves
what matters first, then hands you `/clear`.

The goal isn't fewer tokens used. It's fewer tokens **wasted**.

---

## The problem

Long sessions rot.

You finish a task and its history just stays. You read a whole 1,800-line file when you needed four
lines. You connect ten tool servers and use one. From then on, the model drags all of it through
every single turn.

`/compact` doesn't fix this. It summarizes the mess and keeps it. Lower token count, same garbage.
You feel lean. You're not.

## What it does

You type `/lean`. It reads the session and picks the situation. You never choose a mode.

**Still mid-task** — it names the waste and gives you the exact cut:

- idle MCP servers → `/mcp` to drop them
- a file you read whole → a tighter `Read`, or hand the search to a subagent so the dump never hits your window
- same task, just long → `/compact` (the one time compacting is the right call)

**Switching tasks** — a fresh session beats a compacted one. It saves anything durable first, then
hands you `/clear`. You keep what mattered. You don't drag the old task into the new one.

## Why one command

The first cut had three: `/lean`, a separate `/switch`, and `/clear`. I couldn't remember my own
tool. So I cut it down.

`/clear` is Claude Code's, not mine — a skill can't wipe your window, so that keystroke stays with
you. Everything else folds into `/lean`. It decides. You remember one word.

## Install

```bash
git clone https://github.com/napiermd/claude-skill-lean.git
ln -s "$(pwd)/claude-skill-lean" ~/.claude/skills/lean
```

Mirror it for Codex if you run it:

```bash
ln -s "$(pwd)/claude-skill-lean" ~/.codex/skills/lean
```

Run `/lean`. Done.

## What it won't do

- **Guess your token count.** There's no API for live window size, so it reasons from what's actually
  in the session — files read, servers connected, task drift — and never makes up a number.
- **Clear for you.** Wiping the window is destructive and it's your call. It does the safe part —
  saving what matters — and stops.
- **Pad the list.** Two real cuts beat three to fill a slot. If your session is already clean, it
  says so and shuts up.

## License

MIT. Take it, fork it, make it yours.
