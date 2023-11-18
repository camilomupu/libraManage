from schemas.report import Report
from models.tables import Informe

def create_report(new_report: Report, db):
    report = Informe(**new_report.dict())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def exist_report(id: int, db):
    report = db.query(Informe).filter(Informe.id == id).first()
    return report

def all_report(db):
    return db.query(Informe).all()

def delete_report(id: int, db):
    delReport = db.query(Informe).filter(Informe.id == id).first()
    db.delete(delReport)
    db.commit()
    return delReport