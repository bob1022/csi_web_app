
@app.route(
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
    )                                   