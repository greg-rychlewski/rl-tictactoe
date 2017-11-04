###############################################################################
#                                                                             #
#                                 Dependencies                                #
#                                                                             #
############################################################################### 

# Environment variables
import env

# Tic tac toe functions
import tictactoe

# Web framework
from flask import Flask, render_template, request, session
application = Flask(__name__)
application.secret_key = env.key

# JSON converter
import json

# File/directory operations
import os

# Global game variables
import gamevars

###############################################################################
#                                                                             #
#                                    Routing                                  #
#                                                                             #
############################################################################### 

# Main page
@application.route("/")
def index():
	return render_template("index.html")

# Initialize Game
@application.route("/initialize-game", methods=["POST"])
def initialize():
	# Save player symbols into session cookie
	compSymbol = request.form["comp-symbol"]
	session["computer"] = compSymbol
	session["human"] = gamevars.players[gamevars.players != compSymbol]
	session["previousBoard"] = {"x": None, "o": None}

	# Set global variables
	gamevars.setPlayerSymbols(session)
	gamevars.setPreviousBoard(session)

	return json.dumps({})

# Get computer's move
@application.route("/next-move", methods=["POST"])
def next():
	# Parse data
	currentBoard = request.form["board"]
	compSymbol = request.form["comp-symbol"]
	simulation = request.form["simulation"]
	erase = request.form["erase"]

	# Erase previous board history if new simulation game
	if erase == "true":
		session["previousBoard"] = {"x": None, "o": None}
		gamevars.setPreviousBoard(session)

	# Get new board after computer's move
	gamevars.setPreviousBoard(session)
	newBoard = tictactoe.computerTurn(currentBoard, compSymbol)
	newProb = gamevars.boardTree[compSymbol].search(newBoard).prob
	gameOver = tictactoe.gameOver(newBoard)

	# Save previous board into session cookie
	session["previousBoard"] = gamevars.previousBoard

	# If simulated game, update other computer's last probability
	if simulation == "true" and gameOver:
		opponent = gamevars.players[gamevars.players != compSymbol]

		if tictactoe.win(newBoard, compSymbol):
			tictactoe.learnFromLoss(opponent)
		elif tictactoe.tie(newBoard):
			tictactoe.learnFromTie(opponent)

	# If not a simulation, send back game status and computer's probability of winning 
	if gameOver and simulation == "false":
		gamevars.setPlayerSymbols(session)
		msg = tictactoe.result(newBoard)
	elif simulation =="false":
		msg = newProb
	else:
		msg = ""

	data = json.dumps({"board": newBoard, "over": gameOver, "msg": msg})
	return data

# Check if player caused a game over
@application.route("/game-over", methods=["POST"])
def over():
	currentBoard = request.form["board"]
	gameOver = tictactoe.gameOver(currentBoard)
	tieGame = tictactoe.tie(currentBoard)

	data = json.dumps({"over": gameOver, "tie": tieGame})
	return data

# Update computer's last probability if human ends game
@application.route("/comp-loss", methods=["POST"])
def loss():
	compSymbol = request.form["comp-symbol"]
	tictactoe.learnFromLoss(compSymbol)

	return json.dumps({})

@application.route("/comp-tie", methods=["POST"])
def tie():
	compSymbol = request.form["comp-symbol"]
	tictactoe.learnFromTie(compSymbol)

	return json.dumps({})

# Reset AI probability files
@application.route("/reset-ai")
def reset():
	tictactoe.resetAI()

	return json.dumps({})
	
###############################################################################
#                                                                             #
#                              Start Application                              #
#                                                                             #
############################################################################### 

if __name__ == "__main__":
	application.run()