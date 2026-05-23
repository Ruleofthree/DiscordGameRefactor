from src.feat_repository import get_feat_dictionary
import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# 691

# Stoneskin
# Another feat with A LOT going on.
# Sylzana's creation
def featStoneskin(pOneInfo, pTwoInfo, pOneFeatUsed, token):
    modifier = []
    if pOneFeatUsed[0] == "stoneskin":
        minimum = int(pOneFeatUsed[1][0])
        maximum = int(pOneFeatUsed[1][1])
        stoneskin = random.randint(minimum, maximum)
        stonebonus = 0
        if pOneInfo['build'] == "constitution":
            stonebonus = pOneFeatUsed[1][2]
            stoneskin = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        modifier.append(pOneInfo['name'] + " used [color=yellow]" + str(pOneFeatUsed[0]) +\
                        "[/color], shielding them from up to [color=red]" + str(stoneskin) + "[/color]"
                        " points of damage.")
        if stonebonus != 0:
            modifier.append(pOneInfo['name'] + " also gained a [color=red]+" + str(stonebonus) + \
                            ",[/color] bonus hit and to damage until [color=yellow]" + str(pOneFeatUsed[0]) +\
                            "[/color] is broken.")
    elif pOneFeatUsed[0] == "improved stoneskin":
        minimum = int(pOneFeatUsed[1][0])
        maximum = int(pOneFeatUsed[1][1])
        stoneskin = random.randint(minimum, maximum)
        stonebonus = 0
        if pOneInfo['build'] == "constitution":
            stonebonus = pOneFeatUsed[1][2]
            stoneskin = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        stoneskin = random.randint(minimum, maximum)
        modifier.append(pOneInfo['name'] + " used [color=yellow]" + str(pOneFeatUsed[0]) + \
                        "[/color], shielding them from up to [color=red]" + str(stoneskin) + "[/color] "
                        "points of damage.")
        if stonebonus != 0:
            modifier.append(pOneInfo['name'] + " also gained a [color=red]+" + str(stonebonus) + \
                      ",[/color] bonus to hit and damage until [color=yellow]" + str(pOneFeatUsed[0]) +\
                      "[/color] is broken.")
    elif pOneFeatUsed[0] == "greater stoneskin":
        minimum = int(pOneFeatUsed[1][0])
        maximum = int(pOneFeatUsed[1][1])
        stoneskin = random.randint(minimum, maximum)
        stonebonus = 0
        if pOneInfo['build'] == "constitution":
            stonebonus = pOneFeatUsed[1][2]
            stoneskin = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        stoneskin = random.randint(minimum, maximum)
        modifier.append(pOneInfo['name'] + " used [color=yellow]" + str(pOneFeatUsed[0]) + \
                        ",[/color] shielding them from up to [color=red]" + str(stoneskin) + "[/color]"
                        " points of damage.")
        if stonebonus != 0:
            modifier.append(pOneInfo['name'] + " also gained a [color=red]+" + str(stonebonus) + \
                            ",[/color] bonus to hit and damage until [color=yellow]." + str(pOneFeatUsed[0]) +\
                            " is broken.")
    elif pOneFeatUsed[0] == "stoneform":
        minimum = int(pOneFeatUsed[1][0])
        maximum = int(pOneFeatUsed[1][1])
        stoneskin = random.randint(minimum, maximum)
        stonebonus = 0
        if pOneInfo['build'] == "constitution":
            stonebonus = pOneFeatUse[1][2]
            stoneskin = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        stoneskin = random.randint(minimum, maximum)
        modifier.append(pOneInfo['name'] + " used [color=yellow]" + str(pOneFeatUsed[0]) + \
                        ",[/color] shielding them from up to [color=red]" + str(stoneskin) + "[/color]"
                        " points of damage.")
        if stonebonus != 0:
            modifier.append(pOneInfo['name'] + " also gained a [color=red]+" + str(stonebonus) + \
                            ",[/color] bonus to hit and damage until [color=yellow]" + str(pOneFeatUsed[0]) +\
                            " is broken.")
    return stoneskin, stonebonus, modifier

# Crippling Blow
def featCripplingBlow(pOneInfo, pTwoInfo, total):
    modifier = ""
    featDictionary = get_feat_dictionary()
    if "crippling blow" in pTwoInfo['feats taken']:
        if pTwoInfo['build'] == "strength":
            percent = featDictionary[0]["crippling blow"]["action"][2]
            message = featDictionary[0]["crippling blow"]["action"][4]
        else:
            percent = featDictionary[0]["crippling blow"]["action"][1]
            message = featDictionary[0]["crippling blow"]["action"][3]
    if "improved crippling blow" in pTwoInfo['feats taken']:
        if pTwoInfo['build'] == "strength":
            percent = featDictionary[0]["improved crippling blow"]["action"][2]
            message = featDictionary[0]["improved crippling blow"]["action"][4]
        else:
            percent = featDictionary[0]["improved crippling blow"]["action"][1]
            message = featDictionary[0]["improved crippling blow"]["action"][3]
    if "greater crippling blow" in pTwoInfo['feats taken']:
        if pTwoInfo['build'] == "strength":
            percent = featDictionary[0]["greater crippling blow"]["action"][2]
            message = featDictionary[0]["greater crippling blow"]["action"][4]
        else:
            percent = featDictionary[0]["greater crippling blow"]["action"][1]
            message = featDictionary[0]["greater crippling blow"]["action"][3]
        if pTwoInfo['build'] == "strength":
            modifier =  pTwoInfo['name'] + " landed a [color=yellow]crippling blow[/color], Giving " +\
                        pOneInfo['name'] + " a [color=red]-" + message + "[/color] penalty To their damage."
            total = int(total * percent)
        else:
            modifier =  pTwoInfo['name'] + " landed a [color=yellow]crippling blow[color=yellow], Giving " + \
                        pOneInfo['name'] + " a [color=red]-" + message + "[/color] penalty To their damage."
            total = int(total * percent)
    return total, modifier

# Vile Touch Duration
def featVileTouch(pOneInfo, pTwoInfo, pOneFeatUsed, token):
    if (pOneFeatUsed[0] == "vile touch"
            or pOneFeatUsed[0] == "improved vile touch"
            or pOneFeatUsed[0] == "greater vile touch"
            or pOneFeatUsed[0] == "death touch"):
        duration = pOneFeatUsed[1][0]
        return duration

# Vile Touch Damage
# The fucking hardest feat I've EVER had to code in. But quite possibly the BEST mechanic the game has to offer.
# Sylzana's creation
def featOneVileDamage(pOneInfo, pTwoInfo, pOneVile, pTwoVile, vileOne, pOneCurrentHP, pTwoCurrentHP,
                      modifier):
    featDictionary = get_feat_dictionary()
    if "vile touch" in pOneInfo["feats taken"]:
        if pOneInfo['build'] == "dexterity":
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][3]
        else:
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][2]
    elif "improved vile touch" in pOneInfo["feats taken"]:
        if pOneInfo['build'] == "dexterity":
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][3]
        else:
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][2]
    elif "greater vile touch" in pOneInfo["feats taken"]:
        if pOneInfo['build'] == "dexterity":
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][3]
        else:
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][2]
    elif "death touch" in pOneInfo["feats taken"]:
        if pOneInfo['build'] == "dexterity":
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][3]
        else:
            minimum = featDictionary[0]["vile touch"]["action"][1]
            maximum = featDictionary[0]["vile touch"]["action"][2]
    if pOneVile in range(1, 11):
        vileOne = random.randint(minimum, maximum)
        modifier.append(pOneInfo['name'] + "'s vile touch has done [color=red]" + str(vileOne) + \
                   "[/color] damage to " + pTwoInfo['name'])
    return vileOne, modifier

def featHeavyCounter(pOneInfo, pOneFeatUsed):
    modifier = ""
    featDictionary = get_feat_dictionary()
    print("In Heavy Counter: ")
    if "heavy hand" in pOneInfo["feats taken"]:
        bonus = featDictionary[0]["heavy hand"]["action"]
        if pOneInfo['build'] == "strength":
            word = bonus[1]
            duration = bonus[0]
        else:
            word = bonus[2]
            duration = bonus[0]
    if "improved heavy hand" in pOneInfo["feats taken"]:
        bonus = featDictionary[0]["improved heavy hand"]["action"]
        if pOneInfo['build'] == "strength":
            word = bonus[1]
            duration = bonus[0]
        else:
            word = bonus[2]
            duration = bonus[0]
    elif "greater heavy hand" in pOneInfo["feats taken"]:
        bonus = featDictionary[0]["greater heavy hand"]["action"]
        if pOneInfo['build'] == "strength":
            word = bonus[1]
            duration = bonus[0]
        else:
            word = bonus[2]
            duration = bonus[0]
    modifier = pOneInfo['name'] + " used the feat [color=yellow]heavy hand[/color], improving base damage " \
                                  "by " + str(word) + " for [color=yellow] " + str(duration) + "[/color] turns."
    return duration, modifier

# Heavy Hand
def featHeavyHand(pOneInfo, pOneMaximum, pOneHeavy):
    modifier = ""
    featDictionary = get_feat_dictionary()
    if "heavy hand" in pOneInfo["feats taken"]:
        bonus = featDictionary[0]["heavy hand"]["action"]
        if pOneInfo['build'] == "strength":
            pOneMaximum += bonus[1]
        else:
            pOneMaximum += bonus[2]
    if "improved heavy hand" in pOneInfo["feats taken"]:
        bonus = featDictionary[0]["improved heavy hand"]["action"]
        if pOneInfo['build'] == "strength":
            pOneMaximum = bonus[1]
        else:
            pOneMaximum += bonus[2]
    elif "greater heavy hand" in pOneInfo["feats taken"]:
        bonus = featDictionary[0]["greater heavy hand"]["action"]
        if pOneInfo['build'] == "strength":
            pOneMaximum += bonus[1]
        else:
            pOneMaximum += bonus[2]
    pOneHeavy -= 1
    modifier = pOneInfo["name"] + " strikes with a [color=yellow]heavy hand[/color]"
    return pOneMaximum, pOneHeavy, modifier

# Titan Blow
def featTitanBlow(pOneInfo, pTwoInfo, pOneFeatUsed, damage):
    if pOneInfo['build'] == "strength":
        modifier =  pOneInfo['name'] + " used the feat [color=yellow]titan blow[color=yellow]. Applying a " \
                                      "[color=red]+14[/color] bonus to damage rolled."
        damage = damage + pOneFeatUsed[1][1]
    else:
        modifier =  pOneInfo['name'] + " used the feat [color=yellow]titan blow[color=yellow]. Applying a " \
                                      "[color=red]+10[/color] bonus to damage rolled."
        damage = damage + pOneFeatUsed[1][0]
    return damage, modifier

# Staggering Blow
def featStaggeringBlow(pOneInfo, pTwoInfo, strength, nonStrength, total):
    if pTwoInfo['build'] == "strength":
        modifier =  pTwoInfo['name'] + " used the feat [color=yellow]staggering blow[color=yellow], reducing " + \
                   pOneInfo['name'] + "'s damage by -14"
        total -= strength
    else:
        modifier =  pTwoInfo['name'] + " used the feat [color=yellow]staggering blow[color=yellow], reducing " + \
                   pOneInfo['name'] + "'s damage by -10"
        total -= nonStrength
    return total, modifier

# Nerve Strike
def featNerveStrike(pOneInfo, pTwoInfo, total, hit, totalAC):
    featDictionary = get_feat_dictionary()
    modifier = ""
    nerveDamage = 0
    if 'nerve strike' in pOneInfo['feats taken']:
        if pOneInfo['build'] == "dexterity":
            minimum = featDictionary[0]["nerve strike"]["action"][0]
            maximum = featDictionary[0]["nerve strike"]["action"][2]
        else:
            minimum = featDictionary[0]["nerve strike"]["action"][0]
            maximum = featDictionary[0]["nerve strike"]["action"][1]
        if total >= (totalAC + 5) or hit == 20:
            nerveDamage = random.randint(minimum, maximum)
            modifier =  pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +\
                       str(nerveDamage) + "[/color] to their opponent."
    elif 'improved nerve strike' in pOneInfo['feats taken']:
        if pOneinfo['build'] == "dexterity":
            minimum = featDictionary[0]["nerve strike"]["action"][2]
            maximum = featDictionary[0]["nerve strike"]["action"][3]
        else:
            minimum = featDictionary[0]["nerve strike"]["action"][0]
            maximum = featDictionary[0]["nerve strike"]["action"][1]
        if total >= (totalAC + 5) or hit == 20:
            nerveDamage = random.randint(minimum, maximum)
            modifier =  pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +\
                       str(nerveDamage) + "[/color] to their opponent."
    elif 'greater nerve strike' in pOneInfo['feats taken']:
        if pOneinfo['build'] == "dexterity":
            minimum = featDictionary[0]["nerve strike"]["action"][2]
            maximum = featDictionary[0]["nerve strike"]["action"][3]
        else:
            minimum = featDictionary[0]["nerve strike"]["action"][0]
            maximum = featDictionary[0]["nerve strike"]["action"][1]
        if total >= (totalAC + 5) or hit == 20:
            nerveDamage = random.randint(minimum, maximum)
            modifier =  pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +\
                       str(nerveDamage) + "[/color] to their opponent."
    if 'nerve damage' in pOneInfo['feats taken']:
        if pOneinfo['build'] == "dexterity":
            minimum = featDictionary[0]["nerve strike"]["action"][0]
            maximum = featDictionary[0]["nerve strike"]["action"][2]
        else:
            minimum = featDictionary[0]["nerve strike"]["action"][0]
            maximum = featDictionary[0]["nerve strike"]["action"][1]
        if total >= (totalAC + 5) or hit == 20:
            nerveDamage = random.randint(minimum, maximum)
            modifier =  pOneInfo['name'] + " managed to strike a nerve, doing an additional [color=red]" +\
                       str(nerveDamage) + "[/color] to their opponent."
    return nerveDamage, modifier

# Hurt Me
def featHurtMe(pOneInfo, pTwoInfo, pOneCurrentHP, pOneTotalHP, pOneModifier, bonusHurt):
    modifier = ""
    number = (pOneCurrentHP / pOneTotalHP) * 100
    percentage = int(number)
    featDictionary = get_feat_dictionary()
    if 'hurt me' in pOneInfo['feats taken']:
        hurtMe = featDictionary[0]["hurt me"]["action"]
        if 33 < percentage <= 66:
            bonusHurt = hurtMe[0]
            modifier =  pOneInfo['name'] + " has become enraged because of [color=yellow]" \
                                           "hurt me[/color], and obtains a [color=red]+" + hurtMe[2] +\
                                           " [/color]bonus to their damage."
        elif percentage <= 33:
            bonusHurt = hurtMe[1]
            modifier =  pOneInfo['name'] + " has become further enraged because of [color=yellow]" \
                                           "hurt me,[/color] and obtains a [color=red]+" + hurtMe[3] +\
                                           " [/color]bonus to their damage."
    elif 'improved hurt me' in pOneInfo['feats taken']:
        hurtMe = featDictionary[0]["improved hurt me"]["action"]
        if 33 < percentage <= 66:
            bonusHurt = hurtMe[0]
            modifier =  pOneInfo['name'] + " has become enraged because of [color=yellow]" \
                                           "hurt me[/color], and obtains a [color=red]+" + hurtMe[2] +\
                                           " [/color]bonus to their damage."
        elif percentage <= 33:
            bonusHurt = hurtMe[1]
            modifier =  pOneInfo['name'] + " has become enraged because of [color=yellow]" \
                                           "hurt me[/color], and obtains a [color=red]+" + hurtMe[3] +\
                                           " [/color]bonus to their damage."
    elif 'greater hurt me' in pOneInfo['feats taken']:
        hurtMe = featDictionary[0]["greater hurt me"]["action"]
        if 33 < percentage <= 66:
            bonusHurt = hurtMe[0]
            modifier =  pOneInfo['name'] + " has become enraged because of [color=yellow]" \
                                           "hurt me[/color], and obtains a [color=red]+" + hurtMe[2] +\
                                           " [/color]bonus to their damage."
        elif percentage <= 33:
            bonusHurt = hurtMe[1]
            modifier =  pOneInfo['name'] + " has become further enraged because of [color=yellow]" \
                                           "hurt me,[/color] and obtains a [color=red]+" + hurtMe[3] +\
                                           " [/color]bonus to their damage."
    elif 'hurt me more' in pOneInfo['feats taken']:
        hurtMe = featDictionary[0]["hurt me more"]["action"]
        if 50 < percentage <= 75:
            bonusHurt = hurtMe[0]
            modifier =  pOneInfo['name'] + " has become enraged because of [color=yellow]" \
                                           "hurt me[/color], and obtains a [color=red]+" + hurtMe[3] +\
                                           " [/color]bonus to their damage."
        elif 25 < percentage <= 50:
            bonusHurt = hurtMe[1]
            modifier =  pOneInfo['name'] + " has become further enraged because of [color=yellow]" \
                                           "hurt me,[/color] and obtains a [color=red]+" + hurtMe[4] +\
                                           " [/color]bonus to their damage."
        elif percentage <= 25:
            bonusHurt = hurtMe[2]
            modifier =  pOneInfo['name'] + " has become further enraged because of [color=yellow]" \
                                           "hurt me,[/color] and obtains a [color=red]+" + hurtMe[5] +\
                                           " [/color]bonus to their damage."
    return bonusHurt, modifier

def featRelentlessCounter(pOneInfo, pOneFeatUsed):
    if (pOneFeatUsed[0] == "relentless"
            or pOneFeatUsed[0] == "improved relentless"
            or pOneFeatUsed[0] == "greater relentless"
            or pOneFeatUsed[0] == "unforgiving"):
        duration = pOneFeatUsed[1][0]
    return duration

def featRelentlessDamage(pOneRelentless, pOneRelentlessDamage, pOneInfo, totalHit, totalAC, hit):
    modifier = ""
    featDictionary = get_feat_dictionary()
    if pOneRelentless == 1:
        modifier = pOneInfo['name'] + "'s [color=yellow]relentlessness[/color] has paid off, doing an" \
                                      " additional[color=red] " + str(pOneRelentlessDamage) + "[/color] damage"
    elif "relentless" in pOneInfo['feats taken'] or "improved relentess" in pOneInfo['feats taken']:
        relent = featDictionary[0]["relentless"]["action"]
        if pOneInfo['build'] == "strength":
            if totalHit > totalAC:
                pOneRelentlessDamage += relent[1]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" +\
                           relent[3] + "[/color] to potential damage"
            else:
                pOneRelentlessDamage += relent[2]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" + \
                           relent[4] + "[/color] to potential damage"
        else:
            if totalHit > totalAC:
                pOneRelentlessDamage += relent[2]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" +\
                           relent[4] + "[/color] to potential damage"
    elif "greater relentless" in pOneInfo['feats taken'] or "unforgiving" in pOneInfo['feats taken']:
        relent = featDictionary[0]["unforgiving"]["action"]
        if pOneInfo['build'] == "strength":
            if totalHit > totalAC:
                pOneRelentlessDamage += relent[1]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" + \
                           relent[6] + "[/color] to potential damage"
            elif hit == 20:
                pOneRelentlessDamage += relent[3]
                modifier = pOneInfo["name"] + " is [color=yellow]unforgiving[/color], and has added [color=red]+" +\
                           relent[8] + "[/color] to potential damage"
            elif hit == 1:
                pOneRelentlessDamage += relent[4]
                modifier = pOneInfo["name"] + "'s mistake strengthens their resolve, and has made them [color=yellow]unforgiving[/color], adding [color=red]+" + \
                           relent[9] + "[/color] to potential damage"
            else:
                pOneRelentlessDamage += relent[2]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" + \
                           relent[7] + "[/color] to potential damage"
        else:
            if totalHit > totalAC:
                pOneRelentlessDamage += relent[3]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" + \
                           relent[7] + "[/color] to potential damage"
            else:
                pOneRelentlessDamage += relent[5]
                modifier = pOneInfo["name"] + "'s [color=yellow]relentlessness[/color] has added [color=red]+" + \
                           relent[10] + " to potential damage"
    pOneRelentless -= 1
    return pOneRelentless, pOneRelentlessDamage, modifier

# Bullrush
def featBullrush(pOneInfo, pTwoInfo, pOneFeatInfo, pOneBullrush, total):
    modifier = ""
    featDictionary = get_feat_dictionary()
    if pOneBullrush == 0:
        if "bullrush" in pOneInfo["feats taken"]:
            bullrush = featDictionary[0]["bullrush"]["action"]
        elif "improved bullrush" in pOneInfo["feats taken"]:
            bullrush = featDictionary[0]["improved bullrush"]["action"]
        elif "greater bullrush" in pOneInfo["feats taken"]:
            bullrush = featDictionary[0]["greater bullrush"]["action"]
        modifier = pOneInfo["name"] + " managed to overwhelm " + pTwoInfo["name"] + " with [color=yellow]" +\
                   pOneFeatInfo[0] + "[/color], allowing them an immediate second attack at [color=red]" +\
                   bullrush[1] + "%[/color] damage."
        pOneBullrush = 1
    elif pOneBullrush == 1:
        if "bullrush" in pOneInfo["feats taken"]:
            bullrush = featDictionary[0]["bullrush"]["action"]
        elif "improved bullrush" in pOneInfo["feats taken"]:
            bullrush = featDictionary[0]["improved bullrush"]["action"]
        elif "greater bullrush" in pOneInfo["feats taken"]:
            bullrush = featDictionary[0]["greater bullrush"]["action"]
        total = int(total * bullrush[0])
        pOneBullrush = 0
    return pOneBullrush, total, modifier

#Sunder
def featSunder(pOneInfo, pTwoInfo):
    modifier = ""
    featDictionary = get_feat_dictionary()
    if "sunder" in pOneInfo['feats taken']:
        sunder = featDictionary[0]["sunder"]["action"]
    elif "improved sunder" in pOneInfo['feats taken']:
        sunder = featDictionary[0]["improved sunder"]["action"]
    elif "greater sunder" in pOneInfo['feats taken']:
        sunder = featDictionary[0]["greater sunder"]["action"]
    if pOneInfo['build'] == "strength":
        duration = sunder[0]
        amount = sunder[1]
        modifier = pOneInfo["name"] + " managed to reduce " + pTwoInfo["name"] + "'s Armor Class by [color=green]" +\
                   sunder[4] + "[/color] for [color=yellow]" + sunder[3] + "[/color] rounds."
    else:
        duration = sunder[0]
        amount = sunder[2]
        modifier = pOneInfo["name"] + "managed to reduce " + pTwoInfo["name"] + "'s Armor Class by [color=green]" + \
                   sunder[5] + "[/color] for [color=yellow]" + sunder[3] + "[/color] rounds."
    return duration, amount, modifier

# Focus
def featFocus(pOneInfo, pOneCurrentHP, pOneTotalHP, pOneMinimum, pOneMaximum):
    modifier = ""
    number = (pOneCurrentHP / pOneTotalHP) * 100
    percentage = int(number)
    featDictionary = get_feat_dictionary()
    if "focus" in pOneInfo['feats taken']:
        focus = featDictionary[0]["focus"]["action"]
        if 33 < percentage <= 66:
            pOneMinimum = focus[0]
            pOneMaximum = focus[1]
            modifier = pOneInfo['name'] + " has become more focused because of [color=yellow]" \
                                          "focus[/color], increasing base damage to [color=red]" + focus[4]
        elif percentage <= 33:
            pOneMinimum = focus[2]
            pOneMaximum = focus[3]
            modifier = pOneInfo['name'] + " has become further focused because of [color=yellow]" \
                                          "focus,[/color] increasing base damage to [color=red]+" + focus[5]
    # elif 'improved focus' in pTwoInfo['feats taken']:
    #     focus = featDictionary[0]["improved focus"]["action"]
    #     if 33 < percentage <= 66:
    #         bonusFocus = focus[0]
    #         modifier = pTwoInfo['name'] + " has become more focused because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[2] +\
    #                                       "(For testing purposees: Minimum is set to " + str(pOneMinimum) +\
    #                                       "and Maximum is set to " + str(pOneMaximum)
    #
    #     elif percentage <= 33:
    #         bonusFocus = focus[1]
    #         modifier = pTwoInfo['name'] + " has become enraged because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[3] + \
    #                                       " [/color] bonus to their armor class."
    # elif 'greater focus' in pTwoInfo['feats taken']:
    #     focus = featDictionary[0]["greater focus"]["action"]
    #     if 33 < percentage <= 66:
    #         bonusFocus = focus[0]
    #         modifier = pTwoInfo['name'] + " has become more focused because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[2] +\
    #                                       " [/color]bonus to their armor class."
    #     elif percentage <= 33:
    #         bonusFocus = focus[1]
    #         modifier = pTwoInfo['name'] + " has become enraged because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[3] + \
    #                                       " [/color] bonus to their armor class."
    # elif 'perfect focus' in pTwoInfo['feats taken']:
    #     focus = featDictionary[0]["perfect focus"]["action"]
    #     if 50 < percentage <= 75:
    #         bonusFocus = focus[0]
    #         modifier = pTwoInfo['name'] + " has become more focused because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[2] +\
    #                                       " [/color]bonus to their armor class."
    #     elif 25 < percentage <= 50:
    #         bonusFocus = focus[1]
    #         modifier = pTwoInfo['name'] + " has become enraged because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[3] + \
    #                                       " [/color] bonus to their armor class."
    #     elif percentage <= 25:
    #         bonusFocus = focus[1]
    #         modifier = pTwoInfo['name'] + " has become enraged because of [color=yellow]" \
    #                                       "improved focus[/color], and obtains a [color=red]+" + focus[3] + \
    #                                       " [/color] bonus to their armor class."
    return pOneMinimum, pOneMaximum, modifier
# Reckless Abandon
def featRecklessAbandon(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP, total, pOneFeatUsed):
    modifier = ""
    if pOneFeatUsed[0] == "reckless abandon":
        if pOneInfo['build'] == "constitution":
            damageToPTwo = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][3]))
            damageToPOne = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][1]))
        else:
            damageToPTwo = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][2]))
            damageToPOne = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][1]))
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        modifier =  pOneInfo['name'] + " did [color=red]" + str(damageToPOne) +\
                   "[/color] damage to themselves, to deal an additional [color=red]" + str(damageToPTwo) +\
                   "[/color] damage to their opponent."
    elif pOneFeatUsed[0] == "improved reckless abandon":
        if pOneInfo['build'] == "constitution":
            damageToPTwo = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][3]))
            damageToPOne = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][1]))
        else:
            damageToPTwo = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][2]))
            damageToPOne = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][1]))
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        modifier =  pOneInfo['name'] + " did [color=red]" + str(damageToPOne) +\
                   "[/color] damage to themselves, to deal an additional [color=red]" +\
                   str(damageToPTwo) + "[/color] damage to their opponent."
    elif pOneFeatUsed[0] == "greater reckless abandon":
        if pOneInfo['build'] == "constitution":
            damageToPTwo = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][4]))
            damageToPOne = random.randint(int(pOneFeatUsed[1][3]), int(pOneFeatUsed[1][1]))
        else:
            damageToPTwo = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][2]))
            damageToPOne = random.randint(int(pOneFeatUsed[1][0]), int(pOneFeatUsed[1][1]))
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        modifier =  pOneInfo['name'] + " did [color=red]" + str(damageToPOne) +\
                   "[/color] damage to themselves, to deal an additional [color=red]" + str(damageToPTwo) +\
                   "[/color] damage to their opponent."
    elif pOneFeatUsed[0] == "abandon hope":
        if pOneInfo['build'] == "constitution":
            damageToPTwo = int(pOneFeatUsed[1][0])
            damageToPOne = int(pOneFeatUsed[1][2])
        else:
            damageToPTwo = int(pOneFeatUsed[1][0])
            damageToPOne = int(pOneFeatUsed[1][1])
        pOneCurrentHP = pOneCurrentHP - damageToPOne
        total = total + damageToPTwo
        modifier =  pOneInfo['name'] + " did [color=red]" + str(damageToPOne) +\
                   "[/color] damage to themselves, to deal an additional [color=red]" + str(damageToPTwo) +\
                   "[/color] damage to their opponent."
    return pOneCurrentHP, total, modifier

# Quick Strike Counter
def featQuickCounter(pOneInfo, pTwoInfo, pOneFeatUsed):
    if (pOneFeatUsed[0] == "quick strike"
            or pOneFeatUsed[0] == "improved quick strike"
            or pOneFeatUsed[0] == "greater quick strike"
            or pOneFeatUsed[0] == "riposte"):
        duration = pOneFeatUsed[1][3]
        return duration

# Quick Strike
def featQuickStrike(pOneInfo, pTwoInfo, pTwoQuick, pTwoFeatUsed):
    modifier = ""
    pTwoModifier = pTwoInfo['tdamage']
    featDictionary = get_feat_dictionary()
    if "quick strike" in pTwoInfo["feats taken"]:
        if pTwoInfo['build'] == "dexterity":
            minimum = featDictionary[0]["quick strike"]["action"][0]
            maximum = featDictionary[0]["quick strike"]["action"][2]
        else:
            minimum = featDictionary[0]["quick strike"]["action"][0]
            maximum = featDictionary[0]["quick strike"]["action"][1]
    elif "improved quick strike" in pTwoInfo["feats taken"]:
        if pTwoInfo['build'] == "dexterity":
            minimum = featDictionary[0]["improved quick strike"]["action"][0]
            maximum = featDictionary[0]["improved quick strike"]["action"][2]
        else:
            minimum = featDictionary[0]["improved quick strike"]["action"][0]
            maximum = featDictionary[0]["improved quick strike"]["action"][1]
    elif "greater quick strike" in pTwoInfo["feats taken"]:
        if pTwoInfo['build'] == "dexterity":
            minimum = featDictionary[0]["greater quick strike"]["action"][0]
            maximum = featDictionary[0]["greater quick strike"]["action"][2]
        else:
            minimum = featDictionary[0]["greater quick strike"]["action"][0]
            maximum = featDictionary[0]["greater quick strike"]["action"][1]
    elif "riposte" in pTwoInfo["feats taken"]:
        if pTwoInfo['build'] == "dexterity":
            minimum = featDictionary[0]["riposte"]["action"][0]
            maximum = featDictionary[0]["riposte"]["action"][2]
        else:
            minimum = featDictionary[0]["riposte"]["action"][0]
            maximum = featDictionary[0]["riposte"]["action"][1]
    if pTwoQuick in range(1, 5):
        damage = random.randint(minimum, maximum)
        pTwoQuickDamage = int(damage)
        if pTwoInfo['build'] == "dexterity":
            pTwoQuickDamage += int(pTwoInfo['dexterity'] / 4)
        modifier = pTwoInfo['name'] + "'s quick strike has done [color=red]" + str(pTwoQuickDamage) + \
                   "[/color] damage to " + pOneInfo['name']
    return pTwoQuickDamage, modifier

# Life Leech
def featLifeLeech(pOneInfo, pTwoInfo, damage, pOneFeatUsed, token):
    modifier = ""
    conMod = int(pOneInfo['constitution'] / 2)
    # if token == 1:
    if pOneFeatUsed[0] == "lifeleech" and damage > 0:
        if pOneInfo['build'] == "constitution":
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][2]) + conMod
        else:
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][1])
        modifier =  pOneInfo['name'] + " has healed [color=red]" + str(pOneHeal) + "[/color] hit points."
    elif pOneFeatUsed[0] == "improved lifeleech" and damage > 0:
        if pOneInfo['build'] == "constitution":
            pOneHeal = random.randint(pOneFeatUsed[1][2], pOneFeatUsed[1][3]) + conMod
        else:
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][1])
        modifier =  pOneInfo['name'] + " has healed [color=red]" + str(pOneHeal) + "[/color] hit points."
    elif pOneFeatUsed[0] == "greater lifeleech" and damage > 0:
        if pOneInfo['build'] == "constitution":
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][2]) + conMod
        else:
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][1])
        modifier =  pOneInfo['name'] + " has healed [color=red]" + str(pOneHeal) + "[/color] hit points."
    elif pOneFeatUsed[0] == "improved lifeleech" and damage > 0:
        if pOneInfo['build'] == "constitution":
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][2]) + conMod
        else:
            pOneHeal = random.randint(pOneFeatUsed[1][0], pOneFeatUsed[1][1])
        modifier =  pOneInfo['name'] + " has healed [color=red]" + str(pOneHeal) + "[/color] hit points."
    elif pOneFeatUsed[0] == "lifedrain" and damage > 0:
        if pOneInfo['build'] == "constitution":
            pOneHeal = pOneFeatUsed[1][0]
        else:
            pOneHeal = pOneFeatUsed[1][1] + conMod
        modifier =  pOneInfo['name'] + " has healed [color=red]" + str(pOneHeal) + "[/color] hit points."
    return pOneHeal, modifier, damage

# Evasion
def featEvasion(pOneInfo, pTwoInfo, bEvasion):
    modifier = ""
    if "evasion" in pTwoInfo['feats taken']:
        bEvasion = True
        modifier =  pTwoInfo['name'] + " has an evasion available for use. Type [color=pink]!evasion [/color]" \
                                      "to use, or type [color=pink]!pass[/color]"
    elif "improved evasion" in pTwoInfo['feats taken']:
        bEvasion = True
        modifier =  pTwoInfo['name'] + " has an evasion available for use. Type [color=pink]!evasion [/color]" \
                                      "to use, or type [color=pink]!pass[/color]"
    elif "greater evasion" in pTwoInfo['feats taken']:
        bEvasion = True
        modifier =  pTwoInfo['name'] + " has an evasion available for use. Type [color=pink]!evasion [/color]" \
                                      "to use, or type [color=pink]!pass[/color]"
    return bEvasion, modifier

# Deaths Door
def featDeathsDoor(pOneInfo, pTwoInfo, pTwoCurrentHP, pTwoDeathsDoor):
    featDictionary = get_feat_dictionary()
    modifier = ""
    revive = random.randint(1, 100)
    if pTwoCurrentHP <= 0:
        if ("greater deaths door" in pTwoInfo['feats taken']
                and revive in range(1, 101)
                and pTwoDeathsDoor == 0):
            minimum = featDictionary[0]["greater deaths door"]["action"][0]
            maximum = featDictionary[0]["greater deaths door"]["action"][1]
            returnHeal = random.randint(minimum, maxiumum) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP = 0
            pTwoCurrentHP += returnHeal
            modifier =  pTwoInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +\
                       "[/color] hit points."
        elif ("improved deaths door" in pTwoInfo['feats taken']
                and revive in range(25, 101)
                and pTwoDeathsDoor == 0):
            minimum = featDictionary[0]["improved deaths door"]["action"][0]
            maximum = featDictionary[0]["improved deaths door"]["action"][1]
            returnHeal = random.randint(minimum, maximum) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP = 0
            pTwoCurrentHP += returnHeal
            modifier =  pTwoInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +\
                       "[/color] hit points."
        elif ("deaths door" in pTwoInfo['feats taken']
                and revive in range(50, 101)
                and pTwoDeathsDoor == 0):
            minimum = featDictionary[0]["deaths door"]["action"][0]
            maximum = featDictionary[0]["deaths door"]["action"][1]
            returnHeal = random.randint(minimum, maximum) + int(pTwoInfo['constitution'] / 2)
            pTwoCurrentHP = 0
            pTwoCurrentHP += returnHeal
            modifier =  pTwoInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +\
                       "[/color] hit points."
        else:
            modifier = pTwoInfo['name'] + " 's death's door has failed to kick in, leaving them defeated."
        pTwoDeathsDoor = 1
    return pTwoCurrentHP, pTwoDeathsDoor, modifier

# Deaths Door (onMSGUtils)
def evasionDeathDoor(pOneInfo, pTwoInfo, pOneCurrentHP, pOneDeathsDoor):
    featDictionary = get_feat_dictionary()
    modifier = ""
    revive = random.randint(1, 100)
    if ("deaths door" in pOneInfo['feats taken']
            and pOneCurrentHP <= 0
            and revive <= 50
            and pOneDeathsDoor == 0):
        minimum = featDictionary[0]["death door"]["action"][0]
        maximum = featDictionary[0]["death door"]["action"][1]
        returnHeal = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        pOneCurrentHP += returnHeal
        modifier =  pOneInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +\
                   "[/color] hit points."
    elif ("improved deaths door" in pOneInfo['feats taken']
            and pOneCurrentHP <= 0
            and revive <= 75
            and pOneDeathsDoor == 0):
        minimum = featDictionary[0]["improved death door"]["action"][0]
        maximum = featDictionary[0]["improved death door"]["action"][1]
        returnHeal = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        pOneCurrentHP += returnHeal
        modifier =  pOneInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +\
                   "[/color] hit points."
    elif ("greater deaths door" in pOneInfo['feats taken']
            and pOneCurrentHP <= 0
            and revive <= 100
            and pOneDeathsDoor == 0):
        minimum = featDictionary[0]["greater death door"]["action"][0]
        maximum = featDictionary[0]["greater death door"]["action"][1]
        returnHeal = random.randint(minimum, maximum) + int(pOneInfo['constitution'] / 2)
        pOneCurrentHP += returnHeal
        modifier =  pOneInfo['name'] + " has returned from death's door, regaining [color=red]" + str(returnHeal) +\
                   "[/color] hit points."
    pOneDeathsDoor = 1
    return pTwoCurrentHP, pOneDeathsDoor, modifier

def featInnerDuration(pOneInfo):
    featDictionary = get_feat_dictionary()
    modifier = ""
    if "inner strength" in pOneInfo["feats taken"]:
        duration = featDictionary[0]["inner strength"]["action"][0]
    elif "improved inner strength" in pOneInfo["feats taken"]:
        duration = featDictionary[0]["improved inner strength"]["action"][0]
    elif "greater inner strength" in pOneInfo["feats taken"]:
        duration = featDictionary[0]["greater inner strength"]["action"][0]
    rounds = duration / 2
    bonus = pOneInfo['tdr']
    innerBonus = bonus * 2
    modifier = pOneInfo["name"] + " has tapped into their [color=yellow]inner strength[/color], sacrificing [color=red]"\
               + str(bonus) + "[/color] DR for [color=red]+" + str(innerBonus) + "[/color] to hit for "\
               + str(rounds) + " turns."
    print("why?")
    return innerBonus, duration, modifier

def featExposeCounter(pOneInfo, pTwoInfo):
    featDictionary = get_feat_dictionary()
    print("Why?")
    if "expose" in pOneInfo["feats taken"]:
        print("inside expose statement")
        expose = featDictionary[0]["expose"]["action"]
        if pOneInfo['build'] == 'dexterity':
            duration = expose[0]
        else:
            duration = expose[0]
    elif "improved expose" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["improved expose"]["action"]
        if pOneInfo['build'] == 'dexterity':
            duration = expose[0]
        else:
            duration = expose[0]
    elif "greater expose" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["greater expose"]["action"]
        if pOneInfo['build'] == 'dexerity':
            duration = expose[0]
        else:
            duration = expose[0]
    elif "exploit" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["exploit"]["action"]
        if pOneInfo['build'] == 'dexterity':
            duration = expose[0]
        else:
            duration = expose[0]
        modifier = pOneInfo["name"] + " has used [color=yellow]expose[/color]"
    return duration, modifier

def featExpose(pOneInfo, pTwoInfo):
    featDictionary = get_feat_dictionary()
    modifier = ""
    print("Why?")
    if "expose" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["expose"]["action"]
        if pOneInfo['build'] == 'dexterity':
            defense = expose[2]
        else:
            defense = expose[1]
    elif "improved expose" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["improved expose"]["action"]
        if pOneInfo['build'] == 'dexterity':
            defense = expose[2]
        else:
            defense = expose[1]
    elif "greater expose" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["greater expose"]["action"]
        if pOneInfo['build'] == 'dexerity':
            defense = expose[2]
        else:
            defense = expose[1]
    elif "exploit" in pOneInfo["feats taken"]:
        expose = featDictionary[0]["exploit"]["action"]
        if pOneInfo['build'] == 'dexterity':
            defense = expose[2]
        else:
            defense = expose[1]
    modifier = pOneInfo["name"] + " has [color=yellow]exposed[/color] " + pTwoInfo["name"] +\
               "'s weakness, removing [color=red]" + str(defense) + "[/color] points from their DR/Regeneration."
    return defense, modifier

def featExposeRegeneration(pOneInfo, pTwoInfo):
    featDictionary = get_feat_dictionary()
    if "expose" in pTwoInfo["feats taken"]:
        expose = featDictionary[0]["expose"]["action"]
        if pTwoInfo['build'] == 'dexterity':
            defense = expose[2]
        else:
            defense = expose[1]
    elif "improved expose" in pTwoInfo["feats taken"]:
        expose = featDictionary[0]["improved expose"]["action"]
        if pTwoInfo['build'] == 'dexterity':
            defense = expose[2]
        else:
            defense = expose[1]
    elif "greater expose" in pTwoInfo["feats taken"]:
        expose = featDictionary[0]["greater expose"]["action"]
        if pTwoInfo['build'] == 'dexerity':
            defense = expose[2]
        else:
            defense = expose[1]
    elif "exploit" in pTwoInfo["feats taken"]:
        expose = featDictionary[0]["exploit"]["action"]
        if pTwoInfo['build'] == 'dexterity':
            defense = expose[1]
        else:
            defense = expose[0]
    modifier = pTwoInfo["name"] + " has [color=yellow]exposed[/color] " + pOneInfo["name"] +\
               "'s weakness, removing [color=red]" + str(defense) + "[/color] points from their DR/Regeneration."
    return defense, modifier
def featCheapShot(pOneInfo, pTwoInfo):
    featDictionary = get_feat_dictionary()
    modifier = ""
    lockout = random.randint(1, 100)
    pOneLockout = 0
    print(lockout)
    if "cheap shot" in pOneInfo["feats taken"]:
        cheap = featDictionary[0]["cheap shot"]["action"]
        pOneCheapShot = cheap[0]
        if lockout <= cheap[1]:
            pOneLockout = 1
            print(pOneLockout)
        word = cheap[2]
        duration = cheap[3]
    elif "improved cheap shot" in pOneInfo["feats taken"]:
        cheap = featDictionary[0]["improved cheap shot"]["action"]
        pOneCheapShot = cheap[0]
        if lockout <= cheap[1]:
            pOneLockout = 1
        word = cheap[2]
        duration = cheap[3]
    elif "greater cheap shot" in pOneInfo["feats taken"]:
        cheap = featDictionary[0]["greater cheap shot"]["action"]
        pOneCheapShot = cheap[0]
        if lockout <= cheap[1]:
            pOneLockout = 1
        word = cheap[2]
        duration = cheap[3]
    modifier = pOneInfo["name"] + " has landed a [color=yellow]cheap shot[/color] on " +\
               pTwoInfo["name"] + " giving them a " + word + " penalty when attempting to use a feat for " +\
               duration + " turns."
    return pOneCheapShot, pOneLockout, modifier