import os
import json
import random
import time

from pathlib import Path
from threading import Timer
from src.character_repository import (build_challenge_acceptance_result,
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

            playerOneInit = None
            playerTwoInit = None
            coinFlip = None

            if opponent == character.lower():
                playerOneInit = random.randint(1, 20)
                playerTwoInit = random.randint(1, 20)
                pTwoInfo = load_character(character, charFolder)

                if playerOneInit + int(pOneInfo["initiative"]) == playerTwoInit + int(pTwoInfo["initiative"]):
                    if int(pOneInfo["initiative"]) == int(pTwoInfo["initiative"]):
                        coinFlip = random.randint(1, 2)

            (
                msg,
                pTwoInfo,
                new_game,
                playerTwo,
                bTimer,
                bGameTimer,
                new_oppenent,
                token,
                update,
            ) = build_challenge_acceptance_result(
                character=character,
                opponent=opponent,
                player_one_info=pOneInfo,
                player_one_roll=playerOneInit,
                player_two_roll=playerTwoInit,
                coin_flip=coinFlip,
                characters_dir=charFolder,
            )
        else:
            msg.append("There is no challenge to accept.")
    else:
        msg.append("This command is only available in "
                   "[session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")

    return msg, pTwoInfo, new_game, playerTwo, bTimer, bGameTimer, new_oppenent, token, update
