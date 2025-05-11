import os
from datetime import datetime

from flask import request
from flask import redirect, url_for, flash, render_template, jsonify, current_app
from flask_login import current_user, login_required

from data.location import Location
from decorators import sanitize_title
from forms.new_location import LocationForm
from utils import get_campaign_by_title, save_image


def setup_location_routes(app):
    @app.route('/campaigns/<title>/add_location', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_location(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        form = LocationForm(campaign_id=campaign.id)

        if not campaign:
            flash("Кампания не найдена")
            return redirect(url_for('campaigns'))

        if form.validate_on_submit():
            new_loc = Location(
                name=form.name.data,
                type=form.type.data,
                description=form.description.data,
                campaign_id=campaign.id
            )

            session.add(new_loc)
            session.commit()

            image = request.files.get("image")
            image_path = save_image(
                image,
                campaign.id,
                current_user.id,
                new_loc.id, 'locations'
            )
            new_loc.image = image_path
            campaign.updated_date = datetime.now()

            session.commit()
            return redirect(url_for('campaign_locations', title=title))

        return render_template('campaign/add_location.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/add_location/<int:location_id>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def location_editor(title, location_id):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена", "error")
            return redirect(url_for("campaigns"))

        location = session.query(Location).filter(
            Location.id == location_id,
            Location.campaign_id == campaign.id
        ).first()

        if not location:
            flash("Локация не найдена", "error")
            return redirect(url_for("campaign_locations", title=title))

        form = LocationForm(obj=location, campaign_id=campaign.id)

        if form.validate_on_submit():
            try:
                image = request.files.get("image")
                if image and image.filename:
                    location.image = save_image(
                        image,
                        campaign.id,
                        current_user.id,
                        location.id, 'locations'
                    )

                form.populate_obj(location)
                session.commit()
                return redirect(url_for('campaign_locations', title=title))
            except Exception as e:
                session.rollback()
                flash("Ошибка при сохранении изменений", "error")
                app.logger.error(f"Ошибка редактирования предмета: {e}")

        if not form.is_submitted():
            form.name.data = location.name
            form.type.data = location.type
            form.description.data = location.description

        return render_template('campaign/add_location.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/delete_location/<int:location_id>', methods=['POST'])
    @login_required
    def delete_location(title, location_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            location = session.query(Location).filter(
                Location.id == location_id,
                Location.campaign_id == campaign.id
            ).first()

            if not location:
                return jsonify({"success": False, "message": "Локация не найдена"}), 404

            session.delete(location)
            if location.image:
                image_path = os.path.join(current_app.root_path, 'static', location.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()
