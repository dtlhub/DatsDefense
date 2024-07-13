import json
from pathlib import Path
from base64 import b64encode

from flask import Flask, jsonify, render_template

from gameserver.storage import RoundStorage
from visualizer import get_png_bytes


def create_app() -> Flask:
    app = Flask(__name__)

    storage_base = Path.cwd() / "storage"

    def get_game_storage(game: str):
        return RoundStorage(storage_base / game)

    @app.get("/api/games")
    def get_games():
        games = []
        for f in storage_base.iterdir():
            if f.name.startswith("game"):
                games.append(f.name)
        return jsonify(games)

    @app.get("/api/<game>")
    def get_game(game):
        storage = get_game_storage(game)
        return jsonify({"rounds": len(storage.get_stored())})

    @app.get("/api/<game>/round/<round>")
    def get_round(game, round):
        return jsonify({
            "data": b64encode(get_png_bytes(game, round)).decode()
        })

    @app.get("/game/<game>")
    def view_game(game):
        return render_template("game.html")

    return app
