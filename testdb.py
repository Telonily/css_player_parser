import sqlite3, sys, os
from time import strftime
from datetime import datetime

def sql(query):
    db = sqlite3.connect('players.db')
    try:
        db.execute(query)
    except sqlite3.IntegrityError:
        pass
    db.commit()
    db.close()

def format_time(str):
    return datetime.fromtimestamp(float(str)).strftime("%d %b %Y")

##with open('players.txt', 'r', encoding="utf8") as file:
##    lines = file.readlines()
##lines = [s.strip() for s in lines]
##
##for s in lines:
##    arr = s.split("|||")
##    uid = arr[0]
##    sql("INSERT INTO Player VALUES ('%s', '0')" % uid)
##    for i in range(1, len(arr)):
##        query = "INSERT INTO Name(UID, Name) VALUES('%s', \"%s\")" % (uid, arr[i])
##        sql(query)
        

##non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
##
##db = sqlite3.connect("players.db")
##cursor = db.execute(
##
##'''SELECT p.LastSeen, p.UID, GROUP_CONCAT(n.Name, ',  ')
##FROM Player p
##JOIN Name n ON p.UID = n.UID
##GROUP BY p.UID
##ORDER BY p.LastSeen'''
##)
##
##for row in cursor:
##    line = ''
##    for s in row:
##        line += s+' '
##    print(line.translate(non_bmp_map))



query = "SELECT * FROM Name WHERE Name LIKE 'barb%'"

##query = "SELECT * FROM Name WHERE UID='U:1:3679676428'"
    
##query = "UPDATE player SET FirstSeen = '0'"

##query = "SELECT * FROM Player LIMIT 50"

#query = "SELECT sql FROM sqlite_master WHERE name='Player';"

db = sqlite3.connect("players.db")
cursor = db.execute(query)
db.commit()


for row in cursor:
    line = ''
    #print(row[0], format_time(row[1]), format_time(row[2]))
    print(row)

db.close()

print("\n\n-----------\ndone here!")





