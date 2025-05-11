from flask import render_template, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user

from datetime import datetime
from data.spell import Spell
from decorators import sanitize_title
from forms.new_spell import SpellForm
from utils import get_campaign_by_title


def setup_spell_routes(app):
    @app.route('/campaigns/<title>/add_spell', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_spell(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        form = SpellForm(campaign_id=campaign.id)

        if not campaign:
            flash("Кампания не найдена")
            return redirect(url_for('campaigns'))
        if form.validate_on_submit():
            new_spell = Spell(
                name=form.name.data,
                level=form.level.data,
                components=form.components.data,
                school=form.school.data,
                range=form.range.data,
                duration=form.duration.data,
                casting_time=form.casting_time.data,
                description=form.description.data,
                campaign_id=campaign.id
            )
            campaign.updated_date = datetime.now()
            session.add(new_spell)
            session.commit()
            return redirect(url_for('campaign_spells', title=title))

        return render_template('campaign/add_spell.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/add_spell/<int:spell_id>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def edit_spell(title, spell_id):
        campaign, session = get_campaign_by_title(title, current_user.id)

        spell = session.query(Spell).filter(
            Spell.id == spell_id,
            Spell.campaign_id == campaign.id
        ).first()
        form = SpellForm(campaign_id=campaign.id, obj=spell)

        if form.validate_on_submit():
            spell.name = form.name.data
            spell.level = form.level.data
            spell.components = form.components.data
            spell.school = form.school.data
            spell.range = form.range.data
            spell.duration = form.duration.data
            spell.casting_time = form.casting_time.data
            spell.description = form.description.data

            campaign.updated_date = datetime.now()
            session.commit()
            return redirect(url_for('campaign_spells', title=title))

        if not form.is_submitted():
            form.name.data = spell.name
            form.level.data = spell.level
            form.components.data = spell.components
            form.school.data = spell.school
            form.range.data = spell.range
            form.duration.data = spell.duration
            form.casting_time.data = spell.casting_time
            form.description.data = spell.description

        return render_template('campaign/add_spell.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/delete_spell/<int:spell_id>', methods=['POST'])
    @login_required
    def delete_spell(title, spell_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            spell = session.query(Spell).filter(
                Spell.id == spell_id,
                Spell.campaign_id == campaign.id
            ).first()

            if not spell:
                return jsonify({"success": False, "message": "Заклинание не найдено"}), 404

            session.delete(spell)
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()
