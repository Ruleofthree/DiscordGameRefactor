import os
import json
import random
import time

from pathlib import Path
from threading import Timer
from src.character_repository import load_character


#101

def message_accept(channel, charFolder, unspoiledArena, character, game, opponent, pOneInfo):
    update = False
    msg = []
    if channel == unspoiledArena:
        # make sure that this command cannot be ran if a fight is taking place. During a fight, game counter will
        # be set to 1.
        if game == 0.5:
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            charFile = Path(charFolder + character.lower() + ".json")
            pTwoInfo = None
            new_game = None
            playerTwo = ""
            bTimer = False
            bGameTimer = False
            new_oppenent = None
            token = None
            playerTwo = None
            print("why?")
            playerTwo = character.lower()
            if opponent == character.lower():
                # since challenge is being accepted, set game counter to 1.
                bTimer = True
                new_game = 1
                new_opponent = ""
                pTwoInfo = load_character(character, charFolder)
                # since if a person !accepts a challenge, that mights a fight is about to take place. Just go
                # straight into combat by starting initiative. Depending on who wins, token is set to 1 or 2. Tokens
                # will be used to determine whose turn it is during the fight, and lock out anyone using fight commands
                # but the player whose turn it is.
                msg.append("\nRolling Initiative to see who goes first. In result of tie, person with "
                           "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
                           "it, coin flip. " + pOneInfo['name'] + " wins on a One.")
                playerOneMod = int(pOneInfo['initiative'])
                playerTwoMod = int(pTwoInfo['initiative'])
                playerOneInit = random.randint(1, 20)
                totalOne = playerOneInit + playerOneMod
                playerTwoInit = random.randint(1, 20)
                totalTwo = playerTwoInit + playerTwoMod
                msg.append(pOneInfo['name'] + " rolled: " + str(playerOneInit) + " + " +
                           str(playerOneMod) + " and got [color=red]" + str(totalOne) + "[/color]\n" + pTwoInfo[
                               'name'] +
                           " rolled: " + str(playerTwoInit) + " + " + str(playerTwoMod) +
                           " and got [color=red]" + str(totalTwo) + "[/color]")
                if totalOne > totalTwo:
                    msg.append(pOneInfo['name'] + " Goes first")
                    token = 1
                    msg.append("Type [color=pink]!usefeat <feat>[/color] to use a feat.")
                elif totalTwo > totalOne:
                    msg.append(pTwoInfo['name'] + " Goes first")
                    token = 2
                    msg.append("Type [color=pink]!usefeat <feat>[/color] to use a feat.")
                elif totalOne == totalTwo:
                    msg.append(pOneInfo['name'] + "'s dexterity: [color=red]" + str(playerOneMod) +
                               "[/color]\n" + pTwoInfo['name'] + "'s dexterity: [color=red]" + str(playerTwoMod) +
                               "[/color]")
                    if playerOneMod > playerTwoMod:
                        msg.append(pOneInfo['name'] + " Goes first. Type [color=pink]!usefeat <feat>"
                                                      "[/color] to use a feat.")
                        token = 1
                    elif playerOneMod < playerTwoMod:
                        msg.append(pTwoInfo['name'] + " Goes first. Type [color=pink]!usefeat <feat>"
                                                      "[/color] to use a feat.")
                        token = 2
                    else:
                        value = random.randint(1, 2)
                        if value == 1:
                            msg.append(pOneInfo['name'] + " Goes first. Type [color=pink]!usefeat <feat>"
                                                          "[/color] to use a feat.")
                            token = 1
                        else:
                            msg.append(pTwoInfo['name'] + " Goes first. Type [color=pink]!usefeat <feat>"
                                                          "[/color] to use a feat.")
                            token = 2
                bGameTimer = True
                update = True

            else:
                try:
                    msg.append("I may be a bot, but I'm pretty sure you aren't " + opponent + ". A for"
                               " effort, though.")
                except TypeError:
                    msg.append("Wait for the pervious challenge to expire.")
        else:
            msg.append("There is no challenge to accept.")
    else:
        msg.append("This command is only available in "
                   "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")

    return msg, pTwoInfo, new_game, playerTwo, bTimer, bGameTimer, new_oppenent, token, update
