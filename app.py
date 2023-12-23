from flask import Flask, request, render_template, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
app = Flask(__name__)
app.config['SECRET_KEY']='candy_apple'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#--------------------------------------------------------
boggle_game = Boggle()
new_board = boggle_game.make_board()

@app.route('/')
def show_board():
    '''Show Boggle Board'''

    return render_template("index.html", boggle_board = new_board)

@app.route('/guess', methods=['POST'])
def check_guess():
    '''Check user's guess'''
    user_guess = request.form.get('guess')
    result = boggle_game.check_valid_word(new_board, user_guess)
    if result == "not-on-board":
        msg = "Sorry. This word is not on the board."
    elif result == 'not-word':
        msg = "Sorry. That is not a word."
    else:
        msg = "You found a word! Nice!"
    flash(msg)
    return redirect("/")