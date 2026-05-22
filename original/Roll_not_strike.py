import os
import json
import random
import time

from pathlib import Path
from threading import Timer
from feat_methods import *
from stoneskin_dr_regen import *

# 608

def Not_True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod, pOnemMod,
                    pTwomMod, pOneBullrush, pTwoBullrush, pOneFeatUsed, pTwoFeatUsed, pOneSpentFeat, pTwoSpentFeat,
                    pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade,
                    pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, critical, count,
                    featToken, bGameTimer, token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple,
                    pOneRelentless, pOneRelentlessDamage, pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage,
                    pOneStoneskin, pTwoStoneskin, pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile, pOneQuick,
                    pTwoQuick, pOneSunder, pOneSunderAmount, pTwoSunder, pTwoSunderAmount, pOneHeavy, pTwoHeavy,
                    pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot, pOneLockout, pTwoCheapShot, pTwoLockout,
                    iddqd, new_token):

    pOneToHit = pOneInfo['thit']
    pTwoAC = pTwoInfo['tac']
    pOneDR = pOneInfo['tdr']
    pOneRegen = pOneInfo['regeneration']
    pTwoDR = pTwoInfo['tdr']
    pTwoRegen = pTwoInfo['regeneration']
    pMod = pOnepMod
    cMod = pOnecMod
    dMod = pOnedMod
    mMod = pOnemMod
    featList = ["stoneskin", "inproved stoneskin", "greater stoneskin", "stoneform", "quick strike",
                "improved quick strike", "greater quick strike", "riposte", "none", "inner strength",
                "improved inner strength", "greater inner strength"]
    newDamage = 0
    critical = 0
    bonusHurt = 0
    bonusFocus = 0
    nerveDamage = 0
    innerBonus = 0
    innerDamage = 0
    vileOne = 0
    vileTwo = 0
    pOneHeal = 0
    pTwoHeal = 0
    # Susanna Added , for ask prompt !evation or !pass
    bEvasion = False
    bDeflect = False

    # Start cheap shot if used.
    if "cheap" in pOneFeatUsed[0]:
        pOneCheapShot, pOneLockout, modifier = featCheapShot(pOneInfo, pTwoInfo)
        msg.append(modifier)

    # count it down
    if pOneCheapShot != 0:
        pOneCheapShot -= 1
        # Reset Lockout if duration is over
        if pOneCheapShot == 0:
            pOneLockout = 0

    # determine the roll of the 1d20.
    if iddqd != 0:
        hit = iddqd
    else:
        hit = random.randint(1, 20)

    # if the raw result is equal to 20, count the critical counter up to 1.
    if hit == 20:
        critical = 1
        msg.append(pOneInfo['name'] + " has [color=red][b]critically hit.[/b][/color]")
    elif hit == 1:
        msg.append(pOneInfo['name'] + " has [color=red][b]critically missed.[/b][/color]")

    # If stoneskin was used, apply bonus pool.
    if "stone" in pOneFeatUsed[0]:
        pOneStoneskin, pOneStonebonus, modifier = featStoneskin(pOneInfo, pTwoInfo, pOneFeatUsed, token)
        for modifier_item in modifier:
            msg.append(modifier_item)

    #Determine if Quick Strike was used.
    if "quick" in pOneFeatUsed[0]:
        pOneQuick = featQuickCounter(pOneInfo, pTwoInfo, pOneFeatUsed)

    #Inner Focus
    if "inner" in pOneFeatUsed[0]:
        print("Inner Strength Roll")
        innerBonus, pOneInner, modifier = featInnerDuration(pOneInfo)
        if modifier != "":
            msg.append(modifier)

    if pOneInner != 0:
        innerBonus = pOneDR * 2
        pOneDR = 0
        pOneInner -= 1

    if pTwoInner != 0:
        pTwoDR = 0
        pTwoInner -= 1

    total = int(hit + pOneToHit - pMod + cMod + mMod + pOneInfo['potionhit'] + pOneStonebonus + innerBonus)
    totalHit = total
    # # testing data to see that modifiers are carrying over correctly. Comment out
    # # when project is finished.
    # msg.append("Roll: " + str(hit) + " Base: " + str(pOneToHit) + " PA: " +
    #             str(pMod) + " CE: " + str(cMod) + " DF: " + str(dMod) + " MC: " +
    #             str(mMod) + " Riposte: " + str(pOneBullrush) + " Hurt Me: " + str(bonusHurt) +)

    if pTwoSunder == 0:
        pTwoSunderAmount = 0
    if pTwoSunder != 0:
        pTwoSunder -= 1
    totalAC = pTwoAC + pTwodMod - pTwomMod + pTwoInfo['potionac'] - pTwoSunderAmount
    # # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
    # msg.append("P2 AC: " + str(pTwoAC) + " DF: " + str(pTwodMod) + " MC: " + str(pTwomMod))

    # determine if the total roll, after all modifiers have been included, is a successful hit or not. then
    # head to the appropriate method
    if (total < totalAC or hit == 1) and hit != 20:
        msg.append(pOneInfo['name'] + " rolled a [color=red]" + str(total) + "[/color] to hit an AC [color=green]" +
                   str(totalAC) + "[/color] and missed.(Base Roll: [color=blue]" + str(hit) + "[/color])")

        # Quick Strike
        pTwoMissDamage = 0
        if pTwoQuick != 0:
            if pTwoVile == 0:
                pTwoQuickDamage, modifier = featQuickStrike(pOneInfo, pTwoInfo, pTwoQuick, pTwoFeatUsed)
                pTwoQuick -= 1
                msg.append(modifier)
        if pOneVile != 0:
            modifier = []
            if pOneVile in range(1, 11):
                if pOneVile != 0:
                    vileOne, modifier = featOneVileDamage(pOneInfo, pTwoInfo, pOneVile, pTwoVile, vileOne,
                                                          pOneCurrentHP, pTwoCurrentHP, modifier)
                for modifier_item in modifier:
                    msg.append(modifier_item)

        # Unrelenting Damage
        if pOneRelentless != 0:
            pOneRelentless, pOneRelentlessDamage, modifier = featRelentlessDamage(pOneRelentless,
                                                                                  pOneRelentlessDamage,
                                                                                  pOneInfo, totalHit, totalAC, hit)
            msg.append(modifier)

        # Add together damage done from feats proc'd even during a miss, and apply stoneskin/DR if needed

        pTwoMissDamage = pTwoQuickDamage
        # if pOneStoneskin != 0 and pTwoMissDamage > 0:
        #     modifier, pOneStoneskin, pOneStonebonus,\
        #     pOneCurrentHP, pTwoCurrentHP = missBlurSKDRCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP,
        #                                                      pOneStoneskin, pTwoMissDamage, vileOne)
        # msg.append(modifier)
        if pOneStoneskin != 0 and pTwoMissDamage > 0:
            newTotal = pTwoMissDamage
            oldStoneskin = pOneStoneskin
            pOneStoneskin -= newTotal
            if pOneStoneskin <= 0:
                newStone = abs(pOneStoneskin)
                difference = newTotal - newStone
                pTwoQuickDamage -= difference
                msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                           str(difference) + "[/color] damage, and has broken.")
                pOneStoneskin = 0
                pOneStonebonus = 0
                pTwoQuicKDamage = 0
            else:
                msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                           str(pTwoMissDamage) + "[/color] damage, with [color=red] " + str(pOneStoneskin) +
                           "[/color] points remaining.")
                pTwoMissDamage = 0

        if pTwoStoneskin != 0 and pOneRelentlessDamage > 0:
            oldStoneskin = pTwoStoneskin
            pTwoStoneskin -= newTotal
            if pTwoStoneskin <= 0:
                newStone = abs(pTwoStoneskin)
                difference = newTotal - newStone
                pOnerelentlessDamage -= difference
                msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                           str(difference) + "[/color] damage, and has broken.")
                pOneStoneskin = 0
                pOneStonebonus = 0
                pOneRelentlessDamage = 0
            else:
                msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                           str(pTwoMissDamage) + "[/color] damage, with [color=red] " + str(pOneStoneskin) +
                           "[/color] points remaining.")

        if pOneDR != 0 and pTwoMissDamage > 0:
            msg.append(pOneInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                       str(pOneDR) + "[/color] hp of damage from opponent's roll.")
            pTwoMissDamage -= pOneDR

        if pTwoDR != 0 and vileOne > 0:
            msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                       str(pTwoDR) + "[/color] hp of damage from opponent's roll.")
            vileOne -= pTwoDR

        if pTwoDR != 0 and pOneRelentlessDamage > 0:
            msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                       str(pTwoDR) + "[/color] hp of damage from opponent's roll.")
            pOneRelentlessDamage -= pTwoDR

        # If damage falls below 0 after applying stoneskin/DR, set damage to 0
        if pTwoMissDamage < 0:
            pTwoMissamage = 0
        if vileOne < 0:
            vileOne = 0
        if pOneRelentlessDamage < 0:
            pOneRelentlessDamage = 0
        # subtract damage from current hp
        pOneCurrentHP -= pTwoMissDamage
        pTwoCurrentHP -= vileOne
        pTwoCurrentHP -= pOneRelentlessDamage

        # modifier, pOneCurrentHP, pOneCurrentHP,\
        # pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP,
        #                                       pTwoTotalHP, token)
        # msg.append(modifier)
        if pTwoExpose != 0:
            if pOneRegen != 0:
                defense, modifier = featExposeRegeneration(pOneInfo, pTwoInfo)
                msg.append(modifier)
                pOneRegen -= defense
                if pOneRegen < 0:
                    pOneRegen = 0
        # apply regeneration
        if token == 1 and pOneRegen != 0 and pOneCurrentHP < pOneTotalHP:
            msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneRegen) +
                       "[/color] hp.")
            pOneCurrentHP += pOneRegen
            if pOneCurrentHP > pOneTotalHP:
                pOneCurrentHP = pOneTotalHP
        elif token == 2 and pOneRegen != 0 and pOneCurrentHP < pOneTotalHP:
            msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneRegen) +
                       "[/color] hp.")
            pOneCurrentHP += pOneRegen
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

        if (pOneFeatUsed[0] != 'none' and pOneFeatUsed[0] in pOneSpentFeat) and  hit < 6:
            if pOneFeatUsed[0] not in featList:
                msg.append("[color=yellow]" + pOneFeatUsed[0] + "[/color] was lost due to severity of miss.")
        elif pOneFeatUsed[0] != 'none' and pOneFeatUsed[0] in pOneSpentFeat:
            pOneSpentFeat.remove(pOneFeatUsed[0])
        # reset everything
        pTwodMod = 0
        pTwomMod = 0
        if pOneBullrush == 0:
            token = new_token
        pTwoQuickDamage = 0
        count += 1
        featToken = 0
        iddqd = 0
        pOneFeatInfo = ["none", 0]
        bGameTimer = True
        pTwoFeatInfo = None

    # If hit was successful
    elif total >= totalAC or hit == 20:
        msg.append(pOneInfo['name'] + " rolled a [color=red]" + str(total) + "[/color] to hit an AC [color=green]" +
                   str(totalAC) + "[/color] and was successful. (Base Roll: [color=blue]" + str(hit) + "[/color])")

        # Determine if blur activates or not, if needed.
        totalBlur = pTwoInfo['armorblur'] + pTwoInfo['potionblur'] + pTwoInfo['blur']
        blur = random.randint(1, 100)
        if totalBlur != 0 and blur <= totalBlur:
            blur = random.randint(1, 100)
            msg.append(pTwoInfo['name'] + "'s blur [color=blue]" + str(totalBlur) + "% chance.[/color] "
                       "makes " + pOneInfo['name'] + " strike at a position their "
                       "opponent wasn't, causing them to miss. " + pTwoInfo['name'] + "'s turn. Type: "
                       "[color=pink]!usefeat <feat>[/color] if you wish to use a feat.")

            pTwoMissDamage = 0
            if pTwoQuick != 0:
                pTwoQuickDamage, modifier = featQuickStrike(pOneInfo, pTwoInfo, pTwoQuick, pTwoFeatUsed)
                pTwoQuick -= 1
                msg.append(modifier)

            if pOneVile != 0:
                modifier = []
                if pOneVile in range(1, 11):
                    if pOneVile != 0:
                        vileOne, modifier = featOneVileDamage(pOneInfo, pTwoInfo, pOneVile, pTwoVile, vileOne,
                                                              pOneCurrentHP, pTwoCurrentHP, modifier)
                    for modifier_item in modifier:
                        msg.append(modifier_item)

            if pOneRelentless != 0:
                pOneRelentless, pOneRelentlessDamage, modifier = featRelentlessDamage(pOneRelentless)
                msg.append(modifier)

            # Add together damage done from feats proc'd even during a miss, and apply stoneskin/DR if needed

            pTwoMissDamage = pTwoQuickDamage
            # if pOneStoneskin != 0 and pTwoMissDamage > 0:
            #     modifier, pOneStoneskin, pOneStonebonus,\
            #     pOneCurrentHP, pTwoCurrentHP = missBlurSKDRCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP,
            #                                                      pOneStoneskin, pTwoMissDamage, vileOne)
            # msg.append(modifier)
            if pOneStoneskin != 0 and pTwoMissDamage > 0:
                newTotal = pTwoMissDamage
                oldStoneskin = pOneStoneskin
                pOneStoneskin -= newTotal
                if pOneStoneskin <= 0:
                    newStone = abs(pOneStoneskin)
                    difference = newTotal - newStone
                    pTwoQuickDamage -= difference
                    msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                               str(difference) + "[/color] damage, and has broken.")
                    pOneStoneskin = 0
                    pOneStonebonus = 0
                    pTwoQuickDamage = 0
                else:
                    msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                               str(pTwoMissDamage) + "[/color] damage, with [color=red] " + str(pOneStoneskin) +
                               "[/color] points remaining.")
                    pTwoMissDamage = 0

            if pTwoStoneskin != 0 and pOneRelentlessDamage > 0:
                oldStoneskin = pTwoStoneskin
                pTwoStoneskin -= newTotal
                if pTwoStoneskin <= 0:
                    newStone = abs(pTwoStoneskin)
                    difference = newTotal - newStone
                    pOnerelentlessDamage -= difference
                    msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                               str(difference) + "[/color] damage, and has broken.")
                    pOneStoneskin = 0
                    pOneStonebonus = 0
                    pOneRelentlessDamage = 0
                else:
                    msg.append(pTwoInfo['name'] + "'s [color=yellow]stoneskin[/color] effect absorbed [color=red]" +
                               str(pTwoMissDamage) + "[/color] damage, with [color=red] " + str(pOneStoneskin) +
                               "[/color] points remaining.")

            # Expose
            if pTwoExpose != 0:
                if pOneRegen != 0:
                    defense, modifier = featExposeRegeneration(pOneInfo, pTwoInfo)
                    msg.append(modifier)
                    pOneRegen -= defense
                    if pOneRegen < 0:
                        pOneRegen = 0
                pTwoExpose -= 1

            if pOneDR != 0 and pTwoMissDamage > 0:
                msg.append(pOneInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                           str(pOneDR) + "[/color] hp of damage from opponent's roll.")
                pTwoMissDamage -= pOneDR

            if pTwoDR != 0 and vileOne > 0:
                msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                           str(pTwoDR) + "[/color] hp of damage from opponent's roll.")
                vileOne -= pTwoDR

            if pTwoDR != 0 and pOneRelentlessDamage > 0:
                msg.append(pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                           str(pTwoDR) + "[/color] hp of damage from opponent's roll.")
                pOneRelentlessDamage -= pTwoDR
            # If damage falls below 0 after applying stoneskin/DR, set damage to 0
            if pTwoMissDamage < 0:
                pTwoMissamage = 0
            if vileOne < 0:
                vileOne = 0
            if pOneRelentlessDamage:
                pOneRelentlessDamage = 0

            # subtract damage from current hp
            pOneCurrentHP -= pTwoMissDamage
            pTwoCurrentHP -= vileOne
            pTwoCurrentHP -= pOneRelentlessDamage

            # Expose
            if pOneExpose != 0:
                pOneExpose, defense, modifier = featExpose(pOneInfo, pTwoInfo, token)
                if pTwoDR != 0:
                    pTwoDR -= defense
                    if pTwoDR < 0:
                        pTwoDR = 0
                if pTwoInfo['regenertion'] != 0:
                    pTwoRegen -= defense
                    if pTwoRegen < 0:
                        pTwoRegen = 0
                pOneExpose -= 1

            # modifier, pOneCurrentHP, pOneCurrentHP,\
            # pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP,
            #                                       pTwoTotalHP, token)
            # msg.append(modifier)

            if pTwoExpose != 0:
                defense = featExpose(pOneInfo, pTwoInfo, expose)
                if pOneRegen != 0:
                    pOneRegen -= defense
                    if pOneRegen < 0:
                        pOneRegen = 0

            # apply regeneration
            if token == 1 and pOneRegen != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneRegen) +
                           "[/color] hp.")
                pOneCurrentHP += pOneRegen
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP
            elif token == 2 and pOneRegen != 0 and pOneCurrentHP < pOneTotalHP:
                msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneRegen) +
                           "[/color] hp.")
                pOneCurrentHP += pOneRegen
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # Print the scoreboard. if statements are used to ensure the scoreboard is uniform, and does not
            # alternate positions, depending on if player two goes first or not.
            if pOneBullrush == 1:
                name = pOneInfo['name']
            else:
                name = pTwoInfo['name']

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

            # reset everything
            pTwodMod = 0
            pTwomMod = 0
            if pOneBullrush == 0:
                token = new_token
            count += 1
            featToken = 0
            iddqd = 0
            pOneFeatInfo = ["none", 0]
            bGameTimer = True
            pTwoFeatInfo = None
        else:
            pTwodMod = 0
            pTwomMod = 0
            pOneBaseDamage = pOneInfo['base damage']
            pOneModifier = pOneInfo['tdamage']
            # find Player Two's total AC
            pOneMinimum, pOneMaximum = pOneBaseDamage.split('d')
            pOneMinimum = int(pOneMinimum)
            pOneMaximum = int(pOneMaximum)

            # Focus passive feat
            if "focus" in pOneInfo['feats taken']:
                pOneMinimum, pOneMaximum, modifier = featFocus(pOneInfo, pOneCurrentHP, pOneTotalHP, pOneMinimum, pOneMaximum)
                if msg != "":
                    msg.append(modifier)

            pMod = pOnepMod
            cMod = pOnecMod

            if "hand" in pOneFeatUsed[0]:
                pOneHeavy, modifier = featHeavyCounter(pOneInfo, pOneFeatUsed)
                msg.append(modifier)

            # If 'Heavy Hand' is used, ensure that damage does not fall below specified threshhold
            if  pOneHeavy != 0:
                pOneMaximum, pOneHeavy, modifier = featHeavyHand(pOneInfo, pOneMaximum, pOneHeavy)
                msg.append(modifier)

            msg.append("For Testing Purposes. pOneMinimum: " + str(pOneMinimum) + " pOneMaximum: " + str(pOneMaximum))
            damage = random.randint(int(pOneMinimum), int(pOneMaximum))
            base = damage

            if critical == 1:
                damage = damage * 2

            # if Player One used feat 'titan blow', apply bonus damage.
            if "titan" in pOneFeatUsed[0]:
                damage, modifier = featTitanBlow(pOneInfo, pTwoInfo, pOneFeatUsed, damage)
                msg.append(modifier)

            # Determine if Lifeleech was used
            if "life" in pOneFeatUsed[0]:
                pOneHeal, modifier, damage = featLifeLeech(pOneInfo, pTwoInfo, damage, pOneFeatUsed, token)
                msg.append(modifier)

            if pOneHeal != 0:
                pOneCurrentHP += pOneHeal
                if pOneCurrentHP > pOneTotalHP:
                    pOneCurrentHP = pOneTotalHP

            # Nerve Strike/Nerve Damage
            for feat in pOneInfo['feats taken']:
                if "nerve" in feat:
                    nerveDamage, modifier = featNerveStrike(pOneInfo, pTwoInfo, total, hit, totalAC)
                    if modifier != "":
                        msg.append(modifier)


                # If Player One has Hurt Me, Improved Hurt Me, and Greater Hurt Me, check hit points, and apply
                # bonuses.
                if "hurt" in feat:
                    bonusHurt, modifier = featHurtMe(pOneInfo, pTwoInfo, pOneCurrentHP, pOneTotalHP, pOneModifier,
                                                     bonusHurt)
                    if bonusHurt != 0:
                        msg.append(modifier)

            # If Player's Vile Touch is procc'd, do damage here
            if "touch" in pOneFeatUsed[0]:
                pOneVile = featVileTouch(pOneInfo, pTwoInfo, pOneFeatUsed, token)
            if pOneVile != 0:
                modifier = []
                if pOneVile in range(1, 11):
                    if pOneVile != 0:
                        vileOne, modifier = featOneVileDamage(pOneInfo, pTwoInfo, pOneVile, pTwoVile, vileOne,
                                                                       pOneCurrentHP, pTwoCurrentHP, modifier)
                if pOneVile != 0:
                    pOneVile -= 1
                for modifier_item in modifier:
                    msg.append(modifier_item)

            # Unrelenting Counter
            if "relentless" in pOneFeatUsed[0] or "unforgiving" in pOneFeatUsed[0]:
                pOneRelentless = featRelentlessCounter(pOneInfo, pOneFeatUsed)
            # Unrelenting Damage
            if pOneRelentless != 0:
                pOneRelentless, pOneRelentlessDamage, modifier = featRelentlessDamage(pOneRelentless,
                                                                                      pOneRelentlessDamage,
                                                                                      pOneInfo, totalHit, totalAC, hit)
                msg.append(modifier)


            # calculate damage
            if pOneInner !=0 and "greater inner strength" in pOneInfo["feats taken"]:
                innerDamage = innerBonus
            if pOneStonebonus != 0:
                msg.append(pOneInfo['name'] + " is gaining a [color=red]+" + str(pOneStonebonus) + "[/color] to damage,"
                           " due to stoneskin.")
            total = int(damage + pOneModifier + pMod - cMod - pOnedMod + pOneInfo['potiondamage'] + innerDamage)
            if pOneRelentless == 0 and pOneRelentlessDamage != 0:
                total += pOneRelentlessDamage
                pOneRelentlessDamage = 0
            if pOneStonebonus != 0:
                total += pOneStonebonus
            if nerveDamage != 0:
                total += nerveDamage
            if bonusHurt != 0:
                total += bonusHurt

            # Bullrush
            if "bullrush" in pOneFeatUsed[0]:
                pOneBullrush, total, modifier = featBullrush(pOneInfo, pTwoInfo, pOneFeatInfo, pOneBullrush, total)
                if modifier != "":
                    msg.append(modifier)

            # Crippling Blow
            if "crippling" in pOneFeatUsed[0]:
                msg.append(pOneInfo['name'] + " landed a [color=yellow]crippling blow[/color], affecting the result of "
                           + pTwoInfo['name'] + "'s next successful attack.")
                pOneCripple = 1

            if pTwoCripple != 0:
                total, modifier = featCripplingBlow(pOneInfo, pTwoInfo, total)
                pOneCripple = 0
                msg.append(modifier)

            # Staggering Blow
            if "staggering" in pTwoFeatUsed[0]:
                strength = pTwoFeatUsed[1][1]
                nonStrength = pTwoFeatUsed[1][0]
                total, modifier = featStaggeringBlow(pOneInfo, pTwoInfo, strength, nonStrength, total)
                msg.append(modifier)

            # Reckless Abandon
            if "abandon" in pOneFeatUsed[0]:
                pOneCurrentHP, total, modifier = featRecklessAbandon(pOneInfo, pTwoInfo, pOneCurrentHP,
                                                                     pTwoCurrentHP, total, pOneFeatUsed)
                msg.append(modifier)

            msg.append(pOneInfo['name'] + " did [color=red]" + str(total) + "[/color] points of damage." +
                       " (Base Roll: [color=blue]" + str(base) + "[/color])")

            # Expose timer
            if "expose" in pOneFeatUsed[0]:
                pOneExpose, modifier = featExposeCounter(pOneInfo, pTwoInfo)
                msg.append(modifier)

            if pOneExpose != 0:
                if pTwoDR != 0:
                    defense, modifier = featExpose(pOneInfo, pTwoInfo)
                    msg.append(modifier)
                    pTwoDR -= defense
                    if pTwoDR < 0:
                        pTwoDR = 0
                pOneExpose -= 1

            print(pOneExpose)
            print(pTwoExpose)
            if pTwoExpose != 0:
                if pOneRegen != 0:
                    defense, modifier = featExposeRegeneration(pOneInfo, pTwoInfo)
                    msg.append(modifier)
                    pOneRegen -= defense
                    if pOneRegen < 0:
                        pOneRegen = 0


            # Apply stoneskin if needed
            # if pTwoStoneskin != 0 and total > 0:
            #     modifier, total, pTwoStoneskin,\
            #     pTwoStonebonus, newDamage = stoneskinDRCheck(pOneInfo, pTwoInfo, pOneFeatDamage, pTwoFeatDamage)
            #     msg.append(modifier)
            if pTwoStoneskin != 0 and total > 0:
                newTotal = total
                pTwoStoneskin -= newTotal
                if pTwoStoneskin <= 0:
                    newStone = abs(pTwoStoneskin)
                    difference = newTotal - newStone
                    newTotal -= difference
                    total = newTotal
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
            if pTwoDR != 0 and total > 0:
                msg.append(
                    pTwoInfo['name'] + " has [color=yellow]thick skin[/color], and has absorbed [color=red]" +
                    str(pTwoDR) + "[/color] hp of damage from opponent's roll.")
                total -= pTwoDR
                newDamage = 1
            totalDamage = total
            if vileOne != 0:
                totalDamage += vileOne
            # Ensure that damage done does not display a negative number, should applying DR reduce it to below zero
            if totalDamage < 0:
                totalDamage = 0

            # testing data to see that modifiers are carrying over correctly. Delete this when project is finished.
            # msg.append("Roll: " + str(base) + " Modifier: " + str(pOneModifier) + " PA: " + str(
            #             pMod) + " CD: " + str(cMod))
            # display total damage done, and reset passive feat counters (power attack and combat defense)
            if newDamage == 1:
                msg.append("Reducing " + pOneInfo['name'] + "'s damage to [color=red]" + str(totalDamage) +
                           "[/color] total.")
            pOnepMod = 0
            pOnecMod = 0

            if "sunder" in pOneFeatUsed[0]:
                pTwoSunder, pTwoSunderAmount, modifier = featSunder(pOneInfo, pTwoInfo)
                msg.append(modifier)
            # check to see if player has evasion.
            for feat in pTwoInfo["feats taken"]:
                if "evasion" in pTwoInfo['feats taken'] and pTwoEvade == 1 and critical == 1:
                    bEvasion, modifier = featEvasion(pOneInfo, pTwoInfo, bEvasion)
                    msg.append(modifier)

            # check to see if player has deflect. DEFLECT IS DEPRECIATED, AND IS NO LONGER IN THE GAME! KEPT HERE IN
            # CASE FEAT IS RETURNED
            '''
            if "deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
                bDeflect = True
                msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] "
                           "to use, or type [color=pink]!pass[/color]")
            elif "improved deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
                bDeflect = True
                msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] "
                           " to use, or type [color=pink]!pass[/color]")
            elif "greater deflect" in pTwoInfo['feats taken'] and pTwoDeflect == 1:
                bDeflect = True
                msg.append(pTwoInfo['name'] + " has deflect available for use. Type [color=pink]!deflect[/color] "
                           "to use, or type [color=pink]!pass[/color]")
            '''
            if bEvasion is False:
                if bDeflect is False:
                    pTwoCurrentHP -= totalDamage

                    # Check to see if Player has the feat 'death's door', and if it has been triggered already.
                    for feat in pTwoInfo['feats taken']:
                        if 'door' in feat:
                            pTwoCurrentHP, pTwoDeathsDoor, modifier = featDeathsDoor(pOneInfo, pTwoInfo, pTwoCurrentHP,
                                                                                     pTwoDeathsDoor)
                            if modifier != "":
                                msg.append(modifier)

                    # modifier, pOneCurrentHP, pOneCurrentHP,\
                    # pOneTotalHP, pTwoTotalHP = regenCheck(pOneInfo, pTwoInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP,
                    #                                       pTwoTotalHP, token)
                    # msg.append(modifier)

                    # apply regeneration
                    if token == 1 and pOneRegen != 0 and pOneCurrentHP < pOneTotalHP:
                        msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneRegen) +
                                   "[/color] hp.")
                        pOneCurrentHP += pOneRegen
                        if pOneCurrentHP > pOneTotalHP:
                            pOneCurrentHP = pOneTotalHP
                    elif token == 2 and pOneRegen != 0 and pOneCurrentHP < pOneTotalHP:
                        msg.append(pOneInfo['name'] + " has regenerated [color=red]" + str(pOneRegen) +
                                   "[/color] hp.")
                        pOneCurrentHP += pOneRegen
                        if pOneCurrentHP > pOneTotalHP:
                            pOneCurrentHP = pOneTotalHP

                    # Print the scoreboard. if statements are used to ensure the scoreboard is uniform, and does not
                    # alternate positions, depending on if player two goes first or not.
                    if pOneBullrush == 1:
                        name = pOneInfo['name']
                    else:
                        name = pTwoInfo['name']
                    if token == 2:
                        msg.append(pOneInfo['name'] + ": [color=red]" + str(pOneCurrentHP) + "[/color]/" +
                                   str(pOneTotalHP) + "  ||  " + pTwoInfo['name'] + ": [color=red]" +
                                   str(pTwoCurrentHP) + "[/color]/" + str(pTwoTotalHP) + " \n" +
                                   name + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                   " if you wish to use a feat.")
                    else:
                        msg.append(pTwoInfo['name'] + ": [color=red]" + str(pTwoCurrentHP) + "[/color]/" +
                                   str(pTwoTotalHP) + "  ||  " + pOneInfo['name'] + ": [color=red]" +
                                   str(pOneCurrentHP) + "[/color]/" + str(pOneTotalHP) + " \n" +
                                   name + "'s turn. Type: [color=pink]!usefeat <feat>[/color]"
                                                      " if you wish to use a feat.")

                    # reset everything
                    pOnepMod = 0
                    if pOneBullrush == 0:
                        token = new_token
                    count += 1
                    print("count: " + str(count))
                    featToken = 0
                    iddqd = 0
                    bGameTimer = True
                    pTwoFeatInfo = None

    return msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod,\
        pOnemMod, pTwomMod, pOneBullrush, pTwoBullrush, pOneFeatUsed, pTwoFeatUsed, pOneSpentFeat, pTwoSpentFeat,\
        pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade,\
        pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, critical, count, featToken, bGameTimer,\
        token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,\
        pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneStonebonus,\
        pTwoStonebonus, pOneVile, pTwoVile, pOneQuick, pTwoQuick, pOneSunder, pOneSunderAmount, pTwoSunder,\
        pTwoSunderAmount, pOneHeavy, pTwoHeavy, pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot,\
        pOneLockout, pTwoCheapShot, pTwoLockout, iddqd

