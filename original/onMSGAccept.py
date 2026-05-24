import os
import json
import random
import time

from pathlib import Path
from threading import Timer
from src.character_repository import (build_challenge_accept_initiative_result,
                                      load_character)


#101

def message_accept(channel, charFolder, unspoiledArena, character, game, opponent, pOneInfo):
    update = False
    msg = []
    pTwoInfo = None
    new_game = None
    playerTwo = None
    bTimer = False
    bGameTimer = False
    new_oppenent = None
    token = None

    if channel == unspoiledArena:
        # make sure that this command cannot be ran if a fight is taking place. During a fight, game counter will
        # be set to 1.
        if game == 0.5:
            path = os.getcwd()
            charFolder = os.path.join(path + "/characters/")
            charFile = Path(charFolder + character.lower() + ".json")
            print("why?")
            playerTwo = character.lower()
            if opponent == character.lower():
                # since challenge is being accepted, set game counter to 1.
                bTimer = True
                new_game = 1
                new_opponent = ""
                pTwoInfo = load_character(character, charFolder)

                playerOneInit = random.randint(1, 20)
                playerTwoInit = random.randint(1, 20)
                coinFlip = None

                if playerOneInit + int(pOneInfo["initiative"]) == playerTwoInit + int(pTwoInfo["initiative"]):
                    if int(pOneInfo["initiative"]) == int(pTwoInfo["initiative"]):
                        coinFlip = random.randint(1, 2)

                initiative_msg, token = build_challenge_accept_initiative_result(
                    pOneInfo,
                    pTwoInfo,
                    player_one_roll=playerOneInit,
                    player_two_roll=playerTwoInit,
                    coin_flip=coinFlip,
                )
                msg.extend(initiative_msg)
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
