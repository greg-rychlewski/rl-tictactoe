###############################################################################
#                                                                             #
#                       Enumeration of Possible Boards                        #
#                                                                             #
###############################################################################

# Tree class for holding board configurations
class Tree:
    def __init__(self, board, prob):
        self.board = board
        self.prob = prob
        self.children = []
        
    def insertChild(self, board, prob):
        self.children.append(Tree(board, prob))
        
    def countBoards(self):
        numBoards = 1
        
        for child in self.children:
            numBoards += child.countBoards()
                
        return numBoards
        
    def containsBoard(self, board):
        if board in self.board:
            return True
        else:
            for child in self.children:
                if child.containsBoard(board):
                    return True
            return False
            
    def search(self, board):
        if board in self.board:
            return self
        else:
            for child in self.children:
                result = child.search(board)
                if result is not None:
                    return result
            return None

# Create tree with all possible board configurations, taking symmetry into account
def enumBoards(currentTree, boardTree, currentPlayer):
    currentBoard = currentTree.board[0]
    
    if gameOver(currentBoard):
        return     
    
    for i in range(len(currentBoard)):
        if currentBoard[i] == '-':
            nextBoard = currentBoard[:i] + currentPlayer + currentBoard[i+1:]
            
            if boardTree.containsBoard(nextBoard):
                continue
            
            if win(nextBoard, gamevars.computer):
                prob = gamevars.winProb
            elif win(nextBoard, gamevars.human):
                prob = gamevars.lossProb
            elif tie(nextBoard):
                prob = gamevars.tieProb
            else:
                prob = gamevars.neutralProb
                
            currentTree.insertChild(symmetries(nextBoard), prob)
            
            if currentPlayer == 'x':
                nextPlayer = 'o'
            else:
                nextPlayer = 'x'
                
            enumBoards(currentTree.children[-1], boardTree, nextPlayer)
            
###############################################################################
#                                                                             #
#                               Symmetry Functions                            #
#                                                                             #
###############################################################################

# Rotate board 90 degrees clockwise
def rotate(board):
    oldBoard = [list(board[:3]), list(board[3:6]), list(board[6:])]
    newBoard = ''
    
    for i in range(3):
        newBoard += oldBoard[2][i] + oldBoard[1][i] + oldBoard[0][i]
        
    return newBoard

# Reflect board horizontally, vertically or diagonally
def reflect(board, line):
    oldBoard = [list(board[:3]), list(board[3:6]), list(board[6:])]
    
    if line == 'h':
        oldBoard.reverse()
        newBoard = ''.join(col for row in oldBoard for col in row)
    elif line == 'v':
        for i in range(3):
            temp = oldBoard[i][0]
            oldBoard[i][0] = oldBoard[i][2]
            oldBoard[i][2] = temp
            newBoard = ''.join(col for row in oldBoard for col in row) 
    elif line == 'd1':
        ul = [(0,0), (0,1), (1,0)]
        lr = [(2,2), (1,2), (2,1)]
        for i in range(len(ul)):
            temp = oldBoard[ul[i][0]][ul[i][1]]
            oldBoard[ul[i][0]][ul[i][1]] = oldBoard[lr[i][0]][lr[i][1]]
            oldBoard[lr[i][0]][lr[i][1]] = temp
            newBoard = ''.join(col for row in oldBoard for col in row) 
    elif line == 'd2':
        ur = [(0,2), (0,1), (1,2)]
        ll = [(2,0), (1,0), (2,1)]
        for i in range(len(ur)):
            temp = oldBoard[ur[i][0]][ur[i][1]]
            oldBoard[ur[i][0]][ur[i][1]] = oldBoard[ll[i][0]][ll[i][1]]
            oldBoard[ll[i][0]][ll[i][1]] = temp
            newBoard = ''.join(col for row in oldBoard for col in row)  
        
    return newBoard
    
# Return list of all symmetries of a board        
def symmetries(board):
    rot1 = rotate(board)
    rot2 = rotate(rotate(board))
    rot3 = rotate(rotate(rotate(board)))
    refHor = reflect(board, 'h')
    refVert = reflect(board, 'v')
    refDiag1 = reflect(board, 'd1')
    refDiag2 = reflect(board, 'd2')
    
    result = []
    for symm in [board, rot1, rot2, rot3, refHor, refVert, refDiag1, refDiag2]:
        if symm not in result:
            result.append(symm)
        
    return result

###############################################################################
#                                                                             #
#                              Endgame Scenarios                              #
#                                                                             #
###############################################################################

# Did a player win?
def win(board, player):
    winRow1 = board[0] == player and board[1] == board[0] and board[2] == board[0]
    winRow2 = board[3] == player and board[4] == board[3] and board[5] == board[3]
    winRow3 = board[6] == player and board[7] == board[6] and board[8] == board[6]
    winCol1 = board[0] == player and board[3] == board[0] and board[6] == board[0]
    winCol2 = board[1] == player and board[4] == board[1] and board[7] == board[1]
    winCol3 = board[2] == player and board[5] == board[2] and board[8] == board[2]
    winDia1 = board[0] == player and board[4] == board[0] and board[8] == board[0]
    winDia2 = board[2] == player and board[4] == board[2] and board[6] == board[2]
    
    return winRow1 or winRow2 or winRow3 or winCol1 or winCol2 or winCol3 or winDia1 or winDia2

# Is the game a tie?
def tie(board):
    full = '-' not in board
    
    return full and not win(board, 'x') and not win(board, 'o')

# Is the game over?   
def gameOver(board):
    return win(board, 'x') or win(board, 'o') or tie(board)
    
###############################################################################
#                                                                             #
#                              Game Functions                                 #
#                                                                             #
###############################################################################
    
# Computer's turn
def computerTurn(currentBoard, player):
    nextProbs = []
    nextBoards = []
    
    for i in range(len(currentBoard)):
        if currentBoard[i] == '-':
            tempBoard = currentBoard[:i] + player + currentBoard[i+1:]
            tempTree = gamevars.boardTree[player].search(tempBoard)
            nextProbs.append(tempTree.prob)
            nextBoards.append(tempBoard)
            
    bestProb = max(nextProbs)
    bestProbIdx = [i for i, prob in enumerate(nextProbs) if prob==bestProb]
    bestBoards = [board for i, board in enumerate(nextBoards) if i in bestProbIdx]
    
    explore = random.uniform(0, 1) <= gamevars.probExplore
    
    if explore:
        nextBoard = random.choice(nextBoards)
    else:
        nextBoard = random.choice(bestBoards)
        if gamevars.previousBoard[player] is not None:
            nextTree = gamevars.boardTree[player].search(nextBoard)
            previousTree = gamevars.boardTree[player].search(gamevars.previousBoard[player])
            previousTree.prob += gamevars.learningRate*(nextTree.prob - previousTree.prob)

    saveTree(player)
    gamevars.previousBoard[player] = nextBoard
    
    return nextBoard

# Update probabilities when opponent ends game
def learnFromLoss(player):
    previousTree = gamevars.boardTree[player].search(gamevars.previousBoard[player])
    previousTree.prob += gamevars.learningRate*(gamevars.lossProb - previousTree.prob)

def learnFromTie(player):
    previousTree = gamevars.boardTree[player].search(gamevars.previousBoard[player])
    previousTree.prob += gamevars.learningRate*(gamevars.tieProb - previousTree.prob)

# End-game message
def result(board):
    if win(board, gamevars.computer):
        return "AI Wins"
    elif win(board, gamevars.human):
        return "Human Wins"
    else:
        return"Tie Game" 

# Save tree to disk
def saveTree(player):
    boardPickle = Path("./pickles/board_" + player + ".pickle")
    pickle.dump(gamevars.boardTree[player], open(str(boardPickle), "wb"))

# Reset computer's decision trees
def resetAI():
    for player in gamevars.players:
        gamevars.computer = player
        gamevars.human = gamevars.players[gamevars.players != gamevars.computer]
        gamevars.boardTree[player] = Tree(["---------"], 0.5)
        enumBoards(gamevars.boardTree[player], gamevars.boardTree[player], "x")
        saveTree(player) 

###############################################################################
#                                                                             #
#                                 Dependencies                                #
#                                                                             #
############################################################################### 

# Random number generator
import random

# Object serialization
import pickle

# File path generation
from pathlib import Path

# Global game variables
import gamevars