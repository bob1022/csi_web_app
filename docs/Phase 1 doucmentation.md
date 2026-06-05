Phase 1 is the first part of five to create a system to monitor and administer a construction project that is inline with project documents.

add_item.html - this file supplies the the information for adding new checklist items.

add_project.html - this file is similar to the add checklist file and it adds a new project to monitor.

# VS Code Formatting Issue

Problem:

Format On Save corrupted Jinja template code in edit_item.html.

Example:

Correct:
{% if item.division == "03" %}

Corrupted:
{% if item.division="" ="03" %}

Temporary Solution:

Disable Format On Save.

Status:

Investigate formatter configuration later.