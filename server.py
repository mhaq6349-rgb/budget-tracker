from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone
import os

app = Flask(__name__, static_folder='.')
DATA_FILE = Path(__file__).parent / 'data' / 'transactions.json'

def load():
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding='utf-8') as f:
            return json.load(f)
    return []

def save(txns):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(txns, f, indent=2)

@app.route('/api/transactions', methods=['GET'])
def get_txns():
    return jsonify(load())

@app.route('/api/transactions', methods=['POST'])
def create_txn():
    data = request.get_json()
    if not data or not data.get('desc', '').strip():
        return jsonify({'error': 'Description required'}), 400
    amount = data.get('amount')
    if amount is None or not isinstance(amount, (int, float)):
        return jsonify({'error': 'Valid amount required'}), 400
    txns = load()
    txn = {
        'id': uuid.uuid4().hex,
        'desc': data['desc'].strip(),
        'amount': float(amount),
        'type': data.get('type', 'expense'),
        'category': data.get('category', 'Other'),
        'createdAt': datetime.now(timezone.utc).isoformat(),
    }
    txns.append(txn)
    save(txns)
    return jsonify(txn), 201

@app.route('/api/transactions/<txn_id>', methods=['DELETE'])
def delete_txn(txn_id):
    txns = load()
    txns = [t for t in txns if t['id'] != txn_id]
    save(txns)
    return '', 204

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
