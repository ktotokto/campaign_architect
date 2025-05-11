import os
from datetime import datetime

from flask import request
from flask import redirect, url_for, flash, render_template, jsonify, current_app
from flask_login import current_user, login_required

from data.item import Item
from decorators import sanitize_title
from forms.new_item import ItemForm
from utils import get_campaign_by_title, save_image


def setup_item_routes(app):
    @app.route('/campaigns/<title>/add_item', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def add_item(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        form = ItemForm(campaign_id=campaign.id)

        if not campaign:
            flash("Кампания не найдена")
            return redirect(url_for('campaigns'))

        if form.validate_on_submit():
            new_item = Item(
                name=form.name.data,
                item_type=form.item_type.data,
                rarity=form.rarity.data,
                description=form.description.data,
                weight=form.weight.data,
                value=form.value.data,
                campaign_id=campaign.id
            )

            session.add(new_item)
            session.commit()
            image = request.files.get("image")
            image_path = save_image(
                image,
                campaign.id,
                current_user.id,
                new_item.id, 'items'
            )
            new_item.image = image_path
            campaign.updated_date = datetime.now()

            session.commit()

            return redirect(url_for('campaign_items', title=title))

        return render_template('campaign/add_item.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/add_item/<name_item>', methods=['GET', 'POST'])
    @login_required
    @sanitize_title
    def item_editor(title, name_item):
        campaign, session = get_campaign_by_title(title, current_user.id)

        if not campaign:
            flash("Кампания не найдена", "error")
            return redirect(url_for("campaigns"))

        item = session.query(Item).filter(
            Item.name == name_item,
            Item.campaign_id == campaign.id
        ).first()
        form = ItemForm(obj=item, campaign_id=campaign.id)

        if not item:
            flash("Предмет не найден", "error")
            return redirect(url_for("campaign_items", title=title))

        if form.validate_on_submit():
            try:
                image = request.files.get("image")
                if image and image.filename:
                    item.image = save_image(
                        image,
                        campaign.id,
                        current_user.id,
                        item.id, 'items'
                    )

                form.populate_obj(item)
                session.commit()
                return redirect(url_for('campaign_items', title=title))

            except Exception as e:
                session.rollback()
                flash("Ошибка при сохранении изменений", "error")
                app.logger.error(f"Ошибка редактирования предмета: {e}")

        if not form.is_submitted():
            form.name.data = item.name
            form.item_type.data = item.item_type
            form.rarity.data = item.rarity
            form.description.data = item.description
            form.weight.data = item.weight
            form.value.data = item.value

        return render_template('campaign/add_item.html', form=form, campaign=campaign)

    @app.route('/campaigns/<title>/delete_item/<int:item_id>', methods=['POST'])
    @login_required
    def delete_item(title, item_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            item = session.query(Item).filter(
                Item.id == item_id,
                Item.campaign_id == campaign.id
            ).first()

            if not item:
                return jsonify({"success": False, "message": "Предмет не найден"}), 404

            session.delete(item)
            if item.image:
                image_path = os.path.join(current_app.root_path, 'static', item.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()
