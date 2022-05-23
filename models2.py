from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db2 = SQLAlchemy()
login2 = LoginManager()

class UserModel2 (UserMixin, db2.Model):
    __tablename__ = 'users2'
    
    id = db2.Column(db2.Integer, primary_key=True)
    username = db2.Column(db2.String(20), unique=True, nullable=False)
    password_hash = db2.Column(db2.String(255),nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)   

@login2.user_loader
def load_user(id):
    return UserModel2.query.get(int(id))
    
