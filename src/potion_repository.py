from collections import Counter
from src.data_loader import load_potions

import random


POTION_RARITY_ORDER = ("common", "uncommon", "rare", "vrare", "relic")


def get_potion_dictionary():
    return load_potions()


def get_potion_data():
    return load_potions()[0]


def get_potion_shop_lists():
    potion_data = get_potion_data()

    return tuple(
        list(potion_data[rarity].keys())
        for rarity in POTION_RARITY_ORDER
    )


def find_potion(potion_name):
    potion_data = get_potion_data()

    for rarity in POTION_RARITY_ORDER:
        if potion_name in potion_data[rarity]:
            return rarity, potion_data[rarity][potion_name]

    return None


def get_potion_price(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[0]


def get_potion_description(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[1]


def get_potion_effect_value(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[2]


def get_potion_sell_value(potion_name):
    price = get_potion_price(potion_name)

    if price is None:
        return None

    return int(price / 2)


def get_potion_effect_info(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[2], potion_info[1]


def sell_character_potion(character_data, potion_name):
    """
    Sell one potion from a character inventory.

    This preserves the legacy pri_11_sellpotion message behavior while keeping
    file loading and saving in the legacy wrapper for now.
    """
    if potion_name not in character_data["potions"]:
        return character_data, "You do not have that potion to sell."

    half_price = get_potion_sell_value(potion_name)

    if half_price is None:
        return character_data, "That potion does not exist in the potion data."

    character_data["renown"] += half_price
    character_data["potions"].remove(potion_name)

    message = (
        character_data["name"]
        + " has sold a [color=red]"
        + potion_name
        + "[/color] for [color=yellow]"
        + str(half_price)
        + " renown[/color]."
    )

    return character_data, message


def stock_potion_shop(
    potion_dictionary,
    common_list,
    uncommon_list,
    rare_list,
    very_rare_list,
    relic_list,
):
    """
    Stock the potion shop with 20 potions.

    This preserves the legacy pri_10_stockpotion rarity thresholds and index
    selection behavior while keeping file writing in the legacy wrapper.
    """
    potion_dictionary[0]["shoplist"] = []

    for _ in range(1, 21):
        number = random.randint(1, 100)

        if number in range(98, 101):
            relic_potion = len(relic_list)
            index = random.randint(1, relic_potion - 1)
            chosen_potion = relic_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(90, 98):
            very_rare_potion = len(very_rare_list)
            index = random.randint(1, very_rare_potion - 1)
            chosen_potion = very_rare_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(77, 90):
            rare_potion = len(rare_list)
            index = random.randint(1, rare_potion - 1)
            chosen_potion = rare_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(51, 77):
            uncommon_potion = len(uncommon_list)
            index = random.randint(1, uncommon_potion - 1)
            chosen_potion = uncommon_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(1, 51):
            common_potion = len(common_list)
            index = random.randint(1, common_potion - 1)
            chosen_potion = common_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

    shop_string = ", ".join(potion_dictionary[0]["shoplist"])
    msg = "Shop stocked for the week as follows: \n" + shop_string

    return potion_dictionary, msg, shop_string


def get_potion_price_from_data(potion_data, potion_name):
    """
    Return a potion price from caller-provided potion data.

    This preserves the legacy category search order without loading potions.json
    inside the deterministic purchase helper.
    """
    for rarity in POTION_RARITY_ORDER:
        if potion_name in potion_data[0][rarity]:
            return potion_data[0][rarity][potion_name][0]

    return None


def buy_character_potion(character_data, potion_data, potion_name):
    """
    Buy one potion from the current potion shop.

    This preserves pri_10_buypotion state mutation while keeping file loading
    and saving in the legacy wrapper.
    """
    potion_list = potion_data[0]["shoplist"]

    if potion_name not in potion_list:
        return (
            character_data,
            potion_data,
            "You can not buy that potion, as it is not being sold right now.",
        )

    price = get_potion_price_from_data(potion_data, potion_name)

    if price <= character_data["renown"]:
        if len(character_data["potions"]) >= 5:
            message = "You do not have enough inventory space to own more potions."
        else:
            character_data["renown"] -= price
            potion_data[0]["shoplist"].remove(potion_name)
            character_data["potions"].append(potion_name)
            message = character_data["name"] + " has puchased a potion of " + potion_name + "."
    else:
        message = "You do not have enough renown to purchase this."

    return character_data, potion_data, message


def give_character_potion(gifter_data, gifted_data, item):
    item = item.lower()

    gifter = gifter_data["name"]
    gifted = gifted_data["name"]

    if item not in gifter_data["potions"]:
        msg = "You do not have this item to give."
    elif item in gifter_data["potions"] and len(gifted_data["potions"]) <= 3:
        gifter_data["potions"].remove(item)
        gifted_data["potions"].append(item)
        msg = gifter + " has given " + gifted + " a potion of " + item
    else:
        msg = "You can not give " + gifted + " anything, as they have no space in their inventory to take this item."

    return msg, gifter, gifted


def _apply_permanent_stat_potion(character_data, potion_name):
    permanent_potions = {
        "str": ("pstrength", "strength"),
        "dex": ("pdexterity", "dexterity"),
        "con": ("pconstitution", "constitution"),
    }

    for prefix, (field_name, display_name) in permanent_potions.items():
        if potion_name.startswith(prefix):
            try:
                potion_tier = int(potion_name.removeprefix(prefix))
            except ValueError:
                return None

            required_value = potion_tier - 1

            if character_data[field_name] == required_value:
                character_data[field_name] = potion_tier
                msg = (
                    character_data["name"]
                    + " drank a "
                    + potion_name
                    + " potion, obtaining a permanent [color=red] +1 to "
                    + display_name
                    + "[/color]"
                )
                character_data["potions"].remove(potion_name)
                return msg

            return "You can not drink this potion, as it is either too powerful or too weak to use right now."

    return None


def use_character_potion(character_data, potion_name, potion_info):
    if potion_info is not None:
        potion_effect, potion_description = potion_info

        msg = _apply_permanent_stat_potion(character_data, potion_name)

        if msg is None:
            if potion_name == "respec":
                character_data["reset"] += 1
                msg = (
                    character_data["name"]
                    + " drank a "
                    + potion_name
                    + " potion. Allowing them a chance to change their feats, traits, and stat points."
                )
                character_data["potions"].remove(potion_name)
            elif potion_name == "stimulant":
                character_data["remaining feats"] += 1
                character_data["total feats"] += 1
                msg = (
                    character_data["name"]
                    + " drank a "
                    + potion_name
                    + " potion. Allowing them to learn a new feat they qualify for."
                )
                character_data["potions"].remove(potion_name)
            elif character_data["potioneffect"] == "":
                if potion_name[:3] == "hit":
                    character_data["potionhit"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:6] == "damage":
                    character_data["potiondamage"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + "drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:2] == "ac":
                    character_data["potionac"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:4] == "tstr":
                    character_data["potionstr"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:4] == "tdex":
                    character_data["potiondex"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:4] == "tcon":
                    character_data["potioncon"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:2] == "hp":
                    character_data["potionhp"] = potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + "[/color] for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:2] == "bl":
                    character_data["potionblur"] += potion_effect
                    character_data["potioneffect"] = potion_description
                    msg = (
                        character_data["name"]
                        + " drank a "
                        + potion_name
                        + " potion, [color=red]"
                        + potion_description
                        + " for next match."
                    )
                    character_data["potions"].remove(potion_name)
                elif potion_name[:2] == "re":
                    if (
                        character_data["traitdr"] == 0
                        or character_data["armordr"] == 0
                        or character_data["regeneration"] == 0
                    ):
                        character_data["potionregen"] += potion_effect
                        character_data["potioneffect"] = potion_description
                        msg = (
                            character_data["name"]
                            + " drank a "
                            + potion_name
                            + " potion, [color=red]"
                            + potion_description
                            + " for next match."
                        )
                    else:
                        msg = character_data["name"] + " gains no benefit from this potion."
                else:
                    msg = "You can not drink this potion, as it is either too powerful or too weak to use right now."
            else:
                msg = "You already have a potion in effect."
    else:
        msg = "You do not have a potion of " + potion_name

    return character_data, msg


def build_potion_shop_display(potion_data):
    shop_list = potion_data[0]["shoplist"]
    ordered_list = Counter(shop_list)
    item = []

    for key in ordered_list:
        item.append(key)
        item.append(ordered_list[key])

        if key in potion_data[0]["common"]:
            item.append(potion_data[0]["common"][key][0])
        elif key in potion_data[0]["uncommon"]:
            item.append(potion_data[0]["uncommon"][key][0])
        elif key in potion_data[0]["rare"]:
            item.append(potion_data[0]["rare"][key][0])
        elif key in potion_data[0]["vrare"]:
            item.append(potion_data[0]["vrare"][key][0])
        elif key in potion_data[0]["relic"]:
            item.append(potion_data[0]["relic"][key][0])

    return "\n".join(
        "{}: [color=red]{}[/color] [color=yellow]({} renown)[/color]".format(*i)
        for i in zip(item[::3], item[1::3], item[2::3])
    )