#!/usr/bin/env python3
import global_settings
import sys
import getopt
import time
import chat
import game
import player
import flag
import sql_stats

def HandleData(data):
    if (data.startswith("[register]")):
        #say("register found: " + data) #working but was only useless chat spam for testing        
        pass
    elif (data.startswith("[Console]")):
        if (data.find("No such command") != -1):
            return
        elif (data.startswith("[Console]: !list")):
            echo(str(CountPlayers()) + " players online")
        elif (data.startswith("[Console]: !dev")):
            echo("debug=" + str(global_settings.IsDebug) + " stats=" + global_settings.StatsMode)
    elif (data.endswith("' joined the spectators\n")):
        player.HandlePlayerTeamSwap(data, True)
    elif (data.find("' entered and joined the ") != -1):
        if (data.startswith("[chat]: ***")):
            player.HandlePlayerJoin(data)
    elif (data.find("' joined the ") != -1 and data.endswith(" team\n")):
        if (data.startswith("[chat]: ***")):
            player.HandlePlayerTeamSwap(data)
    elif (data.find("' has left the game") != -1):
        if (data.startswith("[chat]: ***")):
            player.HandlePlayerLeave(data)
    elif (data.startswith("[chat]") or data.startswith("[teamchat]")):
        if (data.startswith("[chat]: ***")):
            if (data.startswith("[chat]: *** The blue flag was captured by '") or data.startswith("[chat]: *** The red flag was captured by '")):
                flag.HandleFlagCap(data)
            elif (data.find("' changed name to '") != -1):
                player.HandleNameChange(data)
            return
        chat.HandleChatMessage(data)
    elif (data.startswith("[game]")):
        game.HandleGame(data)

def MainLoop():
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            HandleData(line[10:]) #cut off the timestamp
    except EOFError:
        pass    # the telnet/netcat process finished; there's no more input

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hd:s:",["debug=","stats="])
    except getopt.GetoptError:
        print("main.py -d <debug:true/false> -s <stats:SQL/file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
             print("test.py -i <inputfile> -o <outputfile>")
             sys.exit()
        elif opt in ("-d", "--debug"):
             IsDebug = arg
        elif opt in ("-s", "--stats"):
             StatsMode = arg
    IsDebug = IsDebug.lower()
    StatsMode = StatsMode.lower()
    if IsDebug == "0":
        IsDebug = "false"
    elif IsDebug == "1":
        IsDebug = "true"
    if not IsDebug == "false" and not IsDebug == "true":
        print("invalid debug argument")
        exit()
    if not StatsMode == "sql" and not StatsMode == "file":
        print("invalid stats mode argument")
        exit()
    if IsDebug == "true":
        global_settings.IsDebug = True
    elif IsDebug == "false":
        global_settings.IsDebug = False
    else:
        print("eror with debug mode")
        exit()
    global_settings.StatsMode = StatsMode
    print("[TEM] debug=" + str(IsDebug) + " stats=" + str(StatsMode))
    sql_stats.InitDataBase()
    MainLoop()

if __name__ == "__main__":
    main(sys.argv[1:])

