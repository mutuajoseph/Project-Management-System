from app import db,bcrypt
# from werkzeug.security  import check_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(45), nullable=False)

    # Create
    def create_task(self):
        db.session.add(self)
        db.session.commit()
    
    # fetch all records
    @classmethod
    def fetch_records(cls):
        records = UserModel.query.all()
        return records
    
    # fetch by email
    @classmethod
    def fetch_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    # update record
    @classmethod
    def update_by_id(cls,id,newUsername, newEmail):
        record = UserModel.query.filter_by(id=id).first()
        if record:
            record.username = newUsername
            record.email = newEmail
            db.session.commit()
            return True
        else:
            return False
    
    # delete record
    @classmethod
    def delete_by_id(cls,id):
        user = UserModel.query.filter_by(id=id)
        if user.first():
            user.delete()
            db.session.commit()
            return True
        else:
            return False

    # Check if email exist
    @classmethod
    def check_email_exist(cls,email):
        record = cls.query.filter_by(email=email).first()
        if record:
            return True
        else:
            return False
    
    # Check password validity
    @classmethod
    def check_password(cls,email,password):
        record = cls.query.filter_by(email=email).first()
        if record and bcrypt.check_password_hash(record.password, password) :
            return True
        else:
            return False

   
    

    

