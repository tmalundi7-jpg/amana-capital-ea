from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/clients', methods=['GET'])
def get_clients():
    # Mock data
    return jsonify({'status': 'success', 'data': []})

@api.route('/portfolio/<client_id>', methods=['GET'])
def get_portfolio(client_id):
    return jsonify({'status': 'success', 'total_value': 124500.00})
