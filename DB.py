import json
from pymongo import MongoClient
import re
client=MongoClient("mongodb://localhost:27017/")
db=client['test']
collection=db['table']

#post to server new game all the data
def addGameToServer(board, p1):
    #Remove line D
    #collection.delete_many({})
    #collection.insert_one({"board": board, "pnum": pnum, "psim": psim})
    collection.insert_one({"board": board, "p1": p1, "p2": "none" , "turn":p1 })

#search in the database by player ID
def searchInServerByPlayerID(pID):
    tmp=collection.find_one({'$or':[{"p1": pID},{"p2": pID}]})
    if tmp != None:
        p1 = tmp["p1"]
        p2 = tmp["p2"]
        turn=tmp["turn"]
        board = tmp["board"]
        boardID=tmp["_id"]
        return board, p1, p2, turn, boardID
    else:
        return tmp


#update game
def updateGameBoard(pID,board):
    tmp = collection.find_one({"turn": pID})
    p1 = tmp["p1"]
    p2 = tmp["p2"]
    turn = tmp["turn"]
    if p1==turn:
        collection.find_one_and_update({"turn":pID},{'$set':{"board": board,"turn": p2}})
    else:
        collection.find_one_and_update({"turn":pID},{'$set':{"board": board,"turn": p1}})


#SerchForGame
def findGame(p2ID):
    tmp = collection.find_one({"p2": "none"})
    #there is a player1 waiting
    if tmp != None:
        collection.find_one_and_update({"p2": "none"}, {'$set': {"p2": p2ID}})
        return 2
    #there are no games
    else:
        board = ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']
        addGameToServer(board, p2ID)
        return 1

#delete when game ends
def endGame(boardID):
    tmp = searchInServerByPlayerID(boardID)
    if tmp == None:
        print()
    else:
        collection.delete_one({ "_id": boardID })


#collection.delete_many({})


#findGame(1)
#findGame(2)
#findGame(3)
#findGame(4)

#board, p1, p2, turn, boardID=searchInServerByPlayerID(2)
#print(boardID)
#endGame(boardID)


