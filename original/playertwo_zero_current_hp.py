import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# 260

def playertwo_currentHP_less_zero(msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP, pTwoCurrentHP,
                                  pOneLevel, pTwoLevel, charFolder, rounds, pOneDeathsDoor, pTwoDeathsDoor):
    print("inside pOneWin")
    pOneDeathsDoor = 0
    pTwoDeathsDoor = 0
    msg.append(pOneInfo['name'] + " won in [color=red]"
               + str(int(rounds)) + "[/color] rounds")
    base = 100
    level = abs(pOneLevel - pTwoLevel)
    opponentLevel = int(pTwoLevel / 2)
    if opponentLevel < 1:
        opponentLevel = 1
    if level == 0:
        level = 1
    if level < 5:
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        if differHP > 20:
            differHP = 20
        xp = int((base * opponentLevel) + (differHP * rounds))
        if rounds > 8:
            rounds = 8
        renown = int((((base * pTwoLevel) ** 1.06) + ((rounds ** 2.5) + base)))

    elif 5 >= level <= 10:
        msg.append("As the level difference between opponents is between 5 and 10, total reward is reduced by half.")
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        if differHP > 20:
            differHP = 20
        xp = int(((base - 25) * opponentLevel) + (differHP * rounds) / 2)
        renown = int((((base - 25) * pTwoLevel) ** 1.06) + ((rounds ** 2.5) + base) / 2)

    elif 10 > level:
        msg.append("As the level difference between opponents is is between 11 and 15, total reward is divided "
                   "by four.")
        differHP = abs(pOneCurrentHP - pTwoCurrentHP)
        if differHP > 20:
            differHP = 20
        xp = int(((base - 50) * opponentLevel) + (differHP * rounds) / 4)
        renown = int((((base - 50) * pTwoLevel / 2) ** 1.06) + ((rounds ** 2.5) + base) / 4)

    if pOneInfo['level'] <= 4:
        anni = int(xp * 0.25)
        xp = xp + anni
        msg.append(pOneInfo['name'] + " has earned an [color=yellow]extra 25%[/color]")
    if pTwoInfo['level'] <= 4:
        anni = int(xp * 0.25)
        xp = xp + anni
        msg.append(pTwoInfo['name'] + " has earned an [color=yellow]extra 25%[/color]")

    if pOneInfo['trait'] == "cursed" or pTwoInfo['trait'] == "cursed":
        reduced = int(xp / 0.9)
        xp = xp - reduced
        reduced = int(renown / 2)
        renown = renown - reduced
        msg.append("One of the opponents was cursed. As a result, xp and renown has been reduced by 90%, and renown halved.")

    msg.append(pOneInfo['name'] + " has earned: [color=red]" + str(xp) +
               "[/color] experience points. and [color=yellow]" +
               str(renown) + "[/color] renown.\n" +
               pTwoInfo['name'] + " has earned: [color=red]" + str(int(xp / 2)) + "[/color] experience points"
               " and [color=yellow]" + str(int(renown / 2)) + "[/color] renown.")
    pOneXP = int(pOneInfo['currentxp'] + xp)
    pOneRenown = int(pOneInfo['renown'] + renown)
    pTwoXP = int(pTwoInfo['currentxp'] + (xp / 2))
    pTwoRenown = int(pTwoInfo['renown'] + (renown / 2))
    nextLevel = pOneInfo['nextlevel']
    winner = playerOne
    loser = playerTwo
    levelUp = pOneInfo['level']

    # Record xp gained and win
    with open(charFolder + winner + '.json', 'r+') as file:
        pOneInfo = json.load(file)
        pOneInfo['currentxp'] = pOneXP
        pOneInfo['renown'] = pOneRenown
        if pOneInfo['trait'] == "cursed":
            pOneInfo['wins'] += 1
        pOneInfo["fight"] += 1
        pOneInfo["potioneffect"] = ""
        pOneInfo["potionhit"] = 0
        pOneInfo["potiondamage"] = 0
        pOneInfo["potionac"] = 0
        pOneInfo["potionhp"] = 0
        pOneInfo["potiondr"] = 0
        pOneInfo["potionstr"] = 0
        pOneInfo["potiondex"] = 0
        pOneInfo["potioncon"] = 0
        file.seek(0)
        file.write(json.dumps(pOneInfo, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

    # Record loss
    with open(charFolder + loser + '.json', 'r+') as file:
        pTwoInfo = json.load(file)
        pTwoInfo['currentxp'] = pTwoXP
        pTwoInfo['renown'] = pTwoRenown
        if pTwoInfo['trait'] == "cursed":
            pTwoInfo['losses'] += 1
        pTwoInfo["fight"] += 1
        pTwoInfo["potioneffect"] = ""
        pTwoInfo["potionhit"] = 0
        pTwoInfo["potiondamage"] = 0
        pTwoInfo["potionac"] = 0
        pTwoInfo["potionhp"] = 0
        pOneInfo["potionblur"] = 0
        pTwoInfo["potionstr"] = 0
        pTwoInfo["potiondex"] = 0
        pTwoInfo["potioncon"] = 0
        file.seek(0)
        file.write(json.dumps(pTwoInfo, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

    if pOneInfo['currentxp'] >= nextLevel:
        newLevel = levelUp + 1
        newLevel = str(newLevel)
        levels = [5, 10, 15, 20]
        msg.append("[color=red][b]" + pOneInfo['name'].capitalize() + " has reached level "
                   + newLevel + "![/b][/color]")
        levelFile = open(charFolder + "levelchart.json", "r", encoding="utf-8")
        levelDict = json.load(levelFile)
        levelFile.close()
        with open(charFolder + winner + '.json', 'r+') as file:
            charData = json.load(file)
            charData['level'] = int(newLevel)
            if  charData['build'] == 'strength':
                if charData['level'] == 18:
                    charData['feats taken'].remove("greater focus")
                    charData['feats taken'].append("perfect focus")
                elif charData['level'] == 15:
                    charData['feats taken'].remove("improved focus")
                    charData['feats taken'].append("greater focus")
                elif charData['level'] == 9:
                    charData['feats taken'].remove("focus")
                    charData['feats taken'].append("improved focus")
                elif charData['level'] == 3:
                    charData['feats taken'].append("focus")
            if charData['level'] in levels:
                if charData['level'] in levels:
                    if charData['trait'] == 'regeneration':
                        charData['traitregen'] += 1
                    elif charData['trait'] == 'brawler':
                        charData['traithit'] += 1
                    elif charData['trait'] == 'thug':
                        charData['traitdamage'] += 1
                    elif charData['trait'] == 'hearty':
                        charData['traithp'] += 5
                    elif charData['trait'] == 'nimble':
                        charData['traitac'] += 1
                    elif charData['trait'] == 'thickskinned':
                        charData['traitdr'] += 1
                    elif charData['trait'] == 'opportunist':
                        charData['opportunist'] += 1
                    elif charData['trait'] == 'nebulous':
                        charData['blur'] += 1
            charData['hp'] = int(levelDict[newLevel][0])
            charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                levelDict[newLevel][2])
            if charData['total feats'] == levelDict[newLevel][4]:
                charData['total feats'] = levelDict[newLevel][4]
            else:
                msg.append(pOneInfo['name'] + " has a new feat slot to fill. Use the [color=pink]!feat[/color] "
                           "command to select new feat.")
                charData['total feats'] = levelDict[newLevel][4]
                charData['remaining feats'] = 1
            if charData['ap'] == levelDict[newLevel][3]:
                charData['ap'] = levelDict[newLevel][3]
            else:
                msg.append(pOneInfo['name'] + " has a new ability point to spend. PM the [color=pink]!add[/color] "
                           "command to Unspoiled Desire, to spend it.")
                charData['ap'] = levelDict[newLevel][3]
                charData['apboost'] = True
            charData['hit'] = int(levelDict[newLevel][5])
            charData['damage'] = int(levelDict[newLevel][5])
            charData['ac'] = int(levelDict[newLevel][6])
            charData['currentxp'] = pOneXP
            charData['renown'] = pOneRenown
            charData['nextlevel'] = int(levelDict[newLevel][7])
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()

    if pTwoInfo['currentxp'] >= pTwoInfo['nextlevel']:
        pTwoInfo['level'] = pTwoInfo['level'] + 1
        newLevel = str(pTwoInfo['level'])
        levels = [5, 10, 15, 20]
        msg.append("[color=red][b]" + pTwoInfo['name'].capitalize() + " has reached level " + newLevel +
                   "![/b][/color]")
        levelFile = open(charFolder + "levelchart.json", "r", encoding="utf-8")
        levelDict = json.load(levelFile)
        levelFile.close()
        with open(charFolder + loser + ".json", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData['level'] = int(newLevel)
            if  charData['build'] == 'strength':
                if charData['level'] == 18:
                    charData['feats taken'].remove("greater focus")
                    charData['feats taken'].append("perfect focus")
                elif charData['level'] == 15:
                    charData['feats taken'].remove("improved focus")
                    charData['feats taken'].append("greater focus")
                elif charData['level'] == 9:
                    charData['feats taken'].remove("focus")
                    charData['feats taken'].append("improved focus")
                elif charData['level'] == 3:
                    charData['feats taken'].append("focus")
            if charData['level'] in levels:
                if charData['trait'] == 'regeneration':
                    charData['regeneration'] += 1
                elif charData['trait'] == 'brawler':
                    charData['strength'] += 1
                elif charData['trait'] == 'thug':
                    charData['damage'] += 1
                elif charData['trait'] == 'hearty':
                    charData['traithp'] += 5
                elif charData['trait'] == 'nimble':
                    charData['dexterity'] += 1
                elif charData['trait'] == 'thickskinned':
                    charData['dr'] += 1
                elif charData['trait'] == 'opportunist':
                    charData['initiative'] += 1
                elif charData['trait'] == 'nebulous':
                    charData['blur'] += 1
            charData['hp'] = int(levelDict[newLevel][0])
            charData['base damage'] = str(levelDict[newLevel][1]) + "d" + str(
                levelDict[newLevel][2])
            if charData['total feats'] == levelDict[newLevel][4]:
                charData['total feats'] = levelDict[newLevel][4]
            else:
                msg.append(pTwoInfo['name'] + " has a new feat slot to fill. Use the [color=pink]!feat[/color] "
                           "command to select new feat.")
                charData['total feats'] = levelDict[newLevel][4]
                charData['remaining feats'] = 1
            if charData['ap'] == levelDict[newLevel][3]:
                charData['ap'] = levelDict[newLevel][3]
            else:
                msg.append(pTwoInfo['name'] + " has a new ability point to spend. PM the [color=pink]!add[/color] "
                           "command to Unspoiled Desire, to spend it.")
                charData['ap'] = levelDict[newLevel][3]
                charData['apboost'] = True
            charData['hit'] = int(levelDict[newLevel][5])
            charData['damage'] = int(levelDict[newLevel][5])
            charData['ac'] = int(levelDict[newLevel][6])
            charData['currentxp'] = pTwoXP
            charData['renown'] = pTwoRenown
            charData['nextlevel'] = int(levelDict[newLevel][7])
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
    return msg, pOneInfo, pTwoInfo, pOneDeathsDoor, pTwoDeathsDoor
