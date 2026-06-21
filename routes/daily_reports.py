from flask import Blueprint

daily_reports_bp = Blueprint(
    "daily_reports",
    __name__
)

@daily_reports_bp.route("/daily_reports")
def daily_reports():
    return "Daily Reports Module Working"