
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

    project_description = db.Column(
    db.Text,
    nullable=True
    )
    project_notes = db.relationship(
        "ProjectNote",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan"
    )

    instructions = db.relationship(
        "Instruction",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan"
    )

    rfis = db.relationship(
        "RFI",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan"
    )

    submittals = db.relationship(
        "Submittal",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan"
    )

    checklist_items = db.relationship(
        "ChecklistItem",
        backref="project",
        lazy=True,
        cascade="all, delete-orphan"
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

class ProjectNote(db.Model):

    #$  Stores notes for a project.

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False
    )

    note_text = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<ProjectNote {self.id}>"
    
class Instruction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False
    )

    instruction_text = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<Instruction {self.id}>" 

class RFI(db.Model):
    #$ Class RFI

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False
    )

    rfi_number = db.Column(
        db.String(20),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=False
    )

    discipline = db.Column(
        db.String(50),
        nullable=False
    )

    date_submitted = db.Column(
        db.Date,
        nullable=False
    )

    date_due = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Open"
    )

    def __repr__(self):
        return f"<RFI {self.rfi_number}>"  
class Submittal(db.Model):
    #$ Class Submittal

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False
    )

    submittal_number = db.Column(
        db.String(20),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=False
    )

    submitted_by = db.Column(
        db.String(100),
        nullable=False
    )

    discipline = db.Column(
        db.String(50),
        nullable=False
    )

    date_submitted = db.Column(
        db.Date,
        nullable=False
    )

    date_due = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    def __repr__(self):
        return (
            f"<Submittal "
            f"{self.submittal_number}>"
        )

class DailyReport(db.Model):
    #$ Class DailyReport
    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False
    )

    report_date = db.Column(db.Date, nullable=False)

    weather = db.Column(db.String(100))

    work_performed = db.Column(db.Text)

    delays = db.Column(db.Text)

    safety_notes = db.Column(db.Text)

    tomorrow_work = db.Column(db.Text)

    general_notes = db.Column(db.Text)

    project = db.relationship(
        'Project',
        backref=db.backref('daily_reports', lazy=True)
    )
   