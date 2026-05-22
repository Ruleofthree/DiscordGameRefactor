import os
import json
import random
import time
from pathlib import Path
from threading import Timer

from Roll_not_strike import *
from Roll_true_strike import *
from playerone_zero_current_hp import *
from playertwo_zero_current_hp import *


#212

def evasionTimer(self):
    pass


def message_roll(character, message, channel, unspoiledArena, charFolder, opponent, playerOne, playerTwo, winner,
                 pOneInfo, pTwoInfo, featToken, game, count, token, critical, bonusHurt, totalDamage, pOneTotalHP,
                 pTwoTotalHP, pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade,
                 pOneDeflect, pOneSunder, pOneSunderAmount, pOneBullrush, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,
                 pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount,
                 pTwoBullrush, pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP,
                 nextLevel, levelUp, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless,
                 pOneRelentlessDamage, pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin,
                 pTwoStoneskin, pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile, pOneQuick, pTwoQuick, pOneHeavy,
                 pTwoHeavy, pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot, pOneLockout, pTwoCheapShot,
                 pTwoLockout, iddqd):
    msg = []
    update = False
    if channel == unspoiledArena:
        # ensures the command can only be used when combat is taking place. To prevent trolls from spamming commands
        if game == 1:

            bGameTimer = False
            bTimer = True

            # Susanna Added , for ask prompt !evasion or !pass
            bEvasion = False
            bDeflect = False
            # assign both player's feat selections to variables
            pOneFeatUsed = pOneFeatInfo
            pTwoFeatUsed = pTwoFeatInfo

            # If a feat wasn't used by a player, assign it default values.
            if pOneFeatUsed is None:
                pOneFeatUsed = ["none", 0]
            if pTwoFeatUsed is None:
                pTwoFeatUsed = ["none", 0]
            nerveDamage = 0
            base = 0

            # ensures the command can only be used by player one, when it is their turn. To prevent trolls from
            # spamming commands.
            if character.lower() == playerOne and token == 1:
                # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go
                # straight to damage.
                if pOneFeatUsed[0] == "true strike":
                    msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod,\
                        pTwodMod, pOnemMod, pTwomMod, pOneBullrush, pTwoBullrush, pOneFeatUsed, pTwoFeatUsed,\
                        pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade,\
                        pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, critical, count,\
                        featToken, bGameTimer, token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor,\
                        pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pTwoHeal, pTwoCripple,\
                        pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneStonebonus,\
                        pTwoStonebonus, pOneVile, pTwoVile, pOneSunder, pOneSunderAmount, pTwoSunder, pTwoSunderAmount,\
                        pOneHeavy, pTwoHeavy, pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot, pOneLockout,\
                        pTwoCheapShot, pTwoLockout, iddqd =\
                        True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod, pTwodMod,
                                    pOnemMod, pTwomMod, pOneBullrush, pTwobullrush, pOneFeatUsed, pTwoFeatUsed,
                                    pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP,
                                    pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage,
                                    critical, count, featToken, bGameTimer, token, totalDamage, pOneDeathsDoor,
                                    pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,
                                    pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin,
                                    pTwoStoneskin, pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile,
                                    pOneSunder, pOneSunderAmount, pTwoSunder, pTwoSunderAmount, pOneheavy, pTwoheavy,
                                    pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot, pOneLockout,
                                    pTwoCheapShot, pTwoLockout, iddqd, 2)

                # Otherwise, continue on with the bulk of this method.
                else:
                    msg, bEvasion, bDeflect, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod,\
                        pTwodMod, pOnemMod, pTwomMod, pOneBullrush, pTwoBullrush, pOneFeatUsed, pTwoFeatUsed,\
                        pOneSpentFeat, pTwoSpentFeat, pOneFeatInfo, pTwoFeatInfo, pOneCurrentHP, pTwoCurrentHP,\
                        pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade, pOneDeflect, pTwoDeflect, pOneQuickDamage,\
                        pTwoQuickDamage, critical, count, featToken, bGameTimer, token, totalDamage,\
                        pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage,\
                        pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin,\
                        pOneStonebonus, pTwoStonebonus, pOneVile, pTwoVile, pOneQuick, pTwoQuick,\
                        pOneSunder, pOneSunderAmount, pTwoSunder, pTwoSunderAmount, pOneHeavy, pTwoHeavy,\
                        pOneInner, pTwoInner, pOneExpose, pTwoExpose, pOneCheapShot, pOneLockout, pTwoCheapShot,\
                        pTwoLockout, iddqd =\
                        Not_True_Strike(msg, pOneInfo, pTwoInfo, pOnepMod, pTwopMod, pOnecMod, pTwocMod, pOnedMod,
                                        pTwodMod, pOnemMod, pTwomMod, pOneBullrush, pTwoBullrush, pOneFeatUsed,
                                        pTwoFeatUsed, pOneSpentFeat, pTwoSpentFeat, pOneFeatInfo, pTwoFeatInfo,
                                        pOneCurrentHP, pTwoCurrentHP, pOneTotalHP, pTwoTotalHP, pOneEvade, pTwoEvade,
                                        pOneDeflect, pTwoDeflect, pOneQuickDamage, pTwoQuickDamage, critical,
                                        count, featToken, bGameTimer, token, totalDamage, pOneDeathsDoor, pTwoDeathsDoor,
                                        pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pTwoHeal,
                                        pTwoCripple, pTwoRelentless, pTwoRelentlessDamage,
                                        pOneStoneskin, pTwoStoneskin, pOneStonebonus, pTwoStonebonus, pOneVile,
                                        pTwoVile, pOneQuick, pTwoQuick, pOneSunder, pOneSunderAmount, pTwoSunder,
                                        pTwoSunderAmount, pOneHeavy, pTwoHeavy, pOneInner, pTwoInner, pOneExpose,
                                        pTwoExpose, pOneCheapShot, pOneLockout, pTwoCheapShot, pTwoLockout, iddqd,  2)
                # If Player Two is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
                # reset game and token counters back to 0.
                if pTwoCurrentHP <= 0:
                    pTwoSpentFeat = []
                    pOneSpentFeat = []
                    game = 0
                    token = 0
                    pOneStoneskin = 0
                    pTwoStoneskin = 0
                    pOneStonebonus = 0
                    pTwoStonebonus = 0
                    pOneDeathsDoor = 0
                    ptwoDeathsDoor = 0
                    pOneVile = 0
                    pTwoVile = 0
                    pOneQuick = 0
                    pTwoQuick = 0
                    pOneCripple = 0
                    pTwoCripple = 0
                    rounds = int(count / 2)
                    bGameTimer = False
                    count = 0
                    msg, pOneInfo, pTwoInfo, pOneDeathsDoor, pTwoDeathsDoor =\
                        playertwo_currentHP_less_zero(msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP,
                                                      pTwoCurrentHP, pOneLevel, pTwoLevel, charFolder, rounds,
                                                      pOneDeathsDoor, pTwoDeathsDoor)

            # ensures the command can only be used by player two, when it is their turn. To prevent trolls from
            # spamming commands.
            elif character.lower() == playerTwo and token == 2:
                # If the feat used was 'true strike' forgo rolling to see if player hit opponent, and go
                # straight to damage.
                if pTwoFeatUsed[0] == "true strike":
                    msg, bEvasion, bDeflect, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,\
                        pOnedMod, pTwomMod, pOnemMod, pTwoBullrush, pOneBullrush, pTwoFeatUsed, pOneFeatUsed,\
                        pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP, pTwoTotalHP, pOneTotalHP,\
                        pTwoEvade, pOneEvade, pTwoDeflect, pOneDeflect, pTwoQuickDamage, pOneQuickDamage,\
                        critical, count, featToken, bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor,\
                        pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneHeal, pOneCripple,\
                        pOneRelentless, pOneRelentlessDamage, pTwoStoneskin, pOneStoneskin, pTwoStonebonus,\
                        pOneStonebonus, pTwoVile, pOneVile, pTwoSunder, pTwoSunderAmount, pOneSunder, pOneSunderAmount,\
                        pTwoHeavy, pOneHeavy, pTwoInner, pOneInner, pTwoExpose, pOneExpose,\
                        pTwoCheapShot, pTwoLockout, pOneCheapShot, pOneLockout, iddqd =\
                        True_Strike(msg, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,
                                        pOnedMod, pTwomMod, pOnemMod, pTwoBullrush, pOneBullrush, pTwoFeatUsed,
                                        pOneFeatUsed, pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP,
                                        pTwoTotalHP, pOneTotalHP, pTwoEvade, pOneEvade, pTwoDeflect, pOneDeflect,
                                        pTwoQuickDamage, pOneQuickDamage, critical, count, featToken,
                                        bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor, pTwoHeal,
                                        pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneHeal, pOneCripple,
                                        pOneRelentless, pOneRelentlessDamage, pTwoStoneskin, pOneStoneskin,
                                        pTwoStonebonus, pOneStonebonus, pTwoVile, pOneVile,
                                        pTwoSunder, pTwoSunderAmount, pOneSunder, pOneSunderAmount, pTwoHeavy,
                                        pOneHeavy, pTwoInner, pOneInner, pTwoExpose, pOneExpose, pTwoCheapShot,
                                        pTwoLockout, pOneCheapShot, pOneLockout, iddqd, 1)

                # Otherwise, continue on with the bulk of this method.
                else:
                    msg, bEvasion, bDeflect, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,\
                        pOnedMod, pTwomMod, pOnemMod, pTwoBullrush, pOneBullrush, pTwoFeatUsed, pOneFeatUsed,\
                        pTwoSpentFeat, pOneSpentFeat, pTwoFeatInfo, pOneFeatInfo, pTwoCurrentHP, pOneCurrentHP,\
                        pTwoTotalHP, pOneTotalHP, pTwoEvade, pOneEvade, pTwoDeflect, pOneDeflect, pTwoQuickDamage,\
                        pOneQuickDamage, critical, count, featToken, bGameTimer, token, totalDamage,\
                        pTwoDeathsDoor, pOneDeathsDoor, pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage,\
                        pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pTwoStoneskin, pOneStoneskin,\
                        pTwoStonebonus, pOneStonebonus, pTwoVile, pOneVile, pTwoQuick, pOneQuick, pTwoSunder,\
                        pTwoSunderAmount, pOneSunder, pOneSunderAmount, pTwoHeavy, pOneHeavy,\
                        pTwoInner, pOneInner, pTwoExpose, pOneExpose, pTwoCheapShot, pTwoLockout, pOneCheapShot,\
                        pOneLockout, iddqd =\
                        Not_True_Strike(msg, pTwoInfo, pOneInfo, pTwopMod, pOnepMod, pTwocMod, pOnecMod, pTwodMod,
                                        pOnedMod, pTwomMod, pOnemMod, pTwoBullrush, pOneBullrush, pTwoFeatUsed,
                                        pOneFeatUsed, pTwoSpentFeat, pOneSpentFeat, pTwoFeatInfo, pOneFeatInfo,
                                        pTwoCurrentHP, pOneCurrentHP, pTwoTotalHP, pOneTotalHP, pTwoEvade, pOneEvade,
                                        pTwoDeflect, pOneDeflect, pTwoQuickDamage, pOneQuickDamage, critical,
                                        count, featToken, bGameTimer, token, totalDamage, pTwoDeathsDoor, pOneDeathsDoor,
                                        pTwoHeal, pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneHeal,
                                        pOneCripple, pOneRelentless, pOneRelentlessDamage,
                                        pTwoStoneskin, pOneStoneskin, pTwoStonebonus, pOneStonebonus, pTwoVile,
                                        pOneVile, pTwoQuick, pOneQuick, pTwoSunder, pTwoSunderAmount, pOneSunder,
                                        pOneSunderAmount, pTwoHeavy, pOneHeavy, pTwoInner, pOneInner, pTwoExpose,
                                        pOneExpose, pTwoCheapShot, pTwoLockout, pOneCheapShot, pOneLockout, iddqd, 1)

                # If Player One is dead, state such, and how many rounds it took to win. Calculate and distribute xp.
                # reset game and token counters back to 0.
                if pOneCurrentHP <= 0:
                    pTwoSpentFeat = []
                    pOneSpentFeat = []
                    pOneStoneskin = 0
                    pTwoStoneskin = 0
                    pOneStonebonus = 0
                    pTwoStonebonus = 0
                    pOneDeathsDoor = 0
                    ptwoDeathsDoor = 0
                    pOneVile = 0
                    pTwoVile = 0
                    pOneQuick = 0
                    pTwoQuick = 0
                    pOneCripple = 0
                    pTwoCripple = 0
                    game = 0
                    token = 0
                    rounds = int(count / 2)
                    bGameTimer = False
                    count = 0
                    msg, pTwoInfo, pOneInfo, pOneDeathsDoor, pTwoDeathsDoor =\
                        playerone_currentHP_less_zero(msg, pOneInfo, pTwoInfo, playerOne, playerTwo, pOneCurrentHP,
                                                      pTwoCurrentHP, pOneLevel, pTwoLevel, charFolder, rounds,
                                                      pOneDeathsDoor, pTwoDeathsDoor)
            update = True
        else:
            msg.append("This command does nothing right now. No combat is taking place.")
    else:
        msg.append("This command is only available in "
                   "[session=Unspoiled Desire Arena]adh-8768ecd732af44bc3be0[/session].")

    print("pOneLockout in Roll: " + str(pOneLockout))
    print("pTwoLockout in Roll: " + str(pTwoLockout))
    return msg, bEvasion, bDeflect, bGameTimer, opponent, playerOne, playerTwo, winner, pOneInfo, pTwoInfo,\
        featToken, game, count, token, critical, bonusHurt, totalDamage, pOneTotalHP, pTwoTotalHP, \
        pOneCurrentHP, pTwoCurrentHP, pOnepMod, pOnecMod, pOnedMod, pOnemMod, pOneEvade, pOneDeflect,\
        pOneSunder, pOneSunderAmount, pOneBullrush, pOneQuickDamage, pOneFeatInfo, pOneSpentFeat,\
        pTwopMod, pTwocMod, pTwodMod, pTwomMod, pTwoEvade, pTwoDeflect, pTwoSunder, pTwoSunderAmount, pTwoBullrush,\
        pTwoQuickDamage, pTwoFeatInfo, pTwoSpentFeat, pOneLevel, pTwoLevel, xp, currentPlayerXP, nextLevel,\
        levelUp, pOneDeathsDoor, pTwoDeathsDoor, pOneHeal, pOneCripple, pOneRelentless, pOneRelentlessDamage, pTwoHeal,\
        pTwoCripple, pTwoRelentless, pTwoRelentlessDamage, pOneStoneskin, pTwoStoneskin, pOneStonebonus, pTwoStonebonus,\
        pOneVile, pTwoVile, pOneQuick, pTwoQuick, pOneHeavy, pTwoHeavy, pOneInner, pTwoInner, pOneExpose,\
        pTwoExpose, pOneCheapShot, pOneLockout, pTwoCheapShot, pTwoLockout, iddqd, update
