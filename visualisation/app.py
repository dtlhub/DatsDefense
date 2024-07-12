from pathlib import Path

from flask import Flask, jsonify

from gameserver.storage import RoundStorage


def create_app(storage: RoundStorage) -> Flask:
    app = Flask(__name__)
    storage_base = Path.cwd() / "storage"

    @app.get("/api/games")
    def get_games():
        games = []
        for f in storage_base.iterdir():
            if f.name.startswith("game"):
                games.append(f.name)
        return jsonify({})

    @app.get("/api/<game>")
    def get_game(game):
        storage = RoundStorage(storage_base / game)
        return jsonify(storage.get_stored())

    @app.get("/api/current_game")
    def get_current(game):
        return jsonify(storage.get_stored())

    @app.get("/api/current_game/round/<index>")
    def get_round(index):
        return jsonify(storage.get_stored()[int(index)])

    return app
