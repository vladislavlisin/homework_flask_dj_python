# Flask
# Разработайте приложение аналогично заданию по Django. Вместо работы с панелью администрирования создайте ограничения
# на возможность выполнять операции Create и Update только зарегистрированным пользователям.

from flask import render_template, request, Flask, flash, url_for, redirect
from forms import StudentForm, UniversityForm, LoginForm, RegisterForm
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
# from sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "DASB3236FG4838GADBY293284NFUSDYUBUFSJDO8"

# db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:GHJCNJZ02!gg@localhost:3306/first_project_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
login_manager = LoginManager(app)


######################################################################################################################
####                                  Models                                                              ############
######################################################################################################################

# нужно установить доп драйвер для работы с mysql через sqlalchemy - pip install pymysql

# Университет
# Полное название
# Сокращенное название
# Дата создания

class UniversityModel(db.Model):

    __tablename__ = 'university'
    id = db.Column(db.Integer, primary_key=True)
    full_title = db.Column(db.String(200), unique=True, nullable=False)
    short_title = db.Column(db.String(15), unique=False, nullable=False)
    foundation_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    students = db.relationship('StudentModel', backref='university_link')

    def __repr__(self):
        return f"<University {self.full_title}>"

# Cтудент
# ФИО
# Дата рождения
# Университет(только из списка университетов, содержащихся в базе)
# Год поступления

class StudentModel(db.Model):

    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(200), unique=False)
    born_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    get_in_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    university = db.Column(db.Integer(), db.ForeignKey('university.id', onupdate="CASCADE", ondelete="CASCADE"))

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(200))


#################################

with app.app_context():
    print()
    #db.create_all()

#################################



# тут нужно инициализировать базу данных и обхект app
#db.init_app(app)
#login_manager = LoginManager()
#login_manager.login_view = 'auth.login' # путь в Blueprint
#login_manager.init_app(app)

@app.route('/')
def index():
    return "Привет, мир!"

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена")


@app.route('/add_student/', methods=["POST", 'GET'])
@app.route('/add_student', methods=["POST", 'GET'])
@login_required
def add_student():

    form = StudentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            st = StudentModel(FIO = request.form["FIO"],
                            born_date = request.form["born_date"],
                            get_in_date = request.form["get_in_date"],
                            university = request.form["university"],
            )

            try:
                db.session.add(st)
                db.session.flush()
                db.session.commit()
                flash('Студент успешно добавлен!', category='success')
            except IntegrityError:
                flash('Ошибка! Возможно Университета с таким ID не существует!', category='error')
                db.session.rollback()
            except:
                flash('Ошибка БД!', category='error')
                db.session.rollback()

    return render_template("add_student.html", form=form)

@app.route('/add_university/', methods=["POST", 'GET'])
@app.route('/add_university', methods=["POST", 'GET'])
@login_required
def add_university():

    form = UniversityForm()
    if request.method == "POST":
        if form.validate_on_submit():
            un = UniversityModel(full_title = request.form["full_title"],
                            short_title = request.form["short_title"],
                            foundation_date = request.form["foundation_date"],
                )

            try:
                db.session.add(un)
                db.session.flush()
                db.session.commit()
                flash('Университет успешно добавлен!', category='success')
            except IntegrityError:
                flash('Ошибка! Полное название Университета должно быть уникальным!', category='error')
                db.session.rollback()
            except Exception:
                flash('Ошибка БД!', category='error')
                db.session.rollback()

    return render_template("add_university.html", form=form)





@app.route('/student_list/')
@app.route('/student_list')
def student_list():
    students = StudentModel.query.all()
    return render_template("student_list.html", students=students)

@app.route('/university_list/')
@app.route('/university_list')
def university_list():
    all_university = UniversityModel.query.all()
    return render_template("university_list.html", all_university=all_university)

@app.route('/student_list/<int:student_id>/')
@app.route('/student_list/<int:student_id>')
def student(student_id):
    st = StudentModel.query.get(student_id)
    return render_template("student.html", st=st)

@app.route('/university_list/<int:university_id>/')
@app.route('/university_list/<int:university_id>')
def university(university_id):
    un = UniversityModel.query.get(university_id)
    return render_template("university.html", un=un)

@app.route('/delete_university/<int:university_id>/')
@app.route('/delete_university/<int:university_id>')
def delete_university(university_id):
    try:
        UniversityModel.query.filter(UniversityModel.id == university_id).delete()
        db.session.flush()
        db.session.commit()
        return redirect(url_for('university_list'))
    except Exception:
        return render_template("Университета с таким id не существует")


@app.route('/delete_student/<int:student_id>/')
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    try:
        StudentModel.query.filter(StudentModel.id == student_id).delete()
        db.session.flush()
        db.session.commit()
        return redirect(url_for('student_list'))
    except Exception:
        return render_template("Университета с таким id не существует")


@app.route('/university_list/<int:university_id>/change/', methods=["POST", 'GET'])
@app.route('/university_list/<int:university_id>/change', methods=["POST", 'GET'])
@login_required
def update_university(university_id):

    info = UniversityModel.query.filter_by(id=university_id).first_or_404()
    form = UniversityForm(full_title=info.full_title,
                         short_title=info.short_title,
                         foundation_date=info.foundation_date,
                         )

    if request.method == "POST":
        form = UniversityForm()
        if form.validate_on_submit():
            info.full_title = request.form["full_title"]
            info.short_title = request.form["short_title"]
            info.foundation_date = request.form["foundation_date"]
            try:
                db.session.commit()
            except IntegrityError:
                flash('Ошибка! Полное название Университета должно быть уникальным!', category='error')
                db.session.rollback()
            except Exception:
                flash('Ошибка БД!', category='error')
                db.session.rollback()

    return render_template("update_university.html", form=form)


@app.route('/student_list/<int:student_id>/change/', methods=["POST", 'GET'])
@app.route('/student_list/<int:student_id>/change', methods=["POST", 'GET'])
@login_required
def update_student(student_id):

    info = StudentModel.query.filter_by(id=student_id).first_or_404()
    form = StudentForm(FIO = info.FIO,
                        born_date = info.born_date,
                        get_in_date = info.get_in_date,
                        university = info.university
                         )

    if request.method == "POST":
        form = StudentForm()
        if form.validate_on_submit():
            info.FIO = request.form["FIO"]
            info.born_date = request.form["born_date"]
            info.get_in_date = request.form["get_in_date"]
            info.university = request.form["university"]
            try:
                db.session.commit()
            except IntegrityError:
                flash('Ошибка! Возможно Университета с таким ID не существует!', category='error')
                db.session.rollback()
            except Exception:
                flash('Ошибка БД!', category='error')
                db.session.rollback()

    return render_template("update_student.html", form=form)



######################################################################################################################
# LOGIN
######################################################################################################################

class UserLogin:

    def from_db(self, user_id, db):
        self.__user = db.session.query(UserModel).filter_by(id=user_id).first_or_404()
        return self

    def create(self, user):
        self.__user = user
        return self


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__user.id

@login_manager.user_loader
def load_user(user_id):
    user = UserLogin()
    return user.from_db(user_id=user_id, db=db)

@app.route('/login/', methods=["POST", 'GET'])
@app.route('/login', methods=["POST", 'GET'])
def login():

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():

            user = UserModel.query.filter_by(login=request.form["login"]).first_or_404()

            if user and check_password_hash(user.password, request.form["password"]):
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                return redirect(url_for("success"))

            flash('Неверный логин/пароль', category='error')

    return render_template("login.html", form=form)

@app.route('/success/')
@app.route('/success')
def success():
    return "Вы успешно зарегистрировались!"

@app.route('/register/', methods=["POST", 'GET'])
@app.route('/register', methods=["POST", 'GET'])
def register():

    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = generate_password_hash(request.form["password"])
            user = UserModel(login=request.form["login"],
                            password=hashed_password,
                            name=request.form["name"],
                                 )
            try:
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                flash('Вы успешно зарегистрировались!', category='success')
                return redirect("/login")
            except IntegrityError:
                flash('Такой логин уже занят!', category='error')
                db.session.rollback()
            except Exception:
                flash('Ошибка БД!', category='error')
                db.session.rollback()

    return render_template("register.html", form=form)

####################################################################################################################
#                                                    differEnt                                                     #
####################################################################################################################



if __name__ == "__main__":
    app.run(debug=True)
