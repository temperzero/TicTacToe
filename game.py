from flask import Flask, render_template, url_for, request, redirect, session, flash, make_response
import uuid
import DB

app = Flask(__name__) ## reference to file name
app.secret_key = "hello" # needed?

@app.route('/')
def start():
	found = checkCookie()
	if found == False:
		unique = uuid.uuid4()
		res = make_response(redirect('/login'))
		res.set_cookie("uid", str(unique)) # key and value
		return res
	else:
		return redirect('/login')

@app.route('/login', methods=["GET"])
def login():
	return render_template('login.html')

@app.route('/login', methods=["POST"])
def loginRedirect():
	uid = request.cookies.get("uid")
	num = DB.findGame(uid)
	print(num)
	if num == 1:
		sim = "X"
	else:
		sim = "O"
	res = make_response(redirect('/game'))
	res.set_cookie("pnum", str(num))
	res.set_cookie("psim", str(sim))
	return res

def checkCookie():
	if "uid" in request.cookies:
		return True
	else:
		return False

@app.route('/game', methods=["GET"])
def gameGet(): 
	if checkCookie():
		uid = request.cookies.get("uid") 
		playersymbol = request.cookies.get("psim")
		playernumber = request.cookies.get("pnum")
		board,p1,p2,turn,boardID= DB.searchInServerByPlayerID(uid)
		if p2 == "none":
			return render_template('game.html',msg = "waiting for second player")
		else:
			if checkVictory(board,playersymbol): 
				return render_template('game.html',table = board, playernumber = playernumber, victory = True)
			elif checkLose(board,playersymbol):
				DB.endGame(boardID)
				return render_template('game.html',table = board, playernumber = playernumber, lose = True)
			elif checkDraw(board):
				DB.endGame(boardID)
				return render_template('game.html', table=board, playernumber=playernumber, draw=True)
			else:
				return render_template('game.html',table = board, playersymbol = playersymbol, playernumber = playernumber, currentplayer = getCurrentPlayer(turn,p1))
	else:
		return render_template('game.html',error = True)

@app.route('/game', methods=["POST"]) 
def gamePost(): 	
	if checkCookie():
		uid = request.cookies.get("uid")
		playersymbol = request.cookies.get("psim")
		playernumber = request.cookies.get("pnum")
		board,p1,p2,turn,boardID = DB.searchInServerByPlayerID(uid)
		row = request.form["row"]
		col = request.form["col"]
		if(turn == uid):
			if(checkInput(row,col)): 
				row = int(row)
				col = int(col)
				Legal, board = setMove(board,playersymbol, row, col)
				if Legal: 
					if checkVictory(board,playersymbol): 
						DB.updateGameBoard(uid,board)
						return render_template('game.html',table = board, playernumber = playernumber ,victory = True)
					else:
						DB.updateGameBoard(uid,board)
						return render_template('game.html',table = board, playersymbol = playersymbol, playernumber = playernumber, currentplayer = getCurrentPlayer(turn,p1))
				else:
					return render_template('game.html',table = board, playersymbol = playersymbol, playernumber = playernumber,currentplayer = getCurrentPlayer(turn,p1) ,illegalmove = True)
			else:
				return render_template('game.html',table = board, playersymbol = playersymbol, playernumber = playernumber,currentplayer = getCurrentPlayer(turn,p1), illegalinput = True)
		else:
			return render_template('game.html',table = board, playersymbol = playersymbol, playernumber = playernumber,currentplayer = getCurrentPlayer(turn,p1), illegalturn = True)
	else:
		return render_template('game.html', error = True)

def checkInput(row,col):
	try:
		row = int(row)
		col = int(col)
		if(row < 3 and row >= 0 and col < 3 and col >= 0):
			return True
		else:
			return False
	except ValueError:
		return False

def setMove(board,symbol,row,col):
	if board[row][col] == "-":  # if the cell is not already marked
		board[row][col] = symbol
		return True, board
	else:
		print("illegal!!!")
		return False, board  # choose a different cell

def checkLose(board,symbol):
	if symbol=='X':
		symbol='O'
	else:
		symbol='X'

	if checkVictory(board,symbol) == True:
		return True
	else:
		return False

def getCurrentPlayer(turn,p1):
	if(turn==p1):
		return 1
	else:
		return 2

def checkVictory(board, symbol):
	# board is luah
	# symbol is x or igul
	win = True  # win condition
	#board = np.array(board);  # from list to array to make use of shape func
	rows = 3;  # calc row count
	cols = 3;  # calc col count
	# checking rows
	# win is reseted to true for each row check
	# after second for, if win = true => there is 3 symbols in a row
	for i in range(rows): 
		win = True
		for j in range(cols):
			if board[i][j] != symbol: 
				win = False
				break  # to remove?
		if win:
			return win

	# checking rows
	# win is reseted to true for each col check
	# after second for, if win = true => there is 3 symbols in a row (in a col)
	for k in range(cols):
		win = True
		for l in range(rows):
			if board[l][k] != symbol:
				win = False
				break
		if win:
			return win

	# checking diagonal
	# if 3 in a alchsonation then cool
	# works for NxN board (rows = cols)
	win = True
	for d in range(rows):
		if board[d][d] != symbol:
			print(board[d][d])
			win = False
			break
	if win:
		return win

	win = True

	# check for second diagonal
	# start from board[0][2] to board[1][1] to board[2][0]
	# rows = 3
	for d2 in range(rows):
		if board[d2][rows - 1 - d2] != symbol:
			win = False
			break
	if win:
		return win
	return False

def checkDraw(board):
	rows = 3  # calc row count
	cols = 3  # calc col count
	draw = True
	for i in range(rows):
		for j in range(cols):
			if board[i][j] == '-':
				draw = False
				break
	return draw

if __name__ == "__main__":
	app.run(debug=True)
