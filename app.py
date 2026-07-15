
# * ==========================================
# !  app.py
# !  Main application file for the CSI Web App.
# *  ==========================================

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
from routes.daily_reports import daily_reports_bp

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
# ! Add a checklist item to a project.
# * ============================================================
@app.route("/project/<int:project_id>/add_item",
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
# ! Add Project Display project form and save project.
# * ============================================================
@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    if request.method == "POST":

        project_name = request.form["project_name"]

        notes = request.form["notes"]

        new_project = Project(
            project_name=project_name,
            notes=notes
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
        daily_reports=daily_reports
    )
# * ============================================================
# ! Complete Item Mark a checklist item as complete.
# * ============================================================ 
@app.route("/complete_item/<int:item_id>")
def complete_item(item_id):
    

    item = ChecklistItem.query.get_or_404(item_id)

    item.status = "Complete"

    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=item.project_id
        )
    )
# * ============================================================
# ! Add Note
# * ============================================================
@app.route("/project/<int:project_id>/add_note",
    methods=["GET", "POST"]
)
def add_note(project_id):

    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        note_text = request.form["note_text"]

        new_note = ProjectNote(
            project_id=project.id,
            note_text=note_text
        )

        db.session.add(new_note)
        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=project.id
            )
        )

    return render_template(
        "notes/add_note.html",
        project=project
    )
# * ============================================================
# ! Edit Note
# * ============================================================
@app.route("/note/<int:note_id>/edit",
    methods=["GET", "POST"]
)
def edit_note(note_id):

    note = ProjectNote.query.get_or_404(note_id)

    if request.method == "POST":

        note.note_text = request.form["note_text"]

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=note.project_id
            )
        )

    return render_template(
        "notes/edit_note.html",
        note=note
    )
# * ============================================================
# ! Delete Note
# * ============================================================
@app.route("/note/<int:note_id>/delete"
)
def delete_note(note_id):

    note = ProjectNote.query.get_or_404(note_id)

    project_id = note.project_id

    db.session.delete(note)
    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
    )
""" # * ============================================================
# ! Add Daily Report
# * ============================================================
@app.route("/project/<int:project_id>/add_daily_report",
    methods=["GET", "POST"]
)
def add_daily_report(project_id):

    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        report = DailyReport(
            project_id=project_id,
            report_date=datetime.strptime(
            request.form.get("report_date"),
                "%Y-%m-%d"
        ).date(),
            weather=request.form.get("weather"),
            work_performed=request.form.get("work_performed")
        )

        db.session.add(report)
        db.session.commit()

        # * flash("Daily Report added successfully.", "success")

        return redirect(
            url_for(
                "project_detail",
                project_id=project_id
            )
        )
    return render_template(
        "daily_reports/add_daily_report.html",
        project=project
    ) """
""" # * ============================================================
# ! Edit Daily Report
# * ============================================================
@app.route("/daily_report/<int:report_id>/edit",
    methods=["GET", "POST"]
)
def edit_daily_report(report_id):

    report = DailyReport.query.get_or_404(report_id)

    if request.method == "POST":

        report.weather = request.form.get("weather")

        report.work_performed = request.form.get(
            "work_performed"
        )

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=report.project_id
            )
        )

    return render_template(
        "daily_reports/edit_daily_report.html",
        report=report
    ) """
""" # * ============================================================
# ! Delete Daily Report
# * ============================================================
@app.route("/daily_report/<int:report_id>/delete"
)
def delete_daily_report(report_id):

    report = DailyReport.query.get_or_404(report_id)

    project_id = report.project_id

    db.session.delete(report)
    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
    ) """
# * ============================================================
# ! Reopen Item Reopen a completed checklist item.
# * ============================================================
@app.route("/reopen_item/<int:item_id>")
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
@app.route("/delete_item/<int:item_id>")
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
@app.route("/edit_item/<int:item_id>",
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
# * ============================================================
# ! Add RFI
# * ============================================================
@app.route("/project/<int:project_id>/add_rfi",
    methods=["GET", "POST"]
)
def add_rfi(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    if request.method == "POST":

        new_rfi = RFI(
            project_id=project.id,
            rfi_number=request.form["rfi_number"],
            description=request.form["description"],
            discipline=request.form["discipline"],
            date_submitted=datetime.strptime(
                request.form["date_submitted"],
                "%Y-%m-%d"
            ).date(),
            date_due=datetime.strptime(
                request.form["date_due"],
                "%Y-%m-%d"
            ).date(),
            status=request.form["status"]
        )

        db.session.add(new_rfi)
        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=project.id
            )
        )

    return render_template(
        "rfis/add_rfi.html",
        project=project
    )
# * ============================================================
# ! Edit RFI
# * ============================================================
@app.route("/rfi/<int:rfi_id>/edit",
    methods=["GET", "POST"]
)
def edit_rfi(rfi_id):

    rfi = RFI.query.get_or_404(rfi_id)

    if request.method == "POST":

        rfi.rfi_number = request.form[
            "rfi_number"
        ]

        rfi.description = request.form[
            "description"
        ]

        rfi.discipline = request.form[
            "discipline"
        ]

        rfi.date_submitted = datetime.strptime(
            request.form["date_submitted"],
            "%Y-%m-%d"
        ).date()

        rfi.date_due = datetime.strptime(
            request.form["date_due"],
            "%Y-%m-%d"
        ).date()

        rfi.status = request.form[
            "status"
        ]

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=rfi.project_id
            )
        )

    return render_template(
        "rfis/edit_rfi.html",
        rfi=rfi
    )
# * ============================================================
# ! Delete RFI
# * ============================================================
@app.route("/rfi/<int:rfi_id>/delete"
)
def delete_rfi(rfi_id):

    rfi = RFI.query.get_or_404(rfi_id)

    project_id = rfi.project_id

    db.session.delete(rfi)
    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
    )
# * ============================================================
# ! Add Submittal
# * ============================================================
@app.route("/project/<int:project_id>/add_submittal",
    methods=["GET", "POST"]
)
def add_submittal(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    if request.method == "POST":

        new_submittal = Submittal(
            project_id=project.id,
            submittal_number=request.form[
                "submittal_number"
            ],
            description=request.form[
                "description"
            ],
            submitted_by=request.form[
                "submitted_by"
            ],
            discipline=request.form[
                "discipline"
            ],
            date_submitted=datetime.strptime(
                request.form["date_submitted"],
                "%Y-%m-%d"
            ).date(),
            date_due=datetime.strptime(
                request.form["date_due"],
                "%Y-%m-%d"
            ).date(),
            status=request.form[
                "status"
            ]
        )

        db.session.add(new_submittal)
        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=project.id
            )
        )

    return render_template(
        "submittals/add_submittal.html",
        project=project
    )

# * ============================================================
# ! Edit Submittal
# * ============================================================
@app.route("/submittal/<int:submittal_id>/edit",
    methods=["GET", "POST"]
)
def edit_submittal(submittal_id):

    submittal = Submittal.query.get_or_404(
        submittal_id
    )

    if request.method == "POST":

        submittal.submittal_number = request.form[
            "submittal_number"
        ]

        submittal.description = request.form[
            "description"
        ]

        submittal.submitted_by = request.form[
            "submitted_by"
        ]

        submittal.discipline = request.form[
            "discipline"
        ]

        submittal.date_submitted = datetime.strptime(
            request.form["date_submitted"],
            "%Y-%m-%d"
        ).date()

        submittal.date_due = datetime.strptime(
            request.form["date_due"],
            "%Y-%m-%d"
        ).date()

        submittal.status = request.form[
            "status"
        ]

        db.session.commit()

        return redirect(
            url_for(
                "project_detail",
                project_id=submittal.project_id
            )
        )

    return render_template(
        "submittals/edit_submittal.html",
        submittal=submittal
    )

# * ============================================================
# ! Delete Submittal
# * ============================================================
@app.route("/submittal/<int:submittal_id>/delete"
)
def delete_submittal(submittal_id):

    submittal = Submittal.query.get_or_404(
        submittal_id
    )

    project_id = submittal.project_id

    db.session.delete(submittal)
    db.session.commit()

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
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

        project.notes = request.form["notes"]

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

if __name__ == "__main__":
    app.run(debug=True)

