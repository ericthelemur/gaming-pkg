import os
import subprocess
import json
from types import SimpleNamespace


def get_games():
    all_games = get_all()
    installed = get_installed()
    installed_keys = set(g.pkgname for g in installed)
    highlight_keys = set(os.environ["HIGHLIGHT_GAMES"].split(";"))
    for game in all_games:
        game.installed = game.pkgname in installed_keys
        game.highlight = game.pkgname in highlight_keys
    return all_games

def get_all():
    proc = subprocess.run([os.environ["DCSPKG_PATH"], "list", "--json"], stdout=subprocess.PIPE)
    output = proc.stdout.decode("utf-8")
    out_json = json.loads(output, object_hook=lambda d: SimpleNamespace(**d))
    return out_json


def get_installed():
    proc = subprocess.run([os.environ["DCSPKG_PATH"], "installed", "--json"], stdout=subprocess.PIPE)
    output = proc.stdout.decode("utf-8")
    out_json = json.loads(output, object_hook=lambda d: SimpleNamespace(**d))
    return out_json


def install_game(game):
    proc = subprocess.run([os.environ["DCSPKG_PATH"], "install", game], stdout=subprocess.PIPE)


def play_game(game):
    proc = subprocess.run([os.environ["DCSPKG_PATH"], "run", game], stdout=subprocess.PIPE)
