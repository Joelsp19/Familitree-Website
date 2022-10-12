from datetime import datetime
from familitree import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    password = db.Column(db.String(60),nullable=False,default='null')
    name_first = db.Column(db.String(60),nullable=True)
    name_last = db.Column(db.String(60),nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True) 
    father = db.relationship('Father',backref='kid',lazy=True)
    mother = db.relationship('Mother',backref='kid',lazy=True)
    kid = db.relationship('Kid',backref='parent',lazy=True)
    people = db.relationship('People',backref='people',lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.name_first}', '{self.name_last}','{self.email}' ,'{self.image_file}')"
        
        
class Post(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted =db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}' ,'{self.date_posted}')"

class Father(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name_first = db.Column(db.String(60), nullable=False)
    name_last = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    father_user_id = db.Column(db.Integer,nullable=True)

    
    def __repr__(self):
        return f"User('{self.name_first}', '{self.name_last}')"

class Mother(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name_first = db.Column(db.String(60), nullable=False)
    name_last = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    mother_user_id = db.Column(db.Integer,nullable=True)
    
    def __repr__(self):
        return f"User('{self.name_first}', '{self.name_last}')"

class Kid(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name_first = db.Column(db.String(60), nullable=False)
    name_last = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    kid_user_id = db.Column(db.Integer,nullable=True)
    
    def __repr__(self):
        return f"User('{self.name_first}', '{self.name_last}')"

class People(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name_first = db.Column(db.String(60),nullable=False)
    name_last = db.Column(db.String(60),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"User('{self.name_first}', '{self.name_last}')"

class Relationship(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_one_id = db.Column(db.Integer,nullable=False)
    user_two_id = db.Column(db.Integer,nullable=False)
    relationship_type=db.Column(db.Integer,nullable=False)

    
    def __repr__(self):
        return f"User('{self.user_one_id}', '{self.user_two_id}')"
