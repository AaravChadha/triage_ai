---
description: Completing a subtask from PLANNING.md
---

When the user asks you to complete a specific subtask (e.g., "3.2.1"), you MUST strictly follow this sequence:

1. **Execute:** Complete the requested subtask in the codebase.
2. **Check-off:** Update `PLANNING.md` to check off the box for the completed subtask.
3. **Commit:** Commit the changes with a message following the past structure: `completed task <number> (<description>)`.
4. **Push:** Run `git push` to push the code to the remote repository.
5. **Ask:** Tell the user what has been done and provide a **brief description of what you have edited** when asking them to accept changes.
6. **Next Steps:** Identify any other subtasks that can easily be grouped with it, and ask the user if you should proceed with those next.
