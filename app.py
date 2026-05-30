"""
app.py

Main application file for the CSI Web App.
"""

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
    )

from flask import Flask, render_template

from flask import Flask

from database import db
from models import Project, ChecklistItem


app = Flask(__name__)

# SQLite database location
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///csi_database.db"

# Disable warning message
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect database to Flask
db.init_app(app)

# Create database and tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """
    Home page route.
    """
    return "CSI Web App Running"

@app.route("/projects")
def projects():

    project_list = Project.query.all()

    return render_template(
        "index.html",
        projects=project_list
    )

@app.route(
    "/project/<int:project_id>/add_item",
    methods=["GET", "POST"]
)
def add_item(project_id):
    """
    Add a checklist item to a project.
    """

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

@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    """
    Display project form and save project.
    """

    if request.method == "POST":

        project_name = request.form["project_name"]

        new_project = Project(
            project_name=project_name
        )

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("projects"))

    return render_template("add_project.html")

@app.route("/project/<int:project_id>")
def project_detail(project_id):
    """
    Display information for a single project.
    """

    project = Project.query.get_or_404(project_id)

    sorted_items = sorted(
        project.checklist_items,
        key=lambda item: (
            item.status == "Complete",
            item.division
        )
    )

    total_items = len(project.checklist_items)

    completed_items = sum(
        1
        for item in project.checklist_items
        if item.status == "Complete"
    )

    open_items = total_items - completed_items

    if total_items > 0:
        progress_percent = round(
            (completed_items / total_items) * 100
        )
    else:
        progress_percent = 0

    sorted_items = sorted(
        project.checklist_items,
        key=lambda item: (
            item.status == "Complete",
            item.division,
            item.description
        )
    )

    return render_template(
        "project.html",
        project=project,
        total_items=total_items,
        completed_items=completed_items,
        open_items=open_items,
        progress_percent=progress_percent,
        sorted_items=sorted_items
    )

@app.route("/complete_item/<int:item_id>")
def complete_item(item_id):
    """
    Mark a checklist item as complete.
    """

    item = ChecklistItem.query.get_or_404(item_id)

    item.status = "Complete"

    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=item.project_id
        )
    )

@app.route("/reopen_item/<int:item_id>")
def reopen_item(item_id):
    """
    Reopen a completed checklist item.
    """

    item = ChecklistItem.query.get_or_404(item_id)

    item.status = "Open"

    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=item.project_id
        )
    )

@app.route("/delete_item/<int:item_id>")
def delete_item(item_id):
    """
    Delete a checklist item.
    """

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

@app.route(
    "/edit_item/<int:item_id>",
    methods=["GET", "POST"]
)
def edit_item(item_id):
    """
    Edit an existing checklist item.
    """

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

if __name__ == "__main__":
    app.run(debug=True)