# & ============================================================
# ! Checklist items. test
# & ============================================================
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for
)

from models import ChecklistItem

from database import db

from models import (
    Project,
    ChecklistItem
)

checklist = Blueprint("checklist", __name__)


# * ============================================================
# ! Complete Item  -  Mark a checklist item as complete.
# * ============================================================ 
@checklist.route("/complete_item/<int:item_id>")
def complete_item(item_id):
    

    item = ChecklistItem.query.get_or_404(item_id)

    item.status = "Complete"

    db.session.commit()

    return redirect(
        url_for("project_detail", project_id=item.project_id
        )
    )

# * ============================================================
# ! Add a checklist item to a project.
# * ============================================================
@checklist.route("/project/<int:project_id>/add_item",
    methods=["GET", "POST"]
)
def add_item(project_id):
    
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        division = request.form["division"]

        description = request.form["description"]

        new_item = ChecklistItem(
            project_id=project.id,
            division=division,
            description=description,
            status="Open"
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=project.id
            )
        )

    return render_template(
        "add_item.html",
        project=project
    )
# * ============================================================
# ! Reopen Item Reopen a completed checklist item.
# * ============================================================
@checklist.route("/reopen_item/<int:item_id>")
def reopen_item(item_id):

    item = ChecklistItem.query.get_or_404(item_id)

    item.status = "Open"

    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=item.project_id
        )
    )

# * ============================================================
# ! Delete Item Delete a checklist item.
# * ============================================================
@checklist.route("/delete_item/<int:item_id>")
def delete_item(item_id):

    item = ChecklistItem.query.get_or_404(item_id)

    project_id = item.project_id

    db.session.delete(item)

    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
    )

# * ============================================================
# ! Edit Item Edit an existing checklist item.
# * ============================================================
@checklist.route("/edit_item/<int:item_id>",
    methods=["GET", "POST"]
)
def edit_item(item_id):

    item = ChecklistItem.query.get_or_404(item_id)

    if request.method == "POST":

        item.division = request.form["division"]

        item.description = request.form["description"]

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=item.project_id
            )
        )

    return render_template(
        "edit_item.html",
        item=item
    )