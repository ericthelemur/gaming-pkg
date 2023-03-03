import glob
import logging
import os
import re
from datetime import datetime
from typing import Union

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response

import subprocess
import json
from gaming import dcspkg
from dataclasses import dataclass

FlaskResponse = Union[Response, str]

bp = Blueprint("gaming", __name__)

@dataclass
class Link:
    name: str
    url: str
    icon: str


links = [
    Link("Steam", "/steam", "bi-steam"),
    Link("Lutris", "/lutris", "bi-controller"),
    Link("Firefox", "/firefox", "bi-browser-firefox"),
]

@bp.route("/")
def main() -> FlaskResponse:
    games = dcspkg.get_games()
    installed_games = [g for g in games if g.installed]
    highlight_games = [g for g in games if g.highlight]
    return render_template("main.html", links=links, highlights=highlight_games, installed=installed_games, games=games)


@bp.route("/install/<string:game>", methods=["GET"])
def install(game: str) -> FlaskResponse:
    dcspkg.install_game(game)
    return redirect(url_for("gaming.main"))

@bp.route("/run/<string:game>", methods=["GET"])
def run(game: str) -> FlaskResponse:
    dcspkg.play_game(game)
    return redirect(url_for("gaming.main"))


@bp.route("/steam", methods=["GET"])
def steam() -> FlaskResponse:
    os.system(os.environ["STEAM_PATH"])
    return redirect(url_for("gaming.main"))


@bp.route("/lutris", methods=["GET"])
def lutris() -> FlaskResponse:
    os.system(os.environ["LUTRIS_PATH"])
    return redirect(url_for("gaming.main"))


@bp.route("/firefox", methods=["GET"])
def firefox() -> FlaskResponse:
    os.system(os.environ["FIREFOX_PATH"])
    return redirect(url_for("gaming.main"))



