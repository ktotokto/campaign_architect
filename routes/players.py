from flask import render_template, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user

from datetime import datetime
from const import SKILL_CHOICES
from data.campaign import Campaign
from forms.new_player import PlayerForm
from data.player import Player
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from decorators import sanitize_title
from utils import get_campaign_by_title


def setup_player_routes(app):
    @app.route('/campaigns/<title>/add_player', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_player(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        form = PlayerForm(campaign_id=campaign.id)

        if not campaign:
            flash("Кампания не найдена", "error")
            return redirect(url_for("campaigns"))

        try:
            if form.validate_on_submit():
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
                    campaign_id=campaign.id
                )

                campaign.updated_date = datetime.now()
                session.add(new_char)
                session.commit()

                return redirect(url_for('current_campaigns', title=title))

            if not form.is_submitted():
                form.strength.data = 10
                form.dexterity.data = 10
                form.constitution.data = 10
                form.intelligence.data = 10
                form.wisdom.data = 10
                form.charisma.data = 10
                form.skills.data = []

            return render_template('campaign/add_player.html', form=form, SKILL_CHOICES=SKILL_CHOICES, campaign=campaign)

        except IntegrityError:
            session.rollback()
            flash("Персонаж с таким именем уже существует", "error")

        except SQLAlchemyError as e:
            session.rollback()
            app.logger.error(f"Ошибка базы данных при добавлении персонажа: {e}")
            flash("Произошла ошибка при сохранении персонажа", "error")

        return render_template('campaign/add_player.html', form=form, SKILL_CHOICES=SKILL_CHOICES, campaign=campaign)

    @app.route('/campaigns/<title>/add_player/<name_player>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def player_editor(title, name_player):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена", "error")
            return redirect(url_for("campaigns"))

        try:
            player = session.query(Player).filter(
                Player.name == name_player,
                Player.campaign_id == campaign.id
            ).first()
            form = PlayerForm(campaign_id=campaign.id, obj=player)

            if not player:
                flash("Персонаж не найден", "error")
                return redirect(url_for("current_campaigns", title=title))

            if form.validate_on_submit():
                form.populate_obj(player)
                player.skills = ",".join(form.skills.data) if form.skills.data else ""
                session.commit()
                return redirect(url_for('current_campaigns', title=title))

            if not form.is_submitted():
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
                form.skills.data = [skill.strip() for skill in player.skills.split(',')] if player.skills else []

            return render_template('campaign/add_player.html', form=form, SKILL_CHOICES=SKILL_CHOICES, campaign=campaign)

        except SQLAlchemyError as e:
            session.rollback()
            app.logger.error(f"Ошибка базы данных при редактировании: {e}")
            flash("Ошибка при сохранении изменений", "error")
            return redirect(url_for("current_campaigns", title=title))
        except Exception as e:
            session.rollback()
            app.logger.error(f"Неожиданная ошибка: {e}")
            flash("Произошла критическая ошибка", "error")
            return redirect(url_for("current_campaigns", title=title))
        finally:
            session.close()

    @app.route('/campaigns/<title>/delete_player/<player_id>', methods=['POST'])
    @login_required
    def delete_player(title, player_id):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            return jsonify({"success": False, "message": "Кампания не найдена"}), 403

        player = session.query(Player).filter(
            Player.id == player_id,
            Campaign.id == campaign.id,
            Campaign.user_id == current_user.id
        ).first()

        if not player:
            return jsonify({"success": False, "message": "Персонаж не найден"}), 404

        try:
            session.delete(player)
            session.commit()
            return jsonify({"success": True})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()