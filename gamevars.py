###############################################################################
#                                                                             #
#                                 Dependencies                                #
#                                                                             #
############################################################################### 

# File path generation
from pathlib import Path

# Object serialization
import pickle

###############################################################################
#                                                                             #
#                              Helper Functions                               #
#                                                                             #
############################################################################### 

# Set symbols for current game
def setPlayerSymbols(session):
	global computer
	computer = session["computer"]

	global human
	human = session["human"]

# Load board object from file
def setBoardTree():
	global boardTree

	for player in players:
		boardPickle = Path("./pickles/board_" + player + ".pickle")
		boardTree[player] = pickle.load(open(str(boardPickle), "rb"))

# Set previous board histories for current game
def setPreviousBoard(session):
	global previousBoard

	if "previousBoard" in session:
		previousBoard = session["previousBoard"]

###############################################################################
#                                                                             #
#                              Global Variables                               #
#                                                                             #
############################################################################### 

# Player symbols
players = ["x", "o"]
computer = None
human = None

# Tree object for board enumeration
boardTree = {}
setBoardTree()

# Save previous board layout for each player
previousBoard = {"x": None, "o": None}

# Probabilities for winning from a board layout
winProb = 1
lossProb = 0
tieProb = 0.5
neutralProb = 0.5

# Game parameters
learningRate = 0.05
probExplore = 0.1