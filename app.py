
# & ==========================================
# !  app.py
# !  Main application file for the CSI Web App.
# &  ==========================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
    )

# @ from flask import Flask, render_template

# @ from flask import Flask

from database import db
# @ from models import Project, ChecklistItem, ProjectNote

from datetime import datetime

from models import (
    Project,
    ChecklistItem,
    ProjectNote,
    Instruction,
    RFI,
    Submittal,
    DailyReport
)
from routes.checklist_routes import checklist

from routes.daily_reports import daily_reports_bp

from routes.notes import notes_bp

from routes.rfi import rfi

from routes.submittals import submittals

app = Flask(__name__)
app.secret_key = "csi-development-key"

# $ SQLite database location
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///csi_database.db"

# $ Disable warning message
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# $ Connect database to Flask
db.init_app(app)

# $ Create database and tables
with app.app_context():
    db.create_all()
app.register_blueprint(daily_reports_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(checklist)
app.register_blueprint(rfi)
app.register_blueprint(submittals)

# $ Home page route
@app.route("/")
def home():
    
    return "CSI Web App Running"
# * ============================================================
# ! Projects list
# * ============================================================
@app.route("/projects")
def projects():

    project_list = Project.query.all()

    project_data = []

    for project in project_list:

        total_items = len(project.checklist_items)

        completed_items = len(
            [
                item
                for item in project.checklist_items
                if item.status == "Complete"
            ]
        )

        open_items = total_items - completed_items

        if total_items > 0:

            progress_percent = int(
                (completed_items / total_items) * 100
            )

        else:

            progress_percent = 0

        project_data.append(
            {
                "project": project,
                "total_items": total_items,
                "completed_items": completed_items,
                "open_items": open_items,
                "progress_percent": progress_percent
            }
        )

    return render_template(
        "index.html",
        project_data=project_data
    )
# * ============================================================
# ! Add Project Display project form and save project.
# * ============================================================
@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    if request.method == "POST":

        project_name = request.form["project_name"]

        project_description = request.form["project_description"]

        new_project = Project(
            project_name=project_name,
            project_description=project_description
    )

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("projects"))

    return render_template("add_project.html")
# * ============================================================
# ! Project Detail Display information for a single project.
# * ============================================================
@app.route("/project/<int:project_id>")
def project_detail(project_id):

    project = Project.query.get_or_404(project_id)
    # $ Sort Checklist Items
    # $ Open items appear first.
    # $ Completed items appear last.
    # $ Within each group, sort by CSI Division.

    daily_reports = sorted(
        project.daily_reports,
        key=lambda report: report.report_date,
        reverse=True
    )

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

    status_order = {
    "Open": 0,
    "In Progress": 1,
    "Complete": 2
    }

    sorted_items = sorted(
        project.checklist_items,
        key=lambda item: (
            status_order.get(item.status, 99),
            item.division
        )
    )

    return render_template(
    "project.html",
    project=project,
    total_items=total_items,
    completed_items=completed_items,
    open_items=open_items,
    progress_percent=progress_percent,
    sorted_items=sorted_items,
    daily_reports=daily_reports,
)
# * ============================================================
# ! Display and edit project form and save changes.
# * ============================================================

@app.route("/edit_project/<int:project_id>",
    methods=["GET", "POST"]
)
def edit_project(project_id):


    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        project.project_name = request.form["project_name"]

        project.project_description = request.form["project_description"]

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=project.id
            )
        )

    return render_template(
        "edit_project.html",
        project=project
    )

# * ============================================================
# ! Delete Project
# * ===========================================================

@app.route("/delete_project/<int:project_id>")
def delete_project(project_id):

    project = Project.query.get_or_404(project_id)

    db.session.delete(project)

    db.session.commit()

    return redirect(
        url_for("projects")
    )

# * ============================================================
# ! Mark Item In Progress
# * ============================================================

@app.route("/in_progress_item/<int:item_id>")
def in_progress_item(item_id):

    item = ChecklistItem.query.get_or_404(item_id)

    item.status = "In Progress"

    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=item.project_id
        )
    )
    


    app.run(debug=True)


# * ============================================================
# ! Add Instruction
# * ============================================================
@app.route("/project/<int:project_id>/add_instruction",
    methods=["GET", "POST"]
)
def add_instruction(project_id):

    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        instruction_text = request.form["instruction_text"]

        new_instruction = Instruction(
            project_id=project.id,
            instruction_text=instruction_text
        )

        db.session.add(new_instruction)
        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=project.id
            )
        )

    return render_template(
        "instruction/add_instruction.html",
        project=project
    )
# * ============================================================
# ! Edit Instructions
# * ============================================================
@app.route("/instruction/<int:instruction_id>/edit",
    methods=["GET", "POST"]
)
def edit_instruction(instruction_id):

    instruction = Instruction.query.get_or_404(
        instruction_id
    )

    if request.method == "POST":

        instruction.instruction_text = request.form[
            "instruction_text"
        ]

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=instruction.project_id
            )
        )

    return render_template(
        "instruction/edit_instruction.html",
        instruction=instruction
    )
# * ============================================================
# ! Delete Instruction
# * ============================================================
@app.route("/instruction/<int:instruction_id>/delete"
)
def delete_instruction(instruction_id):

    instruction = Instruction.query.get_or_404(
        instruction_id
    )

    project_id = instruction.project_id

    db.session.delete(instruction)
    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
    )
@app.route("/routes")
def routes():
    return "<br>".join(
        sorted(rule.endpoint for rule in app.url_map.iter_rules())
    )

if __name__ == "__main__":
    app.run(debug=True)