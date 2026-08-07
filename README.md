# `/lean`

**Save the terminal. Verify the checkpoint. Clear without losing your place.**

`/lean` is the closeout command for a terminal session. It captures what happened, what is still
running, what is blocked, and the exact next action; writes that handoff to Claude file memory and
GBrain; reads both back; and only then says whether it is safe to run `/clear` or `/exit`.

It has one job. An explicit `/lean` never turns into token advice, `/compact`, or an MCP cleanup
audit because the work happens to be unfinished.

## The contract

When you run `/lean`, it:

1. builds a strict, constrained checkpoint;
2. atomically writes a stable handoff per workstream under `lean-handoffs/` and updates a bounded
   managed `MEMORY.md` pointer block;
3. upserts `projects/<project>/lean-handoffs/<workstream>` in GBrain and records a timeline event;
4. verifies both stores by read-back;
5. emits a machine-readable `SAFE_TO_CLEAR` or `NOT_SAFE_TO_CLEAR` receipt.

The default clear gate requires verified file memory and verified GBrain persistence. If either
write fails or its read-back does not match the complete expected checkpoint, Lean tells you not to
clear. A partial handoff remains available while you repair the failed store and rerun `/lean`.

Active work is first-class state. Every recorded job includes its identifier, last-known status,
working directory, poll command, and success signal so a new session can pick it up without guessing.

## Safety and durability

- Input is constrained by a versioned schema and a 64 KiB limit.
- Unknown fields are rejected.
- High-confidence credential, PHI, and prompt-injection patterns are rejected before any write.
- The temporary checkpoint file can be consumed immediately after it is read.
- Consumption is limited to private, current-user-owned `lean-checkpoint-*` files inside the system
  temporary directory; arbitrary caller-selected paths are refused and retained.
- File writes are atomic and private (`0600`).
- Repeating the same checkpoint is idempotent and does not duplicate its timeline event.
- Stable per-workstream pages preserve parallel terminal handoffs without timestamped transcript
  dumps.
- GBrain and file-memory receipts report attempted, verified, warning, and failed states separately.

Lean never runs `/clear` or `/exit` itself. The destructive final keystroke stays with you.

## Requirements

- Python 3.10 or newer on macOS or Linux
- `gbrain` available on `PATH`
- Claude Code with local skills enabled

## Install

```bash
git clone https://github.com/napiermd/claude-skill-lean.git
ln -s "$(pwd)/claude-skill-lean" ~/.claude/skills/lean
```

Then invoke `/lean` when you are ready to checkpoint and close a terminal.

The clear gate is Claude-specific: Codex does not natively auto-load Claude's project `MEMORY.md`,
so a Codex context must not treat Lean's receipt as proof that Codex itself is safe to clear.

## Verification helper

The skill drives [`scripts/lean_closeout.py`](scripts/lean_closeout.py). The helper accepts a private
JSON file conforming to [`references/checkpoint-schema.md`](references/checkpoint-schema.md), writes
both durable stores, verifies them, and prints a JSON receipt. There is no file-only clearance mode:
both stores and the auto-loaded memory pointer must verify before the receipt says it is safe.

Run the test suite with:

```bash
python3 -m unittest discover -s tests -v
```

The tests use an isolated fake GBrain backend; they do not write to your real knowledge base.

To verify the installed GBrain CLI against a disposable PGLite brain with a scrubbed environment and
embeddings disabled:

```bash
LEAN_RUN_REAL_GBRAIN_E2E=1 python3 -m unittest tests/test_real_gbrain_e2e.py -v
```

## Failure behavior

For a real write, exit status `0` means the requested persistence policy was verified. A dry run also
returns `0`, but always carries `safe_to_clear: false` and must never be treated as clearance. Status
`2` means the checkpoint failed validation. Status `3` means persistence did not meet the clear
gate. In either failure case, the receipt remains explicit: `NOT_SAFE_TO_CLEAR`.

## License

MIT.
