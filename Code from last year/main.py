import sqlalchemy.exc

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user
from forms import UserForm, LoginForm, LogoutForm, SettingsForm

from app import app, db, lm
# import models #import after importing app and db always

from models import User, Category, Course, Course_User, recreate_all_databases


# recreate_all_databases()

@lm.user_loader
def user_loader(id):
    user = db.session.get(User, id)
    return user


@app.route('/User/Check', methods=['GET', 'POST'])
def check():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        print("logout")
        redirect(url_for("check"))
    return render_template("helloworld.html", form=form)


def checkUniqueness(column, form):
    query = db.session.query(User).filter(getattr(User, column) == form.__getattribute__(column).data).first()
    print(f'query: {query}')
    if query is None:
        return True
    # checkUnique returns true if unique; if there is no match
    else:
        return False


@app.route('/User/Login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    register_form = UserForm()
    if login_form.validate_on_submit() and login_form.login.data:
        print("Log in form validated")
        user = db.session.query(User).filter(User.username == login_form.username.data).first()
        print(f'login{user}')
        if user is not None:
            passwordCheck = user.check_password(login_form.password.data)
            print(f'pass{login_form.password.data} '
                  f'checkpass{passwordCheck}')
            if passwordCheck is True:
                print(f'remember: {login_form.remember.data}')
                remember = login_form.remember.data
                login_user(user, remember=remember)
                print(f'{current_user}')
            else:
                print("Failed Login")
            return redirect(url_for("check"))
        else:
            print("not a user")
    if register_form.validate_on_submit():
        print("Register Form Validated")
        uniques = ("username", "email")
        uniquecheck = []
        for column in uniques:
            uniquecheck.append(checkUniqueness(column, register_form))
            print(f'uniquecheck: {uniquecheck}')
        if all(uniquecheck):
            print("Unique checking passed")
            toAddUser = User(
                username=register_form.username.data,
                password=register_form.password.data,
                # first_name=register_form.first_name.data,
                # last_name=register_form.last_name.data,
                category=register_form.category.data,
                email=register_form.email.data,
            )
            # Dont need to define date_added, its default is current time, leave it to use that
            for course in ("IELTS", "B1", "Grammar"):
                if request.form.get(f"course_{course}") == "y":
                    toAddUser.courses.append(db.session.query(Course).filter(Course.name == course).first())

            with open('textoutput.txt', 'a') as f:
                f.write(str(toAddUser))

            db.session.add(toAddUser)
            del toAddUser
            print("Committing")
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as err:
                with open('textoutput.txt', 'a') as f:
                    f.write(f'\n\n\n Integrity error >{err} < Integrity error')
            except sqlalchemy.exc.InvalidRequestError as err:
                with open('textoutput.txt', 'a') as f:
                    f.write(f'\n\n\n Invalid Request Error >{err} < Invalid Request Error')
            try:
                with open('textoutput.txt', 'a') as f:
                    f.write(f'\n\n\nuser.query.all{User.query.all()}')
            except sqlalchemy.exc.PendingRollbackError as err:
                with open('textoutput.txt', 'a') as f:
                    f.write(f'\n\n\nPending Rollback Error > {err} < Pending Rollback Error')
                db.session.rollback()

            return render_template('login.html', login_form=login_form, register_form=register_form)
    elif len(register_form.errors) == 0:
        print("not errors")
        # return render_template('login.html', login_form=login_form, register_form=register_form)
    else:print(register_form.register.data)
    with open('textoutput.txt', 'a') as f:
        f.write(f'else form.submit.errs{str(register_form.errors)}' + "\n")
    print("test")
    print(login_form.errors)
    return render_template('login.html', login_form=login_form, register_form=register_form)


def validateAddUser(form):
    """extracted from add_user
    checks the form to see if each validated.
    Form validators can check for some things but others must be checked in more complex ways."""
    # Password match check
    pass1 = form.password.data
    pass2 = form.confirm_password.data
    if pass1 == pass2:
        passcheck = True
    else:
        passcheck = False
    columns = ("username", "email", "phone_number")
    columncount = 0
    for column in columns:
        if checkUniqueness(column, form) is True:
            columncount += 1
    if columncount == len(columns):
        uniquecheck = True
    else:
        uniquecheck = False
    if uniquecheck is True and passcheck is True:
        return True
    else:
        return False


#@app.route('/User/Add', methods=['GET', 'POST'])
# def add_user():
#     form = UserForm()
#     print(form.validate_on_submit())
#     if form.validate_on_submit():  # valid form inputs
#         if validateAddUser(form) is True:  # Including ones that have to be checked
#             # server side such as uniqueness
#             toAddUser = User(
#                 username=form.username.data,
#                 password=form.password.data,
#                 first_name=form.first_name.data,
#                 last_name=form.last_name.data,
#                 category=form.category.data,
#                 email=form.email.data,
#                 phone_number=form.phone_number.data,
#                 address=form.address.data,
#                 gender=form.gender.data,
#                 date_of_birth=form.date_of_birth.data,
#             )
#             # Dont need to define date_added, its default is current time, leave it to use that
#             for course in ("IELTS", "B1", "Grammar"):
#                 if request.form.get(f"course_{course}") == "y":
#                     toAddUser.courses.append(db.session.query(Course).filter(Course.name == course).first())
#
#             with open('textoutput.txt', 'a') as f:
#                 f.write(str(toAddUser))
#
#             db.session.add(toAddUser)
#             del toAddUser
#             print("Committing")
#             try:
#                 db.session.commit()
#             except sqlalchemy.exc.IntegrityError as err:
#                 with open('textoutput.txt', 'a') as f:
#                     f.write(f'\n\n\n Integrity error >{err} < Integrity error')
#             except sqlalchemy.exc.InvalidRequestError as err:
#                 with open('textoutput.txt', 'a') as f:
#                     f.write(f'\n\n\n Invalid Request Error >{err} < Invalid Request Error')
#             try:
#                 with open('textoutput.txt', 'a') as f:
#                     f.write(f'\n\n\nuser.query.all{User.query.all()}')
#             except sqlalchemy.exc.PendingRollbackError as err:
#                 with open('textoutput.txt', 'a') as f:
#                     f.write(f'\n\n\nPending Rollback Error > {err} < Pending Rollback Error')
#                 db.session.rollback()
#             return render_template("add_user.html", form=form)
#     elif form.is_submitted():#todo fix
#         if len(form.errors) == 0:
#             print("not errors")
#             return render_template("add_user.html", form=form, errors=form.errors)
#         with open('textoutput.txt', 'a') as f:
#             f.write(f'else form.submit.errs{str(form.errors)}' + "\n")
#     return render_template("add_user.html", form=form, errors=None)


# @app.route('/User/Settings', methods=['GET', 'POST'])
# def settings():
#     form = SettingsForm()
#     if form.validate_on_submit():
#         pass
#     return render_template('settings.html', form=form)
#     pass
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html',methods=['GET'])
@app.route('/About')
def about():
    return render_template('about.html',methods=['GET'])
@app.route('/Blog')
def blog():
    return render_template('Blog.html')
@app.route('/Contact')
def contact():
    return render_template('Contact.html')
if __name__ == '__main__':
    app.run()
