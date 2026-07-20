
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for
)

from models import Project,RFI, Submittal

from datetime import datetime

from database import db

submittals = Blueprint("submittals", __name__)

# * ============================================================
# ! Add Submittal
# * ============================================================
@submittals.route("/project/<int:project_id>/add_submittal",
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
@submittals.route("/submittal/<int:submittal_id>/edit",
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
@submittals.route("/submittal/<int:submittal_id>/delete"
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
