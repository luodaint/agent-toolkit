# Follow-up tracking

Suggest `TODO.md` when actionable gaps or material unknowns need follow-up. Prefer
an existing project backlog when one already serves that purpose. Creating a
tracking file is conditional on a tracking request or prior authorization; proposing
it during a review does not itself authorize writing it.

## Create or merge

Use the reviewed app's root unless project conventions specify another location.
Inspect an existing file and preserve its structure, comments, IDs, checked items
and unrelated tasks. Merge duplicate work rather than appending the same suggestion
again. Don't mark a task complete without evidence or turn a satisfied check into
busywork. Keep confirmed gaps distinct from verification tasks and optional ideas.

Record the review scope/milestone and, when useful, the reviewed revision. Each
action needs priority, reason/evidence, a concrete next step and acceptance criteria.
Assign an owner/date only when actually known or requested. Link existing issues
and relevant local files without copying secrets, private data or proprietary logs.

For a new file, a concise structure could be:

```markdown
# Launch follow-up

Scope: public marketing pages and authenticated application; initial public beta.
Reviewed revision: <actual commit, or working tree with uncommitted changes>.

## Before launch

- [ ] LR-01 — Verify the password-reset journey.
  Evidence: reset request exists, but no end-to-end completion was observed.
  Next step: use a local/test account and the email sandbox to exercise the link.
  Done when: a valid link works once; expired/reused links explain recovery;
  delivery and completion checks are recorded without exposing tokens.

## Later

- [ ] LR-02 — Add a share image for public product pages.
  Evidence: public page metadata has no configured share image.
  Done when: relevant pages expose resolvable metadata and a preview check passes.
```

The example is not a default task list. Priorities and tasks must come from the
actual review. A question such as whether tracking is needed belongs in a decision
task with a defined purpose, not an unconditional instruction to install analytics.
After creating or updating the file, report its path and the most important next
task. Writing the backlog does not authorize implementing all of it.
