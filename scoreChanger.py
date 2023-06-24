import mysql.connector

#Intiliaze and load environment variables key-value pairs for sensitive information.
from dotenv import load_dotenv
import os
load_dotenv()


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
    username = input("Provide username: ")
    MathScore = input("Provide Math Score: ")
    ITScore = input("Provide IT Score: ")
    ChemScore = input("Provide Chemistry Score: ")

    userArray = [
        username,
        MathScore,
        ITScore,
        ChemScore]
    
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
        

dbKeys = ("username","mathScore","itScore","chemScore") 
#add choice to view testscore or add. if view, allow for specific or all scores.
#Encrypt password and hostname information before adding code to Github   
dbcxn = initSQLconnection()
userScore = inputScore()
updateSQL(dbKeys, userScore, dbcxn)

