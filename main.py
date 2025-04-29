import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from data.campaign import Campaign
from data.db_session import global_init, create_session
from data.user import User
from forms.login_form import LoginForm
from forms.new_campaign_form import CampaignForm
from forms.registration_form import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

global_init("db/campaign.db")


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html',
                           user=current_user,
                           is_authenticated=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session = create_session()
        session.add(user)
        session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        session.commit()
        flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('login.html', form=form)


@app.route('/campaigns')
def campaigns():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session = create_session()
    campaigns_list = session.query(Campaign).filter(Campaign.user_id == current_user.id).all()
    session.commit()
    return render_template('campaigns.html', campaigns=campaigns_list)


@app.route('/campaigns/<title>')
def current_campaigns(title):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session = create_session()
    campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
    session.commit()
    return render_template('campaign.html', campaign=campaign, username=current_user.username)

@app.route('/campaigns/<title>/add_player')
def add_player(title):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session = create_session()
    campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
    session.commit()
    return render_template('add_player.html', campaign=campaign)


@app.route('/new-campaign', methods=['GET', 'POST'])
def new_campaign():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CampaignForm()
    if form.validate_on_submit():
        session = create_session()
        campaign = Campaign(title=form.title.data, description=form.description.data,
                            user_id=current_user.id, system=form.system.data)
        session.add(campaign)
        session.commit()
        return redirect(url_for('index'))

    return render_template('new_campaign.html', form=form)


@app.route('/logaut')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
