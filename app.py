import json
import os
from copy import deepcopy
from re import match
from typing import List, Optional, Tuple, Dict

import sgf
from flask import Flask, render_template, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.beans.board.board import Board
from src.beans.board.color import Color
from src.beans.board.stone import Stone, Pos
from src.preprocessing.adapter.tree_adapter import has_invalid_size, get_init_stones, get_first_stone
from src.preprocessing.corrections.sgf_corrections import apply_corrections
from src.preprocessing.errors.preprocessing_exception import PreprocessingException

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
app.config["UPLOAD_FOLDER"] = "app/tmp"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if len(request.form) != 0:
        return render_template("index.html", placed_stones=request.form["placed_stones"],
                               first_color=request.form["first_color"])

    if "sgf-file" not in request.files:
        return render_template("index.html", error="Please upload a file")

    file: FileStorage = request.files["sgf-file"]
    if not __valid_file(file.filename):
        return render_template("index.html", error="Please upload a valid sgf file")

    filename: str = secure_filename(file.filename)
    path: str = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    placed_stones: Dict[int, str]
    first_color: Optional[str]
    error: str
    placed_stones, first_color, error = __get_placed_stones_from_sgf(path)
    os.remove(path)

    if error is not None:
        return render_template("index.html", error=error)

    return render_template("index.html", placed_stones=placed_stones, first_color=first_color)


@app.route("/solve", methods=["GET", "POST"])
def solve():
    if request.method != "POST":
        return

    stones_str: Dict[str, str] = json.loads(request.form["placed_stones"])
    first_color: str = request.form["first_color"]
    return render_template("solve.html",
                           initial_stones=request.form["placed_stones"],
                           first_color=first_color,
                           forbidden_moves=__get_forbidden_moves(stones_str, first_color))


@app.route("/move", methods=["POST"])
def move():
    if request.method != "POST":
        return

    parent_stones_str: Dict[str, str] = json.loads(request.form["placed_stones"])
    new_stone_str: Dict[str, str] = json.loads(request.form["new_stone"])

    placed_stones: List[Stone] = __dict_str_to_stones(parent_stones_str)
    new_stone: Stone = __dict_str_to_stones(new_stone_str)[0]
    next_color = new_stone.color.get_other()

    parent_board = Board(placed_stones)
    board: Board = deepcopy(parent_board)
    board.place_stone(new_stone)
    new_placed_stones: List[Stone] = [Stone(pos, color) for pos, color in board.placed_stones.items()]

    forbidden_moves: List[Pos] = board.get_forbidden_moves(next_color, parent_board)

    return json.dumps({
        "placed_stones": json.dumps(__stones_to_dict(new_placed_stones)),
        "forbidden_moves": json.dumps([row * 19 + col for row, col in forbidden_moves])
    })

@app.route("/about")
def about():
    return render_template("about.html")

def __valid_file(filename: str) -> bool:
    return match("^.+\.sgf$", filename.lower()) is not None


def __get_placed_stones_from_sgf(path: str) -> Tuple[Dict[int, str], Optional[str], Optional[str]]:
    try:
        with open(path, encoding="GB2312", errors="ignore") as file:
            sgf_str: str = apply_corrections(file.read(), check_only_initial_board=True)

        problem: sgf.GameTree = sgf.parse(sgf_str).children[0]

    except PreprocessingException:
        return {}, "", "The sgf contained no initial stones"
    except (UnicodeDecodeError, sgf.ParseException):
        return {}, "", "There was an error parsing the sgf"

    if has_invalid_size(problem):
        return {}, "", "Invalid size: only 19x19 allowed"

    init_stones: List[Stone] = get_init_stones(problem)

    try:
        first_stone: Stone = get_first_stone(problem)
        first_stone_color: str = first_stone.color.name.lower()
        return __stones_to_dict(init_stones), first_stone_color, None

    except Exception:
        return __stones_to_dict(init_stones), None, None


def __stones_to_dict(stones: List[Stone]) -> Dict[int, str]:
    stone_dict: Dict[int, str] = {}
    for stone in stones:
        pos_index: int = stone.pos[0] * 19 + stone.pos[1]
        stone_dict[pos_index] = stone.color.name.lower()
    return stone_dict


def __dict_to_stones(stone_dict: Dict[int, str]) -> List[Stone]:
    stones: List[Stone] = []
    for index, color in stone_dict.items():
        pos: Pos = (int(index / 19), index % 19)
        color = Color.BLACK if color == "black" else Color.WHITE
        stones.append(Stone(pos, color))
    return stones


def __dict_str_to_stones(stone_dict_str: Dict[str, str]) -> List[Stone]:
    stone_dict = dict([(int(index), color) for index, color in stone_dict_str.items()])
    return __dict_to_stones(stone_dict)


def __get_forbidden_moves(stone_dict_str: Dict[str, str], next_color: str) \
        -> List[int]:
    stones: List[Stone] = __dict_str_to_stones(stone_dict_str)
    color: Color = Color.BLACK if next_color == "black" else Color.WHITE

    forbidden_moves: List[Pos] = Board(stones).get_forbidden_moves(color)
    return [row * 19 + col for row, col in forbidden_moves]
