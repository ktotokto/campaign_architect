from datetime import datetime
from urllib import request

from flask import redirect, url_for, render_template, jsonify
from flask_login import current_user, login_required

from data.campaign import Campaign
from data.db_session import create_session
from data.graph_edge import GraphEdge


def setup_graph_routes(app):
    @app.route('/campaigns/<title>/graph')
    @login_required
    def campaign_graph(title):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

        session = create_session()
        try:
            campaign = session.query(Campaign).filter(
                Campaign.title == title,
                Campaign.user_id == current_user.id
            ).first()

            events = campaign.events
            npcs = campaign.npcs
            items = campaign.items
            players = campaign.players

            return render_template('campaign/campaign_graph.html', campaign=campaign,
                                   events=events, npcs=npcs, items=items, players=players)
        finally:
            session.close()

    @app.route('/api/campaigns/<title>/graph', methods=['GET'])
    @login_required
    def get_campaign_graph(title):
        session = create_session()
        try:
            campaign = session.query(Campaign).filter(
                Campaign.title == title,
                Campaign.user_id == current_user.id
            ).first()

            nodes = []
            edges = []

            for event in campaign.events:
                nodes.append({
                    "id": f"event_{event.id}",
                    "label": event.title,
                    "group": "event",
                    "title": event.description or "",
                    "shape": "box"
                })

            for npc in campaign.npcs:
                nodes.append({
                    "id": f"npc_{npc.id}",
                    "label": npc.name,
                    "group": "npc",
                    "shape": "circle"
                })
                edges.append({
                    "from": f"event_{event.id}",
                    "to": f"npc_{npc.id}",
                    "label": "Участвует"
                })

            for item in campaign.items:
                nodes.append({
                    "id": f"item_{item.id}",
                    "label": item.name,
                    "group": "item",
                    "shape": "dot"
                })
                edges.append({
                    "from": f"event_{event.id}",
                    "to": f"item_{item.id}",
                    "label": "Использовано"
                })

            return jsonify({
                "nodes": nodes,
                "edges": edges
            })
        finally:
            session.close()

    @app.route('/api/campaigns/<title>/graph', methods=['POST'])
    @login_required
    def save_campaign_graph(title):
        data = request.get_json()
        campaign = create_session().query(Campaign).filter(
            Campaign.title == title,
            Campaign.user_id == current_user.id
        ).first()

        if not campaign:
            return jsonify({"success": False, "message": "Кампания не найдена"}), 404

        session = create_session()
        try:
            session.query(GraphEdge).filter(GraphEdge.campaign_id == campaign.id).delete()

            for edge in data["edges"]:
                new_edge = GraphEdge(
                    from_id=edge["from"],
                    to_id=edge["to"],
                    label=edge.get("label", "Связано"),
                    campaign_id=campaign.id
                )
                session.add(new_edge)

            campaign.updated_date = datetime.now()
            session.commit()
            return jsonify({"success": True})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()

