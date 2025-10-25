#!/usr/bin/env python3
"""
Aplicação Flask simples - Olá Mundo
"""

from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Endpoint principal que retorna Olá Mundo"""
    return jsonify({
        'message': 'Olá Mundo! 🌍',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'hostname': os.getenv('HOSTNAME', 'localhost')
    })

@app.route('/health')
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

@app.route('/ready')
def readiness_check():
    """Endpoint de readiness check"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port)