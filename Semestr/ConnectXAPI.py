from flask import Flask, jsonify, request, render_template, Blueprint
from ConnectX import ConnectX, agent_random, agent_leftmost
from data import db_session
import json

api = Blueprint('api', __name__)

game_instance = ConnectX(row_size=6, column_size=7, connect_number=4)


@api.route('/start_game', methods=['POST'])
def start_game():
    game_instance.reset()
    return jsonify({"message": "Game started"}), 200


@api.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    column = data.get('column')
    result = game_instance.step(int(column))
    return jsonify(result), 200

@api.route('/get_board', methods=['GET'])
def get_board():
    return jsonify(game_instance.board), 200

@api.route('/play', methods=['GET'])
def play():
    return render_template('play.html', game_instance=game_instance)

@api.route('/history', methods=['GET'])
def history():
    # Assuming you have a function to fetch game history from your database
    # For demonstration, returning a static JSON object
    return jsonify([{"game_id": 1, "moves": ["A1", "B2", "C3"]}], 200)

