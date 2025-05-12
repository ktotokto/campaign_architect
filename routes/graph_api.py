from datetime import datetime

from flask import render_template, jsonify, request
from flask_login import current_user, login_required

from data.graph_edge import GraphEdge
from utils import get_campaign_by_title


def setup_graph_routes(app):
    @app.route('/campaigns/<title>/campaign_graph')
    @login_required
    def campaign_graph(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            return render_template('campaign/campaign_graph.html', title=title, events=campaign.events)
        finally:
            session.close()

    @app.route('/api/campaigns/<title>/graph', methods=['GET'])
    @login_required
    def get_campaign_graph(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                return jsonify({"success": False, "message": "Кампания не найдена"}), 404

            nodes = [{"id": event.id, "label": event.name} for event in campaign.events]

            edges = [{
                "id": edge.id,
                "from": edge.from_event_id,
                "to": edge.to_event_id,
                "label": edge.label or "",
            } for edge in campaign.graph_edges]

            return jsonify({"nodes": nodes, "edges": edges})
        finally:
            session.close()

    @app.route('/api/campaigns/<title>/add_connection', methods=['POST'])
    @login_required
    def add_connection(title):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            if not campaign:
                return jsonify({"success": False, "message": "Кампания не найдена"}), 404

            if not request.is_json:
                return jsonify({"success": False, "message": "Ожидается JSON"}), 400

            data = request.get_json()
            new_edge = GraphEdge(
                campaign_id = campaign.id,
                from_event_id=data['from'],
                to_event_id=data['to'],
                label=data.get('label', '')
            )
            session.add(new_edge)
            campaign.updated_date = datetime.now()
            session.commit()
            return jsonify({
                "success": True,
                "edge": {
                    "id": new_edge.id,
                    "from": new_edge.from_event_id,
                    "to": new_edge.to_event_id,
                    "label": new_edge.label
                }
            })
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            session.close()

    @app.route('/api/campaigns/<title>/delete_connection/<int:edge_id>', methods=['DELETE'])
    @login_required
    def delete_connection(title, edge_id):
        campaign, session = get_campaign_by_title(title, current_user.id)
        try:
            edge = session.query(GraphEdge).filter(
                GraphEdge.id == edge_id,
                GraphEdge.from_event.has(campaign_id=campaign.id)
            ).first()

            if not edge:
                return jsonify({"success": False, "message": "Связь не найдена"})

            session.delete(edge)
            session.commit()
            return jsonify({"success": True, "message": "Связь удалена"})
        except Exception as e:
            session.rollback()
            return jsonify({"success": False, "message": str(e)}), 500
        finally:
            session.close()

