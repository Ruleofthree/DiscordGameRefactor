from src.feat_repository import get_feat_dictionary_and_names
from src.character_repository import (build_character_who_messages,
                                      build_character_player_score_message,
                                      create_character,
                                      character_exists,
                                      delete_character,
                                      load_character,
                                      save_character)
import os
import json
import random
import time

from pathlib import Path
from threading import Timer
from feat_methods import *


#1502

def featDict():
    return get_feat_dictionary_and_names()

def message_8_compile(users):
    noNoList = ["Unspoiled Desire"]
    masterList = []
    for item in users:
        if item["identity"] not in noNoList:
            masterList.append(item["identity"])
    return masterList

def status_compile(character, statusmsg, masterList):
    try:
        if character in masterList:
            split1 = statusmsg.split("[session=Unspoiled Desire (Command and OoC Room)]")
            room = "adh-8216a753c1ef08445052[/session]"
            split2 = split1[1].split("[")
            if room in split1:
                split2 = room
            split3 = split2.split("[/session]")
            findRoom = split3[0]
            if findRoom in statusmsg:
                path = os.getcwd()
                charFolder = os.path.join(path + "/characters/")
                pInfo = load_character(character, charFolder)
                pInfo['status'] = findRoom
                save_character(character, pInfo, charFolder)
            else:
                pInfo = load_character(character, charFolder)
                pInfo['status'] = ""
                save_character(character, pInfo, charFolder)
    except:
        pass

# depreciated. No longer used.
def message_7_detect(channel, unspoiledBarOOC, character, message):
    if channel == unspoiledBarOOC:
        if message == "!detect" and character == "Kenneth Minus":
            msg = "Ken sees what you're up to."
        elif message != "!detect" and character == "Kenneth Minus":
            msg = "Ken saw what " + message[8:] + " was up to last night. Tisk tisk."
        else:
            msg = "You don't have such powerful intuitive skills! What are you doing? You are looking the fool."
    return msg

# depreciated. No longer used.
def message_5_kill(channel, unspoiledBarOOC, character, message):
    if channel == unspoiledBarOOC:
        ariCharacter = ["Ari Vyn", "Delcaya"]
        if message == "!kill" and character in ariCharacter:
            msg = character + " just killed...someone, or something. We don't know who, or what, cause she didn't "\
                  "specify. This is normal, that's how unpredictable she can be."
        elif message != "!kill" and character in ariCharacter:
            msg = character + " just killed " + message[6:] + " That's just unfortunate."
        else:
            msg = "You do not hold sufficient power to wield this mighty tool."
    return msg

# depreciated. No longer used.
def message_5_bell(channel, unspoiledBarOOC, character, message):
    myCharacters = ["Their Perfect Doll", "An Entity"]
    if character in myCharacters:
        msg = "The adorable silver bell on Kysume's soft denim collar jingles for some inexplicable reason."
    else:
        msg = "For some reason, try as you might, the bell makes no sound."
    return msg


def message_5_name(channel, charFolder, message, charFile, character):
    msg = []

    if charFile.is_file():
        msg.append("You've already created a character.")
    elif message == "!name":
        msg.append("You need to give your character a name.")
    else:
        name = message[6:]
        msg.append("Your character name is: " + name)

        created = create_character(
            character=character,
            name=name,
            char_folder=charFolder,
        )

        if created:
            msg.append("Your character sheet has been created.")
            msg.append("PM [color=pink]Unspoiled Desire[/color] with '!build <strength> <constitution> <dexterity>' to"
                       " determine general build path, and bonuses obtained from selected feats. Example: !build strength")
        else:
            msg.append("You've already created a character.")

    return msg


# Displays the top five players in the desired category:
# !leaderboard wins
# !leaderboard losses
# !leaderboard percent
def message_12_leaderboard(channel, charFolder, unspoiledBarOOC, message):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    msg = []
    if channel == unspoiledBarOOC:
        profile = []
        with open(charFolder + "playerDatabase.json", 'r', encoding="utf-8") as file2:
            playerDatabase = json.loads(file2.read())
            file2.close()
        for item in playerDatabase.items():
            name = item[1]
            profile.append(name)
        ratio = {}
        num = 1
        for player in profile:
            with open(charFolder + player + ".json", "r+", encoding="utf-8") as file:
                charData = json.load(file)
                file.close()
            name = charData['name']
            wins = charData['wins']
            lose = charData['losses']
            level = charData['level']
            total = wins + lose
            try:
                percent = (wins / total) * 100
                charData['percent'] = int(percent)
            except ZeroDivisionError:
                percent = 0
                charData['percent'] = percent
            ratio[num] = [player, name, wins, lose, percent, level]
            num += 1
        answer = message[13:]
        if answer == "win":
            indexSearch = 2
        elif answer == "loss":
            indexSearch = 3
        elif answer == "percent":
            indexSearch = 4
        else:
            indexSearch = 2
        indices = sorted(ratio, key=lambda d: ratio[d][indexSearch], reverse=True)
        sortedDict = {}
        index = 1
        for i in indices:
            sortedDict[index] = ratio[i]
            index += 1
        num = 5
        stringDict = []
        for num in range(1, num + 1):
            total = sortedDict[num][2] + sortedDict[num][3]
            stringDict.append("\n" + sortedDict[num][1] + " (" + sortedDict[num][0] + ", Level: [color=green]" +
                              str(sortedDict[num][5]) + "[/color]): [color=pink]" + str(sortedDict[num][2]) +
                              "[/color] wins/[color=yellow]" + str(sortedDict[num][3]) + "[/color] losses. [color=red]("
                              + str(round(sortedDict[num][4], 2)) + "%)[/color]")
        seperator = " "
        completeMessage = seperator.join(stringDict)
        msg.append(completeMessage)
    else:
        msg = "This Command can only be used in [session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]"
    return msg

# Displays players wins, losses, and ratio. Also display number of forfeits. MUST USE PROFILE NAME
# !who <profile name>
def message_4_who(channel, charFolder, unspoiledBarOOC, message):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    msg = []
    if channel == unspoiledBarOOC:
        profile = message[5:].lower()
        msg = build_character_who_messages(charFolder, profile)
    else:
        msg.append("This Command can only be used in [session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]")

    return msg

# Depreciated. No longer used.
def message_7_player(channel, charFolder, unspoiledBarOOC, message):
    msg = ""
    if channel == unspoiledBarOOC:
        name = message[8:].lower()
        msg = build_character_player_score_message(charFolder, name)
    else:
        msg = "This Command can only be used in [session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]"
    return msg

# Erases a character. Once erase command was used. player must !confirm deletion, or !deny
# !erase
def message_7_erase(character):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    return delete_character(character, charFolder)

# Issue a challange to a player. USE PROFILE NAME
# !challenge <profile name>
def message_10_challenge(channel, charFolder, message, unspoiledArena, character, game):
    msg = ""
    update = False

    if channel == unspoiledArena:
        # make sure that this command cannot be ran if a fight is taking place. During a fight, game counter will
        # be set to 1.
        if game == 0:
            opponent = None
            pOneInfo = None
            bTimer = False
            new_game = 0
            playerOne = ""
            playerOne = character.lower()
            charFile = Path(charFolder + character.lower() + ".json")
            # make sure the only people that can issue a challenge, is a person that has a character made.
            if not character_exists(character, charFolder):
                msg = "You don't even have a character made to fight."
                return msg, update
            else:
                # load in character sheet.
                opponent = message[11:].lower()
                pOneInfo = load_character(character, charFolder)
                pTwoInfo = load_character(opponent, charFolder)
                if opponent == playerOne:
                    msg = "You can't fight yourself. No one is that special."
                elif len(pOneInfo['hfeats taken']) < pOneInfo['total feats']:
                    msg = pOneInfo['name'] + " has empty feat slots, and cannot fight yet"
                elif len(pTwoInfo['hfeats taken']) < pTwoInfo['total feats']:
                    msg = pTwoInfo['name'] + " has empty feat slots, and cannot fight yet"
                else:
                    if pOneInfo['trait'] == "cursed" or pTwoInfo['trait'] == "cursed":
                        msg = pOneInfo['name'].title() + " is challenging " + pTwoInfo['name'].title() + " (" + opponent.title() + ", " \
                              "Type [color=pink]!accept[/color]) Please be aware that one of the opponents" \
                              " is [color=cyan]cursed[/color], and no xp/renown will be awarded at end of match."
                    else:
                        msg = pOneInfo['name'].title() + " is challenging " + pTwoInfo['name'].title() + " (" + opponent.title() + ", " \
                              "Type [color=pink]!accept[/color])"
                    new_game = 0.5
                    timeout = 60
                    bTimer = True
                    update = True
    else:
        msg = "This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session]."
    return msg, opponent, pOneInfo, new_game, bTimer, playerOne, update

# Use a feat in combat. MUST BE USED BEFORE THE !ROLL COMMAND
# !usefeat <feat>
def message_8_usefeat(channel, charFolder, message, unspoiledArena, character, game, playerOne,
                      playerTwo, token, featToken, pOneInfo, pOneSpentFeat, pTwoSpentFeat, pTwoInfo):
    msg = []
    update = False
    if channel == unspoiledArena:
        # ensures the command can only be used when combat is taking place. To prevent trolls from spamming commands
        if game == 1:
            featToken_new = None
            pOneLastFeat = None
            pTwoLastFeat = None
            pOneFeatInfo = None
            pTwoFeatInfo = None
            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character.lower() == playerOne and token == 1:

                # pull in the feat dictionary from the gameFeats definition.
                featDictionary = featDict()[0]
                if message[9:] != "none":
                    pOneLastFeat = message[9:].lower()
                else:
                    pOneLastFeat = None
                # if the feat is one of the listed below. Tell the player that those feats are used with a different
                # command
                if featToken == 0:
                    if pOneLastFeat in ('power attack', 'defenseive fighting', 'masochist', 'nerve strike',
                                        'improved nerve strike', 'greater nerve strike', 'nerve damage', 'evasion',
                                        'improved evasion', 'greater evasion', 'hurt me', 'improved hurt me',
                                        'greater hurt me', 'hurt me more', 'deflect', 'improved deflect',
                                        'greater deflect', 'cat grace', 'improved cat grace', 'greater cat grace',
                                        'bear endurance', 'improved bear endurance', 'greater bear endurance',
                                        'bull strength', 'improved bull strength', 'greater bull strength'):
                        msg.append(pOneLastFeat + " will be determined elsewhere.")
                        pOneLastFeat = None

                    elif pOneLastFeat in ('crushing blow', 'improved crushing blow', 'greater crushing blow',
                                          'precision strike', 'improved precision strike', 'greater precision strike',
                                          'lightning reflexes', 'improved lightning reflexes',
                                          'greater lightning reflexes', 'centered self'):
                        msg.append(pOneLastFeat + " is already factored into your attack/defense.")
                        pOneLastFeat = None

                    # make sure that a player can't reuse a feat already used.
                    elif pOneLastFeat in pOneSpentFeat:
                        msg.append("You have already used this feat.")

                    # if a feat chosen is on their character sheet, used the feat Dictionary load in the required
                    # information to provide benefits/debuffs.
                    elif pOneLastFeat in pOneInfo['feats taken']:
                        featToken_new = 1
                        # pOneSpentFeat = pOneLastFeat
                        pOneFeatInfo = [pOneLastFeat, featDictionary[0][pOneLastFeat]['action']]
                        msg.append(pOneInfo['name'] + " has used [color=yellow]" + pOneLastFeat +
                                   "[/color]")

                    # If the player doesn't have the feat, he can't use it.
                    elif pOneLastFeat not in pOneInfo['feats taken']:
                        msg.append("Either you do not have that feat, or you did not type it correctly")
                else:
                    msg.append("You've already used a feat for this round.")
                # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
                # spamming commands.
                update = True
            elif character.lower() == playerTwo and token == 2:
                # pull in the feat dictionary from the gameFeats definition.
                featDictionary = featDict()[0]
                if message[9:] != 'none':
                    pTwoLastFeat = message[9:].lower()
                else:
                    pTwoLastFeat = "none"
                if featToken == 0:
                    # if the feat is one of the listed below. Tell the player that those feats are used with a different
                    # command
                    if pTwoLastFeat in ('power attack', 'defenseive fighting', 'masochist', 'nerve strike',
                                        'improved nerve strike', 'greater nerve strike', 'nerve damage', 'evasion',
                                        'improved evasion', 'greater evasion', 'hurt me', 'improved hurt me',
                                        'greater hurt me', 'hurt me more', 'deflect', 'improved deflect',
                                        'greater deflect', 'cat grace', 'improved cat grace', 'greater cat grace',
                                        'bear endurance', 'improved bear endurance', 'greater bear endurance',
                                        'bull strength', 'improved bull strength', 'greater bull strength'):
                        msg.append(pTwoLastFeat + " will be determined elsewhere.")

                    elif pTwoLastFeat in ('crushing blow', 'improved crushing blow', 'greater crushing blow',
                                          'precision strike', 'improved precision strike', 'greater precision strike',
                                          'lightning reflexes', 'improved lightning reflexes',
                                          'greater lightning reflexes', 'centered self', 'improved centered self',
                                          'greater centered self'):
                        msg.append(pTwoLastFeat + " is already factored into your attack/defense.")
                        pOneLastFeat = None
                    # make sure that a player can't reuse a feat already used.
                    elif pTwoLastFeat in pTwoSpentFeat:
                        msg.append("You have already used this feat.")

                    # if a feat chosen is on their character sheet, used the feat Dictionary load in the required
                    # information to provide benefits/debuffs.
                    elif pTwoLastFeat in pTwoInfo['feats taken']:
                        featToken_new = 1
                        # pTwoSpentFeat = pTwoLastFeat
                        pTwoFeatInfo = [pTwoLastFeat, featDictionary[0][pTwoLastFeat]['action']]
                        msg.append(pTwoInfo['name'] + " has used [color=yellow]" + pTwoLastFeat +
                                   "[/color]")

                    # If the player doesn't have the feat, he can't use it.
                    elif pTwoLastFeat not in pTwoInfo['feats taken']:
                        msg.append("Either you do not have that feat, or you did not type it correctly")
                else:
                    msg.append("You've already used a feat this round.")
                update = True
        else:
            msg.append("This command does nothing right now. No combat is taking place.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")

    return msg, featToken_new, pOneLastFeat, pOneFeatInfo, pTwoLastFeat, pTwoFeatInfo, update

# Use to give renown to another player MUST USE PROFILE NAME
# !giverenown <amount> <profile name>
def message_11_giverenown(character, channel, unspoiledBarOOC, renown, gifted, charFolder):
    if channel == unspoiledBarOOC:
        try:
            gifterFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
            gifterData = json.load(gifterFile)
            gifterFile.close()
        # isCharacter = Path(charFolder + character.lower() + ".json")
        except FileNotFoundError:
            msg = character + " does not have a character to use this command."
            return msg
        try:
            giftedFile = open(charFolder + gifted.lower() + ".json", "r", encoding="utf-8")
            giftedData = json.load(giftedFile)
            giftedFile.close()
        # isAlsoharacter = Path(charFolder + gifted.lower() + ".json")
        except FileNotFoundError:
            msg = gifted + " does not have a character to use this command."
            return msg
        # if isCharacter.is_file():
        #     if isAlsoCharacter.is_file():
        if renown > gifterData['renown']:
            msg = "You do not have this much to give."
        else:
            gifterData['renown'] -= renown
            giftedData['renown'] += renown
            msg = gifterData['name'] + " has given " + giftedData['name'] + "[color=yellow] " + str(renown) +\
                "[/color] renown"

        file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
        json.dump(gifterData, file, ensure_ascii=False, indent=2)
        file.close()

        file = open(charFolder + gifted.lower() + ".json", "w", encoding="utf-8")
        json.dump(giftedData, file, ensure_ascii=False, indent=2)
        file.close()
        return msg

# Use to not use the evasion feat for an attack
# !pass
def message_5_pass(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count,
                   token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP,
                   pOneFeatInfo, pTwoFeatInfo, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                   pTwoQuickDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCriple, pOneRelentless,
                   pOneRelentlessDamage, pOneBullrush, pTwoBullrush, pTwoHeal, pTwoCripple, pTwoRelentless,
                   pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneVile, pTwoVile, pOneInner, pTwoInner,
                   pOneBreak, pTwoBreak, iddqd):
    msg = []
    bGameTimer = False
    update = False
    if channel == unspoiledArena:
        if token == 2 and character.lower() == playerOne:
            msg.append(pOneInfo['name'] + " has chosen not to prevent this attack.")

            pOneCurrentHP -= totalDamage

            # If Vile touch is procc'd, do damage here
            if pOneVile != 0 or pTwoVile != 0:
                modifier = []
                if pOneVile or pTwoVile in range(1, 11):
                    pOneCurrentHP, pTwoCurrentHP, modifier = featTwoVileDamage(pOneInfo, pTwoInfo, pOneVile,
                                                                               pTwoVile, pOneCurrentHP,
                                                                               pTwoCurrentHP, modifier, token)
                if pTwoVile != 0:
                    pTwoVile -= 1
                for modifier_item in modifier:
                    msg.append(modifier_item)

            # pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP,
            #                                                                     pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
            #                                                                     token)

            # Apply regeneration
            if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP
            elif token == 2 and pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP:
                msg.append(pTwoInfo['name'] + " has regenerated [color=red]" + str(pTwoInfo['regeneration']) +
                           "[/color] hp.")
                pTwoCurrentHP += pTwoInfo['regeneration']
                if pTwoCurrentHP > pTwoTotalHP:
                    pTwoCurrentHP = pTwoTotalHP

            # Print the scoreboard
            if pOneBullrush == 1:
                name = pOneInfo['name']
            else:
                name = pTwoInfo['name']
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                          " if you wish to use a feat.")
            count += 1
            featToken = 0
            if "bullrush" not in pOneFeatInfo[0]:
                token = 1
            pOnedMod = 0
            pOnemMod = 0
            iddqd = 0
            bGameTimer = True
            pOneFeatInfo = None
            update = True

        elif token == 1 and character.lower() == playerTwo:
            msg.append(pTwoInfo['name'] + " has chosen not to evade this attack.")

            pTwoCurrentHP -= totalDamage

            # If Player's Vile touch is procc'd, do damage here
            if pOneVile != 0 or pTwoVile != 0:
                modifier = []
                if pOneVile or pTwoVile in range(1, 11):
                    pOneCurrentHP, pTwoCurrentHP, modifier = featOneVileDamage(pOneInfo, pTwoInfo, pOneVile,
                                                                               pTwoVile, pOneCurrentHP,
                                                                               pTwoCurrentHP, modifier, token)
                if pTwoVile != 0:
                    pTwoVile -= 1
                for modifier_item in modifier:
                    msg.append(modifier_item)

            # pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP,
            #                                                                     pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
            #                                                                     token)

            # Apply regeneration
            if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP
            elif token == 2 and pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP:
                msg.append(pTwoInfo['name'] + " has regenerated [color=red]" + str(pTwoInfo['regeneration']) +
                           "[/color] hp.")
                pTwoCurrentHP += pTwoInfo['regeneration']
                if pTwoCurrentHP > pTwoTotalHP:
                    pTwoCurrentHP = pTwoTotalHP

            # Print the scoreboard
            if pOneBullrush == 1:
                name = pOneInfo['name']
            else:
                name = pTwoInfo['name']
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                       " if you wish to use a feat.")
            count += 1
            featToken = 0
            pOnepMod = 0
            pOnecMod = 0
            iddqd = 0
            if "bullrush" not in pOneFeatInfo[0]:
                token = 2
            bGameTimer = True
            pOneFeatInfo = None
            update = True
        else:
            msg.append(
                "You are either not in the fight, or it's not your turn. Either way, Don't do it again.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")
    return  msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count, token, critical, bonusHurt,\
            totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOneFeatInfo, pTwoFeatInfo, pOnepMod,\
            pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage, pTwoQuickDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal,\
            pOneCripple, pOneRelentless, pOneRelentlessDamage, pOneBullRush, pTwoBullrush, pTwoHeal, pTwoCripple,\
            pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneVile, pTwoVile, pOneInner,\
            pTwoInner, pOneBreak, pTwoBreak, iddqd, update

# Use to activate evasion for an attack
# !evasion
def message_8_evasion(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count,
                   token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP,
                   pOneFeatInfo, pTwoFeatInfo, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                   pTwoQuickDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCriple, pOneRelentless,
                   pOneRelentlessDamage, pOneBullrush, pTwoBullrush, pTwoHeal, pTwoCripple, pTwoRelentless,
                   pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneVile, pTwoVile, pOneInner, pTwoInner,
                   pOneBreak, pTwoBreak, iddqd):
    msg = []
    bGameTimer = False
    update = False

    if channel == unspoiledArena:
        if token == 2 and character.lower() == playerOne:
            for word in pOneInfo['feats taken']:
                if pOneEvade == 1 and word == "evasion":
                    totalDamage = int(totalDamage * 0.5)
                    pOneEvade = 0
                    msg.append(playerOne + " used [color=yellow]" + word + "[/color],"
                                           " reducing damage taken to [color=red]" + str(totalDamage) + "[/color].")
                elif pOneEvade == 1 and word == "improved evasion":
                    totalDamage = int(totalDamage * 0.25)
                    pOneEvade = 0
                    msg.append(playerOne + " used [color=yellow]" + word + "[/color],"
                                           " reducing damage taken to [color=red]" + str(totalDamage) + "[/color].")
                elif pOneEvade == 1 and word == "greater evasion":
                    totalDamage = 0
                    pOneEvade = 0
                    msg.append(playerOne + " used [color=yellow]" + word + "[/color],"
                                           " reducing damage taken to [color=red]" + str(totalDamage) + "[/color].")

            pOneCurrentHP -= totalDamage

            # If Vile touch is procc'd, do damage here
            if pOneVile != 0 or pTwoVile != 0:
                modifier = []
                if pOneVile or pTwoVile in range(1, 11):
                    pOneCurrentHP, pTwoCurrentHP, modifier = featTwoVileDamage(pOneInfo, pTwoInfo, pOneVile,
                                                                               pTwoVile, pOneCurrentHP,
                                                                               pTwoCurrentHP, modifier, token)
                if pTwoVile != 0:
                    pTwoVile -= 1
                for modifier_item in modifier:
                    msg.append(modifier_item)

            # pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP,
            #                                                                     pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
            #                                                                     token)

            # apply regeneration
            if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # If it is the end of Player Two's turn, and they have regeneration:
            elif token == 2 and pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP:
                msg.append(pTwoInfo['name'] + " has regenerated [color=red]" + str(pTwoInfo['regeneration']) +
                           "[/color] hp.")
                pTwoCurrentHP += pTwoInfo['regeneration']
                if pTwoCurrentHP > pTwoTotalHP:
                    pTwoCurrentHP = pTwoTotalHP

            # Print the scoreboard
            if pOneBullrush == 1:
                name = pOneInfo['name']
            else:
                name = pTwoInfo['name']
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                       " if you wish to use a feat.")
            count += 1
            featToken = 0
            if "bullrush" not in pOneFeatUsed[0]:
                token = 1
            pOnedMod = 0
            pOnemMod = 0
            iddqd = 0
            bGameTimer = True
            pOneFeatused = None
            update = True

        elif token == 1 and character.lower() == playerTwo:
            for word in pTwoInfo['feats taken']:
                if pTwoEvade == 1 and word == "evasion":
                    totalDamage = int(totalDamage * 0.5)
                    pTwoEvade = 0
                    msg.append(playerTwo + " used [color=yellow]" + word + "[/color],"
                               " reducing damage taken to [color=red]" + str(totalDamage) + "[/color].")
                elif pTwoEvade == 1 and word == "improved evasion":
                    totalDamage = int(totalDamage * 0.25)
                    pTwoEvade = 0
                    msg.append(playerTwo + " used [color=yellow]" + word + "[/color],"
                               " reducing damage taken to [color=red]" + str(totalDamage) + "[/color].")
                elif pTwoEvade == 1 and word == "greater evasion":
                    totalDamage = 0
                    pTwoEvade = 0
                    msg.append(playerTwo + " used [color=yellow]" + word + "[/color],"
                               " reducing damage taken to [color=red]" + str(totalDamage) + "[/color].")

            pTwoCurrentHP -= totalDamage

            # If Player's Vile touch is procc'd, do damage here
            if pOneVile != 0 or pTwoVile != 0:
                modifier = []
                if pOneVile or pTwoVile in range(1, 11):
                    pOneCurrentHP, pTwoCurrentHP, modifier = featOneVileDamage(pOneInfo, pTwoInfo, pOneVile,
                                                                               pTwoVile, pOneCurrentHP,
                                                                               pTwoCurrentHP, modifier, token)
                if pTwoVile != 0:
                    pTwoVile -= 1
                for modifier_item in modifier:
                    msg.append(modifier_item)

            # pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP,
            #                                                                     pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
            #                                                                     token)

            # apply regeneration
            if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # If it is the end of Player Two's turn, and they have regeneration:
            elif token == 2 and pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP:
                msg.append(pTwoInfo['name'] + " has regenerated [color=red]" + str(pTwoInfo['regeneration']) +
                           "[/color] hp.")
                pTwoCurrentHP += pTwoInfo['regeneration']
                if pTwoCurrentHP > pTwoTotalHP:
                    pTwoCurrentHP = pTwoTotalHP

            # Print the scoreboard
            if pOneBullrush == 1:
                name = pOneInfo['name']
            else:
                name = pTwoInfo['name']
            msg.append(+ pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                       " if you wish to use a feat.")
            count += 1
            featToken = 0
            pOnepMod = 0
            pOnecMod = 0
            iddqd = 0
            if "bullrush" not in pOneFeatUsed[0]:
                token = 2
            bGameTimer = True
            pOneFeatUsed[0]
            update = True
        else:
            msg.append("You are either not in the fight, or it's not your turn. Either way, Don't do it again.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")
    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count, token, totalDamage,\
           pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,\
           pOneQuickDamage, pTwoQuickDamage, pTwoEvade, pOneEvade, pOneDeathsDoor, pTwoDeathsDoor, pOneTempDR, pTwoTempDR,\
           pOneStoneskin, pTwoStoneskin, pOneVile, pTwoVile, iddqd, pOneInner, pTwoInner, pOneBreak, pTwoBreak, update

# command used to forfeit first strike
# !skip
def message_4_skip(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo, count, token,
                   pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP):
    msg = []
    bGameTimer = True
    update = False
    if token == 1 and character.lower() == playerOne and count == 0:
        msg.append(pOneInfo['name'] + " has been bold enough to forgo first strike.")
        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                   str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                   pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                      " if you wish to use a feat.")
        token = 2
        count += 1
    elif token == 2 and character.lower() == playerTwo and count == 0:
        msg.append(pTwoInfo['name'] + " has been bold enough to forgo first strike.")
        # Print the scoreboard
        msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                   str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                   pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                      " if you wish to use a feat.")
        token = 1
        count += 1
    elif token == 1 and character.lower() == playerOne and count != 0:
        msg.append("Why would you skip your turn now " + pOneInfo['name'] + "? That's just silly. You're silly.")
        token = 1
    elif token == 2 and character.lower() == playerTwo and count != 0:
        msg.append("Why would you skip your turn now " + pTwoInfo['name'] + "? That's just silly. You're silly.")
        token = 2
    return msg, count, token, bGameTimer, update
# depeciated. No long used.
def message_8_deflect(character, channel, unspoiledArena, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken,
                      count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP,
                      pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneQuickDamage,
                      pTwoQuickDamage, pTwoDeflect, pOneDeflect, pOneDeathsDoor, pTwoDeathsDoor):
    msg = []
    bGameTimer = False
    update = False

    if channel == unspoiledArena:
        if token == 2 and character.lower() == playerOne:
            for word in pOneInfo['feats taken']:
                if word == "deflect" and pOneDeflect == 1:
                    pOneDeflect = 0
                    oldDamage = totalDamage
                    totalDamage = int(totalDamage - int(pOneInfo['abac'] + pTwoInfo['armordexterity']))
                    if totalDamage < 1:
                        totalDamage = 1
                    msg.append(pOneInfo['name'] + " used [color=yellow]deflect[/color] "
                               "to lessen the blow from [color=red]" + str(oldDamage) +
                               "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

                elif word == "improved deflect" and pOneDeflect == 1:
                    pOneDeflect = 0
                    oldDamage = totalDamage
                    totalDamage = int(totalDamage - int(pOneInfo['abac'] + pTwoInfo['armordexterity'] * 1.5))
                    if totalDamage < 1:
                        totalDamage = 1
                    msg.append(pOneInfo['name'] + " used [color=yellow]deflect[/color] "
                               "to lessen the blow from [color=red]" + str(oldDamage) +
                               "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

                elif word == "greater deflect" and pOneDeflect == 1:
                    pOneDeflect = 0
                    oldDamage = totalDamage
                    totalDamage = int(totalDamage - int(pOneInfo['abac'] + pTwoInfo['armordexterity'] * 2))
                    if totalDamage < 1:
                        totalDamage = 1
                    msg.append(pOneInfo['name'] + " used [color=yellow]deflect[/color] "
                               "to lessen the blow from [color=red]" + str(oldDamage) +
                               "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

            if pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # Determine if Quick Strike was used by Player One and apply damage
            if pOneQuickDamage != 0:
                pTwoCurrentHP = pTwoCurrentHP - totalDamage - pOneQuickDamage
                pOneQuickDamage = 0
            else:
                pOneCurrentHP = pOneCurrentHP - totalDamage

            if "deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                    and revive <= 50 and pOneDeathsDoor == 0:
                returnHeal = random.randint(5, 10) + int(pOneInfo['constitution'] / 2)
                pOneCurrentHP += returnHeal
                pOneDeathsDoor = 1
                msg.append(
                    pOneInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +
                    "[/color] hit points.")
            elif "improved deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                    and revive <= 75 and pOneDeathsDoor == 0:
                returnHeal = random.randint(5, 15) + int(pOneInfo['constitution'] / 2)
                pOneCurrentHP += returnHeal
                pOneDeathsDoor = 1
                msg.append(
                    pOneInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +
                    "[/color] hit points.")
            elif "greater deaths door" in pOneInfo['feats taken'] and pOneCurrentHP <= 0 \
                    and revive <= 100 and pOneDeathsDoor == 0:
                returnHeal = random.randint(5, 20) + int(pOneInfo['constitution'] / 2)
                pOneCurrentHP += returnHeal
                pOneDeathsDoor = 1
                msg.append(
                    pOneInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +
                    "[/color] hit points.")

            # pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP,
            #                                                                     pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
            #                                                                     token)

            # If it is the end of Player One's turn, and they have regeneration:
            if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # If it is the end of Player Two's turn, and they have regeneration:
            elif token == 2 and pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP:
                msg.append(pTwoInfo['name'] + " has regenerated [color=red]" + str(pTwoInfo['regeneration']) +
                           "[/color] hp.")
                pTwoCurrentHP += pTwoInfo['regeneration']
                if pTwoCurrentHP > pTwoTotalHP:
                    pTwoCurrentHP = pTwoTotalHP

            # Print the scoreboard
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pOneInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                       " if you wish to use a feat.")
            count += 1
            featToken = 0
            token = 1
            pOnedMod = 0
            pOnemMod = 0
            bGameTimer = True

        elif token == 1 and character.lower() == playerTwo:
            for word in pTwoInfo['feats taken']:
                if word == "deflect" and pTwoDeflect == 1:
                    pTwoDeflect = 0
                    oldDamage = totalDamage
                    totalDamage = int(totalDamage - int(pTwoInfo['abac']))
                    if totalDamage < 1:
                        totalDamage = 1
                    msg.append(pTwoInfo['name'] + " used [color=yellow]deflect[/color] "
                               "to lessen the blow from [color=red]" + str(oldDamage) + "[/color] to [color=red]" +
                               str(int(totalDamage)) + "[/color]")

                elif word == "improved deflect" and pTwoDeflect == 1:
                    pTwoDeflect = 0
                    oldDamage = totalDamage
                    totalDamage = int(totalDamage - int(pTwoInfo['abac'] * 1.5))
                    if totalDamage < 1:
                        totalDamage = 1
                    msg.append(pTwoInfo['name'] + " used [color=yellow]deflect[/color] "
                               "to lessen the blow from [color=red]" + str(oldDamage) +
                               "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

                elif word == "greater deflect" and pTwoDeflect == 1:
                    pTwoDeflect = 0
                    oldDamage = totalDamage
                    totalDamage = int(totalDamage - int(pTwoInfo['abac'] * 2))
                    if totalDamage < 1:
                        totalDamage = 1
                    msg.append(pTwoInfo['name'] + " used [color=yellow]deflect[/color] "
                               "to lessen the blow from [color=red]" + str(oldDamage) +
                               "[/color] to [color=red]" + str(int(totalDamage)) + "[/color]")

            # Determine if Quick Strike was used by Player Two and apply damage
            if pTwoQuickDamage != 0:
                pOneCurrentHP = pOneCurrentHP - totalDamage - pTwoQuickDamage
                pOneQuickDamage = 0
            else:
                pTwoCurrentHP = pTwoCurrentHP - totalDamage

            # Check to see if Player has the feat 'death's door', and if it has been triggered already.
            revive = random.randint(1, 100)
            if "deaths door" in pTwoInfo['feats taken'] and pTwoTwoCurrentHP <= 0 \
                    and revive <= 50 and pTwoDeathsDoor == 0:
                returnHeal = random.randint(5, 10) + int(pTwoInfo['constitution'] / 2)
                pTwoCurrentHP += returnHeal
                pTwoDeathsDoor = 1
                msg.append(
                    pTwoInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +
                    "[/color] hit points.")
            elif "improved deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                    and revive <= 75 and pTwoDeathsDoor == 0:
                returnHeal = random.randint(5, 15) + int(pTwoInfo['constitution'] / 2)
                pTwoCurrentHP += returnHeal
                pTwoDeathsDoor = 1
                msg.append(
                    pTwoInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +
                    "[/color] hit points.")
            elif "greater deaths door" in pTwoInfo['feats taken'] and pTwoCurrentHP <= 0 \
                    and revive <= 100 and pTwoDeathsDoor == 0:
                returnHeal = random.randint(5, 20) + int(pTwoInfo['constitution'] / 2)
                pTwoCurrentHP += returnHeal
                pTwoDeathsDoor = 1
                msg.append(
                    pTwoInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +
                    "[/color] hit points.")

            # pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP,
            #                                                                     pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
            #                                                                     token)

            # If it is the end of Player One's turn, and they have regeneration:
            if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # If it is the end of Player Two's turn, and they have regeneration:
            elif token == 2 and pTwoInfo['regeneration'] != 0 and pTwoCurrentHP < pTwoTotalHP:
                msg.append(pTwoInfo['name'] + " has regenerated [color=red]" + str(pTwoInfo['regeneration']) +
                           "[/color] hp.")
                pTwoCurrentHP += pTwoInfo['regeneration']
                if pTwoCurrentHP > pTwoTotalHP:
                    pTwoCurrentHP = pTwoTotalHP

            # Print the scoreboard
            msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                       str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                       str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                       pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                       " if you wish to use a feat.")
            count += 1
            featToken = 0
            pOnepMod = 0
            pOnecMod = 0
            token = 2
            bGameTimer = True
        else:
            msg.append("You are either not in the fight, or it's not your turn. Either way, Don't do it again.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")
    return msg, bGameTimer, playerOne, playerTwo, pOneInfo, pTwoInfo, featToken, count, token, totalDamage,\
        pOneTotalHP, pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod,\
        pOneQuickDamage, pTwoQuickDamage, pTwoDeflect, pOneDeflect

# use to toggle the amount of points spent for power attack. Can be used multiple times to change value.
# !pattack <0-5>
def message_8_pattack(character, channel, unspoiledArena, message, game, playerOne, playerTwo, pOneInfo, pTwoInfo,
                      token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel):
    msg = []
    update = False

    if channel == unspoiledArena:
        # make sure that this command cannot be ran if a fight is taking place.
        try:
            if game == 1:
                # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
                # spamming commands.
                if character.lower() == playerOne and token == 1:
                    if 'power attack' in pOneInfo['feats taken']:
                        mod = int(message[9:])
                        if pOneLevel <= 20 and mod == 0:
                            pOnemMod = 0
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color]")
                        elif pOneLevel <= 20 and mod == 1:
                            pOnepMod = 1
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-1 to hit/+1 to damage)[/color]")
                        elif 4 < pOneLevel <= 20 and mod == 2:
                            pOnepMod = 2
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-2 to hit/+2 to damage)[/color]")
                        elif 8 < pOneLevel <= 20 and mod == 3:
                            pOnepMod = 3
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-3 to hit/+3 to damage)[/color]")
                        elif 12 < pOneLevel <= 20 and mod == 4:
                            pOnepMod = 4
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-4 to hit/+4 to damage)[/color]")
                        elif 16 < pOneLevel <= 20 and mod == 5:
                            pOnepMod = 5
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-5 to hit/+5 to damage)[/color]")
                        else:
                            msg.append("You are not high enough level to invest that many points.")
                    else:
                        msg.append("You have not taken this feat.")
                # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
                # spamming commands.
                elif character.lower() == playerTwo and token == 2:
                    if 'power attack' in pTwoInfo['feats taken']:
                        mod = int(message[9:])
                        if pTwoLevel <= 20 and mod == 0:
                            pTwoMod = 0
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color]")
                        elif pTwoLevel <= 20 and mod == 1:
                            pTwopMod = 1
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-1 to hit/+1 to damage)[/color]")
                        elif 4 < pTwoLevel <= 20 and mod == 2:
                            pTwopMod = 2
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-2 to hit/+2 to damage)[/color]")
                        elif 8 < pTwoLevel <= 20 and mod == 3:
                            pTwopMod = 3
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-3 to hit/+3 to damage)[/color]")
                        elif 12 < pTwoLevel <= 20 and mod == 4:
                            pTwopMod = 4
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-4 to hit/+4 to damage)[/color]")
                        elif 16 < pTwoLevel <= 20 and mod == 5:
                            pTwopMod = 5
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]power attack[/color] "
                                       "[color=pink] (-5 to hit/+5 to damage)[/color]")
                        else:
                            msg.append("You are not high enough level to invest that many points.")
                    else:
                        msg.append("You have not taken this feat.")
                else:
                    msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg.append("This command does nothing right now. No combat is taking place.")
        except ValueError:
            msg.append("Please allocate points to use this ability.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")
    return msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnepMod, pTwopMod, pOneLevel, pTwoLevel

# use to toggle the amount of points spent for defensive fighting. Can be used multiple times to change value.
# !dfight <0-5>
def message_8_dfight(character, channel, unspoiledArena, message, game, playerOne, playerTwo, pOneInfo, pTwoInfo,
                     token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel):
    msg = []
    update = False
    if channel == unspoiledArena:
        # make sure that this command cannot be ran if a fight is taking place.
        try:
            if game == 1:
                # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
                # spamming commands.
                if character.lower() == playerOne and token == 1:
                    if 'defensive fighting' in pOneInfo['feats taken']:
                        mod = int(message[8:])
                        if pOneLevel <= 20 and mod == 0:
                            pOnemMod = 0
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color]")
                        elif pOneLevel <= 20 and mod == 1:
                            pOnedMod = 1
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-1 to damage/+1 to AC)[/color]")
                        elif 4 < pOneLevel <= 20 and mod == 2:
                            pOnedMod = 2
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-1 to damage/+1 to AC)[/color]")
                        elif 8 < pOneLevel <= 20 and mod == 3:
                            pOnedMod = 3
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-3 to damage/+4 to AC)[/color]")
                        elif 12 < pOneLevel <= 20 and mod == 4:
                            pOnedMod = 4
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-4 to damage/+4 to AC)[/color]")
                        elif 16 < pOneLevel <= 20 and mod == 5:
                            pOnedMod = 5
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defenseive fighting[/color] "
                                       "[color=pink] (-5 to damage/+5 to AC)[/color]")
                        else:
                            msg.append("You are not high enough level to invest that many points.")
                    else:
                        msg.append("You do not have this feat.")
                # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
                # spamming commands.
                elif character.lower() == playerTwo and token == 2:
                    if 'defensive fighting' in pTwoInfo['feats taken']:
                        mod = int(message[8:])
                        if pTwoLevel <= 20 and mod == 0:
                            pTwoMod = 0
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color]")
                        elif pTwoLevel <= 20 and mod == 1:
                            pTwodMod = 1
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-1 to damage/+1 to AC)[/color]")
                        elif 4 < pTwoLevel <= 20 and mod == 2:
                            pTwodMod = 2
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-2 to damage/+2 to AC)[/color]")
                        elif 8 < pTwoLevel <= 20 and mod == 3:
                            pTwodMod = 3
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-3 to damage/+3 to AC)[/color]")
                        elif 12 < pTwoLevel <= 20 and mod == 4:
                            pTwodMod = 4
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-4 to damage/+4 to AC)[/color]")
                        elif 16 < pTwoLevel <= 20 and mod == 5:
                            pTwodMod = 5
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]defensive fighting[/color] "
                                       "[color=pink] (-5 to damage/+5 to AC)[/color]")
                        else:
                            msg.append("You are not high enough level to invest that many points.")
                    else:
                        msg.append("You did not take that feat.")
                    update = True
                else:
                    msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
            else:
                msg.append("This command does nothing right now. No combat is taking place.")
        except ValueError:
            msg.append("Please allocate points to use this ability.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")
    return msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnedMod, pTwodMod, pOneLevel, pTwoLevel, update

# def message_8_cexpert(character, channel, unspoiledArena, message, game, playerOne, playerTwo,  pOneInfo, pTwoInfo,
#     token, pOnecMod, pTwocMod, pOneLevel, pTwoLevel):
#     msg = []
#     if channel == unspoiledArena:
#        # make sure that this command cannot be ran if a fight is taking place.
#        try:
#                if game == 1:
#                    # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
#                    # spamming commands.
#                    if character.lower() == playerOne and token == 1:
#                        mod = int(message[9:])
#                        if pOneLevel <= 4 and mod == 1:
#                            pOnecMod = 1
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 4 < pOneLevel <= 8 and mod == 2:
#                            pOnecMod = 2
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 8 < pOneLevel <= 12 and mod == 3:
#                            pOnecMod = 3
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 12 < pOneLevel <= 16 and mod == 4:
#                            pOnecMod = 4
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 16 < pOneLevel <= 20 and mod == 5:
#                            pOnecMod = 5
#                            msg.append(pOneInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        else:
#                            msg.append("You are not high enough level to invest that many points.")
#                    # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
#                    # spamming commands.
#                    elif character.lower() == playerTwo and token == 2:
#                        mod = int(message[9:])
#                        if pTwoLevel <= 4 and mod == 1:
#                            pTwocMod = 1
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 4 < pTwoLevel <= 8 and mod == 2:
#                            pTwocMod = 2
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 8 < pTwoLevel <= 12 and mod == 3:
#                            pTwocMod = 3
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 12 < pTwoLevel <= 16 and mod == 4:
#                            pTwocMod = 4
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        elif 16 < pTwoLevel <= 20 and mod == 5:
#                            pTwocMod = 5
#                            msg.append(pTwoInfo['name'] + " invested [color=red]"
#                                        + str(mod) + "[/color] points in [color=yellow]'combat expertise'[/color]")
#                        else:
#                            msg.append("You are not high enough level to invest that many points.")
#
#                    else:
#                        msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
#                else:
#                    msg.append("This command does nothing right now. No combat is taking place.")
#            except ValueError:
#                msg.append("Please allocate points to use this ability.")
#        else:
#            msg.append("This command is only available in the Arena.")
#        return msg, game, playerOne, playerTwo,  pOneInfo, pTwoInfo, token, pOnecMod, pTwocMod, pOneLevel, pTwoLevel

# use to toggle the amount of points spent for masochist. Can be used multiple times to change value.
# !masochist <0-5>
def message_10_masochist(character, channel, unspoiledArena, message, game, playerOne, playerTwo, pOneInfo, pTwoInfo,
                         token, pOnemMod, pTwomMod, pOneLevel, pTwoLevel):
    msg = []
    update = False
    if channel == unspoiledArena:
        # make sure that this command cannot be ran if a fight is taking place.
        try:
            if game == 1:
                # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
                # spamming commands.
                if character.lower() == playerOne and token == 1:
                    if 'masochist' in pOneInfo['feats taken']:
                        mod = int(message[11:])
                        if pOneLevel <= 20 and mod == 0:
                            pOnemMod = 0
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color]")
                        elif pOneLevel <= 20 and mod == 1:
                            pOnemMod = 1
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-1 AC/+1 to hit)[/color]")
                        elif 4 < pOneLevel <= 20 and mod == 2:
                            pOnemMod = 2
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-2 AC/+2 to hit)[/color]")
                        elif 8 < pOneLevel <= 20 and mod == 3:
                            pOnemMod = 3
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-3 AC/+3 to hit)[/color]")
                        elif 12 < pOneLevel <= 20 and mod == 4:
                            pOnemMod = 4
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-4 AC/+4 to hit)[/color]")
                        elif 16 < pOneLevel <= 20 and mod == 5:
                            pOnemMod = 5
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-5 AC/+5 to hit)[/color]")
                        else:
                            msg.append("You are not high enough level to invest that many points.")
                    else:
                        msg.append("You do not have this feat.")
                # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
                # spamming commands.
                elif character.lower() == playerTwo and token == 2:
                    update = True
                    if 'masochist' in pTwoInfo['feats taken']:
                        mod = int(message[11:])
                        if pTwoLevel <= 20 and mod == 0:
                            pTwomMod = 0
                            msg.append(pOneInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color]")
                        elif pTwoLevel <= 20 and mod == 1:
                            pTwomMod = 1
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-1 AC/+1 to hit)[/color]")
                        elif 4 < pTwoLevel <= 20 and mod == 2:
                            pTwomMod = 2
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-2 AC/+2 to hit)[/color]")
                        elif 8 < pTwoLevel <= 20 and mod == 3:
                            pTwomMod = 3
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-3 AC/+3 to hit)[/color]")
                        elif 12 < pTwoLevel <= 20 and mod == 4:
                            pTwomMod = 4
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-4 AC/+4 to hit)[/color]")
                        elif 16 < pTwoLevel <= 20 and mod == 5:
                            pTwomMod = 5
                            msg.append(pTwoInfo['name'] + " invested [color=red]"
                                       + str(mod) + "[/color] points in [color=yellow]masochist[/color] [color=pink]"
                                       "(-5 AC/+5 to hit)[/color]")
                        else:
                            msg.append("You are not high enough level to invest that many points.")
                    else:
                        msg.append("You do not have this feat.")
                else:
                    msg.append("Either it's not your turn, or you aren't even fighting. Either way, No.")
                update = True
            else:
                msg.append("This command does nothing right now. No combat is taking place.")
        except ValueError:
            msg.append("Please allocate points to use this ability.")
    else:
        msg.append("This command is only available in [session=Unspoiled Desire Arena]adh-abfb9b6ebd20f1e7a693[/session].")
    return msg, game, playerOne, playerTwo, pOneInfo, pTwoInfo, token, pOnemMod, pTwomMod, pOneLevel, pTwoLevel, update