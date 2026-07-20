
# & ============================================================
# ! Add RFI
# & ============================================================
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for
)

from models import Project,RFI

from datetime import datetime

from database import db

rfi = Blueprint("rfi", __name__)


@rfi.route("/project/<int:project_id>/add_rfi",
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
        "rfi/add_rfi.html",
        project=project
    )

# * ============================================================
# ! Edit RFI
# * ============================================================
@rfi.route("/rfi/<int:rfi_id>/edit",
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
        "rfi/edit_rfi.html",
        rfi=rfi
    )
# * ============================================================
# ! Delete RFI
# * ============================================================
@rfi.route("/rfi/<int:rfi_id>/delete"
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
