from flask import Flask, render_template, request, jsonify

from linearRegression import initLinearRegModelOverall

import pandas as pd
import numpy as np
import os
import csv 
import math
import operator


#flask instatiation 
app = Flask(__name__)


#convert the csv to a 2d array with only the relevant data for the model. 
#convert every data point to a float. 
def loadDataset(filename):
	with open(filename, 'rt') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		trainingSet = []
		for x in range(1, len(dataset)):
			tempTrainingExample = []
			for y in range(46):
				currIndex = 23
				currIndex += y
				if dataset[x][currIndex] == '':
					tempTrainingExample.append(float(0))
					continue

				dataset[x][currIndex] = float(int(dataset[x][currIndex]))
				tempTrainingExample.append(float(dataset[x][currIndex]))
			#append name on last index
				
			tempTrainingExample.append(dataset[x][3].lower())
			tempTrainingExample.append(dataset[x][3])
			tempTrainingExample.append(dataset[x][9])#overall rating 
			tempTrainingExample.append(dataset[x][10])#potential
			tempTrainingExample.append(dataset[x][8]) #club
			tempTrainingExample.append(dataset[x][7]) #nation
			tempTrainingExample.append(dataset[x][4]) # age
			tempTrainingExample.append(dataset[x][1]) #sofifa page. 
			#append entire row to return 2d
			trainingSet.append(tempTrainingExample)
	return trainingSet


#used by getNeighbors to get the "similarity score" aka cost function
def euclideanDistance(instance1, instance2):
	distance = 0
	for x in range(len(instance1)-8):  #stop the range to avoid the last 8 names at the end of the row
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

#goes through all the other players and compares the eculidean distance
#between the specified players and all the others.
#Returns the players data of the k most most simlar players
def getNeighbors(trainingSet, testInstance, k):
	neighbors = []
	distances =[]
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	counter = k
	for player in distances:
		counter -= 1
		if(counter == -1):
			return neighbors
		player[0].append(player[1])	
		neighbors.append(player[0])
	return neighbors

#gets the player data of the users searched player. 
def findPlayerInstance(trainingSet, name):
	for i in range(len(trainingSet)):
		if name in trainingSet[i][46]:
			#print("found ", trainingSet[i][46], "'s data!")
			return i
	return -1





""" Routes below """

@app.route("/")
def index():
	
	words = request.args.get("q")
	exactUserInput = words
	#if user has not entered anything then just return the page. 
	#print(words , " shling")
	if words is None: 
		return render_template("index.html")

	#else the user has entered something 

	#sanatize to lowercase to increase the searches change of a hit. 
	words = words.lower()

	dataSet = loadDataset("players_20.csv")

	#do input validation and leave the correct player in the varibale, player
	#CHANGE THIS AND VALIDATE INPUT
	player = words
	
	#test training set is loading correctly 
	#print("we have training set, see: ")
	#print(len(dataSet[0]))

	#instance should be -1 if player not found, or the players index
	#in the dataSet if found. 
	print(dataSet[0])
	instance = findPlayerInstance(dataSet, player)
	#print(instance) 

	#if player not found then instance == -1. 
	if(instance == -1):
		return render_template("index.html", playerNotFound=True, lastUserSearch=exactUserInput)

	#get the k nearest neighbors.
	neighbors = getNeighbors(dataSet, dataSet[instance], 10)

	#convert rows to names, use row 47 to get the capitalized names 
	namesNeighbors = []
	for i in range(len(neighbors)):
		tempDict = {}
		tempDict['name'] = neighbors[i][47].strip()
		tempDict['overall'] = neighbors[i][48].strip()
		tempDict['potential'] = neighbors[i][49].strip()
		tempDict['club'] = neighbors[i][50].strip()
		tempDict['nation'] = neighbors[i][51].strip()
		tempDict['age'] = neighbors[i][52].strip()
		tempDict['link'] = neighbors[i][53].strip()

		score = neighbors[i][54]
		score = (((score - 100) * (100 - 1) / (0 - 100))) + 1
		print(score)
		tempDict['score'] = score

		namesNeighbors.append(tempDict)

		#namesNeighbors.append(neighbors[i][47].strip())
		#namesNeighbors.append(neighbors[i][48].strip())


	#print(namesNeighbors)
	#print(namesNeighbors)
	return render_template("index.html", words=namesNeighbors, lastUserSearch=exactUserInput)


@app.route("/linear-regression")
def linearRegression():

	words = request.args.get("q")

	if words is None:
		return render_template("linear-regression.html")

	exactUserInput = words
	player = words.lower()

	print(words, " word from lr request ")
	dataSet = loadDataset("players_20.csv")
	instance = findPlayerInstance(dataSet, player)
	print("instance from lr request", instance)
	if instance == -1:
		return render_template("linear-regression.html", playerNotFound=True, lastUserSearch=exactUserInput)


	results = initLinearRegModelOverall(dataSet, instance)
	print(results)
	predictionOverall = results[0] + 5
	predictionPotential = results[1] + 5

	predictionOverall= str(round(predictionOverall, 2))
	predictionPotential= str(round(predictionPotential, 2))


	print("prediction from lr request ", predictionOverall)
	print("potentail from lr request ", predictionPotential)

	#get the players row in the dataSet and pass it to the model

	playerStats = {}
	playerStats['name'] = dataSet[instance][47].strip()
	playerStats['overall'] = dataSet[instance][48].strip()
	playerStats['potential'] = dataSet[instance][49].strip()
	playerStats['club'] = dataSet[instance][50].strip()
	playerStats['nation'] = dataSet[instance][51].strip()
	playerStats['age'] = dataSet[instance][52].strip()
	playerStats['link'] = dataSet[instance][53].strip()

	return render_template("linear-regression.html", predOverall=predictionOverall, predPotential=predictionPotential, 
	playerStats=playerStats, lastUserSearch=exactUserInput )


@app.route("/about")
def about(): 
	return render_template("about.html")