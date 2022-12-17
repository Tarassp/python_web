from . import app
from src.service_layer import address_book_service, user_service
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from flask import render_template, request, redirect, url_for, session, flash, make_response
from src.libs.validation_schemas import RegistrationSchema, LoginSchema
from marshmallow import ValidationError


@app.before_request
def check_loggin():
    auth = 'username' in session
    if not auth:
        token_user = request.cookies.get('username')
        if token_user:
            user_service.loggin_user_if_can(token_user, SqlAlchemyUnitOfWork())


@app.route('/healthcheck', strict_slashes=False)
def healthcheck():
    return "I am working"


@app.route('/', strict_slashes=False)
def index():
    auth = "username" in session
    return render_template('pages/index.html', auth=auth)


@app.route('/registration', methods=['GET', 'POST'], strict_slashes=False)
def registration():
    if request.method == 'POST':
        try:
            RegistrationSchema().load(request.form)
        except ValidationError as err:
            return render_template('pages/registration.html', messages=err.messages)
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_service.create(username, email, password, SqlAlchemyUnitOfWork())
        return redirect(url_for('login'))

    return render_template('pages/registration.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == "POST":
        try:
            LoginSchema().load(request.form)
        except ValidationError as err:
            return render_template('pages/login.html', messages=err.messages)
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        is_logged_in = user_service.login(
            email, password, SqlAlchemyUnitOfWork())
        if not is_logged_in:
            return render_template('pages/login.html', messages={'err': 'Invalid credentials!'})
        response = make_response(redirect(url_for('index')))
        if remember:
            token, expired_date = user_service.remember_current_user(
                SqlAlchemyUnitOfWork())
            response.set_cookie('username', token, expires=expired_date)
        return response

    return render_template('pages/login.html')


@app.route('/logout', strict_slashes=False)
def logout():
    auth = 'username' in session
    if not auth:
        return redirect(request.url)
    session.pop('username')
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', '', expires=-1)
    return response


@app.route('/contacts', strict_slashes=False)
def contacts():
    auth = 'username' in session
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    contacts = address_book_service.get_all_contacts(
        user_id, SqlAlchemyUnitOfWork())
    return render_template('pages/contacts.html', contacts=contacts, auth=auth)


@app.route('/contacts/add', methods=['GET', 'POST'], strict_slashes=False)
def add_contact():
    auth = 'username' in session
    if not auth:
        return redirect(request.url)
    if request.method == "POST":
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        address = request.form.get('address')
        user_id = session['username']['id']
        address_book_service.add_contact(
            user_id, name, phone_number, email, address, None, SqlAlchemyUnitOfWork())
        return redirect(url_for('contacts'))
    return render_template('pages/add_contact.html', auth=auth)


@app.route('/contacts/edit/<int:id>', methods=['POST', 'GET'], strict_slashes=False)
def edit_contact(id):
    auth = 'username' in session
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    if request.method == "POST":
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        address = request.form.get('address')

        address_book_service.update_contact(
            user_id, id, name, phone_number, email, address, SqlAlchemyUnitOfWork())
        flash('The contact is updated successfully!')
        return redirect(url_for('contacts'))
    contact = address_book_service.get_contact(
        user_id, id, SqlAlchemyUnitOfWork())
    return render_template('pages/edit_contact.html', contact=contact, auth=auth)


@app.route('/contacts/delete/<int:id>', methods=['POST'], strict_slashes=True)
def delete_contact(id):
    auth = 'username' in session
    if not auth:
        return redirect(request.url)
    user_id = session['username']['id']
    address_book_service.delete_contact(user_id, id, SqlAlchemyUnitOfWork())
    flash('Deleted Successfully!')
    return redirect(url_for('contacts'))
