from src.armor_repository import (
    build_armor_shop_display,
    buy_character_armor,
    equip_character_armor,
    get_armor_dictionary,
    get_armor_shop_lists,
    rename_character_armor,
    sell_character_armor,
    stock_armor_shop,
    unequip_character_armor,
)
from src.potion_repository import (
    build_potion_shop_display,
    buy_character_potion,
    create_character_potion,
    get_potion_dictionary,
    get_potion_effect_info,
    get_potion_sell_value,
    get_potion_shop_lists,
    give_character_potion,
    sell_character_potion,
    stock_potion_shop,
    use_character_potion,
)
from src.character_repository import (
    add_ability_point,
    apply_character_view_totals,
    assign_character_stats,
    build_and_save_character_view,
    build_character_view_context,
    build_character_view_message,
    calculate_character_view_totals,
    character_exists,
    format_character_view_armor_inventory,
    format_character_view_potion_inventory,
    list_characters_by_level,
    load_character,
    refresh_character_combat_totals,
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


def pri_potionshop():
    potion_dictionary = get_potion_dictionary()
    return build_potion_shop_display(potion_dictionary)


def pri_createpotion(item, gifted, charFolder):
    potion_dictionary = get_potion_dictionary()
    charData = load_character(gifted, charFolder)
    charData = create_character_potion(charData, potion_dictionary, item)
    save_character(gifted, charData, charFolder)
    return charData


def pri_armorshop():
    armor_dictionary = get_armor_dictionary()
    armor_shop_items = []
    for key in armor_dictionary[0]["armorlist"]:
        armor_shop_items.append(armor_dictionary[0]["armorlist"][key])
    return build_armor_shop_display(armor_shop_items)


def pri_potion_shop_lists():
    return get_potion_shop_lists()


def pri_armor_shop_lists():
    return get_armor_shop_lists()


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
    msg = assign_character_stats(charFolder, character, message)

    if (
        len(msg) > 1
        and "The above points have been placed on your character sheet." in msg[1]
    ):
        refresh_character_combat_totals(character.lower(), charFolder)

    return msg

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
        had_apboost = charData["apboost"]
        charData, msg = add_ability_point(charData, ability)
        file.seek(0)
        file.write(json.dumps(charData, ensure_ascii=False, indent=2))
        file.truncate()

    if had_apboost:
        refresh_character_combat_totals(player, charFolder)

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
        msg.append(build_and_save_character_view(character, charFolder))
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

    msg = select_character_trait(
        char_folder=charFolder,
        character=character,
        message=message,
        trait_list=traitList,
        trait_dictionary=traitDictionary,
        trait=trait,
    )

    if "has been added to your character sheet." in msg:
        refresh_character_combat_totals(character.lower(), charFolder)

    return msg

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
def pri_10_usepotion(character, potion, commonList, uncommonList, rareList, vrareList, relicList, charFolder):
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

    charSheet, msg = use_character_potion(
        charSheet,
        potion,
        potionInfo,
    )

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

    msg, gifter, gifted = give_character_potion(gifterData, giftedData, item)

    file = open(charFolder + character.lower() + ".json", "w", encoding="utf-8")
    json.dump(gifterData, file, ensure_ascii=False, indent=2)
    file.close()

    file = open(charFolder + gifted.lower() + ".json", "w", encoding="utf-8")
    json.dump(giftedData, file, ensure_ascii=False, indent=2)
    file.close()

    return msg, gifter, gifted

def pri_11_stockarmor(catOneCommonList, catOneUncommonList, catOneRareList, catTwoCommonList, catTwoUncommonList,
                      catTwoRareList, catThreeCommonList, catThreeUncommonList, catThreeRareList):
    armorDictionary = get_armor_dictionary()

    armorDictionary, msg = stock_armor_shop(
        armorDictionary,
        catOneCommonList,
        catOneUncommonList,
        catOneRareList,
        catTwoCommonList,
        catTwoUncommonList,
        catTwoRareList,
        catThreeCommonList,
        catThreeUncommonList,
        catThreeRareList,
    )

    armorFile = open("armor.json", "r+", encoding="utf-8")
    armorFile.seek(0)
    armorFile.write(json.dumps(armorDictionary, ensure_ascii=False, indent=2))
    armorFile.truncate()
    armorFile.close()

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

    if isCharacter.is_file():
        charSheet, armorData, msg = buy_character_armor(
            charSheet,
            armorData,
            armor,
        )

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
    try:
        sellerFile = open(charFolder + character.lower() + ".json", "r", encoding="utf-8")
        sellerData = json.load(sellerFile)
        sellerFile.close()
    except FileNotFoundError:
        msg = "You do not have a character to use this command."
        return msg

    sellerData, msg = sell_character_armor(
        sellerData,
        armor,
        character,
    )

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

    msg = rename_character_armor(charSheet, armorName, armorRemove)

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
    except FileNotFoundError:
        msg = "You don't have a character made to use this command."
        return msg

    armorFile = open("armor.json", "r", encoding="utf-8")
    armorDictionary = json.load(armorFile)
    armorFile.close()

    if game != 1:
        msg = equip_character_armor(charSheet, armor, armorDictionary)
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
        except FileNotFoundError:
            msg = "You don't have a character made to use this command."
            return msg

        msg = unequip_character_armor(charSheet, armor)

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