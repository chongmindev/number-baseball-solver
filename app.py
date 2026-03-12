import random
import uuid
from flask import Flask, render_template, request, jsonify, session
from main import ALL_CODES, guess_turn, best_guess, entropy_of_guess

app = Flask(__name__)
app.secret_key = "number-baseball-secret-key"

games = {}

@app.route("/")
def index():
    game_id = str(uuid.uuid4())
    session["game_id"] = game_id
    games[game_id] = {
        "possible_ans": ALL_CODES[:],
        "first_guess_done": False
    }
    return render_template("index.html")

@app.route("/next_guess", methods=["GET"])
def next_guess():
    game_id = session.get("game_id")
    if not game_id or game_id not in games:
        return jsonify({"error": "Game not found. Refresh the page."})

    game = games[game_id]
    possible_ans = game["possible_ans"]

    if len(possible_ans) == 0:
        return jsonify({"error": "No possibilities remain."})

    if not game["first_guess_done"]:
        guess = random.choice(ALL_CODES)
        entropy = entropy_of_guess(guess, possible_ans)

        game["first_guess_done"] = True
        return jsonify({
            "guess": guess,
            "remaining": len(possible_ans),
            "entropy": entropy
        })

    guess, entropy = best_guess(possible_ans, possible_ans)

    return jsonify({
        "guess": guess,
        "remaining": len(possible_ans),
        "entropy": entropy
    })

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    game_id = session.get("game_id")
    if not game_id or game_id not in games:
        return jsonify({"error": "Game not found. Refresh the page."})

    data = request.json
    guess = data["guess"]
    strikes = int(data["strikes"])
    balls = int(data["balls"])

    game = games[game_id]
    possible_ans = game["possible_ans"]
    possible_ans = guess_turn(guess, possible_ans, strikes, balls)
    game["possible_ans"] = possible_ans

    if strikes == 4:
        return jsonify({
            "solved": True,
            "remaining": len(possible_ans)
        })

    if len(possible_ans) == 0:
        return jsonify({
            "error": "No possibilities remain. Your feedback may be inconsistent."
        })

    return jsonify({
        "solved": False,
        "remaining": len(possible_ans)
    })

@app.route("/reset", methods=["POST"])
def reset():
    game_id = session.get("game_id")
    if not game_id:
        return jsonify({"ok": False})

    games[game_id] = {
        "possible_ans": ALL_CODES[:],
        "first_guess_done": False
    }
    return jsonify({"ok": True})


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))