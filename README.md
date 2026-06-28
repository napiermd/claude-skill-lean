# claude-skill-lean

`/lean` — the one command for context hygiene in [Claude Code](https://claude.com/claude-code).

Long sessions fill up with waste: stale task history from a job you already finished, whole files you
read when a few lines would do, schemas for MCP tools you never call, the same file read three times.
Compacting *hides* that waste; it doesn't remove it.

`/lean` reads your current session and does the right thing:

- **Mid-task** — names what's wasting the window and gives you the exact trim: `/mcp` to drop idle
  tool servers, a narrower `Read`, or `/compact` if it's the same task and just long.
- **Switching tasks** — saves anything durable first, then hands you `/clear`. A fresh session beats a
  compacted one when the task has changed; the save step means you don't lose what mattered.

**North star: fewer tokens _wasted_, not fewer _used_.** Used tokens serve the task. The goal is to
stop carrying the ones that don't.

## Why one command

The first cut of this had three things to remember (`/lean`, a separate `/switch`, and `/clear`). Too
many. `/clear` is Claude Code's own built-in — a skill can't wipe the window for you — so it stays.
Everything else folds into `/lean`, which decides the situation itself. You remember one word.

## Install

Clone anywhere and symlink into your Claude Code skills directory:

```bash
git clone https://github.com/napiermd/claude-skill-lean.git
ln -s "$(pwd)/claude-skill-lean" ~/.claude/skills/lean
```

Optionally mirror it for [Codex](https://openai.com/codex):

```bash
ln -s "$(pwd)/claude-skill-lean" ~/.codex/skills/lean
```

Then run `/lean` in any session.

## How it works

It reasons over the live session — which files were read (and whether a slice would have done), which
MCP servers are connected but unused, whether the task has drifted, whether `/compact` already ran. It
**can't see a live token count** (there's no API for it), so it ranks moves qualitatively and never
invents a number.

It is advisory by design on the one irreversible action: it will **never run `/clear` for you**.

## License

MIT — see [LICENSE](LICENSE).
