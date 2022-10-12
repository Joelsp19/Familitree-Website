import os
import secrets
from PIL import Image 
from flask import render_template, url_for, flash, redirect,request
from familitree import app, db, bcrypt
from familitree.form import RegistrationForm, LoginForm, UpdateAccountForm, FamilyForm, IsThisYouForm,KidForm, AddPersonForm, AddRelationshipForm
from familitree.models import User,Post,Father,Mother,Kid,People, Relationship
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title="about")
    
@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('userHome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email= form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} , your account has been created! You can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title="register", form = form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userHome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('userHome'))
        else:
            flash('Login Unsuccessful. Check email and password', 'danger')
    return render_template('login.html',title="login", form= form)

@app.route("/userHome")
@login_required
def userHome():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('userHome.html',title="myhome",image_file=image_file)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
    
@app.route("/account" , methods=['GET','POST'])
@login_required
def account():
    form =UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data = current_user.username  
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title="account",errorOnTop=True,image_file=image_file, form=form)
   
    
@app.route("/logout" )
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
 

infoStep=0

@app.route("/myFamily", methods=['GET','POST'])
@login_required    
def family():
    if current_user.father and current_user.mother and current_user.name_first and current_user.name_last:
        father = Father.query.filter(current_user.id==Father.user_id).first()
        mother = Mother.query.filter(current_user.id==Mother.user_id).first()
        if current_user.kid:
            kid = Kid.query.filter(current_user.id==Kid.user_id).all()
        else:
            kid = None

        legend="Update Info"
    else:
        legend="Get started"
        father=None
        mother=None
        kid=None
    return render_template('myFamilyUpdate.html',title='myFam',legend=legend, father=father, mother=mother,kid =kid)



@app.route("/myFamily/yourInfo", methods=['GET','POST'])
@login_required    
def familyYourName():
    form = FamilyForm()
    name = 'Update Your' 
    global infoStep 
    infoStep= 1
    user = User.query.filter(User.id ==current_user.id).first()
    
    if user.name_first == None and user.name_last == None: 
        form = FamilyForm()
        name = 'Your'
        if form.validate_on_submit():
            user.name_first= form.name_first.data
            user.name_last=form.name_last.data
            db.session.commit()
            return redirect(url_for('familyFatherName'))
        return render_template('myFamily.html',title='myFam', form=form, name=name )

    else:    
       
        if form.validate_on_submit():
            user.name_first= form.name_first.data
            user.name_last=form.name_last.data
            db.session.commit()
            return redirect(url_for('familyFatherName'))
        elif request.method=='GET':
            form.name_first.data = user.name_first
            form.name_last.data = user.name_last   
        return render_template('myFamily.html',title='myFam', form=form, name=name )

        
@app.route("/myFamily/fatherInfo", methods=['GET','POST'])
@login_required    
def familyFatherName():
    global infoStep
    infoStep= 2
    if current_user.father:
        form = FamilyForm()
        name = 'Update Father\'s'
       
        father = Father.query.filter(current_user.id==Father.user_id).first()

        if form.validate_on_submit():
            father.father_user_id=None
            father.name_first= form.name_first.data
            father.name_last=form.name_last.data
            db.session.commit()
            possibleFather = User.query.filter(User.name_first==form.name_first.data).filter(User.name_last==form.name_last.data).all();
            if possibleFather:
                return redirect(url_for('isThisYou'))
            return redirect(url_for('familyMotherName'))
        elif request.method=='GET':
            form.name_first.data = father.name_first
            form.name_last.data = father.name_last   
        
        return render_template('myFamily.html',title='myFam', form=form, name=name,father=father )
        
    else:
        form = FamilyForm()
        name = 'Father\'s'
        if form.validate_on_submit():
            father = Father(name_first = form.name_first.data, name_last = form.name_last.data,kid=current_user)
            db.session.add(father)
            db.session.commit()
            return redirect(url_for('familyMotherName'))
        return render_template('myFamily.html',title='myFam', form=form, name=name )

@app.route("/myFamily/motherInfo", methods=['GET','POST'])
@login_required    
def familyMotherName():
    global infoStep 
    infoStep= 3
    
    if current_user.mother:
        form = FamilyForm()
        name = 'Update Mother\'s'

        mother = Mother.query.filter(current_user.id==Mother.user_id).first()

        if form.validate_on_submit():
            mother.mother_user_id=None
            mother.name_first= form.name_first.data
            mother.name_last=form.name_last.data
            db.session.commit()
            possibleMother = User.query.filter(User.name_first==form.name_first.data).filter(User.name_last==form.name_last.data).all();
            if possibleMother:
                return redirect(url_for('isThisYou'))
            return redirect(url_for('familyKidName'))
        elif request.method=='GET':
            form.name_first.data = mother.name_first
            form.name_last.data = mother.name_last   
        
        return render_template('myFamily.html',title='myFam', form=form, name=name,mother=mother )
            
    else:
        form = FamilyForm()
        name = 'Mother\'s'
        
        if form.validate_on_submit():
            mother = Mother(name_first = form.name_first.data, name_last = form.name_last.data,kid=current_user)
            db.session.add(mother)
            db.session.commit()  
            return redirect(url_for('familyKidName'))
    return render_template('myFamily.html',title='myFam', form=form, name=name )


numKids=0
@app.route("/myFamily/kidInfo", methods=['GET','POST'])
@login_required    
def familyKidName():
    global infoStep 
    global numKids
    infoStep=4
    notDelete=True
    allKids = Kid.query.filter(current_user.id==Kid.user_id).all()

    if numKids>=0:
        if numKids<=len(current_user.kid)-1:        
            form = KidForm()
            name = 'Update '+str(numKids+1)+' Kid\'s'
            kid = allKids[numKids]
            if form.validate_on_submit():
                if form.noKid.data:
                    for i in allKids:
                        db.session.delete(i)
                        db.session.commit()
                    flash('Your family has been updated!', 'success')
                    infoStep=0
                    numKids=0
                    return redirect(url_for('family'))   
                kid.kid_user_id=None
                kid.name_first= form.name_first.data
                kid.name_last=form.name_last.data
                db.session.commit()
                
                if form.addKid.data and form.deleteKid.data:
                    db.session.delete(kid)
                    db.session.commit()
                    notDelete=False
                if form.addKid.data:
                    numKids+=1
                elif form.deleteKid.data:
                    db.session.delete(kid)
                    db.session.commit()
                    numKids-=1
                    notDelete=False
                else:    
                    flash('Your family has been updated!', 'success')
                    infoStep=5
                    numKids=0
                
                possibleKid = User.query.filter(User.name_first==form.name_first.data).filter(User.name_last==form.name_last.data).all();
                if possibleKid and notDelete:
                    return redirect(url_for('isThisYou')) 
                if infoStep==5:
                    infoStep=0
                    numKids=0
                    return redirect(url_for('family'))
                else:
                    return redirect(url_for('familyKidName'))
    
                
            elif request.method=='GET':
                form.name_first.data = kid.name_first
                form.name_last.data = kid.name_last    
            return render_template('myFamily.html',title='myFam', form=form, name=name,kid=kid )

        else:
            form = KidForm()
            name = 'Kid ' + str(numKids+1) + '\'s'
            
            if form.validate_on_submit():
                if form.noKid.data:
                    if allKids:
                        for i in allKids:
                            db.session.delete(i)
                            db.session.commit()
                    flash('Your family has been updated!', 'success')
                    infoStep=0
                    numKids=0
                    return redirect(url_for('family'))   
               
                kid = Kid(name_first = form.name_first.data, name_last = form.name_last.data,parent=current_user)
                db.session.add(kid)
                db.session.commit() 
                numKids+=1
                if form.addKid.data and form.deleteKid.data:
                    db.session.delete(kid)
                    db.session.commit()
                    numKids-=1
                    notDelete=False

                elif form.addKid.data:
                    infoStep=4
                elif form.deleteKid.data:
                    db.session.delete(kid)
                    db.session.commit()
                    numKids-=2
                    notDelete=False
                else:    
                    flash('Your family has been updated!', 'success')
                    infoStep=5
                    numKids=0
                possibleKid = User.query.filter(User.name_first==form.name_first.data).filter(User.name_last==form.name_last.data).all();
                if possibleKid and notDelete:
                    return redirect(url_for('isThisYou')) 
                if infoStep==5:
                    infoStep=0
                    numKids=0
                    return redirect(url_for('family'))
                else:
                    return redirect(url_for('familyKidName'))
    
        return render_template('myFamily.html',title='myFam', form=form, name=name )

    else:
        flash('Your family has been updated!', 'success')
        infoStep=0
        numKids=0
        return redirect(url_for('family'))    





@app.route("/isThisYou" , methods=['GET','POST'])
@login_required
def isThisYou():
    global infoStep
    global numKids
    form = IsThisYouForm() 
    
    if infoStep == 2:
        father = Father.query.filter(current_user.id==Father.user_id).first()
        possibleParent = User.query.filter(User.name_first==father.name_first).filter(User.name_last==father.name_last).first();
        if form.validate_on_submit():
            if form.checkbox.data:
                father.father_user_id = possibleParent.id
                db.session.commit()
            return redirect(url_for('familyMotherName'))

    elif infoStep== 3:
        mother = Mother.query.filter(current_user.id==Mother.user_id).first()
        possibleParent = User.query.filter(User.name_first==mother.name_first).filter(User.name_last==mother.name_last).first();
        if form.validate_on_submit():
            if form.checkbox.data:
                mother.mother_user_id = possibleParent.id
                db.session.commit()
            return redirect(url_for('familyKidName'))
    elif infoStep==4:
        kid = Kid.query.filter(current_user.id==Kid.user_id).all()[numKids-1]
        possibleParent = User.query.filter(User.name_first==kid.name_first).filter(User.name_last==kid.name_last).first();
        if form.validate_on_submit():
            if form.checkbox.data:
                kid.kid_user_id = possibleParent.id
                db.session.commit()
            return redirect(url_for('familyKidName'))
    else:
        kid = Kid.query.filter(current_user.id==Kid.user_id).all()[numKids-1]
        possibleParent = User.query.filter(User.name_first==kid.name_first).filter(User.name_last==kid.name_last).first();
        if form.validate_on_submit():
            if form.checkbox.data:
                kid.kid_user_id = possibleParent.id
                db.session.commit()
                infoStep=0
                numKids=0
                flash('Your family has been updated')
            return redirect(url_for('family'))
    
    return render_template('isThisYou.html',title='isThisYou',form=form, possibleParent = possibleParent)

    
@app.route("/familitree", methods=['GET','POST'])
@login_required
def familyTree():
    person = People.query.filter_by(people=current_user).all()
    relationship = Relationship.query.all()
    
    return render_template('myFamilyTree.html',title='myFamTree',person=person,relationship = relationship)

@app.route("/drawFamilitree/<id>", methods=['GET','POST'])
@login_required
def drawFamilyTree(id):
    person = People.query.all()
    relationship = Relationship.query.all()
    cp = People.query.filter(People.id==id).first()
    cpr = Relationship.query.filter(Relationship.user_one_id==cp.id).all()
    
    return render_template('drawFamilyTree.html',title='myFamTree',person=person,relationship = relationship, cp=cp, cpr=cpr)



@app.route("/updatePeople/<id>", methods=['GET','POST'])
@login_required
def updatePeople(id):
    form = AddPersonForm()
    name = "Update person " +str(id)
    p = People.query.filter(People.id==id).first()
    if form.validate_on_submit():
        p.name_first= form.name_first.data
        p.name_last= form.name_last.data
        db.session.commit()
        flash(f'{form.name_first.data} {form.name_last.data} has been updated', 'success')
        return redirect(url_for('familyTree'))
    elif request.method=='GET':
        form.name_first.data = p.name_first
        form.name_last.data = p.name_last
    return render_template('addPeople.html',title='updatePeople', form=form, name=name)
 
    
@app.route("/addPeople", methods=['GET','POST'])
@login_required
def addPeople():
    form = AddPersonForm()
    name= "Add a person"
    if form.validate_on_submit():
        person = People(name_first=form.name_first.data,name_last=form.name_last.data,people=current_user)
        db.session.add(person)
        db.session.commit()
        flash(f'{form.name_first.data} {form.name_last.data} has been added', 'success')
        return redirect(url_for('familyTree'))
    return render_template('addPeople.html',title='addPeople', form=form, name=name)
  
@app.route("/updateRelationship/<id>", methods=['GET','POST'])
@login_required
def updateRelationship(id):
    form = AddRelationshipForm()
    name = "Update Relationship "
    p = People.query.all()
    r = Relationship.query.filter(Relationship.id==id).first()

    if form.validate_on_submit():
        r.user_one_id= form.user_one_id.data
        r.user_two_id= form.user_two_id.data
        r.relationship_type = form.relationship_type.data
        db.session.commit()
        flash(f'{p[form.user_one_id.data-1].name_first} {p[form.user_one_id.data-1].name_last}\'s and {p[form.user_two_id.data-1].name_first} {p[form.user_two_id.data-1].name_last}\'s relationship has been updated', 'success')
        return redirect(url_for('familyTree'))
    elif request.method=='GET':
        form.user_one_id.data = r.user_one_id
        form.user_two_id.data = r.user_two_id
        form.relationship_type.data = r.relationship_type    
    return render_template('addRelationships.html',title='updatePeople', form=form, name=name, p=p)
   
@app.route("/addRelationships", methods=['GET','POST'])
@login_required
def addRelationships():
    p = People.query.all()
    form = AddRelationshipForm()
    name="Add a relationship"
  
    if form.validate_on_submit():
        rel = Relationship(user_one_id=form.user_one_id.data, user_two_id=form.user_two_id.data, relationship_type = form.relationship_type.data)
        db.session.add(rel)
        db.session.commits()
        flash(f'{p[form.user_one_id.data-1].name_first} {p[form.user_one_id.data-1].name_last}\'s and {p[form.user_two_id.data-1].name_first} {p[form.user_two_id.data-1].name_last}\'s relationship has been added', 'success')
        return redirect(url_for('familyTree'))
    return render_template('addRelationships.html',title='addRelationship', form=form, name=name, p=p)


    