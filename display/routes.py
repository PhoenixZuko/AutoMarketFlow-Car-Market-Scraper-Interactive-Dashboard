from flask import render_template, jsonify
import json
import os

def setup_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/cars')
    def api_cars():
        json_path = os.path.join("data", "cars_tabulator.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
