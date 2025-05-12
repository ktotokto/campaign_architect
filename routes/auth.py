import os

from flask import render_template, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from data.db_session import create_session
from data.user import User
from decorators import sanitize_title
from forms.login_form import LoginForm
from forms.registration_form import RegistrationForm


def setup_auth_routes(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        session = create_session()
        try:
            return session.query(User).get(int(user_id))
        except Exception as e:
            app.logger.error(f"Ошибка загрузки пользователя: {e}")
            return None
        finally:
            session.close()

    @app.route('/register', methods=['GET', 'POST'])
    @sanitize_title
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            session = create_session()
            try:
                existing_user = session.query(User).filter(
                    (User.username == form.username.data) | (User.email == form.email.data)
                ).first()

                if existing_user:
                    flash("Пользователь с таким именем или email уже существует", "error")
                    return render_template('register.html', form=form)

                user = User(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)

                session.add(user)
                session.commit()

                user_campaign_image_folder = os.path.join(current_app.root_path, 'static', 'images', 'campaigns',
                                                     f'user_{user.id}')
                os.mkdir(user_campaign_image_folder)

                flash("Регистрация успешна! Добро пожаловать!", "success")
                login_user(user)
                return redirect(url_for('index'))

            except Exception as e:
                session.rollback()
                app.logger.error(f"Ошибка при регистрации: {e}")
                flash("Произошла ошибка при регистрации", "error")
                return render_template('register.html', form=form)
            finally:
                session.close()

        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    @sanitize_title
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            session = create_session()
            try:
                user = session.query(User).filter_by(username=form.username.data).first()

                if user and user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for('campaigns'))

                flash('Неверное имя пользователя или пароль', 'error')
                return redirect(url_for('login'))
            except Exception as e:
                app.logger.error(f"Ошибка при входе: {e}")
                flash("Не удалось войти. Попробуйте снова.", "error")
                return redirect(url_for('login'))
            finally:
                session.close()

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("Вы вышли из аккаунта", "success")
        return redirect(url_for('login'))
