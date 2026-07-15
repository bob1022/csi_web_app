# * ============================================================
# ! Daily Reports Blueprint
# * ============================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from database import db

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

daily_reports_bp = Blueprint(
    "daily_reports",
    __name__
)

@daily_reports_bp.route("/daily_reports")
def daily_reports():
    return "Daily Reports Module Working"

# * ============================================================
# ! Add Daily Report
# * ============================================================
@daily_reports_bp.route("/project/<int:project_id>/add_daily_report",
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
    )
# * ============================================================
# ! Edit Daily Report
# * ============================================================
@daily_reports_bp.route("/daily_report/<int:report_id>/edit",
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
    )

# * ============================================================
# ! Delete Daily Report
# * ============================================================
@daily_reports_bp.route("/daily_report/<int:report_id>/delete"
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
    )
