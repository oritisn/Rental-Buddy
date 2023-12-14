import os

import flask_login
import sqlalchemy.exc

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_uploads import UploadSet, configure_uploads, UploadNotAllowed
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegisterForm, LoginForm, LogoutForm, PortalForm, LeaseUploadForm, DisplayForm
from flask_wtf.csrf import CSRFError

from app import app, db, lm, basedir
# import models #import after importing app and db always

from models import User, Tenant, Landlord, Lease, Lease_Landlord
from upload_config import leases


# recreate_all_databases()
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html'), 400


@lm.user_loader
def user_loader(id):
    user = db.session.get(User, id)
    return user


@lm.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))


@app.route('/User/Check', methods=['GET', 'POST'])
def check():
    logout_form = LogoutForm()
    portal_form = PortalForm()
    if logout_form.submit.data and logout_form.validate():
        logout_user()
        print("logout")
        return redirect(url_for("index"))
    if portal_form.validate_on_submit():
        if request.form.get("tenant"):  # If they pressed the tenant button and they are a tenant
            if db.session.query(Tenant).filter_by(user_id=current_user.get_id()).first():
                return redirect(url_for("tenant"))
            else:
                print("Not a tenant")
        if request.form.get("landlord"):
            if db.session.query(Landlord).filter_by(user_id=current_user.get_id()).first():
                return redirect(url_for("landlord"))
            else:
                print("Not a landlord")
        if request.form.get("upload"):
            return redirect(url_for("upload_lease"))
    return render_template("check.html", logout_form=logout_form, portal_form=portal_form)


@app.route('/User/Login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print("Log in form validated")
        user = db.session.query(User).filter(User.username == login_form.username.data).first()
        print(f'login:{user}')
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
                flash("Incorrect Password")
                print("Failed Login")
                return redirect()
            return redirect(url_for("check"))
        else:
            print("not a user")
            flash("Incorrect Username")
    return render_template('login.html', form=login_form)


def checkUniqueness(column, form):
    """Extracted from validateAddUser.
    Queries User model for matching data using a form and a column to see if there is a match
    For example, when a form comes in it could check the email address data in the form using the column email."""
    query = db.session.query(User).filter(getattr(User, column) == form.__getattribute__(column).data).first()
    print(f'query: {query}')
    if query is None:
        return True
    # checkUnique returns true if unique; if there is no match
    else:
        return False


def validateAddUser(form):
    """extracted from add_user
    checks the form to see if each validated.
    Form validators can check for some things but others must be checked in more complex ways.
    Returns a list of failed checks"""
    # Password match check
    failures = []
    pass1 = form.password.data
    pass2 = form.confirm_password.data
    if pass1 != pass2:
        failures.append("Passwords don't match")
    columns = ("username", "email")
    for column in columns:
        if not checkUniqueness(column, form):
            failures.append(f'{column} is not unique ')
    return failures


@app.route('/User/Add', methods=['GET', 'POST'])
def add_user():
    form = RegisterForm()
    """
    Form validate on submit:
        checks the validators attached to the form
    validateAddUser:
        checks the data against conditions that aren't on the form, such as uniqueness, or if the 
        passwords match
    """
    if form.validate_on_submit():  # valid form inputs
        validatedform = validateAddUser(form)
        if not validatedform:  # Including ones that have to be checked
            # server side such as uniqueness
            toAddUser = User(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data)
            # Dont need to define date_added, its default is current time, leave it to use that
            with open('textoutput.txt', 'a') as f:
                f.write(str(toAddUser))

            db.session.add(toAddUser)

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
            login_user(toAddUser)
            # Add user to appropriate subclass of user
            if form.landlord.data:
                landlordToAdd = Landlord(user_id=toAddUser.id)
                db.session.add(landlordToAdd)
            if form.tenant.data:
                tenantToAdd = Tenant(user_id=toAddUser.id)
                db.session.add(tenantToAdd)
            db.session.commit()

            del toAddUser
            return redirect("/User/Check", code=301)
        else:
            form = RegisterForm()
            response = render_template("add_user.html", form=form, errors=validatedform)
            response.headers["Cache-Control"] = "no-cache,no-store,must-revalidate"
            return response



    elif form.is_submitted():
        with open('textoutput.txt', 'a') as f:
            f.write(f'form errors:'
                    f'{str(form.errors)}' + "\n")
            return render_template("add_user.html", form=form, errors=form.errors)
    return render_template("add_user.html", form=form, errors=None)


# @app.route('/User/Settings', methods=['GET', 'POST'])
# def settings():
#     form = SettingsForm()
#     if form.validate_on_submit():
#         pass
#     return render_template('settings.html', form=form)
#     pass
@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    print("evaluating forms")
    if register_form.submit.data:
        if register_form.validate():
            validatedform = validateAddUser(register_form)
            if not validatedform:  # Including ones that have to be checked
                # server side such as uniqueness
                toAddUser = User(
                    username=register_form.username.data,
                    password=register_form.password.data,
                    email=register_form.email.data,
                )
                # Dont need to define date_added, its default is current time, leave it to use that
                with open('textoutput.txt', 'a') as f:
                    f.write(str(toAddUser))

                db.session.add(toAddUser)

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
                login_user(toAddUser)
                # Add user to appropriate subclass of user
                if register_form.landlord.data:
                    landlordToAdd = Landlord(user_id=toAddUser.id)
                    db.session.add(landlordToAdd)
                if register_form.tenant.data:
                    tenantToAdd = Tenant(user_id=toAddUser.id)
                    db.session.add(tenantToAdd)
                db.session.commit()

                del toAddUser
                return redirect(url_for("LandlordTenantChoice"))
            # else:
            #     form = RegisterForm()
            #     response = render_template("add_user.html", form=form, errors=validatedform)
            #     response.headers["Cache-Control"] = "no-cache,no-store,must-revalidate"
            #     return response
        else:
            print("not valid")
    if login_form.submit.data and login_form.validate():
        print("Log in form validated")
        user = db.session.query(User).filter(User.username == login_form.username.data).first()
        print(f'login:{user}')
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
                flash("Incorrect Password")
                print("Failed Login")
                return redirect(url_for("index"))
            return redirect(url_for("LandlordTenantChoice"))
        else:
            print("not a user")
            flash("Incorrect Username")
    else:
        print("not login")
    return render_template('loginregister.html', methods=['GET'], login_form=login_form, register_form=register_form)


@app.route("/Tenant", methods=['GET', 'POST'])
@login_required
def tenant():
    return render_template('Tenant.html')


@app.route("/Landlord")
@login_required
def landlord_homepage():
    return render_template("landlord/homepage.html")


@app.route("/FAQ")
def faq():
    return render_template("landlord/FAQs.html")


@app.route("/Contact")
def contact():
    return render_template("landlord/contact.html")


@app.route('/Upload', methods=['GET', 'POST'])
@login_required
def upload_lease():
    display = DisplayForm()
    upform = LeaseUploadForm()
    # Gets all lease IDs for the current user
    lease_names = landlord_lease_list()

    if upform.submit.data and upform.validate():
        print("Upload Block")
        try:
            leasename = leases.save(request.files['lease'])
        except UploadNotAllowed:
            return render_template("landlord/lease.html", lease_names=lease_names, upform=upform,
                                   types=leases.extensions,
                                   errors=f"Wrong file format. Currently only supporting .txt and .pdf")
        # ext = os.path.splitext(leasename)[1]
        landlord = (db.session.query(Landlord).filter_by(user_id=current_user.get_id()).first())
        try:
            newlease = Lease(leasename, landlord=landlord)
            db.session.add(newlease)
            db.session.commit()
            lease_names = landlord_lease_list()
            return render_template("landlord/lease.html", lease_names=lease_names, upform=upform, errors=None,
                                   types=leases.extensions, display=display)
        except Exception as e:
            try:
                print(f"New lease couldnt be created\n\n\n")
                print(f"exception: {e}")
                print(leasename, current_user)
                print(current_user.username)
                print(current_user.id)
                print(current_user.get_id())
                print("search")
                print(db.session.query(Landlord).filter_by(user_id=current_user.get_id()).first())
            except Exception as e:
                print(e)
    return render_template("landlord/lease.html", lease_names=lease_names, upform=upform, errors=None,
                           types=leases.extensions, display=display)


def landlord_lease_list():
    x = db.session.query(Lease_Landlord.c.lease_id).where(Lease_Landlord.c.landlord_id == current_user.get_id()).all()
    y = [row[0] for row in x]
    for i in y:
        print(i)
        print(type(i))
    lease_names = Lease.query.filter(Lease.lease_id.in_(y)).with_entities(Lease.file_name).all()
    lease_names = [item[0] for item in lease_names]
    print(f"x{x},y{y},\nz{lease_names}")
    return lease_names


@app.route("/LandlordTenant")
@login_required
def LandlordTenantChoice():
    return render_template("LandlordTenantChoice.html")


@app.route('/download_lease/<leasename>')
def download_lease(leasename):
    print(f"Attempting to download {leasename}")
    try:
        return send_from_directory(app.config['UPLOADED_LEASES_DEST'], leasename, as_attachment=True)
    except:
        return redirect(url_for("index"))

@app.route("/Settings")
@login_required
def settings():
    return render_template("landlord/settings.html")


if __name__ == '__main__':
    app.run()
