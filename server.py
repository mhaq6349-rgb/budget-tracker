from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone
import os

app = Flask(__name__, static_folder='.')
DATA_DIR = Path(__file__).parent / 'data'
TXN_FILE = DATA_DIR / 'transactions.json'
BUDGET_FILE = DATA_DIR / 'budgets.json'

def load_txns():
    if TXN_FILE.exists():
        with open(TXN_FILE, encoding='utf-8') as f:
            return json.load(f)
    return []

def save_txns(txns):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(TXN_FILE, 'w', encoding='utf-8') as f:
        json.dump(txns, f, indent=2)

def load_budgets():
    if BUDGET_FILE.exists():
        with open(BUDGET_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_budgets(budgets):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(BUDGET_FILE, 'w', encoding='utf-8') as f:
        json.dump(budgets, f, indent=2)

@app.route('/api/transactions', methods=['GET'])
def get_txns():
    return jsonify(load_txns())

@app.route('/api/transactions', methods=['POST'])
def create_txn():
    data = request.get_json()
    if not data or not data.get('desc', '').strip():
        return jsonify({'error': 'Description required'}), 400
    amount = data.get('amount')
    if amount is None or not isinstance(amount, (int, float)):
        return jsonify({'error': 'Valid amount required'}), 400
    txns = load_txns()
    txn = {
        'id': uuid.uuid4().hex,
        'desc': data['desc'].strip(),
        'amount': float(amount),
        'type': data.get('type', 'expense'),
        'category': data.get('category', 'Other'),
        'createdAt': datetime.now(timezone.utc).isoformat(),
    }
    txns.append(txn)
    save_txns(txns)
    return jsonify(txn), 201

@app.route('/api/transactions/<txn_id>', methods=['DELETE'])
def delete_txn(txn_id):
    txns = load_txns()
    txns = [t for t in txns if t['id'] != txn_id]
    save_txns(txns)
    return '', 204

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    return jsonify(load_budgets())

@app.route('/api/budgets', methods=['PUT'])
def update_budgets():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Budget object required'}), 400
    save_budgets(data)
    return jsonify(data)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
