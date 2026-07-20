from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for 
)
from database import db

from models import Project, ProjectNote

from datetime import datetime

notes_bp = Blueprint(
    "notes",
    __name__
)

# * ============================================================
# ! Add Note
# * ============================================================
@notes_bp.route("/project/<int:project_id>/notes.add_note",
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
@notes_bp.route("/note/<int:note_id>/edit",
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
@notes_bp.route("/note/<int:note_id>/delete"
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






""" @app.route(
    "/project/<int:project_id>/add_note",
    methods=["GET", "POST"]
)
def add_note(project_id):
    
    #$ Add a note to a project.

    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        note_text = request.form.get("note_text")

        if not note_text:
            flash("Note text cannot be empty.", "danger")
            return redirect(
                url_for(
                    "project_detail",
                    project_id=project_id
                )
            )

        new_note = ProjectNote(
            project_id=project_id,
            note_text=note_text
        )

        db.session.add(new_note)
        db.session.commit()

        flash("Note added successfully.", "success")
        return redirect(
            url_for(
                "project_detail",
                project_id=project_id
            )
        )

    return render_template(
        "add_note.html",
        project=project
    )                                 """   