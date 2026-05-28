from src.character_repository import apply_passive_status_timer_tick
from src.potion_repository import build_potion_shop_display

import fchat
import random
import discord
import asyncio
import threading

from threading import Thread
from discord.ext import commands
from collections import Counter
from onMSGUtils import *
from onPRIUtils import *
from onMSGRoll import *
from onMSGAccept import *

#2490

def gamefiles():
    path = os.getcwd()
    gameFiles = os.path.join(path + "/gamefiles/")
    return gameFiles

def gameStatReset(channel):
    channel = str(channel)
    gameFiles = gamefiles()
    with open(gameFiles + channel + '.json', 'r+') as file:
        gameData = json.load(file)
        gameData["opponent"] = ""
        gameData["playerone"] = ""
        gameData["playertwo"] = ""
        gameData["winner"] = ""
        gameData["quitter"] = ""
        # PLAYER INFO
        gameData["poneinfo"] = {}
        gameData["ptwoinfo"] = {}
        # HP AND TURN COUNTERS
        # challenge = 0
        # reset = 0
        gameData["feattoken"] = 0
        gameData["game"] = 0
        gameData["count"] = 0
        gameData["token"] = 0
        gameData["critical"] = 0
        gameData["bonushurt"] = 0
        gameData["nervedamage"] = 0
        gameData["totaldamage"] = 0
        gameData["ponetotalhp"] = 0
        gameData["ptwototalhp"] = 0
        gameData["ponecurrenthp"] = 0
        gameData["ptwocurrenthp"] = 0
        # PLAYER ONE FEAT COUNTERS
        gameData["ponepmod"] = 0
        gameData["ponecmod"] = 0
        gameData["ponedmod"] = 0
        gameData["ponemmod"] = 0
        gameData["poneevade"] = 1
        gameData["ponedeflect"] = 1
        gameData["ponesunder"] = 0
        gameData["ponesunderamount"] = 0
        gameData["ponebullrush"] = 0
        gameData["poneheal"] = 0
        gameData["ponecripple"] = 0
        gameData["ponerelentless"] = 0
        gameData["ponerelentlessdamage"] = 0
        gameData["ponestoneskin"] = 0
        gameData["ponestonebonus"] = 0
        gameData["ponedeathsdoor"] = 0
        gameData["ponequickdamage"] = 0
        gameData["ponefeatinfo"] = None
        gameData["ponespentfeat"] = []
        gameData["ponequick"] = 0
        gameData["ponevile"] = 0
        gameData["poneheavy"] = 0
        gameData["poneinner"] = 0
        gameData["poneexpose"] = 0
        gameData["ponecheapshot"] = 0
        gameData["ponelockout"] = 0
        # PLAYER TWO FEAT COUNTERS
        gameData["ptwopmod"] = 0
        gameData["ptwocmod"] = 0
        gameData["ptwodmod"] = 0
        gameData["ptwommod"] = 0
        gameData["ptwoevade"] = 1
        gameData["ptwodeflect"] = 1
        gameData["ptwosunder"] = 0
        gameData["ptwosunderamount"] = 0
        gameData["ptwobullrush"] = 0
        gameData["ptwoheal"] = 0
        gameData["ptwocripple"] = 0
        gameData["ptworelentless"] = 0
        gameData["ptworelentlessdamage"] = 0
        gameData["ptwostoneskin"] = 0
        gameData["ptwostonebonus"] = 0
        gameData["ptwodeathsdoor"] = 0
        gameData["ptwoquickdamage"] = 0
        gameData["ptwofeatinfo"] = None
        gameData["ptwospentfeat"] = []
        gameData["ptwoquick"] = 0
        gameData["ptwovile"] = 0
        gameData["ptwoheavy"] = 0
        gameData["ptwoinner"] = 0
        gameData["ptwoexpose"] = 0
        gameData["ptwocheapshot"] = 0
        gameData["ptwolockout"] = 0
        # XP AND LEVEL COUNTERS
        gameData["ponelevel"] = 0
        gameData["ptwolevel"] = 0
        gameData["xp"] = 0
        gameData["currentplayerxp"] = 0
        gameData["nextlevel"] = 0
        gameData["levelup"] = 0
        gameData["iddqd"] = 0
        # Susanna added
        gameData["bevasion"] = False
        gameData["bdeflect"] = False
        file.seek(0)
        file.write(json.dumps(gameData, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

def gameStatLoad(channel):
    channel = str(channel)
    gameFiles = gamefiles()
    with open(gameFiles + channel + '.json', 'r+') as file:
        gameData = json.load(file)
        file.close()
    opponent = gameData["opponent"]
    playerOne = gameData["playerone"]
    playerTwo = gameData["playertwo"]
    winner = gameData["winner"]
    quitter = gameData["quitter"]
    # PLAYER INFO
    pOneInfo = gameData["poneinfo"]
    pTwoInfo = gameData["ptwoinfo"]
    # HP AND TURN COUNTERS
    # challenge = 0
    # reset = 0
    featToken = gameData["feattoken"]
    game = gameData["game"]
    count = gameData["count"]
    token = gameData["token"]
    critical = gameData["critical"]
    bonusHurt = gameData["bonushurt"]
    nerveDamage = gameData["nervedamage"]
    totalDamage = gameData["totaldamage"]
    pOneTotalHP = gameData["ponetotalhp"]
    pTwoTotalHP = gameData["ptwototalhp"]
    pOneCurrentHP = gameData["ponecurrenthp"]
    pTwoCurrentHP = gameData["ptwocurrenthp"]
    # PLAYER ONE FEAT COUNTERS
    pOnepMod = gameData["ponepmod"]
    pOnecMod = gameData["ponecmod"]
    pOnedMod = gameData["ponedmod"]
    pOnemMod = gameData["ponemmod"]
    pOneEvade = gameData["poneevade"]
    pOneDeflect = gameData["ponedeflect"]
    pOneSunder = gameData["ponesunder"]
    pOneSunderAmount = gameData["ponesunderamount"]
    pOneBullrush = gameData["ponebullrush"]
    pOneHeal = gameData["poneheal"]
    pOneCripple = gameData["ponecripple"]
    pOneRelentless = gameData["ponerelentless"]
    pOneRelentlessDamage = gameData["ponerelentlessdamage"]
    pOneStoneskin = gameData["ponestoneskin"]
    pOneStonebonus = gameData["ponestonebonus"]
    pOneDeathsDoor = gameData["ponedeathsdoor"]
    pOneQuickDamage = gameData["ponequickdamage"]
    pOneFeatInfo = gameData["ponefeatinfo"]
    pOneSpentFeat = gameData["ponespentfeat"]
    pOneQuick = gameData["ponequick"]
    pOneVile = gameData["ponevile"]
    pOneHeavy = gameData["poneheavy"]
    pOneInner = gameData["poneinner"]
    pOneExpose = gameData["poneexpose"]
    pOneCheapShot = gameData["ponecheapshot"]
    pOneLockout = gameData["ponelockout"]
    # PLAYER TWO FEAT COUNTERS
    pTwopMod = gameData["ptwopmod"]
    pTwocMod = gameData["ptwocmod"]
    pTwodMod = gameData["ptwodmod"]
    pTwomMod = gameData["ptwommod"]
    pTwoEvade = gameData["ptwoevade"]
    pTwoDeflect = gameData["ptwodeflect"]
    pTwoSunder = gameData["ptwosunder"]
    pTwoSunderAmount = gameData["ptwosunderamount"]
    pTwoBullrush = gameData["ptwobullrush"]
    pTwoHeal = gameData["ptwoheal"]
    pTwoCripple = gameData["ptwocripple"]
    pTwoRelentless = gameData["ptworelentless"]
    pTwoRelentlessDamage = gameData["ptworelentlessdamage"]
    pTwoStoneskin = gameData["ptwostoneskin"]
    pTwoStonebonus = gameData["ptwostonebonus"]
    pTwoDeathsDoor = gameData["ptwodeathsdoor"]
    pTwoQuickDamage = gameData["ptwoquickdamage"]
    pTwoFeatInfo = gameData["ptwofeatinfo"]
    pTwoSpentFeat = gameData["ptwospentfeat"]
    pTwoQuick = gameData["ptwoquick"]
    pTwoVile = gameData["ptwovile"]
    pTwoHeavy = gameData["ptwoheavy"]
    pTwoInner = gameData["ptwoinner"]
    pTwoExpose = gameData["ptwoexpose"]
    pTwoCheapShot = gameData["ptwocheapshot"]
    pTwoLockout = gameData["ptwolockout"]
    # XP AND LEVEL COUNTERS
    pOneLevel = gameData["ponelevel"]
    pTwoLevel = gameData["ptwolevel"]
    xp = gameData["xp"]
    currentPlayerXP = gameData["currentplayerxp"]
    nextLevel = gameData["nextlevel"]
    levelUp = gameData["levelup"]
    iddqd = gameData["iddqd"]
    # Susanna added
    bEvasion = gameData["bevasion"]
    bDeflect = gameData["bdeflect"]

    return opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, token,\
           critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP,\
           pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount,\
           pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin, pOneStonebonus,\
           pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pOneQuick, pOneVile, pOneHeavy, pOneInner,\
           pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder,\
           pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin,\
           pTwoStonebonus, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile,\
           pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP,\
           nextLevel, levelUp, iddqd, bEvasion, bDeflect

def gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count,
                 token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP,
                 pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder,
                 pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,
                 pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod,
                 pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush,
                 pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy,
                 pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel,
                 levelUp, iddqd, bEvasion, bDeflect, channel):

    gameFiles = gamefiles()
    with open(gameFiles + channel + ".json", "r+") as file:
        gameData = json.load(file)
        print("Why?")
        gameData["opponent"] = opponent
        gameData["playerone"] = playerOne
        gameData["playertwo"] = playerTwo
        gameData["winner"] = winner
        gameData["quitter"] = quitter
        # PLAYER INFO
        gameData["poneinfo"] = pOneInfo
        gameData["ptwoinfo"] = pTwoInfo
        # HP AND TURN COUNTERS
        # challenge = 0
        # reset = 0
        gameData["feattoken"] = featToken
        gameData["game"] = game
        gameData["count"] = count
        gameData["token"] = token
        gameData["critical"] = critical
        gameData["bonushurt"] = bonusHurt
        gameData["nervedamage"] = nerveDamage
        gameData["totaldamage"] = totalDamage
        gameData["ponetotalhp"] = pOneTotalHP
        gameData["ptwototalhp"] = pTwoTotalHP
        gameData["ponecurrenthp"] = pOneCurrentHP
        gameData["ptwocurrenthp"] = pTwoCurrentHP
        # PLAYER ONE FEAT COUNTERS
        gameData["ponepmod"] = pOnepMod
        gameData["ponecmod"] = pOnecMod
        gameData["ponedmod"] = pOnedMod
        gameData["ponemmod"] = pOnemMod
        gameData["poneevade"] = pOneEvade
        gameData["ponedeflect"] = pOneDeflect
        gameData["ponesunder"] = pOneSunder
        gameData["ponesunderamount"] = pOneSunderAmount
        gameData["ponebullrush"] = pOneBullrush
        gameData["poneheal"] = pOneHeal
        gameData["ponecripple"] = pOneCripple
        gameData["ponerelentless"] = pOneRelentless
        gameData["ponerelentlessdamage"] = pOneRelentlessDamage
        gameData["ponestoneskin"] = pOneStoneskin
        gameData["ponestonebonus"] = pOneStonebonus
        gameData["ponedeathsdoor"] = pOneDeathsDoor
        gameData["ponequickdamage"] = pOneQuickDamage
        gameData["ponefeatinfo"] = pOneFeatInfo
        gameData["ponespentfeat"] = pOneSpentFeat
        gameData["ponequick"] = pOneQuick
        gameData["ponevile"] = pOneVile
        gameData["poneheavy"] = pOneHeavy
        gameData["poneinner"] = pOneInner
        gameData["poneexpose"] = pOneExpose
        gameData["ponecheapshot"] = pOneCheapShot
        gameData["ponelockout"] = pOneLockout
        # PLAYER TWO FEAT COUNTERS
        gameData["ptwopmod"] = pTwopMod
        gameData["ptwocmod"] = pTwocMod
        gameData["ptwodmod"] = pTwodMod
        gameData["ptwommod"] = pTwomMod
        gameData["ptwoevade"] = pTwoEvade
        gameData["ptwodeflect"] = pTwoDeflect
        gameData["ptwosunder"] = pTwoSunder
        gameData["ptwosunderamount"] = pTwoSunderAmount
        gameData["ptwobullrush"] = pTwoBullrush
        gameData["ptwoheal"] = pTwoHeal
        gameData["ptwocripple"] = pTwoCripple
        gameData["ptworelentless"] = pTwoRelentless
        gameData["ptworelentlessdamage"] = pTwoRelentlessDamage
        gameData["ptwostoneskin"] = pTwoStoneskin
        gameData["ptwostonebonus"] = pTwoStonebonus
        gameData["ptwodeathsdoor"] = pTwoDeathsDoor
        gameData["ptwoquickdamage"] = pTwoQuickDamage
        gameData["ptwofeatinfo"] = pTwoFeatInfo
        gameData["ptwospentfeat"] = pTwoSpentFeat
        gameData["ptwoquick"] = pTwoQuick
        gameData["ptwovile"] = pTwoVile
        gameData["ptwoheavy"] = pTwoHeavy
        gameData["ptwoinner"] = pTwoInner
        gameData["ptwoexpose"] = pTwoExpose
        gameData["ptwocheapshot"] = pTwoCheapShot
        gameData["ptwolockout"] = pTwoLockout
        # XP AND LEVEL COUNTERS
        gameData["ponelevel"] = pOneLevel
        gameData["ptwolevel"] = pTwoLevel
        gameData["xp"] = xp
        gameData["currentplayerxp"] = currentPlayerXP
        gameData["nextlevel"] = nextLevel
        gameData["levelup"] = levelUp
        gameData["iddqd"] = iddqd
        gameData['bevasion'] = bEvasion
        gameData['bdeflect'] = bDeflect
        file.seek(0)
        file.write(json.dumps(gameData, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()


def featDict():
    # Open up the json object containing the list of feats.
    featFile = open("feats.json", "r", encoding="utf-8")
    featDictionary = json.load(featFile)
    featFile.close()

    # place all keys within a list for comparison later
    featList = []
    for keys in featDictionary[0]:
        featList.append(keys)
    return featDictionary, featList


def traitDict():
    from src.trait_repository import get_trait_dictionary_and_names
    return get_trait_dictionary_and_names()

# global note
# note = ""

class EchoBot(fchat.FChatClient):
    log_filter = ["PIN", "NLN", "FLN", "LIS", "STA", "VAR", "HLO", "CON", "FRL", "IGN", "ADL", "TPN", "LRP"]

    # STATUS COUNTERS
    counter = 0
    confirm = 0

    # Hopefully bullshit relic data
    # # STRINGS
    # opponent = ""
    # playerOne = ""
    # playerTwo = ""
    # winner = ""
    # quitter = ""
    # # PLAYER INFO
    # pOneInfo = {}
    # pTwoInfo = {}
    # # HP AND TURN COUNTERS
    # # challenge = 0
    # # reset = 0
    # featToken = 0
    # game = 0
    # count = 0
    # token = 0
    # critical = 0
    # bonusHurt = 0
    # nerveDamage = 0
    # totalDamage = 0
    # pOneTotalHP = 0
    # pTwoTotalHP = 0
    # pOneCurrentHP = 0
    # pTwoCurrentHP = 0
    # # PLAYER ONE FEAT COUNTERS
    # pOnepMod = 0
    # pOnecMod = 0
    # pOnedMod = 0
    # pOnemMod = 0
    # pOneEvade = 1
    # pOneDeflect = 1
    # pOneBullrush = 0
    # pOneHeal = 0
    # pOneStoneskin = 0
    # pOneStonebonus = 0
    # pOneDeathsDoor = 0
    # pOneQuickDamage = 0
    # pOneFeatInfo = None
    # pOneSpentFeat = []
    # pOneQuick = 0
    # pOneVile = 0
    # # PLAYER TWO FEAT COUNTERS
    # pTwopMod = 0
    # pTwocMod = 0
    # pTwodMod = 0
    # pTwomMod = 0
    # pTwoEvade = 1
    # pTwoDeflect = 1
    # pTwoBullrush = 0
    # pTwoHeal = 0
    # pTwoStoneskin = 0
    # pTwoStonebonus = 0
    # pTwoDeathsDoor = 0
    # pTwoQuickDamage = 0
    # pTwoFeatInfo = None
    # pTwoSpentFeat = []
    # pTwoQuick = 0
    # pTwoVile = 0
    # # XP AND LEVEL COUNTERS
    # pOneLevel = 0
    # pTwoLevel = 0
    # xp = 0
    # currentPlayerXP = 0
    # nextLevel = 0
    # levelUp = 0
    #
    # # Susanna added
    # bEvasion = False
    # bDeflect = False
    masterList = []

    # Auto-resets a challenge should a minute pass with no answer
    def challengeTimeOut(self):
        gameFiles = gamefiles()
        channel = "ADH-abfb9b6ebd20f1e7a693"
        super().MSG(unspoiledArena, "Challenge was not accepted. Challenge reset.")
        gameStatReset(channel)

    # Auto-resets a fight should an hour pass without any progress
    def combatTimeOut(self):
        try:
            self.gameTimer.cancel()
        except AttributeError:
            self.resumeTimer.cancel()
        super().PRI('Unspoiled Desire', "!confirm")



    # Join the chatroom
    def JCH(self, channel):
        super().JCH(channel)
        if channel == "ADH-8216a753c1ef08445052":
            super().PRI("Unspoiled Desire", "!status")

    def on_COL(self, channel, oplist):
        pass

    def on_ICH(self, users, channel, mode):
        if channel == unspoiledArena:
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 1:
                super().MSG(channel, "It looks like a game was preserved with " + pOneInfo['name'] + " and " +
                          pTwoInfo['name'] + " Before system's failed. Either of you have 10 minutes to type !resume to "
                          "resume match, or it will be purged.")
                self.confirm = 1
                resumetimeout = 600
                self.resumeTimer = Timer(resumetimeout, self.combatTimeOut)
                self.resumeTimer.start()
        if channel == unspoiledBarOOC:
            self.masterList = message_8_compile(users)
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            for character in self.masterList:
                charSheet = Path(charFolder + character.lower() + ".json")
                if charSheet.is_file():
                    with open(charFolder + character.lower() + '.json', 'r+') as file:
                        pInfo = json.load(file)
                        pInfo['statuscounter'] = 0
                        file.seek(0)
                        file.write(json.dumps(pInfo, ensure_ascii=False, indent=2))
                        file.truncate()
                        file.close()

    def on_JCH(self, character, channel, title):
        if character not in self.masterList and channel == unspoiledBarOOC:
            self.masterList.append(character)

    def on_LCH(self, channel, character):
        if character in self.masterList and channel == unspoiledBarOOC:
            self.masterList.remove(character)
            # path = os.getcwd()
            # charFolder = os.path.join(path + "/characters/")
            # charSheet = Path(charFolder + character.lower() + ".json")
            # if charSheet.is_file():
            #     with open(charFolder + character.lower() + '.json', 'r+') as file:
            #         pInfo = json.load(file)
            #         if self.counter == 24:
            #             pInfo['status']

    def on_FLN(self, character):
        if character in self.masterList:
            self.masterList.remove(character)
            # path = os.getcwd()
            # charFolder = os.path.join(path + "/characters/")
            # charSheet = Path(charFolder + character.lower() + ".json")
            # if charSheet.is_file():
            #     with open(charFolder + character.lower() + '.json', 'r+') as file:
            #         pInfo = json.load(file)
            #         if self.counter == 24:
            #             pInfo['status'] = ""
            #             file.seek(0)
            #             file.write(json.dumps(pInfo, ensure_ascii=False, indent=2))
            #             file.truncate()
            #             file.close()

    def on_STA(self, status, character, statusmsg):
        if character in self.masterList:
            status_compile(character, statusmsg, self.masterList)

    def statusTimer(self):
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")

        self.counter, renown_profiles = apply_passive_status_timer_tick(
            self.masterList,
            self.counter,
            charFolder,
        )

        for character in renown_profiles:
            print("Gave " + character.lower() + " 10 renown.")

        print(self.counter)
        super().PRI("Unspoiled Desire", "!status")

    # function dedicated to sending public messages to the chatroom
    def on_MSG(self, character, message, channel):
        super().on_MSG(character, message, channel)

        file = open("room.json", "r", encoding="utf-8")
        room = json.load(file)
        file.close()

        unspoiledBar = room['unspoiledIC']
        unspoiledArena = room['unspoiledArena']
        unspoiledBarOOC = room['unspoiledOOC']
        thePhotoPub = room['thePhotoPub']
        setWelcome = room['setWelcome']
        pubModerators = ["Mimi Halliwell", "Mordecai", "Sakura Barnes", "Seann Mac Bowe", "Mark Halliwell",
                         "Crimson Hourglass", "Eion OClair", "Sgt James Barnes"]

        # put in variables to grab the location of all character sheets. It's gonna be used a lot.
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + character.lower() + ".json")

#------------------------------------------------MISC COMMANDS----------------------------------------------------------
        #     if message[:7] == "!photo":
        #         super().MSG(unspoiledBarOOC, "[session=The Photo Pub]adh-b2a35a8f84b81b45834a[/session]")

#         if channel != unspoiledBarOOC:
#             super().MSG(channel, "This command can only be used in the OOC room")
#         else:
#             super().MSG(unspoiledBarOOC, "Welcome to Unspoiled Desire! To get started, just type !name <name>, where"
#                                          " <name> is your character name! If you need any help at all, don't hesitate"
#                                          " to ask!")

        if (message[:10] == "!sellarmor"
            or message[:9] == "!buyarmor"
            or message[:9] == "!buyarmor"
            or message[:10] == "!armorname"
            or message[:6] == "!equip"
            or message[:8] == "!unequip"
            or message[:10] == "!buypotion"
            or message[:10] == "!usepotion"
            or message[:11] == "!givepotion"
            or message[:11] == "!sellpotion"
            or message == "!potionshop"
            or message == "!armorshop"):
                if channel in unspoiledRooms:
                    super().MSG(channel, "Please use this command in PMs with Unspoiled Desire" )

 #-----------------------------------------------RENOWN COMMANDS--------------------------------------------------------
        #!giverenown <number> <person>
        if message[:11] == "!giverenown":
            words = message.split()
            words.remove(words[0])
            try:
                renown = int(words[0])
                if renown < 0:
                    super().MSG(channel, "You can't give someone negative renown")
                else:
                    words.remove(words[0])
                    gifted = " ".join(words)
                    if character.lower() == gifted.lower():
                        super().MSG(channel, "You can't give renown to yourself")
                    else:
                        path = os.getcwd()
                        charFolder = os.path.join(path + "/characters/")
                        msg = message_11_giverenown(character, channel, unspoiledBarOOC, renown, gifted, charFolder)
                        super().MSG(channel, msg)
                        super().PRI("An Entity", msg)
            except ValueError:
                super().PRI(character, "Please make sure the format is as follows: !giverenown"
                                       " [color=yellow]<amount>[/color] [color=pink] "
                                       "<profile name>[/color]. Example: !giverenown 100 an entity")

#-----------------------------------------------COMBAT COMMANDS---------------------------------------------------------

        # Initiate a challenge to the room. Opponent is whoever uses the !accept command. This command should be
        # unavailable for use the moment someone !accepts, to ensure no one trolls during a fight.
        if message[:10] == "!challenge":
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            opponent = message[11:].lower()
            charSheet = Path(charFolder + opponent + ".json")
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 1 or game == 0.5:
                super().MSG(channel, "A game is already taking place, wait your turn.")
            elif not charSheet.is_file():
                super().MSG(channel, opponent + " doesn't have a character made for you to fight.")
            else:
                msg, opponent, pOneInfo, new_game, bTimer, playerOne, update = \
                    message_10_challenge(channel, charFolder, message, unspoiledArena, character, game)
                # if opponent is not "":
                #     opponent = opponent
                if pOneInfo is not None:
                    # pOneInfo = pOneInfo
                    pOneTotalHP = pOneInfo['thp']
                    pOneCurrentHP = pOneInfo['thp']
                    pOneLevel = pOneInfo['level']
                if new_game != 0:
                    game = new_game
                if bTimer is True:
                    timeout = 60
                    self.timer = Timer(timeout, self.challengeTimeOut)
                    self.timer.start()
                # if playerOne is not "":
                #     playerOne = playerOne
                super().MSG(channel, msg)
                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,
                                 pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush, pOneHeal,
                                 pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin, pOneStonebonus,
                                 pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pOneQuick, pOneVile,
                                 pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod,
                                 pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount,
                                 pTwoBullrush, pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage,
                                 pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo,
                                 pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose,
                                 pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP,
                                 nextLevel, levelUp, iddqd, bEvasion, bDeflect, channel)

        # Response to use to accept a challenge.
        if message == "!accept":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 1:
                super().MSG(channel, "A fight is already taking place. Wait your turn.")
            else:
                msg, pTwoInfo, new_game, playerTwo, bTimer, bGameTimer, new_oppenent, token, update =\
                    message_accept(channel, charFolder, unspoiledArena, character, game, opponent, pOneInfo)
                if not charFile.is_file():
                    super().MSG(channel, "You don't even have a character made to fight.")
                else:
                    if new_game is not None:
                        game = new_game
                    if pTwoInfo is not None:
                        #pTwoInfo = pTwoInfo
                        pTwoTotalHP = pTwoInfo['thp']
                        pTwoCurrentHP = pTwoInfo['thp']
                        pTwoLevel = pTwoInfo['level']
                    if bTimer:
                        self.timer.cancel()
                    if bGameTimer:
                        gametimeout = 3600
                        self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                        self.gameTimer.start()
                    if new_oppenent is not None:
                        opponent = new_oppenent
                    # if playerTwo is not None:
                    #     playerTwo = playerTwo
                    # if token is not None:
                    #     token = token
                    separator = '\n'
                    report = separator.join(msg)
                    super().MSG(channel,report)
                    if update:
                        gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                     game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                     pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                     pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                     pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                     pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                     pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                     pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                     pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                     pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                     pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                     pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                     pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                     bEvasion, bDeflect, channel)
                    # for msg_item in msg:
                    #     super().MSG(channel, msg_item)
                    try:
                        super().MSG(unspoiledBarOOC, "A fight between " + pOneInfo['name'].title() + " and " +
                                    pTwoInfo['name'].title() + " is taking place in the Arena: "
                                    "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
                        super().MSG(unspoiledBar, "A fight between " + pOneInfo['name'].title() + " and " +
                                    pTwoInfo['name'].title() + " is taking place in the Arena: "
                                    "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
                        super().MSG(thePhotoPub, "A fight between " + pOneInfo['name'].title() + " and " +
                                    pTwoInfo['name'].title() + " is taking place in the Arena: "
                                    "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
                    except KeyError:
                        pass

        # command to forgo using deflect/evasion that turn
        if message[:5] == "!pass":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if character.lower() != playerOne and character.lower() != playerTwo:
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count,\
                    token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,\
                    pOneCurrentHP, pTwoCurrentHP, pOneFeatInfo, pTwoFeatInfo, pOnepMod, pOnecMod, pOnedMod, pOnemMod,\
                    pOneQuickDamage, pTwoQuickDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple,\
                    pOneRelentless, pOneRelentlessDamage, pOneBullRush, pTwoBullrush, pTwoHeal, pTwoCripple,\
                    pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneVile,\
                    pTwoVile, pOneInner, pTwoInner, pOneExpose, pTwoExpose, iddqd, update =\
                    message_5_pass(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo,
                                   featToken, count, token, critical, bonusHurt, totalDamage, pOneTotalHP,
                                   pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOneFeatInfo, pTwoFeatInfo, pOnepMod,
                                   pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, pOneDeathsDoor,
                                   pTwoDeathsDoor, pOneHeal, pOneCriple, pOneRelentless, pOneRelentlessDamage,
                                   pOneBullrush, pTwoBullrush, pTwoHeal, pTwoCripple, pTwoRelentless,
                                   pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneVile, pTwoVile,
                                   pOneInner, pTwoInner, pOneExpose, pTwoExpose, iddqd)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel, report)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)
                if bGameTimer:
                    gametimeout = 3600
                    gameTimer = Timer(gametimeout, self.combatTimeOut)
                    gameTimer.start()

                if bEvasion is True:
                    bEvasion = False
                if bDeflect is True:
                    bDeflect = False

                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)
        # command ot use evasion feat
        if message[:8] == "!evasion":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if character.lower() != playerOne and character.lower() != playerTwo:
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count, token, critical,\
                bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOneFeatInfo,\
                pTwoFeatInfo, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage,\
                pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,\
                pOneBullRush, pTwoBullrush, pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage,\
                pOneStoneskin, pTwoStoneskin, pOneVile, pTwoVile, pOneInner, pTwoInner, pOneExpose, pTwoExpose,\
                iddqd, update =\
                    message_8_evasion(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo,
                                      featToken, count, token, critical, bonusHurt, totalDamage, pOneTotalHP,
                                      pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOneFeatInfo, pTwoFeatInfo,
                                      pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage,
                                      pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCriple, pOneRelentless,
                                      pOneRelentlessDamage, pOneBullrush, pTwoBullrush, pTwoHeal, pTwoCripple,
                                      pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin,
                                      pOneVile, pTwoVile, pOneInner, pTwoInner, pOneExpose, pTwoExpose, iddqd)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel, report)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)
                if bGameTimer:
                    gametimeout = 3600
                    self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                    self.gameTimer.start()
                if bEvasion is True:
                    bEvasion = False
                if bDeflect is True:
                    bDeflect = False

                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)
        # command to use deflect feat
        # if message[:8] == "!deflect":
        #    msg, bGameTimer, self.playerOne, self.playerTwo, self.pOneInfo, self.pTwoInfo, self.featToken, self.count,\
        #    self.token, self.totalDamage, self.pOneTotalHP, self.pTwoTotalHP, self.pOneCurrentHP, self.pTwoCurrentHP,\
        #    self.pOnepMod, self.pOnecMod, self.pOnedMod, self.pOnemMod, self.pOneQuickDamage, self.pTwoQuickDamage,\
        #    self.pTwoDeflect, self.pOneDeflect, self.pOneDeathsDoor, self.pTwoDeathsDoor =\
        #        message_8_deflect(character, channel, unspoiledArena, self.playerOne, self.playerTwo, self.pOneInfo,
        #                          self.pTwoInfo, self.featToken, self.count, self.token, self.critical, self.bonusHurt,
        #                          self.totalDamage, self.pOneTotalHP, self.pTwoTotalHP, self.pOneCurrentHP,
        #                          self.pTwoCurrentHP, self.pOnepMod, self.pOnecMod, self.pOnedMod, self.pOnemMod,
        #                          self.pOneQuickDamage, self.pTwoQuickDamage, self.pTwoDeflect, self.pOneDeflect,
        #                          self.pOneDeathsDoor, self.pTwoDeathsDoor)
        #    for msg_item in msg:
        #        super().MSG(channel, msg_item)
        #    if bGameTimer:
        #        gametimeout = 3600
        #        self.gameTimer = Timer(gametimeout, self.combatTimeOut)
        #        self.gameTimer.start()
        #    if self.bDeflect is True:
        #        self.bDeflect = False
        #    if self.bEvasion is True:
        #        self.bEvasion = False

        if message == "!resume":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if channel == unspoiledArena and (character.lower() == playerOne or character.lower() == playerTwo):
                self.resumeTimer.cancel()
                bGameTimer = True
                if bGameTimer:
                    gametimeout = 3600
                    self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                    self.gameTimer.start()
                if token == 1:
                    super().MSG(channel, "The fight has been resumed. It is " + pOneInfo['name'] + "'s turn.")
                else:
                    super().MSG(channel, "The fight has been resumed. It is " + pTwoInfo['name'] + "'s turn.")
                # try:
                #     super().MSG(unspoiledBarOOC, "A fight between " + pOneInfo['name'].title() + " and " +
                #                 pTwoInfo['name'].title() + " has resumed in the Arena: "
                #                 "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
                #     super().MSG(unspoiledBar, "A fight between " + pOneInfo['name'].title() + " and " +
                #                 pTwoInfo['name'].title() + " has resumed in the Arena: "
                #                 "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
                #     super().MSG(thePhotoPub, "A fight between " + pOneInfo['name'].title() + " and " +
                #                 pTwoInfo['name'].title() + " has resumed in the Arena: "
                #                 "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
                # except KeyError:
                #     pass
            elif channel != unspoiledArena:
                super().MSG(channel, "This Command can only be used in "
                                    "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]")
            else:
                super().MSG(channel, "You aren't one of the combatants in the fight being preserved.")
        # Option to forfeit a fight.

        if message == "!forfeit":
            # playerOne = self.playerOne
            # playerTwo = self.playerTwo
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if channel == unspoiledArena:
                # if self.game == 1:
                if character.lower() != playerOne and character.lower() != playerTwo:
                    super().MSG(channel, "So the fact that you even thought to try this, makes me think you are a"
                                         " bad person, trying to grief a game. Not funny in the slightest. "
                                         "This has been noted")
                if game == 1:
                    if character.lower() == playerOne or character.lower() == playerTwo:
                        oneFile = open(charFolder + playerOne + ".json", "r", encoding="utf-8")
                        pOneInfo = json.load(oneFile)
                        oneFile.close()
                        twoFile = open(charFolder + playerTwo + ".json", "r", encoding="utf-8")
                        pTwoInfo = json.load(twoFile)
                        twoFile.close()
                        if character.lower() == playerOne:
                            super().MSG(unspoiledArena, pOneInfo['name'] +
                                        " has forfeited the match, and obtains no reward.")
                            xpCap = pTwoInfo['nextlevel'] - 10
                            forfeit = pOneInfo['forfeits'] + 1
                            if pTwoInfo['currentxp'] < xpCap:
                                super().MSG(unspoiledArena, pTwoInfo['name'] + " has earned 10xp")
                                xp = pTwoInfo['currentxp'] + 10
                                with open(charFolder + playerTwo.lower() + '.json', 'r+') as file:
                                    charData = json.load(file)
                                    pTwoInfo['currentxp'] = xp
                                    file.seek(0)
                                    file.write(json.dumps(pTwoInfo, ensure_ascii=False, indent=2))
                                    file.truncate()
                                    file.close()
                            else:
                                super().MSG(unspoiledArena, pTwoInfo['name'] + " has earned 0xp")
                            with open(charFolder + playerOne.lower() + '.json.', 'r+') as file:
                                charData = json.load(file)
                                pOneInfo['forfeits'] = forfeit
                                file.seek(0)
                                file.write(json.dumps(pOneInfo, ensure_ascii=False, indent=2))
                                file.truncate()
                                file.close()
                        elif character.lower() == playerTwo:
                            super().MSG(unspoiledArena, pTwoInfo['name'] +
                                        " has forfeited the match, and obtains no reward.")
                            xpCap = pOneInfo['nextlevel'] - 10
                            forfeit = pTwoInfo['forfeits'] + 1
                            if pOneInfo['currentxp'] < xpCap:
                                super().MSG(unspoiledArena, pOneInfo['name'] + " has earned 10xp")
                                xp = pOneInfo['currentxp'] + 10
                                with open(charFolder + playerOne.lower() + '.json', 'r+') as file:
                                    charData = json.load(file)
                                    pOneInfo['currentxp'] = xp
                                    file.seek(0)
                                    file.write(json.dumps(pOneInfo, ensure_ascii=False, indent=2))
                                    file.truncate()
                                    file.close()
                            else:
                                super().MSG(unspoiledArena, pOneInfo['name'] + " has earned 0xp")
                            with open(charFolder + playerTwo.lower() + '.json.', 'r+') as file:
                                charData = json.load(file)
                                pTwoInfo['forfeits'] = forfeit
                                file.seek(0)
                                file.write(json.dumps(pTwoInfo, ensure_ascii=False, indent=2))
                                file.truncate()
                                file.close()
                        gameStatReset(channel)
                        # self.opponent = ""
                        # self.playerOne = ""
                        # self.playerTwo = ""
                        # self.winner = ""
                        # self.loser = ""
                        # self.pOneUsername = None
                        # self.pTwoUsername = None
                        # # PLAYER INFO
                        # self.pOneInfo = {}
                        # self.pTwoInfo = {}
                        # # HP AND TURN COUNTERS
                        # self.gameTimer.cancel()
                        # self.gameTimer = 0
                        # self.count = 0
                        # self.base = 0
                        # self.token = 0
                        # self.game = 0
                        # self.critical = 0
                        # self.bonusHurt = 0
                        # self.nerveDamage = 0
                        # self.totalDamage = 0
                        # self.pOneTotalHP = 0
                        # self.pTwoTotalHP = 0
                        # self.pOneCurrentHP = 0
                        # self.pTwoCurrentHP = 0
                        # # PLAYER ONE FEAT COUNTERS
                        # self.pOnepMod = 0
                        # self.pOnecMod = 0
                        # self.pOnedMod = 0
                        # self.pOnemMod = 0
                        # self.pOneEvade = 1
                        # self.pOneDeflect = 1
                        # self.pOneBullrush = 0
                        # self.pOneHeal = 0
                        # self.pOneStoneskin = 0
                        # self.pOneStonebonus = 0
                        # self.pOneDeathsDoor = 0
                        # self.pOneQuickDamage = 0
                        # self.pOneVile = 0
                        # self.pOneFeatInfo = None
                        # self.pOneSpentFeat = []
                        # # PLAYER TWO FEAT COUNTERS
                        # self.pTwopMod = 0
                        # self.pTwocMod = 0
                        # self.pTwodMod = 0
                        # self.pTwomMod = 0
                        # self.pTwoEvade = 1
                        # self.pTwoDeflect = 1
                        # self.pTwoBullrush = 0
                        # self.pTwoHeal = 0
                        # self.pTwoStoneskin = 0
                        # self.pTwoStonebonus = 0
                        # self.pTwoDeathsDoor = 0
                        # self.pTwoQuickDamage = 0
                        # self.pTwoVile = 0
                        # self.pTwoFeatInfo = None
                        # self.pTwoSpentFeat = []
                        # # XP AND LEVEL COUNTERS
                        # self.pOneLevel = 0
                        # self.pTwoLevel = 0
                        # self.xp = 0
                        # self.currentPlayerXP = 0
                        # self.nextLevel = 0
                        # self.levelUp = 0
                        # bEvasion = False
                        # bDeflect = False

                        super().MSG(unspoiledArena, "Seems like one of the fighters disappeared. Show's over folks."
                                                    " (Resetting Match Status)")
                else:
                    super().MSG(unspoiledArena, "What are you running from? There isn't even a fight taking place that"
                                " you are involved in.")

        # !usefeat <feat name> command that can be used before !roll command. Used to...well...use a feat.
        if message[:8] == "!usefeat":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            print("pOneLockout: " + str(pOneLockout))
            print("pTwoLockout: " + str(pTwoLockout))
            print("token " + str(token))
            if (character.lower() != playerOne and token == 1)\
                    or (character.lower() != playerTwo and token == 2):
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                if pTwoCheapShot != 0 and pTwoLockout != 0 and token == 1:
                    super().MSG(channel, pTwoInfo['name'] + "'s [color=yellow]cheap shot[/color] has prevented them"
                                                            "from using a feat this round.")
                    update = True
                elif pOneCheapShot != 0 and pOneLockout != 0 and token == 2:
                    super().MSG(channel, pOneInfo['name'] + "'s [color=yellow]cheap shot[/color] has prevented them"
                                                            "from using a feat this round.")
                    update = True
                else:
                    msg, featToken_new, pOneLastFeat, pOneFeatInfo, pTwoLastFeat, pTwoFeatInfo, update =\
                        message_8_usefeat(channel, charFolder, message, unspoiledArena, character, game, playerOne,
                                          playerTwo, token, featToken, pOneInfo, pOneSpentFeat,
                                          pTwoSpentFeat, pTwoInfo)
                    separator = '\n'
                    report = separator.join(msg)
                    super().MSG(channel, report)
                    # for msg_item in msg:
                    #     super().MSG(channel, msg_item)
                    if featToken_new is not None:
                        featToken = featToken_new
                    if pOneLastFeat is not None:
                        pOneSpentFeat.append(pOneLastFeat)
                    # if pOneFeatInfo is not None:
                    #     pOneFeatInfo = pOneFeatInfo
                    if pTwoLastFeat is not None:
                        pTwoSpentFeat.append(pTwoLastFeat)
                    # if pTwoFeatInfo is not None:
                    #     pTwoFeatInfo = pTwoFeatInfo
                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)

        # command to make an attack.
        if message == "!roll":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if (character.lower() != playerOne and token == 1)\
                    or (character.lower() != playerTwo and token == 2):
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                if game == 1:
                    self.gameTimer.cancel()
                msg, bEvasion, bDeflect, bGameTimer, opponent, playerOne, playerTwo, winner, pOneInfo, pTwoInfo,\
                featToken, game, count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,\
                pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect,\
                pOneSunder, pOneSunderAmount, pOneBullrush, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, pTwopMod,\
                pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush,\
                pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel,\
                levelUp, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,\
                pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin,\
                pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile, pOneQuick, pTwoQuick, pOneHeavy, pTwoHeavy,\
                pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot, pOneLockout, pTwoCheapShot,\
                pTwoLockout, iddqd, update =\
                    message_roll(character, message, channel, unspoiledArena, charFolder, opponent, playerOne,
                                 playerTwo, winner, pOneInfo, pTwoInfo, featToken, game, count, token, critical,
                                 bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP,
                                 pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder,
                                 pOneSunderAmount, pOneBullrush, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder,
                                 pTwoSunderAmount, pTwoBullrush, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, pOneDeathsDoor,
                                 pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,
                                 pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin,
                                 pTwoStoneskin, pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile, pOneQuick,
                                 pTwoQuick, pOneHeavy, pTwoHeavy, pOneInner, pTwoInner, pOneExpose, pTwoExpose,
                                 pOneCheapShot, pOneLockout, pTwoCheapShot, pTwoLockout, iddqd)
                print(playerOne, playerTwo)
                separator = '\n'
                report = separator.join(msg)
                print(report)
                super().MSG(channel,report)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)
                if bGameTimer:
                    gametimeout = 3600
                    self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                    self.gameTimer.start()
                    if update:
                        gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                     game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                     pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                     pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                     pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                     pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                     pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                     pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                     pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                     pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                     pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                     pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                     pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                     bEvasion, bDeflect, channel)
                elif bGameTimer is False:
                    gameStatReset(channel)
                # except AttributeError:
                #     super().MSG(channel, "Either a fight is not taking place, or it isn't your turn.")

        # command to forgo first strike.
        if message == "!skip":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if character.lower() != playerOne and character.lower() != playerTwo:
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg, count, token, bGameTimer, update = message_4_skip(character, channel, unspoiledArena, playerOne, playerTwo,
                                                               pOneInfo, pTwoInfo, count, token, pOneTotalHP,
                                                               pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel, report)
                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)

        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels. !pattack <number from 1-5>
        if message[:8] == "!pattack":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if character.lower() != playerOne and character.lower() != playerTwo:
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel, update =\
                    message_8_pattack(character, channel, unspoiledArena, message, game, playerOne, playerTwo, pOneInfo,
                                      pTwoInfo, token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel, report)

                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)

        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels. !dfight <number from 1-5>
        if message[:7] == "!dfight":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if character.lower() != playerOne and character.lower() != playerTwo:
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel, update =\
                    message_8_dfight(character, channel, unspoiledArena, message, game, playerOne, playerTwo, pOneInfo,
                                     pTwoInfo, token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel, report)

                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)

        # Allows for the use of the 'defensive fighting' passive feat. Makes sure it applies correct bonuses for correct
        # levels.
        # if message[:8] == "!cexpert":
        #     msg, self.game, self.playerOne, self.playerTwo, self.pOneInfo, self.pTwoInfo, self.token, self.pOnecMod,
        #       self.pTwocMod, self.pOneLevel, self.pTwoLevel =
        #       message_8_cexpert(character, channel, unspoiledArena, message, self.game, self.playerOne,
        #                           self.playerTwo, self.pOneInfo, self.pTwoInfo, self.token, self.pOnecMod,
        #                           self.pTwocMod, self.pOneLevel, self.pTwoLevel)
        #     for msg_item in msg:
        #         super().MSG(channel, msg_item)

        # Allows for the use of the 'masochist' passive feat. Makes sure it applies correct bonuses for correct
        # levels. !masochist <number from 1-5>
        if message[:10] == "!masochist":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,\
            bEvasion, bDeflect = gameStatLoad(channel)
            if character.lower() != playerOne and character.lower() != playerTwo:
                super().MSG(channel, "Either it is not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnemMod, pTwomMod, pOneLevel,\
                pTwoLevel, update = message_10_masochist(character, channel, unspoiledArena, message, game,
                                                         playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnemMod,
                                                         pTwomMod, pOneLevel, pTwoLevel)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel, report)
                if update:
                    gameStatDump(opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken,
                                 game, count, token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP,
                                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod,
                                 pOnemMod, pOneEvade, pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush,
                                 pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneStoneskin,
                                 pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                                 pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot,
                                 pOneLockout, pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect,
                                 pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, pTwoCripple,
                                 pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus,
                                 pTwoDeathsDoor, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick,
                                 pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, pTwoCheapShot, pTwoLockout,
                                 pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd,
                                 bEvasion, bDeflect, channel)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)

#------------------------------------------------NON-COMBAT COMMANDS----------------------------------------------------

        """ useless joke commands
        if message[:5] == "!kill":
            msg = message_5_kill(channel, unspoiledBarOOC, character, message)
            super().MSG(channel, msg)

        if message[:7] == "!detect":
            msg = message_7_detect(channel, unspoiledBarOOC, character, message)
            super().MSG(channel, msg)
        """

        if message[:5] == "!bell":
            msg = message_5_bell(channel, unspoiledBarOOC, character, message)
            super().MSG(channel, msg)

        # !leaderboard win - Displays the top five people with most wins
        # !leaderboard lose - Displays the top five people with most loses
        # !leaderboard percent - Displays the top five people with highest percentage
        # !leaderboard - Displays '!leaderboard win' by default
        if message[:12] == "!leaderboard":
            msg = message_12_leaderboard(channel, charFolder, unspoiledBarOOC, message)
            # super().MSG(channel, "This is working.")
            separator = '\n'
            report = separator.join(msg)
            super().MSG(channel, report)
            # for msg_item in msg:
            #     super().MSG(channel, msg_item)

        # !who <profile name> Allows the user to find a profile name's character and level
        if message[:4] == "!who":
            msg = message_4_who(channel, charFolder, unspoiledBarOOC, message)
            separator = '\n'
            report = separator.join(msg)
            super().MSG(channel, report)
            # for msg_item in msg:
            #     super().MSG(channel, msg_item)

        # !player <profile name> Allows the user to broadcast another player's win/loss rate to the chat
        # if message[:7] == "!player":
        #    msg = message_7_player(channel, charFolder, unspoiledBarOOC, message)
        #    super().MSG(channel, msg)

        # Tell user to PM bot when creating stats
        if message[:6] == "!stats":
            if charFile.is_file():
                super().MSG(channel, "Well that's not good. Now everyone knows. PM me with"
                            " '!stats <str> <dex> <con>' to set your"
                            " abilities.")
            else:
                super().MSG(channel, "You don't even have a character created yet.")

        # !name <character name> Get the name of character being created
        if message[:5] == "!name":
            # make sure that this command cannot be ran if a fight is taking place.
            if channel == unspoiledBarOOC:
                super().MSG(channel, "[color=red]Note:[/color] The fight bot is live, but it's also still new, Bugs"
                                     " still exist. If bot crashes, have patience, one of the developers will get to "
                                     "it.")
                super().MSG(channel, "Sometimes major changes occur. [color=green][b]Please bookmark my profile "
                                     "name,[/b][/color] to see any [color=yellow][b]major updates[/b][/color] "
                                     "concerning the game, as they will be [color=green][b]updated in the profile"
                                     "[/b][/color]. Thanks!")
                msg = message_5_name(channel, charFolder, message, charFile, character)
                separator = '\n'
                report = separator.join(msg)
                super().MSG(channel,report)
                # for msg_item in msg:
                #     super().MSG(channel, msg_item)
            else:
               super().MSG(channel, "This Command can only be used in "
                                    "[session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]")

        # erase player character
        if message[:6] == "!erase":
            if channel == unspoiledBarOOC:
                self.quitter = character.lower()
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                charFile = Path(charFolder + self.quitter + ".json")
                try:
                    charSheet = open(charFolder + self.quitter + ".json", "r", encoding="utf-8")
                    pInfo = json.load(charSheet)
                    charSheet.close()
                    super().MSG(channel, "Are you sure you want to delete " + pInfo['name'] +
                                "? (Type [color=pink]!confirm[/color]"
                                " to do the deed, or [color=pink]!deny[/color] to save a life.)")
                except FileNotFoundError:
                    super().MSG(channel, "You don't have a character to delete.")
            else:
                super().MSG(channel, "This Command can only be used in "
                                   "[session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]")

        # confirm delection of a character. Used after invoking the '!erase' command
        if message[:8] == "!confirm":
            if channel == unspoiledBarOOC:
                if self.quitter == "":
                    pass
                elif character.lower() == self.quitter:
                    msg = message_7_erase(character)
                    super().MSG(channel, msg)
                    self.quitter = ""
                else:
                    super().MSG(channel, "You aren't " + self.quitter + ", not cool.")
            else:
                super().MSG(channel, "This Command can only be used in"
                                   " [session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]")

        # deny deletion of a character. Used after invoking the '!erase' command
        if message[:5] == "!deny":
            if channel == unspoiledBarOOC:
                if self.quitter == "":
                    pass
                elif character.lower() == self.quitter:
                    super().MSG(channel, "Yay.")
                    self.quitter = ""
                else:
                    super().MSG(channel, "You aren't " + self.quitter + ", not cool.")
            else:
                super.MSG(channel, "This Command can only be used in "
                                   "[session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]")


    def on_PRI(self, character, message):
        super().on_PRI(character, message)
        file = open("exiled.json", "r", encoding="utf-8")
        exiled = json.load(file)
        file.close()
        myCharacters = ["Unspoiled Desire", "An Entity", "Their Perfect Doll", "Vhissilka"]
        myModerators = ["Unspoiled Desire", "An Entity", "Their Perfect Doll", "Vhissilka",
                        "Mark Halliwell", "Sylzana", "Riley_Tassinari", "Mayank", "Unspoiled Assistant"]

        # Default message if no command giving after '!'
        if character in exiled:
            super().PRI(character, "Sorry, but records indicate that you have been banned. If you wish to contact The "
                                   "Devs, please send a note to this profile name. Thanks!")
        elif message[:1] == "~":
            note = character + ": " + message
            pri_discord_echo(note)
            super().PRI("An Entity", note)
            super().PRI("Unspoiled Assistant", note)
        elif message[:1] != "!":
            if character != "Unspoiled Desire":
                super().PRI(character, "I see you are trying to PM me something that [i]isn't[/i] a command."
                                       "As I am just a bot, I'm not going to be able to give a meaningful answer to "
                                       "your inquiry. If you wish to get in contact with one of my developers, please "
                                       "respond here with a '~' before your message (Example: ~ Hi, UD's developers!), "
                                       "and I am sure they will get back to you as soon as they are able.")

        if message[:11] == "!setwelcome" and character == "Mimi Halliwell":
            with open('room.json', 'r+') as file:
                setWelcome = json.load(file)
                setWelcome['setWelcome'] = message[12:]
                file.seek(0)
                file.write(json.dumps(setWelcome, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()
            super().PRI(character, "Message Set!")

#--------------------------------------------------------DEVELOPER COMMANDS---------------------------------------------
        channel = "ADH-abfb9b6ebd20f1e7a693"
        # Make person a moderator
        if message[:8] == "!promote":
            if character in myCharacters:
                person = message[9:]
                super().COA(unspoiledBarOOC, person)
                super().COA(unspoiledBar, person)
                super().COA(unspoiledArena, person)

        # Remove person as moderator
        if message[:7] == "!demote":
            if character in myCharacters:
                person = message[8:]
                super().COR(unspoiledBarOOC, person)
                super().COR(unspoiledBar, person)
                super().COR(unspoiledArena, person)

        # change the description of the bar
        if message[:8] == "!descbar":
            if character in myCharacters:
                description = message[9:]
                super().CDS(unspoiledBar, description)
                super().MSG(unspoiledBar, "/warn Hey. That description tab at the top of the channel? The one no "
                                             "one bothers to look at? Yea, it's just been updated.")

        # change the description of the OoC room
        if message[:8] == "!descooc":
            if character in myCharacters:
                description = message[9:]
                super().CDS(unspoiledBarOOC, description)
                super().MSG(unspoiledBarOOC, "/warn Hey. That description tab at the top of the channel? The one no "
                                             "one bothers to look at? Yea, it's just been updated.")

        # change the description of the arena
        if message[:10] == "!descarena":
            if character in myCharacters:
                description = message[11:]
                super().CDS(unspoiledArena, description)
                super().MSG(unspoiledArena, "/warn Hey. That description tab at the top of the channel? The one no "
                                             "one bothers to look at? Yea, it's just been updated.")

        # restock armor
        if message == "!stockarmor":
            if character in myCharacters:
                catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList, catTwoUncommonList, \
                    catTwoRareList, catThreeCommonList, catThreeUncommonList, catThreeRareList = pri_armor_shop_lists()
                msg = pri_11_stockarmor(catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList,
                                        catTwoUncommonList, catTwoRareList, catThreeCommonList,
                                        catThreeUncommonList, catThreeRareList)
                super().PRI(character, msg)
            else:
                super().PRI(character, "You don't have permission to use this command.")

        # restock potions
        if message == "!stockpotion":
            if character in myCharacters:
                commonList, uncommonList, rareList, vrareList, relicList = pri_potion_shop_lists()
                msg, shopList = pri_10_stockpotion(commonList, uncommonList, rareList, vrareList, relicList)
                super().PRI(character, msg)
            else:
                super().PRI(character, "You don't have permission to use this command.")

        # command to talk inside the bar under bot
        if message[:4] == "!bar":
            if character in myCharacters:
                statement = message[5:]
                super().MSG(unspoiledBar, statement)
            else:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")

        # command to talk inside the arena under bot
        if message[:6] == "!arena":
            if character in myCharacters:
                statement = message[7:]
                super().MSG(unspoiledArena, statement)
            else:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")

        # command to talk inside the OoC room under bot
        if message[:4] == "!ooc":
            if character in myCharacters:
                statement = message[5:]
                super().MSG(unspoiledBarOOC, statement)
            else:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")

        # command to PM people under bot
        # !converse <target> - <message>
        if message[:9] == "!converse":
            try:
                if character in myCharacters:
                    words = message[10:].split(" ` ")
                    target = words[0]
                    script = words[1]
                    super().PRI(target, script)
                else:
                    super().PRI(character,
                                "So either you found the git holding this bot code, a manager made a poor life "
                                "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                                "you are getting.")
            except:
                super().PRI(character, "This didn't seem to work for some reason. Make sure you are using command "
                                       "in th proper format: !converse <profile name> ` <message>")

        # command to reward those advertising the room
        if message == "!status":
            if character in myCharacters:
                timeout = 3600
                self.timer = Timer(timeout, self.statusTimer)
                self.timer.start()
            else:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")

        # command to pay registered characters
        if message == "!globalrenown":
            if character in myCharacters:
                profile = []
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                with open(charFolder + "playerDatabase.json", 'r', encoding="utf-8") as file2:
                    playerDatabase = json.loads(file2.read())
                    file2.close()
                for item in playerDatabase.items():
                    name = item[1]
                    profile.append(name)
                for player in profile:
                    with open(charFolder + player + ".json", "r+", encoding="utf-8") as file:
                        charData = json.load(file)
                        file.close()
                        level = charData['level']
                        if charData['fight'] >= 2:
                            renown = level * 125
                            charData['renown'] += renown
                            if charData['fight'] >= 3:
                                overThree = charData['fight'] - 3
                                bonus = charData['level'] * 25
                                total = overThree * bonus
                                charData['renown'] += total
                            charData['fight'] = 0
            else:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")
#--------------------------------------------------------MODERATOR COMMANDS---------------------------------------------
        # command for moderators to manually reset a discontinued fight
        if message == "!resetmatch":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, \
            bDeflect = gameStatLoad(channel)
            if character in myModerators and (game == 0.5 or game == 1):
                super().PRI(character, "Are you absolutely certain this match needs to be reset? Please respond here "
                                       "with !confirm, if you are.")
                self.confirm = 1
            elif character not in myModerators:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")
            else:
                super().PRI(character, "There is no game to reset.")

        # command for moderators to confirm manually resetting a discontinued fight
        if message == "!confirm":
            if character in myModerators and self.confirm == 1:
                self.confirm = 0
                gameStatReset(channel)
                super().MSG(unspoiledArena,
                            "Seems like one of the fighters disappeared. Show's over folks. (Resetting Match Status)")
                # self.opponent = ""
                # self.playerOne = ""
                # self.playerTwo = ""
                # self.winner = ""
                # self.loser = ""
                # self.pOneUsername = None
                # self.pTwoUsername = None
                # # PLAYER INFO
                # self.pOneInfo = {}
                # self.pTwoInfo = {}
                # # HP AND TURN COUNTERS
                # self.gameTimer.cancel()
                # self.gameTimer = 0
                # self.count = 0
                # self.base = 0
                # self.token = 0
                # self.game = 0
                # self.critical = 0
                # self.bonusHurt = 0
                # self.nerveDamage = 0
                # self.totalDamage = 0
                # self.pOneTotalHP = 0
                # self.pTwoTotalHP = 0
                # self.pOneCurrentHP = 0
                # self.pTwoCurrentHP = 0
                # # PLAYER ONE FEAT COUNTERS
                # self.pOnepMod = 0
                # self.pOnecMod = 0
                # self.pOnedMod = 0
                # self.pOnemMod = 0
                # self.pOneEvade = 1
                # self.pTwoDeflect = 1
                # self.pOneBullrush = 0
                # self.pOneHeal = 0
                # self.pOneStoneskin = 0
                # self.pOneStonebonus = 0
                # self.pOneDeathsDoor = 0
                # self.pOneQuickDamage = 0
                # self.pOneVile = 0
                # self.pOneFeatInfo = None
                # self.pOneSpentFeat = []
                # # PLAYER TWO FEAT COUNTERS
                # self.pTwopMod = 0
                # self.pTwocMod = 0
                # self.pTwodMod = 0
                # self.pTwomMod = 0
                # self.pTwoEvade = 1
                # self.pTwoDeflect = 1
                # self.pTwoBullrush = 0
                # self.pTwoHeal = 0
                # self.pOneStoneskin = 0
                # self.pOneStonebonus = 0
                # self.pTwoDeathsDoor = 0
                # self.pTwoQuickDamage = 0
                # self.pTwoVile = 0
                # self.pTwoFeatInfo = None
                # self.pTwoSpentFeat = []
                # # XP AND LEVEL COUNTERS
                # self.pOneLevel = 0
                # self.pTwoLevel = 0
                # self.xp = 0
                # self.currentPlayerXP = 0
                # self.nextLevel = 0
                # self.levelUp = 0


        # command for moderators to invite people into rooms as bot
        if message[:7] == "!invite":
            if character in myModerators:
                super().CIU(unspoiledBar, message[8:])
                super().CIU(unspoiledBarOOC, message[8:])
                super().CIU(unspoiledArena, message[8:])
            else:
                super().PRI(character,
                            "So either you found the git holding this bot code, a manager made a poor life "
                            "choice, and told you, or you made a good guess. Here, have a cookie. It's all "
                            "you are getting.")

        # kick a person from the room for 1440 minutes
        if message[:7] == "!detain":
            if character in myModerators:
                person = message[8:]
                if person in myCharacters:
                    super().PRI(character, "Yea...that's not gonna happen, now is it?")
                else:
                    super().CTU(unspoiledBarOOC, person, 1440)
                    super().CTU(unspoiledArena, person, 1440)
                    super().CTU(unspoiledBar, person, 1440)

        # ban a person from the room
        if message[:6] == "!exile":
            if character in myModerators:
                person = message[7:]
                if person in myCharacters:
                    super().PRI(character, "Yea...that's not gonna happen, now is it?")
                else:
                    super().CBU(person, unspoiledBar)
                    super().CBU(person, unspoiledArena)
                    super().CBU(person, unspoiledBarOOC)
                    with open("exiled.json", "r+", encoding="utf-8") as file:
                        exiled = json.load(file)
                        exiled.append(person)
                        file.seek(0)
                        file.write(json.dumps(exiled, ensure_ascii=False, indent=2))
                        file.truncate()
                        file.close()

        # remove ban status from the room
        if message[:7] == "!redeem":
            if character in myModerators:
                person = message[8:]
                super().CUB(unspoiledBarOOC, person)
                super().CUB(unspoiledArena, person)
                super().CUB(unspoiledBar, person)
                with open("exiled.json", "r+", encoding="utf-8") as file:
                    exiled = json.load(file)
                    if person in exiled:
                        exiled.remove(person)
                    file.seek(0)
                    file.write(json.dumps(exiled, ensure_ascii=False, indent=2))
                    file.truncate()
                    file.close()

        # !createrenown <amount> <name>
        if message[:13] == "!createrenown":
            if character in myModerators:
                words = message.split()
                words.remove(words[0])
                try:
                    renown = int(words[0])
                    if renown < 0:
                        super().PRI(character, "You can't give someone negative renown")
                    else:
                        words.remove(words[0])
                        gifted = " ".join(words)
                        path = os.getcwd()
                        charFolder = os.path.join(path + "/characters/")
                        try:
                            giftedFile = open(charFolder + gifted.lower() + ".json", "r", encoding="utf-8")
                            giftedData = json.load(giftedFile)
                            giftedFile.close()
                        # isCharacter = Path(charFolder + character.lower() + ".json")
                        except FileNotFoundError:
                            super().MSG(gifted + " does not have a character.")
                        giftedData['renown'] += renown
                        super().MSG(unspoiledBarOOC, gifted + " has been awarded [color=yellow]" + str(renown) +
                                    " renown[/color]")
                        super().PRI("An Entity", character + " has used the bot to give " + gifted + " " + str(renown) + " renown")

                        file = open(charFolder + gifted.lower() + ".json", "w", encoding="utf-8")
                        json.dump(giftedData, file, ensure_ascii=False, indent=2)
                        file.close()
                except ValueError:
                    super().PRI(character, "Please make sure the format is as follows: !giverenown "
                                           "[color=yellow]<amount>[/color] [color=pink] "
                                           "<profile name>[/color]. Example: !giverenown 100 an entity")

        # !takerenown <amount> name>
        if message[:11] == "!takerenown":
            if character in myModerators:
                words = message.split()
                words.remove(words[0])
                try:
                    renown = int(words[0])
                    if renown < 0:
                        super().PRI(character, "You can't take away negative renown")
                    else:
                        words.remove(words[0])
                        gifted = " ".join(words)
                        path = os.getcwd()
                        charFolder = os.path.join(path + "/characters/")
                        try:
                            giftedFile = open(charFolder + gifted.lower() + ".json", "r", encoding="utf-8")
                            giftedData = json.load(giftedFile)
                            giftedFile.close()
                        # isCharacter = Path(charFolder + character.lower() + ".json")
                        except FileNotFoundError:
                            super().MSG(gifted + " does not have a character.")
                        if giftedData['renown'] < renown:
                            super().MSG(unspoiledBarOOC, gifted + " has lost [color=yellow]" + str(giftedData['renown']) +
                                        " renown[/color]")
                            super().PRI("An Entity", character + " has used the bot to take from " + gifted +
                                        " " + str(giftedData['renown']) + " renown")
                        else:
                            super().MSG(unspoiledBarOOC, gifted + " has lost [color=yellow] " + str(renown) +
                                        " renown[/color]")
                            super().PRI("An Entity", character + " has used the bot to take from " + gifted +
                                        " " + str(renown) + " renown")
                        giftedData['renown'] -= renown
                        if giftedData['renown'] < 0:
                            giftedData['renown'] = 0

                        file = open(charFolder + gifted.lower() + ".json", "w", encoding="utf-8")
                        json.dump(giftedData, file, ensure_ascii=False, indent=2)
                        file.close()
                except ValueError:
                    super().PRI(character, "Please make sure the format is as follows: !giverenown "
                                           "[color=yellow]<amount>[/color] [color=pink]"
                                           "<profile name>[/color]. Example: !giverenown 100 an entity")

        # !createpotion <potion> - <person>
        if message[:13] == "!createpotion":
            if character in myModerators:
                words = message[14:].split(" - ")
                try:
                    path = os.getcwd()
                    item = words[0]
                    gifted = words[1]
                    charFolder = os.path.join(path + "/characters/")
                    try:
                        charSheet = pri_createpotion(item, gifted, charFolder)
                    except FileNotFoundError:
                        super.PRI(character, "Doesn't look like this character sheet exists. Please use proper format:"
                                             "!createpotion <potion> - <profile name>")
                    super().MSG(unspoiledBarOOC, charSheet['name'] + " has obtained a potion of " + item)
                    super().PRI("An Entity",
                                character + " has just used the bot to give " + gifted + "a potion of " + item)
                except ValueError:
                    super().PRI(character, "Please make sure the format is as follows: !givepotion "
                                           "[color=yellow]<potions name>[/color] - [color=pink] "
                                           "<profile name>[/color]. Example: !givepotion str3 an entity")

        # !freerespec
        # Gives one respec point to every registered player. Used only for major updates.
        # Go give a specific person a respec, please use !givepotion
        if message[:11] == "!freerespec":
            if character in myModerators:
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                with open(charFolder + "playerDatabase.json", 'r', encoding="utf-8") as file2:
                    playerDatabase = json.loads(file2.read())
                    file2.close()
                    profile = []
                    for item in playerDatabase.items():
                        name = item[1]
                        profile.append(name)
                    for player in profile:
                        with open(charFolder + player + ".json", "r+", encoding="utf-8") as file:
                            charData = json.load(file)
                            charData["reset"] += 1
                            file.seek(0)
                            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                            file.truncate()
                            file.close()
                    super().PRI("An Entity", character + " used bot to give everyone 1 free respec point.")

#--------------------------------------------------------GAME COMMANDS--------------------------------------------------

        # Select character build path.
        if message[:6] == "!build":
            if message == "!build":
                super().PRI(character, "You need to specify what build you are taking, Example: !build strength, "
                                       "!build dexterity, or !build constitution")
            else:
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                charFile = Path(charFolder + character.lower() + ".json")
                if not charFile.is_file():
                    super().PRI(character, "You don't even have a character created yet. Type !name <name> in the "
                                           "room. Where <name> is your character's actual name. (Example: !name Joe)")
                else:
                    charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
                    charSheet = json.load(charFile)
                    charFile.close()
                    words = message.split(" ")
                    message = words[1].lower()
                    builds = ["strength", "dexterity", "constitution"]
                    if message not in builds:
                        super().PRI(character, message + " is not a choice. Please select: strength, dexterity,"
                                                         " or constitution.")
                    else:
                        msg = pri_6_build(charFolder, message, charFile, character)
                        super().PRI(character, msg)

        # !wholevel <number from 1-20>
        if message[:9] == "!wholevel":
            msg = pri_9_wholevel(character, message)
            for msg_item in msg:
                super().PRI(character, msg_item)

        # keep the bot from crashing if !roll is used in PM
        if message == "!roll":
            super().PRI(character, "This command can only be used in the arena.")

        # keep the bot from crashing if !name used in PM
        if message[:5] == "!name":
            super().PRI(character, "You need to use the !name command in the Unspoiled Desire chatroom.")

        # give a list of traits
        if message == "!traitlist":
            traitDictionary = traitDict()[0]
            traitList = traitDict()[1]

            stringList = "\n".join(traitList)
            super().PRI(character, "\n" + stringList +
                        "\n Type: [color=pink]!traithelp <trait name>[/color] to get information on trait.")

        # !traithelp <trait>
        elif message[:10] == "!traithelp":
            trait = message[11:].lower()
            traitDictionary = traitDict()[0]
            traitList = traitDict()[1]
            if trait not in traitList:
                super().PRI(character, "Make sure you have spelled the feat correctly")
            else:
                super().PRI(character, traitDictionary[0][trait]['desc'])

        # !traitpick <trait>
        elif message[:10] == "!traitpick":
            traitDictionary = traitDict()[0]
            traitList = traitDict()[1]
            trait = message[11:].lower()

            msg = pri_6_trait(character, message, traitList, traitDictionary, trait)
            super().PRI(character, msg)

        # used to 'reroll' a character
        if message == "!respec":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, \
            bDeflect = gameStatLoad(channel)
            if game == 1 and (character.lower() == playerOne or character.lower() == playerTwo):
                super().PRI(character, "Seriously? You seriously want to respec [i]now[/i], in th middle of a fight?"
                                       "No. No you can wait.")
            else:
                msg = pri_7_respec(character)
                super().PRI(character, msg)

        # Obtain correct .json for various commands
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")
        charFile = Path(charFolder + character.lower() + ".json")
        try:
            charSheet = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
            charData = json.load(charSheet)
            charSheet.close()
        except:
            pass

        # !stats <str> <con> <dex>
        if message[:6] == "!stats":
            try:
                msg = pri_6_stats(message, character, charData, charFile)
                for msg_item in msg:
                    super().PRI(character, msg_item)
            except IndexError:
                super().PRI(character, "You need to use the command as instructed. !stat <str> <dex> <con>. Where "
                                       "<str> is your desired strength, <dex> is your desired dexterity, and "
                                       "<con> is your desired constitution. do [b]NOT[/b] use commas, and place a "
                                       "space between each number. Example; !stats 10 5 0")
            except ValueError:
                super().PRI(character, "You need to use the command as instructed. !stat <str> <dex> <con>. Where "
                                       "<str> is your desired strength, <dex> is your desired dexterity, and "
                                       "<con> is your desired constitution. do [b]NOT[/b] use commas, and place a "
                                       "space between each number. Example: !stats 10 5 0")
            except UnboundLocalError:
                super().PRI(character, "You don't even have a character created yet. Type !name <name> in the room. "
                                       "Where <name> is your character's actual name. (Example: !name Joe)")

        # Add function, to add an ability point once reaching the proper level.
        if message == "!add":
            super().PRI(character, "You need to specify the ability you want to put the point to. "
                                   "Type '!add str' or '!add strength' for strength, and so on.")

        elif message[:4] == "!add":
            msg = pri_4_add(message, character)
            for msg_item in msg:
                super().PRI(character, msg_item)

        # sends a PM to the character to allow them to see character sheet.
        if message == "!viewchar":
            # Find out if player even has a character created yet. If not. Tell them they are an idiot.
            msg = pri_viewchar(character)
            for msg_item in msg:
                super().PRI(character, msg_item)

        # grab dictionaries for feats before the upcoming 'if' statement. Just so it can be used through all if
        # statements used...and there are a lot.
        featDictionary = featDict()[0]
        featList = featDict()[1]
        if message == "!feat":
            super().PRI(character, "For a list of all the available feats, type '!featlist'. "
                                   "For information on a specific feat, type '!feathelp <feat>' "
                                   "To choose a specific feat, type '!featpick <feat>'")

        # if !feats was followed up with the word 'lists' PM them the names of all available feats.
        if message == "!featlist":
            # stringList = "\n".join(featList)
            # super().PRI(character, stringList +
            #             "\n Type: [color=pink]!feathelp <feat name>[/color] to get a PM of feat info\n"
            #             "or just go to the Unspoiled Desire profile for a full list.")
            super().PRI(character, "I [i]could[/i] just list a massive list of 62 feats here for you to scroll up and "
                                   "look at. Or I [i]could[/i] tell you to look at the long list in the profile. Or I "
                                   "can just give you a "
                                   "[url=https://docs.google.com/spreadsheets/d/18ama_CtAPHm_GqTVZGZxLmJ0xZ5QYivarrjn"
                                   "1Yq8FFU/edit#gid=0]google sheet[/url] to look at.")

        # if !feats was followed up with 'help' continue on to capture the feat they want help on (Example:
        # !feathelp power attack, capture 'power attack' in a variable, then use feat dictionary stored above
        # to grab required information. Then PM them said information.
        if message[:9] == "!feathelp":
            answer = message[10:].lower()
            if answer not in featList:
                super().PRI(character, "Make sure you have spelled the feat correctly")
            else:
                reqStat = featDictionary[0][answer]['stat']
                featStatus = featDictionary[0][answer]['status']
                level = featDictionary[0][answer]['requirements'][0]
                reqFeats = featDictionary[0][answer]['requirements'][4]
                super().PRI(character, answer + " (" + reqStat + ") (" + featStatus + ")\n" +
                            featDictionary[0][answer]['desc'] +
                            "\nPrerequisites: " + "\nLevel: " + str(level) +  " Required Feats: " + reqFeats)

        # if the command is just !feat, followed by the feat name. Then they just want to take that feat.
        if message[:9] == "!featpick":
            msg = pri_10_feat_pick(character, message, featList, featDictionary)
            for msg_item in msg:
                super().PRI(character, msg_item)

# -----------------------------------------------ARMOR COMMANDS---------------------------------------------------------
        # view armor in shop
        if message == "!armorshop":
            armorList = pri_armorshop()
            super().PRI(character, "Items available in shop: (Item:  Armor: [color=red][stats][/color]"
                                   "[color=yellow] (cost)[/color]) \n" + armorList)

        # !sellarmor <current armor name>
        if message[:10] == "!sellarmor":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion, \
            bDeflect = gameStatLoad(channel)
            if game == 0 and (playerOne != character.lower() or playerTwo != character.lower()):
                armor = message[11:]
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                msg = pri_10_sellarmor(character, armor, charFolder)
                if "You" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().MSG(unspoiledBarOOC, msg)
            else:
                super().PRI(character, "No no no, silly. You can't possibly do that right now. You are in a fight!")
        # !buyarmor <armor name in list>
        if message[:9] == "!buyarmor":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,\
            bDeflect = gameStatLoad(channel)
            if game == 0 and (playerOne != character.lower() or playerTwo != character.lower()):
                armor = message[10:].lower()
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                msg = pri_9_buyarmor(character, armor, charFolder)
                if "You" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().MSG(unspoiledBarOOC, msg)
            else:
                super().PRI(character, "Wha- Ho- But....you are in a fight? Why you trying to buy stuff [i]now?[/i]")
        # !armorname <current armor name> - <new armor name>
        if message[:10] == "!armorname":
            if "-" not in message:
                super().MSG(channel, "You need to seperate the [color=green]old name[/color] and the [color=yellow]"
                                     "new name[/color]. Example: !armorname <oldname> - <newname>")
            else:
                words = message[11:].split(' - ')
                armorRemove = words[0]
                armorName = words[1].lower()
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                msg = pri_10_namearmor(character, armorName, armorRemove, charFolder)
                if "command" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().MSG(unspoiledBarOOC, msg)

        # equip armor
        if message[:6] == "!equip":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod,\
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal,\
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor,\
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose,\
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,\
            bDeflect = gameStatLoad(channel)
            armor = message[7:].lower()
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            msg = pri_6_equip(character, armor, charFolder, game)
            if "command" in msg:
                super().PRI(character, msg)
            elif "fight" in msg:
                super().PRI(character, msg)
            else:
                super().MSG(unspoiledArena, msg)
                super().PRI(character, msg)

        # unequip armor
        if message[:8] == "!unequip":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod,\
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal,\
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor,\
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose,\
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, bEvasion,\
            bDeflect = gameStatLoad(channel)
            armor = message[9:].lower()
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            msg = pri_8_unequip(character, armor, charFolder, game)
            if "command" in msg:
                super().PRI(character, msg)
            elif "fight" in msg:
                super().PRI(character, msg)
            else:
                super().MSG(unspoiledArena, msg)
                super().PRI(character, msg)
# -----------------------------------------------POTION COMMANDS--------------------------------------------------------
        # view potions in shop
        if message == "!potionshop":
            shopList = pri_potionshop()

            super().PRI(character, "Items available in shop: (Item:  [color=red]Amount[/color]"
                                   "[color=yellow] (cost)[/color]) \n" + shopList)

        # !buypotion <potion>
        if message[:10] == "!buypotion":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 0 and (playerOne != character.lower() or playerTwo != character.lower()):
                potion = message[11:]
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                msg, buyer, potion = pri_10_buypotion(character, potion, charFolder)
                if "You" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().MSG(unspoiledBarOOC, msg)
            else:
                super().PRI(character, "How are you even getting to the shop in the Bar right now? You are in a fight. "
                                       "No.")
        # !sellpotion <potion>
        if message[:11] == "!sellpotion":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 0 and (playerOne != character.lower() or playerTwo != character.lower()):
                potion = message[12:]
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                msg = pri_11_sellpotion(character, potion, charFolder)
                if "You" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().MSG(unspoiledBarOOC, msg)
            else:
                super().PRI(character, "You are in a fight, the potionshop is in the bar. Seems like you missed your "
                                       "chance, buddy.")

        # !givepotion <potion> <person>
        if message[:11] == "!givepotion":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 0 and (playerOne != character.lower() or playerTwo != character.lower()):
                words = message.split()
                words.remove(words[0])
                item = words[0]
                words.remove(words[0])
                gifted = " ".join(words)
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                msg, gifter, gifted = pri_11_givepotion(character, item, gifted, charFolder)
                if "You" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().PRI("An Entity", msg)
                    super().MSG(unspoiledBarOOC, msg)
            else:
                    super().PRI(character, "How..how you doing that? You are in the arena, focusing on not getting your"
                                           " ass kicked. Presumably the person you are trying to give a potion too is"
                                           " still in the bar? Hmmm...nope. No you can wait. :)")

        # !usepotion <potion>
        if message[:10] == "!usepotion":
            opponent, playerOne, playerTwo, winner, quitter, pOneInfo, pTwoInfo, featToken, game, count, \
            token, critical, bonusHurt, nerveDamage, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, \
            pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect, pOneSunder, \
            pOneSunderAmount, pOneBullrush, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, \
            pOneStoneskin, pOneStonebonus, pOneDeathsDoor, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat, \
            pOneQuick, pOneVile, pOneHeavy, pOneInner, pOneExpose, pOneCheapShot, pOneLockout, pTwopMod, pTwocMod, \
            pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush, pTwoHeal, \
            pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pTwoStoneskin, pTwoStonebonus, pTwoDeathsDoor, \
            pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pTwoQuick, pTwoVile, pTwoHeavy, pTwoInner, pTwoExpose, \
            pTwoCheapShot, pTwoLockout, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel, levelUp, iddqd, \
            bEvasion, bDeflect = gameStatLoad(channel)
            if game == 0 and (playerOne != character.lower() or playerTwo != character.lower()):
                potion = message[11:]
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                print("in usepotion")
                commonList, uncommonList, rareList, vrareList, relicList = pri_potion_shop_lists()
                msg = pri_10_usepotion(character, potion, commonList, uncommonList, rareList,
                                           vrareList, relicList, charFolder)
                if "You" in msg:
                    super().PRI(character, msg)
                else:
                    super().PRI(character, msg)
                    super().MSG(unspoiledBarOOC, msg)
            else:
                    super().PRI(character, "C'mon now...do you [i]really[/i] think I'm gonna let you drink a potion"
                                           " [i]while[/i] in a fight? How rediculously unfair would that be? Baiting"
                                           " someone into a fight, then drinking a potion to become neigh unbeatable."
                                           " A for effort though.")

# client = discord.Client()
#
# async def flistEcho():
#     """Background task that sends message sent from F-list to an appropriate Discord channel
#     when global Facebook messenge data is updated"""
#     await client.wait_until_ready()
#     channel = client.get_channel(serverroom)
#     while not client.is_closed():
#         global note
#         if note != "":
#             await channel.send(note)
#             note = ""


file = open("credentials.json", "r", encoding="utf-8")
info = json.load(file)
file.close()

file = open("room.json", "r", encoding="utf-8")
room = json.load(file)
file.close()

website = info['website']
user = info['user']
password = info['password']
profile = info['profile']
# token = info["discord"]
# serverroom = info["serverroom"]

# client.loop.create_task(flistEcho())
# client.run(token)

unspoiledBar = room['unspoiledIC']
unspoiledBarOOC = room['unspoiledOOC']
unspoiledArena = room['unspoiledArena']
thePhotoPub = room['thePhotoPub']
unspoiledRooms = [unspoiledBar, unspoiledArena, unspoiledBarOOC]

bot = EchoBot(website, user, password, profile)
bot.setup()
bot.connect()
bot.JCH(unspoiledBar)
bot.JCH(unspoiledArena)
bot.JCH(unspoiledBarOOC)
bot.JCH(thePhotoPub)
bot.run_forever()
# threading.Thread(target=lambda: bot.run_forever().start())
# threading.Thread(target=lambda: client.run(token)).start()