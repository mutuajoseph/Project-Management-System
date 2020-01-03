from app import db

class ProjectsModel(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    projectTitle =db.Column(db.String(45), nullable= False)
    description = db.Column(db.String(120), nullable=False)
    dateCreated = db.Column(db.String(45), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    timeframe = db.Column(db.String(45), nullable=False)
    # 0 = imcomplete & 1 = complete
    status = db.Column(db.String, default=0 )   
    workers  = db.Column(db.Integer, nullable=False)


    # Create
    def create_task(self):
        db.session.add(self)
        db.session.commit()
        

    # fetch records
    @classmethod
    def fetch_records(cls):
        records = ProjectsModel.query.all()
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
    


    
    


