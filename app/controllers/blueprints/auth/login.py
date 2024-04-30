from flask import (
    render_template, url_for, redirect, flash, session, current_app)
from flask_login import (login_user, logout_user)
from app.models import Users
from app.models.forms import (LoginForm, RegisterForm, OTPForm)
from app.services import (validate_sensitive_infos, generate_otp_code,
    send_new_acc_email, send_otp_email, convert_str_to_date)
from app.controllers.blueprints.auth import auth_bp
from app.models.database.queries import (insert_user, get_user)
from datetime import datetime


@auth_bp.route('/login/', methods=['post', 'get'])
def login_():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        ignore, user = get_user('email', email, True)
        if user is None:
            flash('E-mail não cadastrado!')
            return redirect(url_for('auth.login_'))
        
        if not user.check_password(password=password):
            flash('Senha incorreta!')
            return redirect(url_for('auth.login_'))
        
        login_user(user)

        return redirect(url_for('home.index'))

    return render_template('pages/auth/login.html',
        form=form)


@auth_bp.route('/register/', methods=['post', 'get'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.date_of_birth.data)
        payload = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data, 'password': form.password.data,
            'date_of_birth': form.date_of_birth.data}

        check_email = validate_sensitive_infos({'email': payload.get('email')}, Users)
        if not check_email.get('success'):
            flash('E-mail já cadastrado!')
            return redirect(url_for('auth.login_'))

        session['user_registration'] = payload

        return redirect(url_for('auth.get_otp'))
    return render_template('pages/auth/register.html',
        form=form)

@auth_bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('auth.login_'))

@auth_bp.route('/auth/get-otp/')
def get_otp():
    otp = generate_otp_code()
    session['otp'] = otp
    user = session.get('user_registration')

    send_otp_email(otp, user.get('email'), user.get('first_name'))
    return redirect(url_for('auth.otp'))


@auth_bp.route('/auth/confirm-otp/', methods=['get', 'post'])
def otp():
    form = OTPForm()
    otp = session.get('otp')
    user = session.get('user_registration')
    current_app.logger.debug(user)
    if form.validate_on_submit():
        form_otp = f'{form.otp1.data}{form.otp2.data}{form.otp3.data}{form.otp4.data}{form.otp5.data}{form.otp6.data}'
        if not form_otp == otp:
            flash('Código Incorreto')
            return redirect(url_for('auth.otp'))

        session['user_registration'] = user
        return redirect(url_for('auth.register_user'))
    return render_template('pages/auth/otp.html', form=form, user_email=user.get('email'))


@auth_bp.route('/auth/register-user/')
def register_user():
    user = session.get('user_registration')
    user['date_of_birth'] = datetime.strptime(user.get('date_of_birth'), '%a, %d %b %Y %H:%M:%S %Z')
    user['date_of_birth'] = user.get('date_of_birth').strftime('%Y-%m-%d')
    user['date_of_birth'] = convert_str_to_date(user.get('date_of_birth'))

    current_app.logger.debug(user)
    insertion = insert_user(user)
    current_app.logger.debug(insertion)
    flash('Usuário registrado')
    send_new_acc_email(user.get('email'), user.get('first_name'))
    return redirect(url_for('auth.login_'))
