from src.armor_repository import get_armor_dictionary
from src.potion_repository import get_potion_effect_info, get_potion_sell_value
from src.character_repository import character_exists, load_character, save_character
import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# Method to echo private messages to discord
def pri_discord_echo(note):
    with open('room.json', 'r+') as file:
        setWelcome = json.load(file)
        setWelcome['note'] = note
        file.seek(0)
        file.write(json.dumps(setWelcome, ensure_ascii=False, indent=2))
        file.truncate()
        file.close()

#1899

# reset character's ability points, feats, and trait. Ensure that proper allotment of ability points and traits are
# kept. Also ensures that any PERMANENT potions drunk remain.
# !respec
def pri_7_respec(character):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    file = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
    charData = json.load(file)
    file.close()
    reset = charData['reset']
    tFeats = charData['total feats']
    renown = charData['renown']
    if reset != 0:
        reset -= 1
        with open(charFolder + character.lower() + ".json", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData['build'] = ""
            charData['base damage'] = "1d10"
            charData['strength'] = 0
            charData['dexterity'] = 0
            charData['constitution'] = 0
            charData['regeneration'] = 0
            charData['traithit'] = 0
            charData['traitdamage'] = 0
            charData['traitac'] = 0
            charData['traitdr'] = 0
            charData['traithp'] = 0
            charData['traitregen'] = 0
            charData['cursed'] = 0
            charData['initiative'] = 0
            charData['blur'] = 0
            charData['feats taken'] = []
            charData['hfeats taken'] = []
            charData["feathp"] = 0
            charData["feathit"] = 0
            charData["featdamage"] = 0
            charData["featac"] = 0
            charData["dexfighter"] = 0
            charData['remaining feats'] = tFeats
            charData['reset'] = reset
            charData['tdr'] = 0
            charData['trait'] = ""
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
        msg = "your characters abilities, trait, and feats have been reset. Please use [color=pink]!build[/color]" \
              " to select your character's build path, then please use the [color=pink]!stats[/color]" \
              " command to select new Strength, Dexterity, and Constitution, the [color=pink]!traitpick[/color]"\
              " command to pick a new trait, and the [color=pink]!featpick[/color] command to select new feats."\
              " (you have [color=red]" + str(reset) + "[/color] reset points remaining.)"
    elif reset == 0 and renown > 250:
        renown -= 250
        with open(charFolder + character.lower() + ".json", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            charData['build'] = ""
            charData['base damage'] = "1d10"
            charData['strength'] = 0
            charData['dexterity'] = 0
            charData['constitution'] = 0
            charData['regeneration'] = 0
            charData['traithit'] = 0
            charData['traitdamage'] = 0
            charData['traitac'] = 0
            charData['traitdr'] = 0
            charData['traithp'] = 0
            charData['traitregen'] = 0
            charData['cursed'] = 0
            charData['initiative'] = 0
            charData['blur'] = 0
            charData['feats taken'] = []
            charData['hfeats taken'] = []
            charData["feathp"] = 0
            charData["feathit"] = 0
            charData["featdamage"] = 0
            charData["featac"] = 0
            charData["dexfighter"] = 0
            charData['remaining feats'] = tFeats
            charData['reset'] = reset
            charData['tdr'] = 0
            charData['trait'] = ""
            charData['trait'] = ""
            file.seek(0)
            file.write(json.dumps(charData, ensure_ascii=False, indent=2))
            file.truncate()
            file.close()
        msg = "your characters abilities, trait, and feats have been reset. Please use [color=pink]!build[/color]" \
              " to select your character's build path, then please use the [color=pink]!stats[/color]" \
              " command to select new Strength, Dexterity, and Constitution, the [color=pink]!traitpick[/color]"\
              " command to pick a new trait, and the [color=pink]!featpick[/color] command to select new feats."\
              " (As you had no reset points, [color=yellow]250 renown[/color] was taken from your total.)"
    else:
        msg = "You currently have no more reset points to use, or renown to spend."
    return msg

# Set up a character's stats after creation. Stat points MUST equal 15 in total, and no single stat can be above 10
# !stat <str> <dex> <con>
def pri_6_stats(message, character, charData, charFile):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    msg = []
    ap = charData["ap"]
    reset = charData["reset"]
    build = charData["build"]
    level = charData["level"]
    rangeOne = [1, 2, 3, 4]
    rangeTwo = [5, 6, 7, 8, 9]
    rangeThree = [10, 11, 12, 13, 14]
    rangeFour = [15, 16, 17, 18, 19]
    rangeFive = 20
    info = message.split(" ")
    hitMod = 0
    strength = int(info[1])
    dexterity = int(info[2])
    constitution = int(info[3])
    total = strength + dexterity + constitution
    # Find out if player even has a character created yet. If not. Tell them they are an idiot.
    if not character_exists(character, charFolder):
        msg.append("You don't even have a character created yet. Type !name <name> in the room. "
                   "Where <name> is your character's actual name. (Example: !name Joe)")
    # Find out if player has reset points to use. If not. Tell them they are an idiot.
    elif charData['strength'] != 0 and charData['dexterity'] != 0 and charData['constitution'] != 0:
        msg.append("You have already set up your character's stats. If you want to change them, you will "
                   "need to use the [color=pink]!respec[/color] command.")
    # If it turns out, they aren't an idiot, and are using the command correctly. Record information and place
    # it in .json.
    elif build == "":
        msg.append("You need to pick a build path first. Please use the [color=pink]!build[/color] command.")
    else:
        total = strength + dexterity + constitution
        if total > ap or total < ap:
            msg.append("Make sure total points used is no more or less than " +
                       str(ap) + ".")
        elif (strength > 10 or dexterity > 10 or constitution > 10) and charData["level"] in rangeOne:
            msg.append("No one stat can be above 10 at this point in time. Please try again.")
        elif (strength > 11 or dexterity > 11 or constitution > 11) and charData["level"] in rangeTwo:
            msg.append("No one stat can be above 11 at this point in time. Please try again.")
        elif (strength > 12 or dexterity > 12 or constitution > 12) and charData["level"] in rangeThree:
            msg.append("No one stat can be above 12 at this point in time. Please try again.")
        elif (strength > 13 or dexterity > 13 or constitution > 13) and charData["level"] in rangeFour:
            msg.append("No one stat can be above 13 at this point in time. Please try again.")
        elif (strength > 14 or dexterity > 14 or constitution > 14) and charData["level"] == 20:
            msg.append("No one stat can be above 14 at this point in time. Please try again.")
        elif strength < 0 or dexterity < 0 or constitution < 0:
            msg.append("Why would you even try to pick a negative stat? Please try again.")
        else:
            if build == "strength":
                hitMod = int(int(strength) / 2)
                strMod = int(int(strength) / 2)
                dexMod = int(int(dexterity) / 2)
                conMod = int(int(constitution) / 2) * 5
                # rawDamage = "1d12"
            elif build == "dexterity":
                strMod = int(int(strength) / 5)
                dexMod = int(int(dexterity) / 2)
                conMod = int(int(constitution) / 2) * 5
                # rawDamage = "1d6"
            elif build == "constitution":
                strMod = int(int(strength) / 3)
                dexMod = int(int(dexterity) / 2)
                conMod = int(int(constitution) / 2) * 3
                # rawDamage = "1d10"
            # if strenth < 2:
            #     strMod = int(int(strength - strength) - 2)
            # elif dexterity < 2:
            #     dexMod = int(int(dexterity - dexterity) - 2)
            # elif constitution < 2:
            #     conMod = int(int(constitution - constitution) - 10)
            msg.append("Allocating the following: \n\nStrength: " + str(strength) +
                       "   (+" + str(hitMod) + " bonus to hit and " +
                       str(strMod) + " to damage.)\nDexterity: " +
                       str(dexterity) + "   (+" + str(dexMod) + " bonus to armor class.)\n"
                          "Constitution: " + str(constitution) + "   (+" + str(conMod) + " bonus to hit points.)\n")
                          # "And base damage is: " + rawDamage)
            msg.append("The above points have been placed on your character sheet. Please "
                       "type [color=pink]!viewchar[/color] to see your character sheet. "
                       "You need to chose two feats, and a trait as well. Type [color=pink]!featlist[/color] "
                       "to see a list of feats. Type [color=pink]!feathelp <feat name>[/color], "
                       "to get help on a specific feat, or type "
                       "[color=pink]!featpick <feat name>[/color] to choose that feat. To see a list of traits, "
                       "use [color=pink]!traitlist[/color], use [color=pink]!traithelp <trait name>[/color] for its "
                       "description and use [color=pink]!traitpick <trait name>[/color] to select that trait.")
            # load the new data in the character's .json file.
            charData = load_character(character, charFolder)
            charData["strength"] = int(strength)
            charData["dexterity"] = int(dexterity)
            charData["constitution"] = int(constitution)
            charData["abhit"] = strMod
            charData["abdamage"] = strMod
            charData["abac"] = dexMod
            charData["abhp"] = conMod
            charData["initiative"] = dexMod
            save_character(character, charData, charFolder)
    return msg

# !build <strength> <dexterity> <constitution>
def pri_6_build(charFolder, message, charFile, character):
    charData = load_character(character, charFolder)
    baseDamage = charData['base damage']
    # minimum, maximum = baseDamage.split('d')
    # minimum = int(minimum)
    # maximum = int(maximum)
    if charData['build'] == "":
        if message == "strength":
            charData['build'] = message
            if charData['level'] <= 3:
                charData['feats taken'].append("focus")
            # elif charData['level'] <= 12:
            #     charData['feats taken'].append("improved focus")
            # elif charData['level'] <= 15:
            #     charData['feats taken'].append("greater focus")
            # elif charData['level'] <= 18:
            #     charData['feats taken'].append("perfect focus")
            # maximum += 2
            # charData['base damage'] = str(minimum) + "d" + str(maximum)
        elif message == "dexterity":
            charData['build'] = message
            # maximum -= 4
            # charData['base damage'] = str(minimum) + "d" + str(maximum)
        elif message == "constitution":
            charData['build'] = message
        msg = "You have identified your character as a " + message + " build, and it has been recorded as such in your" \
              " character sheet. Please ues [color=pink]!stats[/color] command to select your stat points, before selecting" \
              " feats."
    else:
        msg = "You already have selected a build."

    save_character(character, charData, charFolder)
    return msg

# Automatically adds 1 point to Strength, Dexterity, or Constitution. used only when character reaches 5, 10, 15, or 20
# !add strength, !add dexterity, !add constitution OR !add str, !add dex, !add con
def pri_4_add(message, character):
    msg = []
    ability = message[5:]
    ability.lower()
    answer = ["str", "strength", "dex", "dexterity", "con", "constitution"]
    if ability not in answer:
        msg.append("You need to specify the ability you want to point the point to. "
                   "Type '!add str' or '!add strength' for strength, and so on.")
    else:
        player = character.lower()
        path = os.getcwd()
        charFolder = os.path.join(path + "/characters/")

        charData = load_character(player, charFolder)
        total = charData['apboost']
        if total:
            charData['apboost'] = False
            if ability == "strength" or ability == "str":
                charData['strength'] += 1
                save_character(player, charData, charFolder)
                msg.append("You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] "
                           "to ensure changes.")
            if ability == "dexterity" or ability == "dex":
                charData['dexterity'] += 1
                save_character(player, charData, charFolder)
                msg.append("You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] "
                           "to ensure changes.")
            if ability == "constitution" or ability == "con":
                charData['constitution'] += 1
                save_character(player, charData, charFolder)
                msg.append("You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] "
                           "to ensure changes.")
        else:
            msg.append("You do not have any more ability points to spend.")
    return msg

# Shows character sheet in its entirety.
# !viewchar
def pri_viewchar(character):
    msg = []
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    if not character_exists(character, charFolder):
        msg.append("You don't even have a character created yet. Type !name <name> in the room. "
                   "Where <name> is your character's actual name. (Example: !name Joe")
    else:
        # try:
        charData = load_character(character, charFolder)
        #print(charData['armor']["[url=https://static.f-list.net/images/charimage/21526036.jpg]x-45 agile combat armor[/url]"])
        keyDict = []
        for key in charData['armor']:
            keyDict.append(key)
        armorOne = keyDict[0]
        armorTwo = keyDict[1]
        armorThree = keyDict[2]
        #print(charData['armor'][armorThree])
        armorInvOne = "n/a"
        armorInvTwo = "n/a"
        armorInvThree = "n/a"
        if charData['armor'][armorOne] != "n/a":
            equipprice = int(charData['armor'][armorOne][-1] / 2)
            del charData['armor'][armorOne][-1]
            armorInvOne = ", ".join(charData['armor'][armorOne]) + \
                          " Selling Value: [color=yellow]" + str(equipprice) + "[/color] renown"
        if charData['armor'][armorTwo] != "n/a":
            equipprice = int(charData['armor'][armorTwo][-1] / 2)
            del charData['armor'][armorTwo][-1]
            armorInvTwo = ", ".join(charData['armor'][armorTwo]) +\
                          " Selling Value: [color=yellow]" + str(equipprice) + "[/color] rewnown"
        if charData['armor'][armorThree] != "n/a":
            equipprice = int(charData['armor'][armorThree][-1] / 2)
            del charData['armor'][armorThree][-1]
            armorInvThree = ", ".join(charData['armor'][armorThree]) +\
                            " Selling Value: [color=yellow]" + str(equipprice) + "[/color] renown"
        #print(armorInvThree)
        equip = charData['equip']
        name = charData['name']
        build = charData['build']
        trait = charData['trait']
        level = charData['level']
        hp = charData['hp']
        tFeats = charData['total feats']
        baseDamage = charData['base damage']
        hit = charData['hit']
        damage = charData['damage']
        ac = charData['ac']
        renown = charData['renown']
        xp = charData['currentxp']
        nextLevel = charData['nextlevel']
        baseStrength = charData['strength']
        baseDexterity = charData['dexterity']
        baseConstitution = charData['constitution']
        remainingFeats = charData['remaining feats']
        hasTaken = charData['feats taken']
        hiddenTaken = charData['hfeats taken']
        ap = charData['ap']
        reset = charData['reset']
        wins = charData['wins']
        losses = charData['losses']
        forfeits = charData['forfeits']
        # Ability Bonuses
        abhp = charData["abhp"]
        abhit = charData["abhit"]
        abdamage = charData["abdamage"]
        abac = charData["abac"]
        # Feat Bonuses
        feathp = charData["feathp"]
        feathit = charData["feathit"]
        featdamage = charData["featdamage"]
        featac = charData["featac"]
        dexfighter = charData["dexfighter"]
        # Potion Bonuses
        potionEffect = charData["potioneffect"]
        potionInventory = charData["potions"]
        potionstr = charData["potionstr"]
        potiondex = charData["potiondex"]
        potioncon = charData["potioncon"]
        potionRegen = charData["potionregen"]
        pstrength = charData["pstrength"]
        pdexterity = charData["pdexterity"]
        pconstitution = charData["pconstitution"]
        potionblur = charData["potionblur"]
        potionhp = charData["potionhp"]
        # Armor Bonuses
        armorhit = charData["armorhit"]
        armordamage = charData["armordamage"]
        armorac = charData["armorac"]
        armorhp = charData["armorhp"]
        armordr = charData["armordr"]
        armorstrength = charData["armorstrength"]
        armordexterity = charData["armordexterity"]
        armorconstitution = charData["armorconstitution"]
        armorblur = charData["armorblur"]
        armorinitiative = charData["armorinitiative"]
        # Trait Bonuses
        nblur = charData['blur']
        traitHit = charData['traithit']
        traitDamage = charData['traitdamage']
        traitAC = charData['traitac']
        traitDR = charData['traitdr']
        traitHP = charData['traithp']
        traitRegen = charData['traitregen']
        cursed = charData['cursed']
        ninitiative = charData["initiative"]

        #Total bonuses
        thp = charData["thp"] + charData['potionhp']
        tac = charData["tac"]
        tdr = charData["tdr"]
        thit = charData["thit"]
        tdamage = charData["tdamage"]

        # except:
        #     print("Something above doesn't exist")
        print("What?")

        strength = baseStrength + pstrength + armorstrength + potionstr
        dexterity = baseDexterity + pdexterity + armordexterity + potiondex
        constitution = baseConstitution + pconstitution + armorconstitution + potioncon

        if build == "constitution":
            thp = hp + feathp + armorhp + potionhp + traitHP + int(int(constitution / 2) * 3)
            thit = hit + feathit + armorhit + traitHit - cursed + int((strength + constitution) / 2.4)
            tdamage = damage + featdamage + armordamage - cursed + traitDamage + int(thp / 15) + int(strength / 5)
            ac += 4
            print(thit)
            print(tdamage)
            print(thp)
        elif build == "dexterity":
            thp = hp + feathp + armorhp + potionhp + traitHP + int(int(constitution / 2) * 5)
            thit = hit + feathit + armorhit + traitHit - cursed + int(dexterity / 1.5)
            tdamage = damage + featdamage + armordamage + traitDamage - cursed + int(dexterity / 4) + int(strength / 5)
        else:
            thit = hit + feathit + armorhit + traitHit - cursed + int(strength / 2)
            tdamage = damage + featdamage + armordamage - cursed + traitDamage + int(strength / 1.5)
            thp = hp + feathp + armorhp + potionhp + traitHP + int(int(constitution / 2) * 5)
            ac += 2


        tac = ac + featac + armorac + traitAC - cursed + int(dexterity / 2)
        tdr = armordr + traitDR
        # print("Armor: " + str(amrordr))
        # print("traitDR " + str(traitDR))
        regen = traitRegen + potionRegen
        hasTakenList = ", ".join(hasTaken)
        potionInventoryList = ", ".join(potionInventory)
        blur = potionblur + armorblur + nblur
        initiative = int(dexterity / 2) + armorinitiative

        msg.append("\n" + name + "'s Character Sheet:\n"
                   "𝙲𝚑𝚊𝚛𝚊𝚌𝚝𝚎𝚛 𝙽𝚊𝚖𝚎:\t\t\t\t\t[color=red]" + name + "[/color]\n"
                   "Build:\t\t\t\t\t\t\t[color=red]" + build + "[/color]\n" 
                   "𝚂𝚝𝚛𝚎𝚗𝚐𝚝𝚑:\t\t\t\t\t\t[color=red]" + str(strength) + "[/color]\t\t\t\t\t"
                   "𝙻𝚎𝚟𝚎𝚕:\t\t\t\t\t\t\t[color=red]" + str(level) + "[/color]\n"
                   "𝙳𝚎𝚡𝚝𝚎𝚛𝚒𝚝𝚢:\t\t\t\t\t\t[color=red]" + str(dexterity) + "[/color]\t\t\t\t\t"
                   "𝙰𝚛𝚖𝚘𝚛 𝙲𝚕𝚊𝚜𝚜:\t\t\t\t\t[color=red]" + str(tac) + "[/color]\n"
                   "𝙲𝚘𝚗𝚜𝚝𝚒𝚝𝚞𝚝𝚒𝚘𝚗:\t\t\t\t\t[color=red]" + str(constitution) + "[/color]\t\t\t\t\t"
                   "𝙷𝚒𝚝 𝙿𝚘𝚒𝚗𝚝𝚜:\t\t\t\t\t\t[color=red]" + str(thp) + "[/color]\n"
                   "𝚃𝚘 𝙷𝚒𝚝 𝙼𝚘𝚍𝚒𝚏𝚒𝚎𝚛:\t\t\t\t\t[color=red]" + str(thit) + "[/color]\t\t\t\t\t"
                   "𝚃𝚘𝚝𝚊𝚕 𝙰𝚋𝚒𝚕𝚒𝚝𝚢 𝙿𝚘𝚒𝚗𝚝𝚜:\t\t\t[color=red]" + str(ap) + "[/color]\n"
                   "𝙳𝚊𝚖𝚊𝚐𝚎 𝙼𝚘𝚍𝚒𝚏𝚒𝚎𝚛:\t\t\t\t[color=red]" + str(tdamage) + "[/color]\t\t\t\t\t"
                   "𝙱𝚊𝚜𝚎 𝙳𝚊𝚖𝚊𝚐𝚎:\t\t\t\t\t[color=red]" + str(baseDamage) + "[/color]\n"
                   "𝚁𝚎𝚐𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚘𝚗:\t\t\t\t\t[color=red]" + str(regen) + "[/color]\t\t\t\t\t"
                   "𝙳𝚊𝚖𝚊𝚐𝚎 𝚁𝚎𝚍𝚞𝚌𝚝𝚒𝚘𝚗:\t\t\t\t[color=red]" + str(tdr) + "[/color]\n"
                   "𝚁𝚎𝚜𝚎𝚝:\t\t\t\t\t\t\t[color=red]" + str(reset) + "[/color]\t\t\t\t\t"
                   "𝚃𝚘𝚝𝚊𝚕 𝙵𝚎𝚊𝚝𝚜:\t\t\t\t\t[color=red]" + str(tFeats) + "[/color]\n"
                   "𝚆𝚒𝚗𝚜:\t\t\t\t\t\t\t[color=red]" + str(wins) + "[/color]\t\t\t\t\t"
                   "𝙻𝚘𝚜𝚜𝚎𝚜:\t\t\t\t\t\t\t[color=red]" + str(losses) + "[/color]\n"
                   "Forfeits:\t\t\t\t\t\t\t[color=red]" +str(forfeits) + "[/color]\t\t\t\t\t"                                                                                           
                   "𝚁𝚎𝚗𝚘𝚠𝚗:\t\t\t\t\t\t\t[color=red]" + str(int(renown)) + "[/color]\n"
                   "𝚃𝚛𝚊𝚒𝚝:\t\t\t\t\t\t\t[color=red]" + str(trait) + "[/color]\n"
                   "𝙱𝚕𝚞𝚛:\t\t\t\t\t\t\t[color=red]" + str(blur) + "%[/color]\n"
                   "𝙸𝚗𝚒𝚝𝚒𝚊𝚝𝚒𝚟𝚎 Bonus:\t\t\t\t[color=red]" + str(initiative) + "[/color]\n"
                   "𝙲𝚞𝚛𝚛𝚎𝚗𝚝 𝚇𝙿:\t\t\t\t\t\t[color=red]" + str(xp) + "[/color]\n"
                   "𝚇𝙿 𝚗𝚎𝚎𝚍𝚎𝚍 𝚝𝚘 𝚕𝚎𝚟𝚎𝚕:\t\t\t\t[color=red]" + str(nextLevel) + "[/color]\n"
                   "𝙿𝚘𝚝𝚒𝚘𝚗 𝙸𝚗𝚟𝚎𝚗𝚝𝚘𝚛𝚢:\t\t\t\t[color=red]" + str(potionInventoryList) + "[/color]\n"
                   "𝙿𝚘𝚝𝚒𝚘𝚗 𝙴𝚏𝚏𝚎𝚌𝚝:\t\t\t\t\t[color=red]" + str(potionEffect) + "[/color]\n"
                   "𝙿𝚎𝚛𝚖𝚊𝚗𝚎𝚗𝚝 𝙱𝚘𝚗𝚞𝚜𝚎𝚜 (𝚂𝚝𝚛, 𝙳𝚎𝚡, 𝙲𝚘𝚗)\t[color=red]" + str(pstrength) + ", " +
                   str(pdexterity) + ", " + str(pconstitution) + "[/color]\n" 
                   "𝙰𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝙵𝚎𝚊𝚝𝚜:\t\t\t\t[color=red]" + str(remainingFeats) + "[/color]\n"
                   "𝙵𝚎𝚊𝚝𝚜 𝚃𝚊𝚔𝚎𝚗:\t\t\t\t\t" + hasTakenList + "\n"
                   "𝙰𝚛𝚖𝚘𝚛 𝙸𝚗𝚟𝚎𝚗𝚝𝚘𝚛𝚢:\t\t\t\t\t[color=red] " + armorOne + ": (" + armorInvOne + "), " +
                   armorTwo + ": (" + armorInvTwo + "), " + armorThree + ": (" + armorInvThree + "), [/color]\n"
                   "𝙰𝚛𝚖𝚘𝚛 𝙴𝚚𝚞𝚒𝚙𝚙𝚎𝚍:\t\t\t\t[color=red] " + equip)
        charData['thp'] = thp
        charData['tac'] = tac
        charData['tdr'] = tdr
        charData['thit'] = thit
        charData['tdamage'] = tdamage
        charData['initiative'] = initiative
        charData['regeneration'] = regen
        save_character(character, charData, charFolder)
    return msg

# shows every single character in the game that is the level selected
# !wholevel 3
def pri_9_wholevel(character, message):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    files = os.listdir(charFolder)

    profile = []
    response = []
    msg = []
    with open(charFolder + "playerDatabase.json", 'r', encoding="utf-8") as file2:
        playerDatabase = json.loads(file2.read())
        file2.close()

    for item in playerDatabase.items():
        name = item[1]
        profile.append(name)
    levelList = {}
    for player in profile:
        with open(charFolder + player + ".json", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            file.close()
        name = player
        level = charData['level']
        levelList[name] = level
    msg.append("Level " + str(message[10:] + " characters:"))
    for key, value in levelList.items():
        if value == int(message[10:]):
            response.append(key)
    stringResponse = "\n" + "\n".join(response)
    msg.append(stringResponse)
    return msg

# select a starting trait for character
# !traitpick <trait>
def pri_6_trait(character, message, traitList, traitDictionary, trait):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    # try:
    charSheet = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
    charData = json.load(charSheet)
    charSheet.close()
    regeneration = charData['traitregen']
    brawler = charData['traithit']
    thug = charData['traitdamage']
    nimble = charData['traitac']
    hearty = charData['traithp']
    thickskinned = charData['traitdr']
    opportunist = charData['initiative']
    nebulous = charData['blur']
    strength = charData['strength']
    dexterity = charData['dexterity']
    constitution = charData['constitution']
    # ap = charData['ap']
    # regeneration = charData['regeneration']
    # print("why?")
    # initiative = charData['initiative']
    # blur = charData['blur']
    # except:
    #     pass
    if charData['trait'] != "":
        msg = "You've already selected a trait. If you wish to change it, you must !respec if you have the points."
    elif strength >= 0 and dexterity >= 0 and constitution >= 0:
        with open(charFolder + character.lower() + ".json", "r+", encoding="utf-8") as file:
            charData = json.load(file)
            if trait in traitList:
                level = charData['level']
                charData['trait'] = trait
                if trait == 'cursed' and level in range(1, 5):
                    cursed = traitDictionary[0]["cursed"]["bonus"][0]
                    charData['cursed'] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == 'cursed'and level in range(5, 10):
                    cursed = traitDictionary[0]["cursed"]["bonus"][1]
                    charData['cursed'] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == 'cursed'and level in range(10, 15):
                    cursed = traitDictionary[0]["cursed"]["bonus"][2]
                    charData['cursed'] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == 'cursed'and level in range(15, 20):
                    cursed = traitDictionary[0]["cursed"]["bonus"][3]
                    charData['cursed'] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == 'cursed'and level == 20:
                    cursed = traitDictionary[0]["cursed"]["bonus"][4]
                    charData['cursed'] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                if charData['tdr'] == 0:
                    if trait == 'regeneration' and level in range(1, 5):
                        regeneration = traitDictionary[0]["regeneration"]["bonus"][0]
                        charData['traitregen'] = regeneration
                        msg = "The trait Regeneration' has been added to your character sheet."
                    elif trait == 'regeneration'and level in range(5, 10):
                        regeneration = traitDictionary[0]["regeneration"]["bonus"][1]
                        charData['traitregen'] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                    elif trait == 'regeneration' and level in range(10, 15):
                        regeneration = traitDictionary[0]["regeneration"]["bonus"][2]
                        charData['traitregen'] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                    elif trait == 'regeneration' and level in range(15, 20):
                        regeneration = traitDictionary[0]["regeneration"]["bonus"][3]
                        charData['traitregen'] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                    elif trait == 'regeneration' and level == 20:
                        regeneration = traitDictionary[0]["regeneration"]["bonus"][4]
                        charData['traitregen'] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                else:
                    msg = "You can not take regeneration as you have a non-zero value for Damage Reduction"
                if trait == 'brawler' and level in range(1, 5):
                    brawler = traitDictionary[0]["brawler"]["bonus"][0]
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'brawler' and level in range(5, 10):
                    brawler = traitDictionary[0]["brawler"]["bonus"][1]
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'bralwer' and level in range(10, 15):
                    brawler = traitDictionary[0]["brawler"]["bonus"][2]
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'brawler' and level in range(15, 20):
                    brawler = traitDictionary[0]["brawler"]["bonus"][3]
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == 'brawler' and level == 20:
                    brawler = traitDictionary[0]["brawler"]["bonus"][4]
                    charData['traithit'] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                if trait == 'thug' and level in range(1, 5):
                    thug = traitDictionary[0]["thug"]["bonus"][0]
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level in range(5, 10):
                    thug = traitDictionary[0]["thug"]["bonus"][1]
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level in range(10, 15):
                    thug = traitDictionary[0]["thug"]["bonus"][2]
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug' and level in range(15, 20):
                    thug = traitDictionary[0]["thug"]["bonus"][3]
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == 'thug'  and level == 20:
                    thug = traitDictionary[0]["thug"]["bonus"][4]
                    charData['traitdamage'] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                if trait == 'hearty' and level in range(1, 5):
                    hearty = traitDictionary[0]["hearty"]["bonus"][0]
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level in range(5, 10):
                    hearty = traitDictionary[0]["hearty"]["bonus"][1]
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level in range(10, 15):
                    hearty = traitDictionary[0]["hearty"]["bonus"][2]
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty' and level in range(15, 20):
                    hearty = traitDictionary[0]["hearty"]["bonus"][3]
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == 'hearty'  and level == 20:
                    hearty = traitDictionary[0]["hearty"]["bonus"][4]
                    charData['traithp'] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                if trait == 'nimble' and level in range(1, 5):
                    nimble = traitDictionary[0]["nimble"]["bonus"][0]
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level in range(5, 10):
                    nimble = traitDictionary[0]["nimble"]["bonus"][1]
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level in range(10, 15):
                    nimble = traitDictionary[0]["nimble"]["bonus"][2]
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level in range(15, 20):
                    nimble = traitDictionary[0]["nimble"]["bonus"][3]
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == 'nimble' and level == 20:
                    nimble = traitDictionary[0]["nimble"]["bonus"][4]
                    charData['traitac'] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                if charData['regeneration'] == 0:
                    if trait == 'thickskinned' and level in range(1, 5):
                        thickskinned = traitDictionary[0]["thickskinned"]["bonus"][0]
                        charData['traitdr'] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == 'thickskinned'and level in range(5, 10):
                        thickskinned = traitDictionary[0]["thickskinned"]["bonus"][1]
                        charData['traitdr'] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == 'thickskinned' and level in range(10, 15):
                        thickskinned = traitDictionary[0]["thickskinned"]["bonus"][2]
                        charData['traitdr'] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == 'thickskinned' and level in range(15, 20):
                        thickskinned = traitDictionary[0]["thickskinned"]["bonus"][3]
                        charData['traitdr'] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == 'thickskinned' and level == 20:
                        thickskinned = traitDictionary[0]["thickskinned"]["bonus"][4]
                        charData['traitdr'] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                else:
                    msg = "You can not take thickskinned as you have a non-zero value for regeneration"
                if trait == 'opportunist' and level in range(1, 5):
                    opportunist = traitDictionary[0]["opportunist"]["bonus"][0]
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level in range(5, 10):
                    opportunist = traitDictionary[0]["opportunist"]["bonus"][1]
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level in range(10, 15):
                    opportunist = traitDictionary[0]["opportunist"]["bonus"][2]
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level in range(15, 20):
                    opportunist = traitDictionary[0]["opportunist"]["bonus"][3]
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == 'opportunist' and level == 20:
                    opportunist = traitDictionary[0]["opportunist"]["bonus"][4]
                    charData['initiative'] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                if trait == 'nebulous' and level in range(1, 5):
                    nebulous = traitDictionary[0]["nebulous"]["bonus"][0]
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level in range(5, 10):
                    nebulous = traitDictionary[0]["nebulous"]["bonus"][1]
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level in range(10, 15):
                    nebulous = traitDictionary[0]["nebulous"]["bonus"][2]
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level in range(15, 20):
                    nebulous = traitDictionary[0]["nebulous"]["bonus"][3]
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == 'nebulous' and level == 20:
                    nebulous = traitDictionary[0]["nebulous"]["bonus"][4]
                    charData['blur'] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()
            elif trait not in traitList:
                msg = message + " is not a trait. Please use [color=pink]!traitlist[/color] for a list ot traits."
            else:
                msg = "You need to set up your stats first, before selecting a trait. please use the !stats command."
    return msg

# select a feat when a feat slot is available
# !featpick <feat>
def pri_10_feat_pick(character, message, featList, featDictionary):
    msg = []
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    charFile = Path(charFolder + character.lower() + ".json")
    try:
        charSheet = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        charData = json.load(charSheet)
        charSheet.close()
        name = charData['name']
        level = charData['level']
        build = charData['build']
        hp = charData['hp']
        tFeats = charData['total feats']
        baseDamage = charData['base damage']
        hit = charData['hit']
        damage = charData['damage']
        ac = charData['ac']
        xp = charData['currentxp']
        nextLevel = charData['nextlevel']
        strength = charData['strength']
        dexterity = charData['dexterity']
        constitution = charData['constitution']
        remainingFeats = charData['remaining feats']
        hasTaken = charData['feats taken']
        hiddenTaken = charData['hfeats taken']
        ap = charData['ap']
        reset = charData['reset']
        wins = charData['wins']
        losses = charData['losses']
        abhp = charData["abhp"]
        abhit = charData["abhit"]
        abdamage = charData["abdamage"]
        abac = charData["abac"]
        feathp = charData["feathp"]
        feathit = charData["feathit"]
        featdamage = charData["featdamage"]
        featac = charData["featac"]
        dexfighter = charData["dexfigher"]
        thp = charData["thp"]
        tac = charData["tac"]
        thit = charData["thit"]
        tdamage = charData["tdamage"]
    except:
        pass
    total = strength + dexterity + constitution
    toggleFeat = ["defensive fighting", "power attack", "masochist"]
    strOnly = ["hurt me", "improved hurt me", "greater hurt me", "hurt me more", "bullrush",
               "improved bullrush", "greater bullrush"]
    dexOnly = ["evasion", "improved evasion", "greater evasion", "cheap shot", "improved cheap shot",
               "greater cheap shot"]
    conOnly = ["deaths door", "improved deaths door", "greater deaths door", "inner strength",
               "improved inner strength", "greater inner strength"]
    nope = ["focus", "improved focus", "greater focus", "perfect focus"]
    answer = message[10:].lower()
    # Check to see if they even have an open feat slot to fill. If not, they are an idiot.
    if total < ap:
        msg.append("Please select your character stats with the [color=pink]!stats[/color] command first.")
    # Check to see if they even have an open feat slot to fill. If not, they are an idiot.
    elif (answer in strOnly and build != "strength"
        or answer in dexOnly and build != "dexterity"
        or answer in conOnly and build != "constitution"):
        msg.append("This feat is not available for your build choice.")
    elif answer in toggleFeat and ("defensive fighting" in hasTaken or
                                     "power attack" in hasTaken or
                                     "masochist" in hasTaken):
      msg.append("You can not take more than one toggle feat. You already have either [color=yellow]Power "
                 "Attack[/color], [color=yellow]Defensive Fighting[/color], or [color=yellow]Masochist[/color].")
    elif answer in nope:
        msg.append("This feat is given to strength builds automatically at levels 3/9/15/18, and can not be taken "
                   "in any other fashion")
    elif charData["remaining feats"] == 0:
        msg.append("You have no feat slots left to select a new feat")
        # Check to see if they are not taking a feat that is weaker than the one they already have.
        # if it is, they are an idiot.
    elif answer in hiddenTaken:
        msg.append("Why are you trying to take a weaker feat than the one you already have? No.")
    # Check to see if the feat they want is even spelled correctly, or is a feat at all. If not, they are an
    # idiot.
    elif answer not in featList:
        msg.append("Make sure you have spelled the feat correctly")
    # If they do have a slot available, and they spelled it right. Congratulations, not an idiot.
    else:
        reqLevel = featDictionary[0][answer]['requirements'][0]
        reqStr = featDictionary[0][answer]['requirements'][1]
        reqDex = featDictionary[0][answer]['requirements'][2]
        reqCon = featDictionary[0][answer]['requirements'][3]
        reqFeats = featDictionary[0][answer]['requirements'][4]
        # Check to see if they meet the required level for chosen feat. If not, they are an idiot.
        if reqLevel > level:
            msg.append("You are not the required level for this feat.")
        # Check to see if they meet the required strength for chosen feat. If not, they are an idiot.
        # elif reqStr > strength - charData['armorstrength']:
        #     msg.append("You do not have the required strength for this feat.")
        # # Check to see if they meet the required dexterity for chosen feat. If not, they are an idiot.
        # elif reqDex > dexterity - charData['armordexterity']:
        #     msg.append("You do not have the required dexterity for this feat.")
        # # Check to see if they meet the required constitution for chosen feat. If not, they are an idiot.
        # elif reqCon > constitution - charData['armorconstitution']:
        #     msg.append("You do not have the required constitution for this feat.")
        # # Check to see if they meet the required prerequisites for chosen feat. If not, they are an idiot.
        elif reqFeats not in hasTaken and reqFeats != "none":
            msg.append("You do hot have the required prerequisites to take this feat.")
        # If they passed all the above checks: Congratulations, not an idiot.
        elif answer not in hasTaken:
            msg.append(answer + " has been added to your character sheet.")
            msg.append("Make sure you use [color=pink]!viewchar[/color] to ensure you are "
                       "obtaining proper bonuses during fights.")
            remainingFeats -= 1
            hiddenTaken.append(answer)
            hasTaken.append(answer)

            # Since there are a lot of passive feats. Let's just apply those permanent bonuses here, and be done
            # with it. Feats that are a part of a 'feat tree' (Example: crushing blow, improved crushing blow,
            # and greater crushing blow) do NOT stack. So this ensures previous feat is 'popped out' of list
            # of feats taken, and replaced with upgraded feat.

            with open(charFolder + character.lower() + ".json", "r+", encoding="utf-8") as file:
                charData = json.load(file)
                switchHit = 0
                acMod = 0
                damageMod = 0
                hitMod = 0
                hpMod = 0
                dr = 0

                if answer == "bull strength":
                    charData['strength'] = charData['strength'] + 2
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                if answer == "improved bull strength":
                    charData['strength'] = charData['strength'] + 2
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                    index = hasTaken.index("bull strength")
                    hasTaken.pop(index)
                if answer == "greater bull strength":
                    charData['strength'] = charData['strength'] + 2
                    charData['abhit'] = int(charData['strength'] / 2)
                    charData['abdamage'] = int(charData['strength'] / 2)
                    index = hasTaken.index("improved bull strength")
                    hasTaken.pop(index)

                if answer == "cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                if answer == "improved cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                    index = hasTaken.index("cat grace")
                    hasTaken.pop(index)
                if answer == "greater cat grace":
                    charData['dexterity'] = charData['dexterity'] + 2
                    charData['abac'] = int(charData['dexterity'] / 2)
                    index = hasTaken.index("improved cat grace")
                    hasTaken.pop(index)

                if answer == "bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                if answer == "improved bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                    index = hasTaken.index("bear endurance")
                    hasTaken.pop(index)
                if answer == "greater bear endurance":
                    charData['constitution'] = charData['constitution'] + 2
                    charData['abhp'] = charData['abhp'] + 5
                    index = hasTaken.index("improved bear endurance")
                    hasTaken.pop(index)

                if answer == "crushing blow":
                   damageMod = 2
                   charData["featdamage"] += damageMod
                if answer == "improved crushing blow":
                    damageMod = 2
                    charData["featdamage"] += damageMod
                    index = hasTaken.index("crushing blow")
                    hasTaken.pop(index)
                if answer == "greater crushing blow":
                    damageMod = 2
                    charData["featdamage"] += damageMod
                    index = hasTaken.index("improved crushing blow")
                    hasTaken.pop(index)

                if answer == "precision strike":
                    hitMod = 2
                    charData["feathit"] += hitMod
                if answer == "improved precision strike":
                    damageMod = 2
                    charData["feathit"] += damageMod
                    index = hasTaken.index("precision strike")
                    hasTaken.pop(index)
                if answer == "greater precision strike":
                    damageMod = 2
                    charData["feathit"] += damageMod
                    index = hasTaken.index("improved precision strike")
                    hasTaken.pop(index)

                if answer == "lightning reflexes":
                    acMod = 2
                    charData["featac"] += acMod
                if answer == "improved lightning reflexes":
                    acMod = 2
                    charData["featac"] += acMod
                    index = hasTaken.index("lightning reflexes")
                    hasTaken.pop(index)
                if answer == "greater lightning reflexes":
                    acMod = 2
                    charData["featac"] += acMod
                    index = hasTaken.index("improved lightning reflexes")
                    hasTaken.pop(index)

                # if answer == "endurance":
                #     hpMod = 5
                #     charData["feathp"] += hpMod
                # if answer == "quickling":
                #     initiative = 4
                #     charData["initiative"] += initiative
                # if answer == "metabolic":
                #     hpMod = 15
                #     charData["feathp"] += hpMod

                if answer == "improved crippling blow":
                    index = hasTaken.index("crippling blow")
                    hasTaken.pop(index)
                if answer == "greater crippling blow":
                    index = hasTaken.index("improved crippling blow")
                    hasTaken.pop(index)
                if answer == "staggering blow":
                    index = hasTaken.index("greater crippling blow")
                    hasTaken.pop(index)

                if answer == "improved evasion":
                    index = hasTaken.index("evasion")
                    hasTaken.pop(index)
                if answer == "greater evasion":
                    index = hasTaken.index("improved evasion")
                    hasTaken.pop(index)

                if answer == "improved quick strike":
                    index = hasTaken.index("quick strike")
                    hasTaken.pop(index)
                if answer == "greater quick strike":
                    index = hasTaken.index("improved quick strike")
                    hasTaken.pop(index)
                if answer == "riposte":
                    index = hasTaken.index("greater quick strike")
                    hasTaken.pop(index)

                if answer == "improved deflect":
                    index = hasTaken.index("deflect")
                    hasTaken.pop(index)
                if answer == "greater deflect":
                    index = hasTaken.index("improved deflect")
                    hasTaken.pop(index)

                if answer == "improved hurt me":
                    index = hasTaken.index("hurt me")
                    hasTaken.pop(index)
                if answer == "greater hurt me":
                    index = hasTaken.index("improved hurt me")
                    hasTaken.pop(index)
                if answer == "hurt me more":
                    index = hasTaken.index("greater hurt me")
                    hasTaken.pop(index)

                if answer == "improved reckless abandon":
                    index = hasTaken.index("reckless abandon")
                    hasTaken.pop(index)
                if answer == "greater reckless abandon":
                    index = hasTaken.index("improved reckless abandon")
                    hasTaken.pop(index)

                if answer == "improved deaths door":
                    index = hasTaken.index("deaths door")
                    hasTaken.pop(index)
                if answer == "greater deaths door":
                    index = hasTaken.index("improved deaths door")
                    hasTaken.pop(index)
                
                if answer == "improved lifeleech":
                    index = hasTaken.index("life leech")
                    hasTaken.pop(index)
                if answer == "greater lifeleech":
                    index = hasTaken.index("improved life leech")
                    hasTaken.pop(index)
                if answer == "lifedrain":
                    index = hasTaken.index("greater life leech")
                    hasTaken.pop(index)

                if answer == "improved vile touch":
                    index = hasTaken.index("vile touch")
                    hasTaken.pop(index)
                if answer == "greater vile touch":
                    index = hasTaken.index("improved vile touch")
                    hasTaken.pop(index)
                if answer == "death touch":
                    index = hasTaken.index("greater vile touch")
                    hasTaken.pop(index)

                if answer == "improved heavy hand":
                    index = hasTaken.index("heavy hand")
                    hasTaken.pop(index)
                if answer == "greater heavy hand":
                    index = hasTaken.index("improved heavy hand")
                    hasTaken.pop(index)

                charData["feats taken"] = hasTaken
                charData["hfeats taken"] = hiddenTaken
                charData["remaining feats"] = remainingFeats
                file.seek(0)
                file.write(json.dumps(charData, ensure_ascii=False, indent=2))
                file.truncate()
                file.close()

    return msg

# DEVELOPER USE ONLY - Stocks the store with 20 new potions. Potions can stack
def pri_10_stockpotion(commonList, uncommonList, rareList, vrareList, relicList):
    potionFile = open("potions.json", "r+", encoding="utf-8")
    potionDictionary = json.load(potionFile)
    potionDictionary[0]['shoplist'] = []
    for num in range(1, 21):
        number = random.randint(1, 100)
        # 98-100 (3% chance)
        if number in range(98, 101):
            relicPotion = len(relicList)
            index = random.randint(1, (relicPotion - 1))
            chosenPotion = relicList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        # 90-97 (8% chance)
        elif number in range(90, 98):
            vrarePotion = len(vrareList)
            index = random.randint(1, (vrarePotion - 1))
            chosenPotion = vrareList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        # 77-89 (13% chance)
        elif number in range(77, 90):
            rarePotion = len(rareList)
            index = random.randint(1, (rarePotion - 1))
            chosenPotion = rareList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        # 51-76 (26% chance)
        elif number in range(51, 77):
            uncommonPotion = len(uncommonList)
            index = random.randint(1, (uncommonPotion - 1))
            chosenPotion = uncommonList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
        # 1-50 (50% chance)
        elif number in range(1, 51):
            commonPotion = len(commonList)
            index = random.randint(1, (commonPotion - 1))
            chosenPotion = commonList[index]
            potionDictionary[0]['shoplist'].append(chosenPotion)
    shopString = ", ".join(potionDictionary[0]['shoplist'])
    potionFile.seek(0)
    potionFile.write(json.dumps(potionDictionary, ensure_ascii=False, indent=2))
    potionFile.truncate()
    potionFile.close()

    msg = "Shop stocked for the week as follows: \n" + shopString
    return msg, shopString

# Use to buy a potion
# !buypotion <potion name>
def pri_10_buypotion(character, potion, charFolder):
    potionFile = open("potions.json", "r", encoding="utf-8")
    potionData = json.load(potionFile)
    potionFile.close()

    try:
        charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You don't have a character made to use this function."

    potionList = potionData[0]['shoplist']
    buyer = charSheet['name']
    print(potionList)
    price = 0
    if isCharacter.is_file():
        if potion in potionList:
            if potion in potionData[0]['common']:
                price += potionData[0]['common'][potion][0]
            elif potion in potionData[0]['uncommon']:
                price += potionData[0]['uncommon'][potion][0]
            elif potion in potionData[0]['rare']:
                price += potionData[0]['rare'][potion][0]
            elif potion in potionData[0]['vrare']:
                price += potionData[0]['vrare'][potion][0]
            elif potion in potionData[0]['relic']:
                price += potionData[0]['relic'][potion][0]
            if price <= charSheet['renown']:
                if len(charSheet['potions']) >= 5:
                    msg = "You do not have enough inventory space to own more potions."
                else:
                    charSheet['renown'] -= price
                    potionData[0]['shoplist'].remove(potion)
                    charSheet['potions'].append(potion)
                    msg = charSheet['name'] + " has puchased a potion of " + potion + "."
            else:
                msg = "You do not have enough renown to purchase this."
        else:
            msg = "You can not buy that potion, as it is not being sold right now."

    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()

    file = open("potions.json", "w", encoding="utf-8")
    json.dump(potionData, file, ensure_ascii=False, indent=2)
    file.close()

    return msg, buyer, potion

# Use to sell a potion
# !sellpotion <potion name>
def pri_11_sellpotion(character, potion, charFolder):

    try:
        sellerFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        sellerData = json.load(sellerFile)
        sellerFile.close()
    # isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You do not have a character to use this command."

    if potion in sellerData['potions']:
        halfPrice = get_potion_sell_value(potion)

        if halfPrice is not None:
            sellerData['renown'] += halfPrice
            sellerData['potions'].remove(potion)
            msg = sellerData['name'] + " has sold a [color=red]" + potion + "[/color] for [color=yellow]" + \
                  str(halfPrice) + " renown[/color]."
        else:
            msg = "That potion does not exist in the potion data."
    else:
        msg = "You do not have that potion to sell."

    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(sellerData, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# use to use a potion
# !usepotion <potion name>
def pri_10_usepotion(character, potion, commonList, uncommonList, rareList,
                         vrareList, relicList, charFolder):
    try:
        charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You don't have a character made to use these potions."
        return msg
    print("in potion method")
    potionList = commonList + uncommonList + rareList + vrareList + relicList
    print("in potion method")
    potionInfo = get_potion_effect_info(potion)

    if potionInfo is not None:
        potionEffect, potionDescription = potionInfo

        if potion == "str1" and charSheet['pstrength'] == 0:
            charSheet['pstrength'] = 1
            msg = charSheet['name'] + " drank a " + potion + \
                " potion, obtaining a permanent [color=red] +1 to strength[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "dex1" and charSheet['pdexterity'] == 0:
            charSheet['pdexterity'] = 1
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to dexterity[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "con1" and charSheet['pconstitution'] == 0:
            charSheet['pconstitution'] = 1
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to constitution[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "str2" and charSheet['pstrength'] == 1:
            charSheet['pstrength'] = 2
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to strength[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "dex2" and charSheet['pdexterity'] == 1:
            charSheet['pdexterity'] = 2
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to dexterity[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "con2" and charSheet['pconstitution'] == 1:
            charSheet['pconstitution'] = 2
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to constitution[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "str3" and charSheet['pstrength'] == 2:
            charSheet['pstrength'] = 3
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to strength[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "dex3" and charSheet['pdexterity'] == 2:
            charSheet['pdexterity'] = 3
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to dexterity[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "con3" and charSheet['pconstitution'] == 2:
            charSheet['pconstitution'] = 3
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to constitution[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "str4" and charSheet['pstrength'] == 3:
            charSheet['pstrength'] = 4
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to strength[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "dex4" and charSheet['pdexterity'] == 3:
            charSheet['pdexterity'] = 4
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to dexterity[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "con4" and charSheet['pconstitution'] == 3:
            charSheet['pconstitution'] = 4
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to constitution[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "str5" and charSheet['pstrength'] == 4:
            charSheet['pstrength'] = 5
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to strength[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "dex5" and charSheet['pdexterity'] == 4:
            charSheet['pdexterity'] = 5
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to dexterity[/color]"
            charSheet['potions'].remove(potion)
        elif potion == "con5" and charSheet['pconstitution'] == 4:
            charSheet['pconstitution'] = 5
            msg = charSheet['name'] + " drank a " + potion +\
                " potion, obtaining a permanent [color=red] +1 to constitution[/color]"
            charSheet['potions'].remove(potion)
        else:
            msg = "You can not drink this potion, as it is either too powerful or too weak to use right now."
        if potion == "respec":
            charSheet['reset'] += 1
            msg = charSheet['name'] + " drank a " + potion + " potion. Allowing them a chance to change their " \
                "feats, traits, and stat points."
            charSheet['potions'].remove(potion)
        elif potion == "stimulant":
            charSheet['remaining feats'] += 1
            charSheet['total feats'] += 1
            msg = charSheet['name'] + " drank a " + potion + " potion. Allowing them to learn a new feat they " \
                "qualify for."
            charSheet['potions'].remove(potion)
        elif charSheet['potioneffect'] == "":
            if potion[:3] == "hit":
                charSheet['potionhit'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" +\
                    potionDescription + "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:6] == "damage":
                charSheet['potiondamage'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + "drank a " + potion + " potion, [color=red]" + potionDescription +\
                    "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:2] == "ac":
                charSheet['potionac'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" + potionDescription +\
                    "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:4] == "tstr":
                charSheet['potionstr'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" +\
                    potionDescription + "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:4] == "tdex":
                charSheet['potiondex'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" +\
                    potionDescription + "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:4] == "tcon":
                charSheet['potioncon'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" +\
                    potionDescription + "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:2] == "hp":
                charSheet['potionhp'] = potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" +\
                    potionDescription + "[/color] for next match."
                charSheet['potions'].remove(potion)
            elif potion[:2] == "bl":
                charSheet['potionblur'] += potionEffect
                charSheet['potioneffect'] = potionDescription
                msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" + \
                      potionDescription + " for next match."
                charSheet['potions'].remove(potion)
            elif potion[:2] == "re":
                if charSheet['traitdr'] == 0 or charSheet['armordr'] == 0 or charSheet['regeneration'] == 0:
                    charSheet['potionregen'] += potionEffect
                    charSheet['potioneffect'] = potionDescription
                    msg = charSheet['name'] + " drank a " + potion + " potion, [color=red]" + \
                          potionDescription + " for next match."
                else:
                    msg = charSheet['name'] + " gains no benefit from this potion."
        else:
            msg = "You already have a potion in effect."
    else:
        msg = "You do not have a potion of " + potion

    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# !givepotion <potion name> <player>
def pri_11_givepotion(character, item, gifted, charFolder):
    try:
        gifterFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        gifterData = json.load(gifterFile)
        gifterFile.close()
    # isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You do not have a character to use this command."
        return msg
    try:
        giftedFile = open(charFolder + gifted.lower() + ".json", "r", encoding="utf-8")
        giftedData = json.load(giftedFile)
        giftedFile.close()
    # isAlsoharacter = Path(charFolder + gifted.lower() + ".json")
    except FileNotFoundError:
        msg = "You can not give this posiont, as " + gifted + " does not have a character."
        return msg
    gifter = gifterData['name']
    gifted = giftedData['name']
    if item.lower() not in gifterData['potions']:
        msg = "You do not have this item to give."
    elif item.lower() in gifterData['potions'] and len(giftedData['potions']) <= 3:
        gifterData['potions'].remove(item.lower())
        giftedData['potions'].append(item.lower())
        msg = gifter + " has given " + gifted + " a potion of " + item.lower()
    else:
        msg = "You can not give " + gifted + " anything, as they have no space in their inventory to take this item."
    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(gifterData, file, ensure_ascii=False, indent=2)
    file.close()

    file = open(charFolder + gifted.lower() + ".json", "w", encoding="utf-8")
    json.dump(giftedData, file, ensure_ascii=False, indent=2)
    file.close()

    return msg, gifter, gifted

# DEVELOPER USE ONLY - Stocks the store with 20 new pieces of equipment
def pri_11_stockarmor(catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList, catTwoUncommonList,
                      catTwoRareList, catThreeCommonList, catThreeUncommonList, catThreeRareList):
    armorData = get_armor_dictionary()
    num = 1
    msg = []
    for num in range(1, 21):
        rand = random.randint(1, 100)
        if rand in range(1, 101):
            category = random.randint(1, 100)
            # 15% chance
            if category in range(80, 101):
                item = []
                randomAttribute = random.choice(catOneRareList)
                item.append(randomAttribute)
            # 35% chance
            if category in range(46, 80):
                item = []
                randomAttribute = random.choice(catOneUncommonList)
                item.append(randomAttribute)
            # 50% chance
            if category in range(1, 46):
                item = []
                randomAttribute = random.choice(catOneCommonList)
                item.append(randomAttribute)
        if rand in range(1, 41):
            category = random.randint(1, 100)
            # 15% chance
            if category in range(86, 101):
                randomAttribute = random.choice(catTwoRareList)
                item.append(randomAttribute)
            # 35% chance
            if category in range(51, 86):
                randomAttribute = random.choice(catTwoUncommonList)
                item.append(randomAttribute)
            # 50% chance
            if category in range(1, 51):
                randomAttribute = random.choice(catTwoCommonList)
                item.append(randomAttribute)
        if rand in range(1, 11):
            category = random.randint(1, 100)
            # 15% chance
            if category in range(86, 101):
                randomAttribute = random.choice(catThreeRareList)
                item.append(randomAttribute)
            # 35% chance
            elif category in range(51, 86):
                randomAttribute = random.choice(catThreeUncommonList)
                item.append(randomAttribute)
            # 50% chance
            elif category in range(1, 51):
                randomAttribute = random.choice(catThreeCommonList)
                item.append(randomAttribute)
        armorDictionary[0]["armorlist"]["armor" + str(num)] = item
    armorFile = open("armor.json", "r+", encoding="utf-8")
    armorFile.seek(0)
    armorFile.write(json.dumps(armorDictionary, ensure_ascii=False, indent=2))
    armorFile.truncate()
    armorFile.close()
    # num = 1
    # for num in range(1, 21):
    #     msg.append("Armor" + str(num) + " (" + ", ".join(armorDictionary[0]["armorlist"]["armor" + str(num)]) + ")")

    msg = "Armor Shop has been stocked for the week."
    return msg

# Allows player to view armor shop
# !armorshop
def pri_10_armorshop(myList):
    armorData = get_armor_dictionary()
    armorPrice = []
    num = 0
    for item in myList:
        if item == "sold":
            price = 0
            armorPrice.append(price)
        if len(item) == 1:
            stat = " ".join(item)
            if stat in armorDictionary[0]["cat1"]["common"]:
                price = armorDictionary[0]["cat1"]["common"][stat][0]
            elif stat in armorDictionary[0]["cat1"]["uncommon"]:
                price = armorDictionary[0]["cat1"]["uncommon"][stat][0]
            elif stat in armorDictionary[0]["cat1"]["rare"]:
                price = armorDictionary[0]["cat1"]["rare"][stat][0]
            armorPrice.append(price)
        if len(item) == 2:
            wordOne = item[0]
            wordTwo = item[1]
            if wordOne in armorDictionary[0]["cat1"]["common"]:
                priceOne = armorDictionary[0]["cat1"]["common"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["uncommon"]:
                priceOne = armorDictionary[0]["cat1"]["uncommon"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["rare"]:
                priceOne = armorDictionary[0]["cat1"]["rare"][wordOne][0]
            if wordTwo in armorDictionary[0]["cat2"]["common"]:
                priceTwo = armorDictionary[0]["cat2"]["common"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["uncommon"]:
                priceTwo = armorDictionary[0]["cat2"]["uncommon"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["rare"]:
                priceTwo = armorDictionary[0]["cat2"]["rare"][wordTwo][0]
            price = priceOne + priceTwo
            armorPrice.append(price)
        if len(item) == 3:
            wordOne = item[0]
            wordTwo = item[1]
            wordThree = item[2]
            if wordOne in armorDictionary[0]["cat1"]["common"]:
                priceOne = armorDictionary[0]["cat1"]["common"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["uncommon"]:
                priceOne = armorDictionary[0]["cat1"]["uncommon"][wordOne][0]
            elif wordOne in armorDictionary[0]["cat1"]["rare"]:
                priceOne = armorDictionary[0]["cat1"]["rare"][wordOne][0]
            if wordTwo in armorDictionary[0]["cat2"]["common"]:
                priceTwo = armorDictionary[0]["cat2"]["common"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["uncommon"]:
                priceTwo = armorDictionary[0]["cat2"]["uncommon"][wordTwo][0]
            elif wordTwo in armorDictionary[0]["cat2"]["rare"]:
                priceTwo = armorDictionary[0]["cat2"]["rare"][wordTwo][0]
            if wordThree in armorDictionary[0]["cat3"]["common"]:
                priceThree = armorDictionary[0]["cat3"]["common"][wordThree][0]
            elif wordThree in armorDictionary[0]["cat3"]["uncommon"]:
                priceThree = armorDictionary[0]["cat3"]["uncommon"][wordThree][0]
            elif wordThree in armorDictionary[0]["cat3"]["rare"]:
                priceThree = armorDictionary[0]["cat3"]["rare"][wordThree][0]
            price = priceOne + priceTwo + priceThree
            armorPrice.append(price)
        num += 1
    shopList = {}
    num = 1
    for item in myList:
        shopList["Armor" + str(num)] = item
        num += 1
    item = []
    for key in shopList:
        item.append(key)
        item.append(shopList[key])
    print(item)
    print(armorPrice)
    armorList = "\n".join("{} [color=red]{}[/color]: [color=yellow]({} renown)[/color]".format(*i)
                          for i in zip(item[0::2], item[1::2], armorPrice[0:]))
    return armorList

# Use to buy a piece of equipment from the shop
# !buyarmor <armor name>
def pri_9_buyarmor(character, armor, charFolder):
    armorData = get_armor_dictionary()
    try:
        charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You don't have a character made to use this function."
        return msg

    if armor not in armorData[0]['armorlist']:
        msg = "You seemed to have not typed in your desired choice correctly."
    else:
        choice = armorData[0]['armorlist'][armor]
        if choice == "sold":
            msg = "This armor has already been sold."
            return msg
        armorString = ", ".join(choice)
        price = 0
        if isCharacter.is_file():
            for word in choice:
                if word in armorData[0]["cat1"]["common"]:
                    price += armorData[0]["cat1"]["common"][word][0]
                elif word in armorData[0]["cat1"]['uncommon']:
                    price += armorData[0]["cat1"]['uncommon'][word][0]
                elif word in armorData[0]["cat1"]['rare']:
                    price += armorData[0]["cat1"]['rare'][word][0]
                if word in armorData[0]["cat2"]["common"]:
                    price += armorData[0]["cat2"]["common"][word][0]
                elif word in armorData[0]["cat2"]["uncommon"]:
                    price += armorData[0]["cat2"]["uncommon"][word][0]
                elif word in armorData[0]["cat2"]["rare"]:
                    price += armorData[0]["cat2"]["rare"][word][0]
                if word in armorData[0]["cat3"]["common"]:
                    price += armorData[0]["cat3"]["common"][word][0]
                elif word in armorData[0]["cat3"]["uncommon"]:
                    price += armorData[0]["cat3"]["uncommon"][word][0]
                elif word in armorData[0]["cat3"]["rare"]:
                    price += armorData[0]["cat3"]["common"][word][0]
                else:
                    msg = "You have not selected an armor that is listed (Example: !buyarmor armor4)"
        invList = []
        for keys in charSheet['armor']:
            invList.append(keys)
        armor1 = invList[0]
        armor2 = invList[1]
        armor3 = invList[2]
        if price <= charSheet['renown']:
            if charSheet['armor'][armor1] != "n/a" \
                    and charSheet['armor'][armor2] != "n/a"\
                    and charSheet['armor'][armor3] != "n/a":
                msg = "You do not have enough inventory space to own more armor."
            else:
                charSheet['renown'] -= price
                armorData[0]["armorlist"][armor] = "sold"
                if charSheet['armor'][armor1] == "n/a":
                    charSheet['armor'][armor1] = choice
                    charSheet['armor'][armor1].append(price)
                elif charSheet['armor'][armor2] == "n/a":
                    charSheet['armor'][armor2] = choice
                    charSheet['armor'][armor2].append(price)
                elif charSheet['armor'][armor3] == "n/a":
                    charSheet['armor'][armor3] = choice
                    charSheet['armor'][armor3].append(price)
                msg = charSheet['name'] + " has purchased an armor of [color=red]" + armorString + "[/color]."
        else:
            msg = "You do not have enough renown to purchase this."

        file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
        json.dump(charSheet, file, ensure_ascii=False, indent=2)
        file.close()

        file = open("armor.json", "w", encoding="utf-8")
        json.dump(armorData, file, ensure_ascii=False, indent=2)
        file.close()
    return msg

# Use to sell a piece of equipment
# !sellarmor <armor name>
def pri_10_sellarmor(character, armor, charFolder):
    armorData = get_armor_dictionary()

    try:
        sellerFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        sellerData = json.load(sellerFile)
        sellerFile.close()
    # isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You do not have a character to use this command."
        return msg
    if armor in sellerData['armor']:
        if armor in sellerData['equip']:
            msg = "You can't sell armor that is currently equipped."
        else:
            price = int(sellerData['armor'][armor][-1] / 2)
            sellerData['renown'] += price
            sellerData['armor'][armor] = "n/a"
            if 'armor1' not in sellerData['armor']:
                sellerData["armor"]['armor1'] = sellerData['armor'].pop(armor)
            elif 'armor2' not in sellerData['armor']:
                sellerData["armor"]['armor2'] = sellerData['armor'].pop(armor)
            elif 'armor3' not in sellerData['armor']:
                sellerData["armor"]['armor3'] = sellerData['armor'].pop(armor)
            msg = character + " sold some armor for [color=yellow] " + str(price) + " renown[/color]"
    else:
        msg = "You do not have that armor to sell."

    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(sellerData, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# Use to name a piece of equipment
# !armorname <old name> - <new name>
def pri_10_namearmor(character, armorName, armorRemove, charFolder):
    try:
        charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
    except FileNotFoundError:
        msg = "You don't have a character made to use this command."
        return msg

    if armorRemove not in charSheet['armor'].keys():
        msg = armorRemove + " is not within your inventory to rename. Please check you are typing armor name correctly," \
              " then try this command again"
    elif armorName in charSheet['armor'].keys():
        msg = "You already have a piece of armor named " + armorName + ". Please use a new name, and try this command " \
              "again"
    elif armorRemove == charSheet['equip']:
        msg = "You need to unequip the armor first, before using this command."
    elif charSheet['armor'][armorRemove]  != "n/a":
        charSheet['armor'][armorName] = charSheet['armor'].pop(armorRemove)
        msg = charSheet['name'] + " renamed " + armorRemove + " to " + armorName + "."
    else:
        msg = "There is no armor in that slot to rename. Please double check inventory, then use this command again."
    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# Use to equip a piece of equipment
# !equip <armor name>
def pri_6_equip(character, armor, charFolder, game):
    try:
        charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        charSheet = json.load(charFile)
        charFile.close()
        isCharacter = Path(charFolder + character.lower() + ".json")
    except FileNotFoundError:
        msg = "You don't have a character made to use this command."
        return msg

    armorData = get_armor_dictionary()

    if game != 1:
        charSheet["armorhit"] = 0
        charSheet["armordamage"] = 0
        charSheet["armorac"] = 0
        charSheet["armorhp"] = 0
        charSheet["armordr"] = 0
        charSheet["armorinitiative"] = 0
        charSheet["armorstrength"] = 0
        charSheet["armordexterity"] = 0
        charSheet["armorconstitution"] = 0
        charSheet["armorblur"] = 0
        if armor in charSheet['armor']:
            charSheet['equip'] = armor
            msg = charSheet['name'] + " has equipped " + armor
            if len(charSheet['armor'][armor]) == 2:
                statOne = charSheet['armor'][armor][0]
                statTwo = ""
                statThree = ""
            elif len(charSheet['armor'][armor]) == 3:
                statOne = charSheet['armor'][armor][0]
                statTwo = charSheet['armor'][armor][1]
                statThree = ""
            elif len(charSheet['armor'][armor]) == 4:
                statOne = charSheet['armor'][armor][0]
                statTwo = charSheet['armor'][armor][1]
                statThree = charSheet['armor'][armor][2]
            if statOne != "":
                if statOne in armorDictionary[0]["cat1"]["common"]:
                    statOneValue = armorDictionary[0]["cat1"]["common"][statOne][1]
                elif statOne in armorDictionary[0]["cat1"]["uncommon"]:
                    statOneValue = armorDictionary[0]["cat1"]["uncommon"][statOne][1]
                elif statOne in armorDictionary[0]["cat1"]["rare"]:
                    statOneValue = armorDictionary[0]["cat1"]["rare"][statOne][1]
            if statTwo != "":
                if statTwo in armorDictionary[0]["cat2"]["common"]:
                    statTwoValue = armorDictionary[0]["cat2"]["common"][statTwo][1]
                elif statTwo in armorDictionary[0]["cat2"]["uncommon"]:
                    statTwoValue = armorDictionary[0]["cat2"]["uncommon"][statTwo][1]
                elif statTwo in armorDictionary[0]["cat2"]["rare"]:
                    statTwoValue = armorDictionary[0]["cat2"]["rare"][statTwo][1]
            if statThree != "":
                if statThree in armorDictionary[0]["cat3"]["common"]:
                    statThreeValue = armorDictionary[0]["cat3"]["common"][statThree][1]
                elif statThree in armorDictionary[0]["cat3"]["uncommon"]:
                    statThreeValue = armorDictionary[0]["cat3"]["uncommon"][statThree][1]
                elif statThree in armorDictionary[0]["cat3"]["rare"]:
                    statThreeValue = armorDictionary[0]["cat3"]["rare"][statThree][1]
            if statOne[:2] == "st":
                charSheet["armorstrength"] = statOneValue
            elif statOne[:2] == "de":
                charSheet["armordexterity"] = statOneValue
            elif statOne[:2] == "co":
                charSheet["armorconstitution"] = statOneValue
            if statTwo[:2] == "ac":
                charSheet["armorac"] = statTwoValue
            elif statTwo[:2] == "dr":
                if charSheet["traitdr"] == 0 and charSheet["regeneration"] == 0:
                    charSheet["armordr"] = statTwoValue
            elif statTwo[:2] == "in":
                charSheet["armorinitiative"] = statTwoValue
                charSheet["initiative"] = statTwoValue
            elif statTwo[:2] == "hp":
                charSheet["armorhp"] += statTwoValue
            if statThree[:2] == "hi":
                charSheet["armorhit"] = statThreeValue
            elif statThree[:2] == "da":
                charSheet["armordamage"] = statThreeValue
            elif statThree[:2] == "bl":
                charSheet["armorblur"] += statThreeValue
        else:
            msg = armor + " doesn't exist in your inventory. Make sure you are typing the armor name correctly when using" \
                          " this command"
    else:
        msg = "A fight is currently taking place...please wait until it is concluded."

    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(charSheet, file, ensure_ascii=False, indent=2)
    file.close()
    return msg

# Use to unequip a piece of equipment
# !unequip <armor name>
def pri_8_unequip(character, armor, charFolder, game):
    if game != 1:
        try:
            charFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
            charSheet = json.load(charFile)
            charFile.close()
            isCharacter = Path(charFolder + character.lower() + ".json")
        except FileNotFoundError:
            msg = "You don't have a character made to use this command."
            return msg

        charSheet['equip'] = ""
        msg = charSheet['name'] + " has unequipped " + armor
        charSheet["armorhit"] = 0
        charSheet["armordamage"] = 0
        charSheet["armorac"] = 0
        charSheet["armorhp"] = 0
        charSheet["armordr"] = 0
        charSheet["armorinitiative"] = 0
        charSheet["armorstrength"] = 0
        charSheet["armordexterity"] = 0
        charSheet["armorconstitution"] = 0
        charSheet["armorblur"] = 0

        file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
        json.dump(charSheet, file, ensure_ascii=False, indent=2)
        file.close()
    else:
        msg = "A fight is currently taking place...please wait until it is concluded."
    return msg