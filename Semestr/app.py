from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User
from data.games import Game
from data.moves import Move
from forms.user import LoginForm, RegisterForm
from ConnectXAPI import api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('api.play'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        db_session.global_init("db/connectx.db")
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter_by(username=request.form["username"]).first()

        if user and user.check_password(request.form["password"]):
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        db_session.global_init("db/connectx.db")
        db_sess = db_session.create_session()

        new_user = User(username=request.form['username'], hashed_password=request.form['password'])
        new_user.set_password(request.form['password'])

        db_sess.add(new_user)
        db_sess.commit()

        db_sess.close()
        flash('Аккаунт успешно создан!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run()
