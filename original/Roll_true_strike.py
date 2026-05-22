import os
import json
import random
import time
import feat_methods
from pathlib import Path
from threading import Timer

# 225

def True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod,
                pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo,
                pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect,
                pOneQuickDamage, pTwoQuickDamage, critical, count, featToken, bGameTimer, token,
                totalDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pTwoHeal, pOneStoneskin, pTwoStoneskin,
                pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile,pTwoSunder, pTwoSunderAmount, pOneSunder,
                pOneSunderAmount, iddqd, new_token):
    msg.append(pOneInfo['name'] + " used the feat [color=yellow]'True Strike.'[/color] And forgoes the need to"
               " determine if hit was success.\n")

    # Susanna Added , for ask prompt !evasion or !pass
    bEvasion = False
    bDeflect = False

    pOneBaseDamage = pOneInfo['base damage']
    pOneModifier = pOneInfo['tdamage']
    pOneMinimum, pOneMaximum = 3, 24
    pMod = pOnepMod
    cMod = pOnecMod
    dMod = pOnedMod
    damage = random.randint(int(pOneMinimum), int(pOneMaximum))
    base = damage
    bonusHurt = 0
    nerveDamage = 0
    # if critical counter is a value of 1, double the damage done, then reset counter to 0.
    if critical == 1:
        damage = damage * 2
        critical = 0
    # Titan Blow
    if "titan" in pOneFeatUsed:
        damage, modifier = featTitanBlow(pOneInfo, pTwoInfo, pOneFeatUsed, damage)
        msg.append(modifier)

    # Hurt Me
    if 'hurt' in pOneInfo['feats taken']:
        bonusHurt, modifier = (pOneInfo, pTwoInfo, pOneCurrentHP, pOneTotalHP, pOneModifier, pOneFeatUsed)
        msg.append(modifier)

    # ensure that no matter what, raw damage can not fall below 1, then assign total damage to variable, and in turn
    # assign it to variable to be accessed for scoreboard.
    if damage < 1:
        damage = 1
    total = int(damage + pOneModifier + pMod - cMod - dMod - pTwoInfo['tdr'] + pOneInfo['potiondamage'] +
                pOneStonebonus)
    if bonusHurt != 0:
        total += bonusHurt

    # Crippling Blow
    if "crippling" in pTwoFeatUsed[0]:
        total, modifier = featCripplingBlow(pOneInfo, pTwoInfo, pTwoFeatUsed, total)
        msg.append(modifier)

    # Staggering Blow
    if "staggering" in pTwoFeatUsed[0]:
        strength = pTwoFeatUsed[1][1]
        nonStrength = pTwoFeatUsed[1][0]
        total, modifier = featStaggeringBlow(pOneInfo, pTwoInfo, strength, nonStrength, total)
        msg.append(modifier)

    if pTwoInfo['tdr'] != 0:
        msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed " +
                   str(pTwoInfo['tdr']) + " hp of damage from opponent's roll.")

    # Reckless Abandon
    if "abandon" in pOneFeatUsed[0]:
        pOneCurrentHP, pTwoCurrentHP, total, modifier = featRecklessAbandon(pOneInfo, pTwoInfo, pOneCurrentHP, total,
                                                             pOneFeatUsed)
        msg.append(modifier)

    # Nerve Strike/Nerve Damage
    for feat in pOneInfo['feats taken']:
        if "nerve" in feat:
            nerveDamage, modifier = featNerveStrike(pOneInfo, pTwoInfo, total, hit, totalAC)
            msg.append(modifier)

    # if Player Two used 'quick strike', 'improved quick strike', or 'greater quick strike', apply the return
    # damage here
    pTwoBaseDamage = pTwoInfo['base damage']
    pTwoModifier = pTwoInfo['tdamage']
    pTwoMinimum, pTwoMaximum = pTwoBaseDamage.split('d')
    pMod = pTwopMod
    cMod = pTwocMod

    if total < 1:
        total = 1

    # Apply stoneskin if needed
    # if pTwoStoneskin != 0 and total > 0:
    #     modifier, total, pTwoStoneskin,\
    #     pTwoStonebonus, newDamage = stoneskinDRCheck(pOneInfo, pTwoInfo, pOneFeatDamage, pTwoFeatDamage)
    #     msg.append(modifier)
        # Expose
    if "expose" in pOneFeatUsed[0] or "exploit" in pOneFeatUsed[0] or pOneExpose != 0:
        pOneExpose, defense, modifier = featExpose(pOneInfo, pTwoInfo)
        if "expose" in pOneFeatUsed[0] or "exploit" in pOneFeatUsed[0]:
            msg.append(modifier)
        if pTwoInfo['tdr'] != 0:
            pTwoInfo['tdr'] -= defense
            if pTwoInfo['tdr'] < 0:
                pTwoInfo['tdr'] = 0
        if pTwoInfo['regenertion'] != 0:
            pTwoInfo['regeneration'] -= defense
            if pTwoInfo['regeneration'] < 0:
                pTwoInfo['regeneration'] = 0
        pOneExpose -= 1
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
            msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                       str(difference) + "[/color] damage, and has broken")
            newDamage = 1
            pTwoStoneskin = 0
            pTwoStonebonus = 0
            vileOne = 0
        else:
            msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                       str(total) + "[/color] damage, with [color=red] " + str(pTwoStoneskin) +
                       "[/color] points remaining.")
            newDamage = 1
            total = 0
            vileOne = 0
    if pTwoInfo['tdr'] != 0 and total > 0:
        msg.append(
            pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
            str(pTwoInfo['tdr']) + "[/color] hp of damage from opponent's roll.")
        total -= pTwoInfo['tdr']
        newDamage = 1
    print("before total vileOne: " + str(vileOne))
    totalDamage = total

    if totalDamage < 0:
        totalDamage = 0
    # # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
    # msg.append("Roll: " + str(base) + " Modifier: " + str(pOneModifier) + " PA: " + str(pMod) + " CE: " + str(cMod))
    # # display total damage done, and reset passive feat counters (power attack and combat defense)
    msg.append(pOneInfo['name'] + " did [color=red]" + str(totalDamage) + "[/color]"
               " points of damage." + "(Base Roll: [color=blue]" + str(base) + "[/color])\n")

    # Evasion
    if "evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1:
        bEvasion, modifier = featEvasion(pOneInfo, pTwoInfo, bEvasion)
        msg.append(modifier)

    # check to see if player has deflect. DEFLECT IS DEPRECIATED, AND IS NO LONGER IN THE GAME! KEPT HERE IN
    # CASE FEAT IS RETURNED
    '''
    if "deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
        bDeflect = True
        msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                   "use, or type [color=pink]!pass[/color]")
    elif "improved deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
        bDeflect = True
        msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                   "use, or type [color=pink]!pass[/color]")
    elif "greater evasion" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
        bDeflect = True
        msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] to "
                   "use, or type [color=pink]!pass[/color]")
    '''
    if bEvasion is False:
        if bDeflect is False:
            pTwoCurrentHP -= totalDamage

            # Deaths Door
            if 'door' in pTwoInfo['feats taken']:
                pTwoCurrentHP, pTwoDeathsDoor, modifier = featDeathsDoor(pOneInfo, pTwoInfo, pTwoCurrentHP,
                                                                         pTwoDeathsDoor)
                msg.append(modifier)

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
            elif token == 2 and pOneInfo['regeneration'] != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneInfo['regeneration']) +
                           "[/color] hp.")
                pOneCurrentHP += pOneInfo['regeneration']
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # Print the scoreboard. if statements are used to ensure the scoreboard is uniform, and does not
            # alternate positions, depending on if player two goes first or not.
            if token == 2:
                msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                           str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                           str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                           pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                              " if you wish to use a feat.")
            else:
                msg.append(pTwoInfo['name'] + ": [color=red]" + str(pTwoCurrentHP) + "[/color]/" +
                           str(pTwoTotalHP) + "  ||  " + pOneInfo['name'] + ": [color=red]" +
                           str(pOneCurrentHP) + "[/color]/" + str(pOneTotalHP) + " \n" +
                           pTwoInfo['name'] + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                              " if you wish to use a feat.")

            if pTwoFeatUsed[0] == "riposte":
                pTwoRiposte = 5

            pOnepMod = 0
            pOnecMod = 0
            pOnedMod = 0
            token = new_token
            count += 1
            iddqd = 0
            featToken = 0
            bGameTimer = True
            pTwoFeatInfo = None

        return msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod,\
            pOnemMod, pTwomMod, pOneRiposte, pTwoRiposte, pOneFeatUsed, pTwoFeatUsed, pOneFeatInfo, pTwoFeatInfo,\
            pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect,\
            pOneQuickDamage, pTwoQuickDamage, critical, count, featToken, bGameTimer, token, totalDamage,\
            pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pTwoHeal, pOneStonskin, pTwoStoneskin, pOneStonebonus,\
            pTwoStonebonus, pTwoVile, pOneVile, pTwoSunder, pTwoSunderAmount, pOneSunder, pOneSunderAmount, iddqd
