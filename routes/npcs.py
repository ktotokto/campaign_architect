import os

from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from data.npc import NPC
from forms.new_npc import NpcForm
from decorators import sanitize_title
from utils import save_image, get_campaign_by_title


def npc_form(npc, form):
    npc.name = form.name.data
    npc.race = form.race.data
    npc.char_class = form.char_class.data
    npc.level = form.level.data
    npc.background = form.background.data
    npc.strength = form.strength.data
    npc.dexterity = form.dexterity.data
    npc.constitution = form.constitution.data
    npc.intelligence = form.intelligence.data
    npc.wisdom = form.wisdom.data
    npc.charisma = form.charisma.data
    npc.location = request.form.get("location") or None


def setup_npc_routes(app):
    @app.route('/campaigns/<title>/add_npc', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_npc(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        form = NpcForm(campaign_id=campaign.id)
        locations = [loc.name for loc in campaign.locations]

        if not campaign:
            flash('Кампания не найдена', 'error')
            return redirect(url_for('campaigns'))

        if form.validate_on_submit():
            try:
                new_npc = NPC(
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
                    location=request.form.get("location") or None,
                    campaign_id=campaign.id
                )

                campaign.updated_date = datetime.now()

                session.add(new_npc)
                session.commit()

                image_path = save_image(
                    request.files.get("image"),
                    campaign.id,
                    current_user.id,
                    new_npc.id, 'npcs'
                )
                new_npc.image = image_path

                session.commit()

                return redirect(url_for('campaign_npcs', title=title))

            except IntegrityError:
                session.rollback()
                flash('Ошибка сохранения: нарушение целостности данных', 'error')

            except IOError as e:
                session.rollback()
                flash(str(e), 'error')

            except Exception as e:
                session.rollback()
                flash('Произошла ошибка при сохранении', 'error')
                app.logger.error(f"Ошибка добавления NPC: {e}")

            finally:
                session.close()

        if not form.is_submitted():
            form.strength.data = 10
            form.dexterity.data = 10
            form.constitution.data = 10
            form.intelligence.data = 10
            form.wisdom.data = 10
            form.charisma.data = 10

        return render_template('campaign/add_npc.html', form=form, locations=locations, campaign=campaign)

    @app.route('/campaigns/<title>/add_npc/<name_npc>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def npc_editor(title, name_npc):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена", "error")
            return redirect(url_for("campaigns"))

        npc = session.query(NPC).filter(
            NPC.name == name_npc,
            NPC.campaign_id == campaign.id
        ).first()
        form = NpcForm(obj=npc, campaign_id=campaign.id)
        locations = [loc.name for loc in campaign.locations]

        if not npc:
            flash("Персонаж не найден", "error")
            return redirect(url_for("campaign_npcs", title=title))

        if form.validate_on_submit():
            try:
                image = request.files.get("image")
                if image and image.filename:
                    npc.image = save_image(
                        image,
                        campaign.id,
                        current_user.id,
                        npc.id, 'npcs'
                    )

                form.populate_obj(npc)
                session.commit()
                return redirect(url_for('campaign_npcs', title=title))

            except Exception as e:
                session.rollback()
                flash("Ошибка при сохранении изменений", "error")
                app.logger.error(f"Ошибка редактирования NPC: {e}")

        if not form.is_submitted():
            form.name.data = npc.name
            form.race.data = npc.race
            form.char_class.data = npc.char_class
            form.level.data = npc.level
            form.background.data = npc.background
            form.strength.data = npc.strength
            form.dexterity.data = npc.dexterity
            form.constitution.data = npc.constitution
            form.intelligence.data = npc.intelligence
            form.wisdom.data = npc.wisdom
            form.charisma.data = npc.charisma

        return render_template('campaign/add_npc.html', form=form, locations=locations, campaign=campaign)

    @app.route('/campaigns/<title>/delete_npc/<int:npc_id>', methods=['POST'])
    @login_required
    def delete_npc(title, npc_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            npc = session.query(NPC).get(npc_id)

            if not npc:
                return jsonify({"success": False, "message": "NPC не найден"}), 404

            session.delete(npc)
            if npc.image:
                image_path = os.path.join(current_app.root_path, 'static', npc.image)
                if os.path.exists(image_path):
                    os.remove(image_path)

            session.commit()
            return jsonify({"success": True})

        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500

        finally:
            session.close()
