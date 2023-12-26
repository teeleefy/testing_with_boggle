from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
app = Flask(__name__)
app.config['SECRET_KEY']='candy_apple'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#--------------------------------------------------------
boggle_game = Boggle()

@app.route('/')
def show_board():
    '''Show Boggle Board'''
    new_board = boggle_game.make_board()
    session['board'] = new_board
    highscore = session.get('highscore', 0)
    times_played = session.get('times_played', 0)
    return render_template("index.html", boggle_board = new_board, highscore= highscore, times_played = times_played)

# @app.route('/guess', methods=['POST'])
# def check_guess():
#     '''Check user's guess'''
#     user_guess = request.form.get('guess')
#     new_board = session.get('board')
#     result = boggle_game.check_valid_word(new_board, user_guess)
#     if result == "not-on-board":
#         msg = "Sorry. This word is not on the board."
#     elif result == 'not-word':
#         msg = "Sorry. That is not a word."
#     else:
#         msg = "You found a word! Nice!"
    
#     flash(msg)

#     return redirect("/")

@app.route('/check-word')
def check_word():
    """References the Boggle class method "check_valid_word" in boggle.py to check to see if a word is valid and can score points"""
    word = request.args['new_word']
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route('/post-score', methods=["POST"])
def post_new_score():
    """Receives score after timer is up and game over. Updates the times user has played. Updates high score if new high score achieved."""
    score = request.json['score']
    highscore = session.get("highscore", 0)
    times_played = session.get("times_played", 0)

    session['times_played'] = times_played + 1
    session['highscore'] = max(score, highscore)

    #brokeRecord will return a true or false value.  It will be referenced in app.js in the method scoreGame. If it is true, it will congrat the user on breaking the old record. 
    return jsonify(brokeRecord = score > highscore)