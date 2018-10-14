import sqlite3, time, sys, os, cProfile

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

#path to css log
#parses "status" console command, which shows us data about players on the server
#enables by command in game's console
#write "status" every moment you want to save players
#or simple bind this, example: bind w "status;+forward"

con_log_path = "D:\Apps\Counter-Strike Source\cstrike\con_log.log"

db_name = "players.db"
db = sqlite3.connect(db_name)

class Player:
    def __init__(self, name, uid, last_seen):
        self.name = name
        self.uid = uid
        self.last_seen = last_seen

def parse_name(string):
    n_index1 = string.index(r'"')
    n_index2 = string.rindex(r'"')
    nickname = string[n_index1+1 : n_index2]
    return nickname

def parse_uid(string):
    id_index1 = string.rindex(r'[')
    id_index2 = string.rindex(r']')
    uid = string[id_index1+1 : id_index2]
    return uid

def parse_player(string):
    name = parse_name(string)
    uid = parse_uid(string)
    return Player(name, uid, round(time.time()))

def create_db():
    
    db = sqlite3.connect('players.db')
    db.execute("DROP TABLE IF EXISTS Player")
    db.execute("DROP TABLE IF EXISTS Name")
    db.execute(
        '''CREATE TABLE Player(
    UID CHAR[20] PRIMARY KEY NOT NULL,
    LastSeen TEXT NOT NULL)''')
    db.execute(
    '''CREATE TABLE Name(
    UID CHAR[20] NOT NULL,
    Name CHAR[32] NOT NULL,
    FOREIGN KEY(UID) REFERENCES Player(UID),
    PRIMARY KEY (UID, Name)
    )''')
    db.commit()
    db.close()

def db_add_player(player):
    #db = sqlite3.connect('players.db');
    db.execute("INSERT OR IGNORE INTO Player VALUES('%s', '%s', '%s')" % (player.uid, player.last_seen, round(time.time())))
    db.execute("UPDATE Player SET LastSeen='%s' WHERE UID='%s'" % (player.last_seen, player.uid))
    db.execute("INSERT OR IGNORE INTO Name(UID, Name) VALUES('%s','%s')" % (player.uid, player.name))
    #db.close()


def main():
    with open(con_log_path, 'r', encoding="utf8") as file:
        lines = file.readlines()
    lines = [s.strip() for s in lines]

    for s in lines:
        if len(s)>0 and s[0] == '#':
            try:
                db_add_player(parse_player(s.replace(r"'", '')))
            except ValueError:
                pass
    db.commit()
    try:
        os.remove('D:\Apps\Counter-Strike Source\cstrike\con_log.log')
        print("Log deleted\n")
    except PermissionError:
        print("Log can't be deleted, close CSS first\n")

            
    #db = sqlite3.connect('players.db');
    cursor = db.execute(
    '''SELECT p.LastSeen, p.UID, GROUP_CONCAT(n.Name, ',  ') 
    FROM Player p 
    JOIN Name n ON p.UID = n.UID
    GROUP BY p.UID
    ORDER BY p.LastSeen DESC, n.Name LIMIT 75''')

    for row in cursor:
        line = ''
        for s in row:
            line += s+' '
        print(line.translate(non_bmp_map))


    db.close()
    input("Press RETURN to close window")




main()
