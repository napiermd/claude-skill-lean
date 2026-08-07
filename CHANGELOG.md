# Changelog

All notable changes to Lean are documented here.

## 0.1.0.0 — 2026-08-07

### Added

- A deterministic closeout helper that writes Claude file memory and GBrain, verifies both by
  read-back, and emits a machine-readable clear/no-clear receipt.
- A strict checkpoint schema with complete resume recipes for active work.
- Atomic private file writes, per-project closeout locking, stable per-workstream GBrain page
  upserts, and idempotent timeline events.
- A 35-case isolated test suite covering happy paths, parallel workstreams, concurrency, historical
  idempotency, partial failures, read-back failures, unsafe input, and temporary-file cleanup, plus
  an opt-in round trip against an isolated real GBrain/PGLite backend.
- Generated skill metadata and a documented verification interface.

### Changed

- `/lean` now has one purpose: save and verify the terminal before `/clear` or `/exit`.
- Active or unfinished work is checkpointed instead of triggering `/compact` or MCP cleanup advice.
- The clear gate now requires verified file memory and verified GBrain by default.

### Security

- Checkpoints reject unknown fields, oversized input, secret-like values, high-confidence PHI, and
  recognizable prompt-injection text before either persistence backend is touched.
- File-only clearance is not permitted; both durable stores must satisfy the clear gate.
