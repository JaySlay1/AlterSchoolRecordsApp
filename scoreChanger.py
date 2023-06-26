import mysql.connector
import re

#Intiliaze and load environment variables key-value pairs for sensitive information.
from dotenv import load_dotenv
import os
load_dotenv()

def checkCorrectInt(inputInt):
    try:
        int(inputInt)
        return True
    except:
        return False

def checkCorrectStr(inputStr):
    return not bool(re.search(r'[^a-zA-Z\s]', inputStr))


def initSQLconnection():
    #Add a try here incase the db is offline
    mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
    )
    return mydb

def inputScore():
#need to check for incorrect inputs. -0 +100, floats, ints, exceeding char count
    #Add function to pull examSubjects from SQL server
    examSubjects = ["Math","IT","Chemistry"]
    userArray=[]

    #Check valid string and within Char limit (50)
    username = None

    while username is None or checkCorrectStr(username) == False:
        username = input("Provide username: ")
        if checkCorrectStr(username) == False:
              print("Please use a valid username")
        elif len(str(username)) == 0 or len(str(username)) > 5:
            print("Please use a username within the character limit")
            username = None

    userArray.append(username)

    #Check valid integer inputs for all examSubjects
    for examSubject in examSubjects:
        score = None
        while score is None or checkCorrectInt(score) == False:
            score = input(f"Please provide {examSubject} score: ")
            if checkCorrectInt(score) == False:
                print("Please add a valid score")
            elif int(score) > 100 or int(score) < 0:
                print("Please add a score between 0 and 100")
                score = None
        userArray.append(score)
    return userArray

def updateSQL(keys, values,mydb):

    myCursor = mydb.cursor()
    myCursor.execute("USE PyProj")
    colNames = ", ".join(keys)
    valNames = ", ".join(f"'{value}'" for value in values)
    sql = f"INSERT INTO StudentTests ({colNames}) VALUES ({valNames})"
    myCursor.execute(sql)
    mydb.commit()
    print(myCursor.rowcount, "record inserted.")
        
#Main code

dbKeys = ("username","mathScore","itScore","chemScore") 

#add choice to view testscore or add. if view, allow for specific or all scores.
#Encrypt password and hostname information before adding code to Github 
  
dbcxn = initSQLconnection()
userScore = inputScore()
updateSQL(dbKeys, userScore, dbcxn)

