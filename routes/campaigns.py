import os

from flask import render_template, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from shutil import rmtree

from data.campaign import Campaign
from data.db_session import create_session
from forms.new_campaign_form import CampaignForm
from decorators import sanitize_title
from utils import get_campaign_by_title


def setup_campaign_routes(app):
    @app.route('/campaigns')
    @login_required
    def campaigns():
        session = create_session()
        try:
            campaigns_list = session.query(Campaign).filter(
                Campaign.user_id == current_user.id
            ).all()
            return render_template('campaigns.html', campaigns=campaigns_list)
        except Exception as e:
            app.logger.error(f"Ошибка при загрузке кампаний: {e}")
            flash("Не удалось загрузить список кампаний", "error")
            return redirect(url_for("campaigns"))
        finally:
            session.close()

    @app.route('/new-campaign', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def new_campaign():
        form = CampaignForm()
        if form.validate_on_submit():
            session = create_session()
            try:
                existing = session.query(Campaign).filter(
                    Campaign.title == form.title.data,
                    Campaign.user_id == current_user.id
                ).first()

                if existing:
                    flash("Кампания с таким названием уже существует", "error")
                    return render_template('new_campaign.html', form=form)

                campaign = Campaign(
                    title=form.title.data,
                    description=form.description.data,
                    user_id=current_user.id,
                    system=form.system.data
                )
                session.add(campaign)
                session.commit()

                campaign_image_folder = os.path.join(current_app.root_path, 'static', 'images', 'campaigns',
                                                     f'user_{current_user.id}', f'campaign_{campaign.id}')

                image_folder = [campaign_image_folder,
                                os.path.join(campaign_image_folder, 'npcs'),
                                os.path.join(campaign_image_folder, 'items'),
                                os.path.join(campaign_image_folder, 'players'),
                                os.path.join(campaign_image_folder, 'locations'),
                                os.path.join(campaign_image_folder, 'monsters'),
                                os.path.join(campaign_image_folder, 'spells')]

                for url in image_folder:
                    os.makedirs(url)

                flash("Кампания успешно создана!", "success")
                return redirect(url_for('current_campaigns', title=campaign.title))

            except IntegrityError:
                session.rollback()
                flash("Ошибка: такая кампания уже существует", "error")
            except SQLAlchemyError as e:
                session.rollback()
                app.logger.error(f"Ошибка базы данных при создании кампании: {e}")
                flash("Не удалось создать кампанию", "error")
            except Exception as e:
                session.rollback()
                app.logger.error(f"Неожиданная ошибка при создании кампании: {e}")
                flash("Произошла критическая ошибка", "error")
            finally:
                session.close()

        return render_template('new_campaign.html', form=form)

    @app.route('/campaigns/<title>/campaign_notes')
    @login_required
    @sanitize_title
    def current_campaigns(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена", "error")
                return redirect(url_for("campaigns"))

            return render_template('campaign/campaign_events.html',
                                   campaign=campaign,
                                   username=current_user.username)
        finally:
            session.close()

    @app.route('/campaigns/<title>/campaign_npcs')
    @login_required
    def campaign_npcs(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена", "error")
                return redirect(url_for("campaigns"))

            return render_template('campaign/campaign_npcs.html',
                                   campaign=campaign,
                                   username=current_user.username)
        finally:
            session.close()

    @app.route('/campaigns/<title>/campaign_spells')
    @login_required
    def campaign_spells(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена")
                return redirect(url_for('campaigns'))

            return render_template('campaign/campaign_spells.html', campaign=campaign)
        finally:
            session.close()

    @app.route('/campaigns/<title>/campaign_items')
    @login_required
    def campaign_items(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена")
                return redirect(url_for('campaigns'))

            return render_template('campaign/campaign_items.html', campaign=campaign)
        finally:
            session.close()

    @app.route('/campaigns/<title>/campaign_monsters')
    @login_required
    def campaign_monsters(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена")
                return redirect(url_for('campaigns'))

            return render_template('campaign/campaign_monsters.html', campaign=campaign)
        finally:
            session.close()

    @app.route('/campaigns/<title>/campaign_locations')
    @login_required
    def campaign_locations(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена")
                return redirect(url_for('campaigns'))

            return render_template('campaign/campaign_locations.html', campaign=campaign)
        finally:
            session.close()

    @app.route('/campaigns/<title>/campaign_events')
    @login_required
    def campaign_events(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                flash("Кампания не найдена")
                return redirect(url_for('campaigns'))

            return render_template('campaign/campaign_events.html', campaign=campaign)
        finally:
            session.close()

    @app.route('/campaigns/<title>/delete_campaign', methods=['POST'])
    @login_required
    def delete_campaign(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                return jsonify({"success": False, "message": "Кампания не найдена"}), 404

            path = os.path.join(current_app.root_path, 'static', 'images', 'campaigns', f'user_{current_user.id}',
                                f'campaign_{campaign.id}')
            if os.path.exists(path):
                rmtree(path)
            session.delete(campaign)
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()

    @app.route('/profile')
    @login_required
    def profile():
        session = create_session()
        try:
            campaigns_list = session.query(Campaign).filter(
                Campaign.user_id == current_user.id
            ).all()

            return render_template('profile.html', user=current_user, campaigns=campaigns_list)
        finally:
            session.close()
