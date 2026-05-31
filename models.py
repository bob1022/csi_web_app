
#$============================================
#$models.py
#$Database models for the CSI Web App.
#$Defines the Project and ChecklistItem models using SQLAlchemy.
#$============================================

from database import db


class Project(db.Model):
    
    #$Stores project information.

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_name = db.Column(
        db.String(100),
        nullable=False
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    checklist_items = db.relationship(
        "ChecklistItem",
        backref="project",
        lazy=True
    )

    def __repr__(self):
        return f"<Project {self.project_name}>"
    
class ChecklistItem(db.Model):
    
    #$Stores checklist items for a project.

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False
    )

    division = db.Column(
        db.String(10),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Open"
    )

    def __repr__(self):
        return f"<ChecklistItem {self.description}>"
