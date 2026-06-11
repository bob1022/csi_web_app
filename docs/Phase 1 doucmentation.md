Phase 1 is the first part of five to create a system to monitor and administer a construction project that is inline with project documents.

add_item.html - this file supplies the the information for adding new checklist items.

add_project.html - this file is similar to the add checklist file and it adds a new project to monitor.

# VS Code Formatting Issue

Problem:

# Format On Save corrupted Jinja template code in edit_item.html.

Example:

Correct:
{% if item.division == "03" %}

Corrupted:
{% if item.division="" ="03" %}

Temporary Solution:

Disable Format On Save.

Status:

Investigate formatter configuration later.

In Plain English

This code says:

Take some text based on the selected type,
put that text into the modal window,
and make the modal window visible.

# This is a good example of something to document in your future docs/javascript_notes.md:

# Modal Window

Purpose:
Display help text or instructions.

Process:
1. Find modal-text area.
2. Insert selected text.
3. Display modal window.

Key Functions:
getElementById()
innerText
style.display