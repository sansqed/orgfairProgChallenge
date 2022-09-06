import csv
import random
import time
import sys
import math
import shutil

unsolved = {}
players = []

class Player:
    def __init__(self, name, year, hrScore, hrTotal, problemID, successRate, timerRem, score=None):
        self.name = name
        self.year = year
        self.hrScore = hrScore
        self.hrTotal = hrTotal
        self.problemID = problemID
        self.successRate = successRate
        self.minRem = timerRem
        if score == None:
            self.score = math.floor(((hrScore/hrTotal) * (10/(successRate**10))) + timerRem)
        else:
            self.score = score

def loadProblems():
    with open('problems.csv', 'r') as problemscsv:
        reader = csv.reader(problemscsv)

        for row in reader:
            if row[1] == 'No':
                unsolved[row[0]] = row[2:]

def newProblem():
    probID = random.choice(list(unsolved.keys()))
    sucRate = unsolved[probID][3]

    print("YOU'RE PROBLEM IS: " + unsolved[probID][0])
    time.sleep(1)
    print("DIFFICULTY: " +  unsolved[probID][2])
    time.sleep(1)
    print("PROBLEM SUCCESS RATE: " + str(unsolved[probID][3]))


    time.sleep(1)
    print("\nLink: " + unsolved[probID][1])
    
    unsolved.pop(probID)
    problemSolved(probID)
    

    return [probID, sucRate]

def problemSolved(problemID):

    with open('problems.csv', 'r') as original:
        

        # tempFile = open('tempproblems.csv', 'x')
        
        tempFile = open('tempproblems.csv', 'w', newline='')

        writer = csv.writer(tempFile)
        reader = csv.reader(original)

        for row in reader:
            if row[0] == problemID:
                row[1] = 'Yes'
            writer.writerow(row)
        tempFile.close()

    shutil.move('tempproblems.csv', "problems.csv")

def problemUnsolved(problemID):

    with open('problems.csv', 'r') as original:
        

        # tempFile = open('tempproblems.csv', 'x')
        
        tempFile = open('tempproblems.csv')

        writer = csv.writer(tempFile)
        reader = csv.reader(original)

        for row in reader:
            if row[0] == problemID:
                row[1] = 'No'
            writer.writerow(row)
        tempFile.close()

    shutil.move('tempproblems.csv', "problems.csv")
                

def welcomeMessage():
    print()
    print("-----------------------------------------------------")
    print("|    WELCOME TO THE UPCSG PROGRAMMING CHALLENGE!    |")
    print("-----------------------------------------------------")
    print()

    return input("TYPE 'START' TO START: ")


def timer():

    print("\nTO STOP THE TIMER, PRESS CTRL+C ONCE.")

    time.sleep(3)

    print("\nYour remaining time:")
    timer = [00, 15]

    while timer != [0,0]:

        try:
            # decrease time
            if timer[1] == 0:
                timer[1] = 59
                timer[0] -= 1
            else:
                timer[1] -= 1

            # print("%d:%d" %(timer[0], timer[1]))
            
            sys.stdout.write("\r")
            sys.stdout.write("{:2d}:" .format(timer[0]) + "{:2d}" .format(timer[1])) 
            sys.stdout.flush()
                
            time.sleep(1)

        except KeyboardInterrupt:
            return timer
    return timer

def addPlayer2csv(player:Player):
    with open('players.csv', 'a', newline='') as playercsv:

        writer = csv.writer(playercsv)

        row = [player.name, player.year, player.hrScore, player.hrTotal, 
            player.problemID, player.successRate, player.minRem, player.score]

        writer.writerow(row)
def loadPlayers():
    with open('players.csv', 'r') as playerscsv:
        reader = csv.reader(playerscsv)

        for row in reader:
            tempPlayer = Player(row[0], row[1], int(row[2]), int(row[3]), row[4], float(row[5]), int(row[6]), int(row[7]))
            players.append(tempPlayer)

# sort and print
def leaderboard():
    for i in range(1, len(players)):
        key = players[i]

        j = i-1

        while j>=0 and key.score > players[j].score:
            players[j+1] = players[j]
            j-=1
        players[j+1] = key

    rank=1
    print("           --LEADERBOARD--")
    print("RANK  NAME                 YEAR SCORE")
    
    for player in players:
        print("{0:<5}" .format(rank) + " {0:<20}" .format(player.name) + " {0:<5}".format(player.year) + " %s" %(player.score))
        # print("%d %s\t%s\t%d" %(rank, player.name, player.year, player.score))
        rank += 1



def main():

    loadPlayers()
    while True:
        leaderboard()
        startCode = welcomeMessage()

        if startCode == "START":

            print() 
            loadProblems()
            prob = newProblem()
            
            print()
            print("Open the link first before starting the timer")
            time.sleep(2)
            input("--PRESS ENTER TO START THE TIMER--")
            rem = timer()


            print()
            print()
            name = input("Name: ")
            year = input("Year: ")
            hrScore = int(input("HackerRank Score: "))
            hrTotal = int(input("HackerRank Total Score: "))

            
            player = Player(name, year, hrScore, hrTotal, prob[0], float(prob[1]), rem[0])
            players.append(player)
            addPlayer2csv(player)
            
            print()






        else:
            break
    # print("hello")

    
def test():
    # problemSolved('E1')
    loadPlayers()
    leaderboard()


if __name__ == '__main__':
    main()
    # test()