from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_login = request.form.get('email_login')
        senha_login = request.form.get('senha_login')

        user = User.query.filter_by(email=email_login).first()
        if user:
            if check_password_hash(user.password, senha_login):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente', category='error')
        else:
            flash('Email não existe.', category='error')

    return render_template("login.html", user=current_user, page='login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email_cad = request.form.get('email_cad')
        nome_cad = request.form.get('nome_cad')
        senha_cad = request.form.get('senha_cad')
        confirma_senha_cad = request.form.get('confirma_senha_cad')

        user = User.query.filter_by(email=email_cad).first()
        if user:
            flash('Email já cadastrado.', category='error')
        elif len(email_cad) < 4:
            flash('Email deve ter mais de 3 caracteres.', category='error')
        elif len(nome_cad) < 2:
            flash('O nome deve ter pelo menos 2 caracteres.', category='error')
        elif senha_cad != confirma_senha_cad:
            flash('As senhas não coincidem.', category='error')
        elif len(senha_cad) < 7:
            flash('A senha deve ter pelo menos 7 caracteres.', category='error')
        else:
            new_user = User(email=email_cad, first_name=nome_cad, password=generate_password_hash(senha_cad, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada com sucesso!', category='success')
            return redirect(url_for('auth.account_created'))

    return render_template("sign_up.html", user=current_user, page='sign-up')

@auth.route('/account-created')
@login_required
def account_created():
    flash('Conta criada com sucesso!', category='success')
    return redirect(url_for('views.home'))

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Simular o envio do email com instruções para redefinir a senha
            flash('Se um usuário com esse email existe, instruções para redefinir a senha foram enviadas.', 'success')
        else:
            flash('Email não encontrado.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html')
