---
name: lean
description: >-
  Save and verify a Claude Code terminal closeout before clearing or exiting.
  Use when the user invokes /lean, reaches a crossroads, wants to close a Claude
  terminal, asks to preserve unfinished work, or needs an exact handoff for the
  next Claude session. Writes a constrained checkpoint to Claude project memory
  and GBrain, verifies both by read-back, and reports whether /clear is safe.
---

# Lean — checkpoint, verify, clear

`/lean` has one contract: preserve the terminal's durable state and prepare it to close. Active or
unfinished work is a reason to checkpoint, never a reason to substitute `/compact` or MCP cleanup.

This clear gate is for Claude Code, whose project memory auto-loads `MEMORY.md`. If this skill is
inspected or invoked from Codex, it may prepare a separate Claude workspace, but it must not use the
helper receipt to claim that clearing Codex's own context is auto-resumable.

Do not run `/clear` or `/exit` for the user. Only the user performs the destructive final action.

## Closeout workflow

1. Resolve the directory containing this `SKILL.md`. Read
   `references/checkpoint-schema.md` from that directory completely before building the checkpoint.
2. Identify the project root and inspect only the state needed for an accurate handoff. Prefer
   narrow, read-only checks of git state, running jobs, deployment status, or referenced files. Do
   not start a new workstream.
3. Distill the session into the exact schema. Capture:
   - one stable workstream name that distinguishes this terminal's task from parallel terminals;
   - the objective and material events;
   - decisions and their reasons;
   - whether the work is done, running, blocked, or waiting;
   - blockers and unresolved questions;
   - every active job's identifier, status, working directory, poll command, and success signal;
   - one exact next action with its command, working directory, and success signal when known.
4. Remove secrets, credentials, PHI, patient content, raw transcripts, raw logs, and repeated tool
   chatter. Point to safe paths, commits, PRs, job IDs, or URLs instead of copying recoverable data.
   Set both safety attestations to `false` only after checking the complete payload.
5. Create a private file inside the system temporary directory with a name beginning
   `lean-checkpoint-` (for example, `mktemp "${TMPDIR:-/tmp}/lean-checkpoint-XXXXXXXX"`). Write the
   JSON with the environment's file tool, then ensure the mode is `0600`. The file must be a regular
   file owned by the current user with one hard link. Never place the payload in a shell argument or
   interpolate its content into a command.
6. Run the bundled helper, resolving it relative to this skill directory rather than the current
   working directory:

   ```bash
   python3 <skill-directory>/scripts/lean_closeout.py \
     --input <private-temp-json> \
     --consume-input \
     --project-root <project-root>
   ```

   The helper atomically updates the workstream handoff under `lean-handoffs/` and its managed
   `MEMORY.md` pointer, writes the stable per-workstream GBrain page, adds a timeline event when
   needed, and verifies persistence by read-back.
7. Parse the JSON receipt. Treat the receipt—not the process narrative—as the source of truth.

## Clear gate

Under the default dual-store policy, say it is safe to clear only when all of these are true:

- the command exited successfully;
- `safe_to_clear` is `true`;
- `clear_status` is `SAFE_TO_CLEAR`;
- `file_memory.verified` is `true`;
- `file_memory.autoload_ready` is `true`;
- `gbrain.verified` is `true`.

A verified file-memory write by itself never satisfies the `/lean` contract. There is no file-only
clearance mode; repair GBrain and rerun `/lean`.

If validation or persistence fails, say **NOT SAFE TO CLEAR**, name the failed stage, preserve the
copyable handoff in the response, follow `repair.instructions`, run or give the safe commands in
`repair.diagnostics`, and rerun `/lean` after the backend is repaired. Never claim a write succeeded
without a verified receipt. Never echo rejected secret, PHI, or prompt-injection content in the
failure response. Never truncate existing memory to fix an autoload budget failure.

## Response contract

Keep the closeout compact and concrete:

```text
## Closeout — SAFE TO CLEAR | NOT SAFE TO CLEAR

What happened: <one sentence>
Workstream: <stable workstream name>
Current state: <done/running/blocked/waiting plus key identifier>
Next: <one exact action>

Checkpoint: <checkpoint ID>
- File memory: <verified path, warning, or failure>
- GBrain: <verified slug and timeline status, or failure>

<Run /clear to reuse this terminal with fresh context.>
<Run /exit instead if you are closing the terminal.>
```

Include the `/clear` and `/exit` lines only for a `SAFE_TO_CLEAR` receipt. The user does not need to
clear before exiting; either action is safe after the verified checkpoint.

## Non-negotiable rules

- An explicit `/lean` always performs this closeout workflow.
- Do not answer `/lean` with `/compact`, `/mcp`, token advice, or an audit of context consumers.
- Do not omit running work because it is unfinished or ephemeral; record the complete resume recipe.
- Do not create timestamped transcript dumps. Reuse the stable per-workstream handoff page.
- Do not persist secrets or PHI, even if doing so would make the handoff more complete.
- Do not say “saved” or “safe” based only on an attempted write.
