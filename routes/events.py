from datetime import datetime

from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from data.event import Event
from decorators import sanitize_title
from forms.new_event import EventForm
from utils import get_campaign_by_title


def setup_event_routes(app):
    @app.route('/campaigns/<title>/add_event', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_event(title):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена")
            return redirect(url_for('campaigns'))

        form = EventForm(campaign_id=campaign.id)

        if form.validate_on_submit():
            new_event = Event(
                name=form.name.data,
                description=form.description.data,
                campaign_id=campaign.id
            )

            campaign.updated_date = datetime.now()
            session.add(new_event)
            session.commit()
            return redirect(url_for('campaign_events', title=title))

        return render_template('campaign/add_event.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/add_event/<event_name>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def event_editor(title, event_name):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена", "error")
            return redirect(url_for("campaigns"))

        event = session.query(Event).filter(
            Event.name == event_name,
            Event.campaign_id == campaign.id
        ).first()

        if not event:
            flash("Событие не найдено", "error")
            return redirect(url_for("campaign_events", title=title))

        form = EventForm(obj=event, campaign_id=campaign.id)

        if form.validate_on_submit():
            try:
                form.populate_obj(event)
                campaign.updated_date = datetime.now()
                session.commit()
                return redirect(url_for('campaign_events', title=title))
            except Exception as e:
                session.rollback()
                flash("Ошибка при сохранении изменений", "error")
                app.logger.error(f"Ошибка редактирования предмета: {e}")

        if not form.is_submitted():
            form.name.data = event.name
            form.description.data = event.description

        return render_template('campaign/add_event.html', form=form, campaign=campaign)
    @app.route('/campaigns/<title>/delete_event/<int:event_id>', methods=['POST'])
    @login_required
    def delete_event(title, event_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:

            event = session.query(Event).filter(
                Event.id == event_id,
                Event.campaign_id == campaign.id
            ).first()

            if not event:
                return jsonify({"success": False, "message": "Событие не найдено"}), 404

            for con in event.connections:
                session.delete(con)
            session.delete(event)
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()