import os

from werkzeug.utils import secure_filename

from data.campaign import Campaign


def get_campaign_by_title(title, user_id):
    from data.db_session import create_session
    session = create_session()
    campaign = session.query(Campaign).filter(
        Campaign.title == title,
        Campaign.user_id == user_id
    ).first()

    if not campaign:
        return None, None

    return campaign, session


def save_image(image, campaign_id, user_id, essence_id, directory):
    if image and image.filename:
        campaign_folder = os.path.join('static', 'images', 'campaigns', f'user_{user_id}', f'campaign_{campaign_id}', directory)

        ext = os.path.splitext(secure_filename(image.filename))[1]
        filename = f"{essence_id}{ext}"
        path = os.path.join(campaign_folder, filename)

        try:
            image.save(path)
            return f'images/campaigns/user_{user_id}/campaign_{campaign_id}/{directory}/{filename}'
        except Exception as e:
            raise IOError(f"Ошибка сохранения изображения: {e}")
    return None


def check_and_create_directories():
    db_dir = "db"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    campaigns_dir = os.path.join("static", "images", "campaigns")
    if not os.path.exists(campaigns_dir):
        os.makedirs(campaigns_dir)

