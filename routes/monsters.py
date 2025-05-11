import os
from datetime import datetime

from flask import request
from flask import redirect, url_for, flash, render_template, jsonify, current_app
from flask_login import current_user, login_required

from data.monster import Monster
from decorators import sanitize_title
from forms.new_monster import MonsterForm
from utils import get_campaign_by_title, save_image


def setup_monster_routes(app):
    @app.route('/campaigns/<title>/add_monster', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_monster(title):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена")
            return redirect(url_for('campaigns'))

        form = MonsterForm(campaign_id=campaign.id)

        if form.validate_on_submit():
            new_monster = Monster(
                name=form.name.data,
                monster_type=form.monster_type.data,
                cr=form.cr.data,
                description=form.description.data,
                campaign_id=campaign.id
            )

            session.add(new_monster)
            session.commit()
            image = request.files.get("image")
            image_path = save_image(
                image,
                campaign.id,
                current_user.id,
                new_monster.id, 'monsters'
            )
            new_monster.image = image_path
            campaign.updated_date = datetime.now()

            session.commit()
            return redirect(url_for('campaign_monsters', title=title))

        return render_template('campaign/add_monster.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/add_monster/<int:monster_id>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def monster_editor(title, monster_id):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена")
            return redirect(url_for('campaigns'))

        monster = session.query(Monster).filter(
            Monster.id == monster_id,
            Monster.campaign_id == campaign.id
        ).first()

        if not monster:
            flash("Монстр не найден", "error")
            return redirect(url_for("campaign_monsters", title=title))

        form = MonsterForm(obj=monster, campaign_id=campaign.id)

        if form.validate_on_submit():
            try:
                image = request.files.get("image")
                if image and image.filename:
                    monster.image = save_image(
                        image,
                        campaign.id,
                        current_user.id,
                        monster.id, 'monsters'
                    )

                form.populate_obj(monster)
                session.commit()
                return redirect(url_for('campaign_monsters', title=title))
            except Exception as e:
                session.rollback()
                flash("Ошибка при сохранении изменений", "error")
                app.logger.error(f"Ошибка редактирования предмета: {e}")

        if not form.is_submitted():
            form.name.data = monster.name
            form.cr.data = monster.cr
            form.monster_type.data = monster.monster_type
            form.description.data = monster.description

        return render_template('campaign/add_monster.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/delete_monster/<int:monster_id>', methods=['POST'])
    @login_required
    def delete_monster(title, monster_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            monster = session.query(Monster).filter(
                Monster.id == monster_id,
                Monster.campaign_id == campaign.id
            ).first()

            if not monster:
                return jsonify({"success": False, "message": "Монстр не найден"}), 404

            session.delete(monster)
            if monster.image:
                image_path = os.path.join(current_app.root_path, 'static', monster.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()
