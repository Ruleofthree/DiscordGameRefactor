from src.armor_repository import build_armor_shop_display, get_armor_dictionary
from src.potion_repository import (
    buy_character_potion,
    get_potion_effect_info,
    get_potion_sell_value,
    sell_character_potion,
    stock_potion_shop,
)
from src.character_repository import (
    add_ability_point,
    apply_character_view_totals,
    assign_character_stats,
    build_character_view_context,
    calculate_character_view_totals,
    character_exists,
    format_character_view_armor_inventory,
    format_character_view_potion_inventory,
    list_characters_by_level,
    load_character,
    save_character,
    select_character_build,
    select_character_feat,
    select_character_trait,
)
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
    charData = load_character(character, charFolder)
    reset = charData['reset']
    tFeats = charData['total feats']
    renown = charData['renown']

    if reset != 0:
        reset -= 1
        charData = load_character(character, charFolder)
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
        save_character(character, charData, charFolder)

        msg = "your characters abilities, trait, and feats have been reset. Please use [color=pink]!build[/color]" \
              " to select your character's build path, then please use the [color=pink]!stats[/color]" \
              " command to select new Strength, Dexterity, and Constitution, the [color=pink]!traitpick[/color]" \
              " command to pick a new trait, and the [color=pink]!featpick[/color] command to select new feats." \
              " (you have [color=red]" + str(reset) + "[/color] reset points remaining.)"

    elif reset == 0 and renown > 250:
        renown -= 250
        charData = load_character(character, charFolder)
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
        save_character(character, charData, charFolder)

        msg = "your characters abilities, trait, and feats have been reset. Please use [color=pink]!build[/color]" \
              " to select your character's build path, then please use the [color=pink]!stats[/color]" \
              " command to select new Strength, Dexterity, and Constitution, the [color=pink]!traitpick[/color]" \
              " command to pick a new trait, and the [color=pink]!featpick[/color] command to select new feats." \
              " (As you had no reset points, [color=yellow]250 renown[/color] was taken from your total.)"
    else:
        msg = "You currently have no more reset points to use, or renown to spend."

    return msg

# Set up a character's stats after creation. Stat points MUST equal 15 in total, and no single stat can be above 10
# !stat <str> <dex> <con>
def pri_6_stats(message, character, charData, charFile):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    return assign_character_stats(charFolder, character, message)

# !build <strength> <dexterity> <constitution>
def pri_6_build(charFolder, message, charFile, character):
    return select_character_build(character, message, charFolder)

# Automatically adds 1 point to Strength, Dexterity, or Constitution. used only when character reaches 5, 10, 15, or 20
# !add strength, !add dexterity, !add constitution OR !add str, !add dex, !add con
def pri_4_add(message, character):
    ability = message[5:]
    ability = ability.lower()
    player = character.lower()
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")
    charFile = Path(charFolder + player + ".json")

    if ability not in ["str", "strength", "dex", "dexterity", "con", "constitution"]:
        msg = [
            "You need to specify the ability you want to point the point to. "
            "Type '!add str' or '!add strength' for strength, and so on."
        ]
        return msg

    with open(charFile, "r+", encoding="utf-8") as file:
        charData = json.load(file)
        charData, msg = add_ability_point(charData, ability)
        file.seek(0)
        file.write(json.dumps(charData, ensure_ascii=False, indent=2))
        file.truncate()

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

        view_context = build_character_view_context(charData)

        totals = view_context["totals"]

        armorOne = view_context["armor_one"]
        armorTwo = view_context["armor_two"]
        armorThree = view_context["armor_three"]
        armorInvOne = view_context["armor_inv_one"]
        armorInvTwo = view_context["armor_inv_two"]
        armorInvThree = view_context["armor_inv_three"]

        potionInventoryList = view_context["potion_inventory"]

        equip = view_context["equip"]
        name = view_context["name"]
        build = view_context["build"]
        trait = view_context["trait"]
        level = view_context["level"]
        tFeats = view_context["total_feats"]
        baseDamage = view_context["base_damage"]
        renown = view_context["renown"]
        xp = view_context["current_xp"]
        nextLevel = view_context["next_level"]
        remainingFeats = view_context["remaining_feats"]
        hasTakenList = view_context["feats_taken"]
        ap = view_context["ap"]
        reset = view_context["reset"]
        wins = view_context["wins"]
        losses = view_context["losses"]
        forfeits = view_context["forfeits"]
        potionEffect = view_context["potion_effect"]
        pstrength = view_context["permanent_strength"]
        pdexterity = view_context["permanent_dexterity"]
        pconstitution = view_context["permanent_constitution"]

        # except:
        #     print("Something above doesn't exist")
        print("What?")

        strength = totals["strength"]
        dexterity = totals["dexterity"]
        constitution = totals["constitution"]
        thp = totals["thp"]
        tac = totals["tac"]
        tdr = totals["tdr"]
        thit = totals["thit"]
        tdamage = totals["tdamage"]
        regen = totals["regeneration"]
        blur = totals["blur"]
        initiative = totals["initiative"]

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

        apply_character_view_totals(charData, totals)
        save_character(character, charData, charFolder)
    return msg

# shows every single character in the game that is the level selected
# !wholevel 3
def pri_9_wholevel(character, message):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    requested_level = int(message[10:])
    response = list_characters_by_level(requested_level, charFolder)

    msg = []
    msg.append("Level " + str(message[10:] + " characters:"))
    stringResponse = "\n" + "\n".join(response)
    msg.append(stringResponse)

    return msg

# select a starting trait for character
# !traitpick <trait>
def pri_6_trait(character, message, traitList, traitDictionary, trait):
    path = os.getcwd()
    charFolder = os.path.join(path + "/characters/")

    return select_character_trait(
        char_folder=charFolder,
        character=character,
        message=message,
        trait_list=traitList,
        trait_dictionary=traitDictionary,
        trait=trait,
    )

# select a feat when a feat slot is available
# !featpick <feat>
def pri_10_feat_pick(character, message, featList, featDictionary):
    answer = message[10:].lower()

    return select_character_feat(
        character=character,
        feat_name=answer,
        feat_list=featList,
        feat_dictionary=featDictionary,
    )

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

    buyer = charSheet["name"]

    if isCharacter.is_file():
        charSheet, potionData, msg = buy_character_potion(
            charSheet,
            potionData,
            potion,
        )

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

    sellerData, msg = sell_character_potion(sellerData, potion)

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
    return build_armor_shop_display(myList)

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


def pri_10_stockpotion(commonList, uncommonList, rareList, vrareList, relicList):
    potionFile = open("potions.json", "r+", encoding="utf-8")
    potionDictionary = json.load(potionFile)

    potionDictionary, msg, shopString = stock_potion_shop(
        potionDictionary,
        commonList,
        uncommonList,
        rareList,
        vrareList,
        relicList,
    )

    potionFile.seek(0)
    potionFile.write(json.dumps(potionDictionary, ensure_ascii=False, indent=2))
    potionFile.truncate()
    potionFile.close()

    return msg, shopString