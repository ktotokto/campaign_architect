import secrets

from flask import Flask
from flask_login import LoginManager

from data.db_session import global_init

from routes.home import setup_home_routes
from routes.auth import setup_auth_routes
from routes.campaigns import setup_campaign_routes
from routes.items import setup_item_routes
from routes.locations import setup_location_routes
from routes.players import setup_player_routes
from routes.npcs import setup_npc_routes
from routes.spells import setup_spell_routes
from routes.monsters import setup_monster_routes
from routes.graph_api import setup_graph_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

global_init("db/campaign.db")

setup_home_routes(app)
setup_auth_routes(app)
setup_campaign_routes(app)
setup_player_routes(app)
setup_npc_routes(app)
setup_spell_routes(app)
setup_item_routes(app)
setup_location_routes(app)
setup_monster_routes(app)
setup_graph_routes(app)

if __name__ == '__main__':
    app.run()
