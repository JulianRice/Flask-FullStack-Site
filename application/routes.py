from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

course_data = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, 
        {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, 
        {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, 
        {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, 
        {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")

def index():
    return render_template("index.html", index=True)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term == None:
        term = "2019"
    classes = Course.objects.all()
    #classes = Course.objects.order_by("+courseID") # + is ascending order, - is descending

    #Create variable named course_data and pass the above data into courses.html
    return render_template("courses.html", course_data=classes, courses=True, term=term) 

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if (form.validate_on_submit()):
        user_id     = User.objects.count()
        user_id    += 1

        email       = form.email.data
        password    = form.password.data
        firstName   = form.firstName.data
        lastName    = form.lastName.data
        # username    = form.username.data

        user = User(user_id=user_id, email=email, first_name=firstName, last_name=lastName)
        user.SetPassword(password)
        user.save()
        flash('You have successfully registered! Congrats!')
        return redirect(url_for('index'))
    return render_template("register.html", register=True, form=form, title="Register")

@app.route("/logout")
def logout():
    session['user_id'] = False      #Both types work (this and next)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginForm()
    if (form.validate_on_submit()):
        email       = form.email.data
        password    = form.password.data

        user = User.objects(email=email).first()
        if user and user.GetPassword(password):
            flash(f"{ user.first_name }, you have successfully logged in!", "success")
            session['user_id'] = user.user_id       #Needed to process the enrollment
            session['username'] = user.first_name   #User is logged in and session is active
            return redirect("/index")
        else:
            flash("Sorry, something went wrong", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))

    #When using GET instead of POST, use request.args.get instead of request.form.get()
    courseID      = request.form.get('courseID')
    courseTitle   = request.form.get('title')
    user_id = session.get('user_id')

    if (courseID):
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"You already registered for {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You have enrolled in {courseTitle}!", "success")

    classes = list(User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))
    term    = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, classes=classes, title="Enrollment")

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if (idx == None):
        jdata = course_data
    else:
        jdata = course_data[int(idx)]
    #6 parameters but we'll use two
    return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    #User(user_id=1, first_name="Julian", last_name="Rice", email="julian@ricegames.net", password="Kuribo").save()
    #User(user_id=2, first_name="Kuribo", last_name="Goomba", email="goomba@ricegames.net", password="Julian").save()
    users = User.objects.all()
    return render_template("user.html", users=users)