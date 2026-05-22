import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# 96
def stoneskinDRCheck(pOneInfo, pTwoInfo, pOneFeatDamage, pTwoFeatDamage):
    # Apply stoneskin if needed
    print("Token: " + str(token))
    if pTwoStoneskin != 0 and total > 0:
        newTotal = total
        print("total + vileOne: " + str(newTotal))
        pTwoStoneskin -= newTotal
        if pTwoStoneskin <= 0:
            newStone = abs(pTwoStoneskin)
            difference = newTotal - newStone
            newTotal -= difference
            print("difference: " + str(difference))
            total = newTotal
            print("total: " + str(total))
            modifier = pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" + \
                       str(difference) + "[/color] damage, and has broken"
            newDamage = 1
            pTwoStoneskin = 0
            pTwoStonebonus = 0
            vileOne = 0
        else:
            modifier = pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +\
                       str(total) + "[/color] damage, with [color=red] " + str(pTwoStoneskin) +\
                       "[/color] points remaining."
            newDamage = 1
            total = 0
            vileOne = 0
    if pTwoInfo['tdr'] != 0 and total > 0:
        modifier = pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +\
                   str(pTwoInfo['tdr']) + "[/color] hp of damage from opponent's roll."
        total -= pTwoInfo['tdr']
        newDamage = 1
    return modifier, total, pTwoStoneskin, pTwoStonebonus, newDamage

def missBlurSKDRCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP, pOneStoneskin, pTwoMissDamage, vileOne):
    modifier = ""
    if pOneStoneskin != 0 and pTwoMissDamage > 0:
        newTotal = pTwoMissDamage
        oldStoneskin = pOneStoneskin
        pOneStoneskin -= newTotal
        if pOneStoneskin <= 0:
            newStone = abs(pOneStoneskin)
            difference = newTotal - newStone
            pTwoQuickDamage -= difference
            modifier = pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +\
                       str(difference) + "[/color] damage, and has broken."
            pOneStoneskin = 0
            pOneStonebonus = 0
            pTwoQuicKDamage = 0
        else:
            modifier = pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +\
                       str(pTwoMissDamage) + "[/color] damage, with [color=red] " + str(pOneStoneskin) +\
                       "[/color] points remaining."

            pTwoMissDamage = 0

    if pOneInfo['tdr'] != 0 and pTwoMissDamage > 0:
        modifier = pOneInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +\
                   str(pOneInfo['tdr']) + "[/color] hp of damage from opponent's roll."
        pTwoMissDamage -= pOneInfo['tdr']

    if pTwoInfo['tdr'] != 0 and vileOne > 0:
        modifier = pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +\
                   str(pTwoInfo['tdr']) + "[/color] hp of damage from opponent's roll."
        vileOne -= pTwoInfo['tdr']

    # If damage falls below 0 after applying stoneskin/DR, set damage to 0
    if pTwoMissDamage < 0:
        pTwoMissamage = 0

    # subtract damage from current hp
    pOneCurrentHP -= pTwoMissDamage
    pTwoCurrentHP -= vileOne
    return modifier, pOneStoneskin, pOneStonebonus, pOneCurrentHP, pTwoCurrentHP

def regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, token):
    # apply regeneration
    if token == 1 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
        modifier = pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) + " hp."
        pOneCurrentHP += pOneInfo['regeneration']
        if pOneCurrentHP > pOneTotalHP:
            pOneCurrentHP = pOneTotalHP
    elif token == 2 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
        modifier = pOneInfo['name'] + " has regenerated " + str(pOneInfo['regeneration']) + " hp."
        pOneCurrentHP += pOneInfo['regeneration']
        if pOneCurrentHP > pOneTotalHP:
            pOneCurrentHP = pOneTotalHP
    return modifier, pOneCurrentHP, pOneCurrentHP, pOneTotalHP, pTwoTotalHP