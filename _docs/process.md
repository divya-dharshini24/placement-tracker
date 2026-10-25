# Process

- Work is tracked as GitHub issues, one at a time.
- Read the acceptance criteria before starting and before closing an issue.
- Commit regularly with a clear message.
- Run `python manage.py test` before every push.

## Roles

- PM - grooms a task and writes acceptance criteria. See `_docs/team/pm.md`.
- Engineer - implements one task. See `_docs/team/software-engineer.md`.
- QA - checks the result against the criteria. See `_docs/team/qa-engineer.md`.

## Lifecycle

1. Pick an open issue.
2. PM role: make sure the acceptance criteria are checkable.
3. Engineer role: implement it and add tests.
4. QA role: check each criterion and write PASS or FAIL as a comment.
5. If FAIL, go back to step 3. If PASS, close the issue.