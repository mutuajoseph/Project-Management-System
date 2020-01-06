from main import db
from datetime import datetime

class ProjectsModel(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    projectTitle =db.Column(db.String(45), nullable= False)
    description = db.Column(db.String(120), nullable=False)
    dateCreated = db.Column(db.String(45), default=datetime.now())
    cost = db.Column(db.Integer, nullable=False)
    timeframe = db.Column(db.String(45), nullable=False)
    # 0 = imcomplete & 1 = complete
    status = db.Column(db.String, default='Incomplete')   
    workers  = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    # Create
    def create_task(self):
        db.session.add(self)
        db.session.commit()
        

    # fetch records
    @classmethod
    def fetch_records(cls,id):
        records = ProjectsModel.query.filter_by(user_id=id).all()
        return records

    # update record
    @classmethod
    def update_by_id(cls,id,newProjectTitle,newDescription,newDateCreated,newCost,newTimeframe,newStatus, newWorkers):
        record = ProjectsModel.query.filter_by(id=id).first()
        if record:
            record.projectTitle = newProjectTitle
            record.description = newDescription
            record.dateCreated = newDateCreated
            record.cost = newCost
            record.timeframe = newTimeframe
            record.status = newStatus
            record.workers = newWorkers
            db.session.commit()
            return True
        else:
            return False
    
     # delete record
    @classmethod
    def delete_by_id(cls,id):
        project = ProjectsModel.query.filter_by(id=id)
        if project.first():
            project.delete()
            db.session.commit()
            return True
        else:
            return False
    


    
    


