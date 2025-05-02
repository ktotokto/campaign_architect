import secrets
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data.campaign import Campaign
from data.db_session import global_init, create_session
from data.player import Player
from data.user import User
from forms.login_form import LoginForm
from forms.new_campaign_form import CampaignForm
from forms.registration_form import RegistrationForm
from forms.new_player import CharacterForm
from const import SKILL_CHOICES

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

@app.route('/campaigns/<title>/campaign_notes')
def current_campaigns(title):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session = create_session()
    campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
    session.commit()
    return render_template('campaign/campaign_notes.html', campaign=campaign, username=current_user.username)

@app.route('/campaigns/<title>/campaign_npcs')
def campaign_npcs(title):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session = create_session()
    campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
    session.commit()
    return render_template('campaign/campaign_npcs.html', campaign=campaign, username=current_user.username)

@app.route('/campaigns/<title>/add_npc', methods=['GET', 'POST'])
def add_player(title):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CharacterForm()


@app.route('/campaigns/<title>/add_player', methods=['GET', 'POST'])
def add_player(title):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CharacterForm()

    if form.validate_on_submit():
        session = create_session()
        campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
        new_char = Player(
            name=form.name.data,
            race=form.race.data,
            char_class=form.char_class.data,
            level=form.level.data,
            background=form.background.data,
            strength=form.strength.data,
            dexterity=form.dexterity.data,
            constitution=form.constitution.data,
            intelligence=form.intelligence.data,
            wisdom=form.wisdom.data,
            charisma=form.charisma.data,
            skills=",".join(form.skills.data) if form.skills.data else "",
            campaign_id=campaign.id,
            campaign=campaign
        )
        session.add(new_char)
        campaign.updated_date = datetime.now()
        session.commit()
        return redirect(url_for('current_campaigns', title=title))

    if not form.is_submitted():
        form.strength.data = 10
        form.dexterity.data = 10
        form.constitution.data = 10
        form.intelligence.data = 10
        form.wisdom.data = 10
        form.charisma.data = 10
        form.skills = []
    return render_template('campaign/add_player.html', form=form, SKILL_CHOICES=SKILL_CHOICES)


@app.route('/campaigns/<title>/add_player/<name_player>', methods=['GET', 'POST'])
def player_editor(title, name_player):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CharacterForm()
    session = create_session()
    campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
    player = session.query(Player).filter(Player.name == name_player, Player.campaign == campaign).first()

    if form.validate_on_submit():
        form.populate_obj(player)
        player.skills = ",".join(form.skills.data) if form.skills.data else ""
        session.commit()
        return redirect(url_for('current_campaigns', title=title))

    form.name.data = player.name
    form.race.data = player.race
    form.char_class.data = player.char_class
    form.level.data = player.level
    form.background.data = player.background
    form.strength.data = player.strength
    form.dexterity.data = player.dexterity
    form.constitution.data = player.constitution
    form.intelligence.data = player.intelligence
    form.wisdom.data = player.wisdom
    form.charisma.data = player.charisma

    if player.skills:
        form.skills.data = [skill.strip() for skill in player.skills.split(',')]
    else:
        form.skills.data = []
    return render_template('campaign/add_player.html', form=form, SKILL_CHOICES=SKILL_CHOICES)


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
        return redirect(url_for('campaigns'))

    return render_template('new_campaign.html', form=form)


@app.route('/campaigns/<title>/delete_player/<name_player>', methods=['POST'])
def delete_player(title, name_player):
    session = create_session()
    campaign = session.query(Campaign).filter(Campaign.title == title, Campaign.user_id == current_user.id).first()
    player = session.query(Player).filter(Player.name == name_player, Player.campaign_id == campaign.id).first()
    session.delete(player)
    session.commit()
    return jsonify({"success": True})


@app.route('/logaut')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
