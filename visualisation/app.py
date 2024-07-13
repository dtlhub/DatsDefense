from pathlib import Path

from flask import Flask, jsonify, render_template

from gameserver.storage import RoundStorage


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
        return jsonify({})

    @app.get("/api/<game>")
    def get_game(game):
        storage = get_game_storage(game)
        return jsonify(storage.get_stored())

    @app.get("/api/<game>/round/<round>")
    def get_round(game, round):
        return jsonify(get_game_storage(game).get_stored()[int(round)])

    @app.get("/game/<game>")
    def view_game(game):
        return render_template("game.html")

    return app
