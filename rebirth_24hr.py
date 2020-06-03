import time
# Helper classes
from classes.features   import (AdvancedTraining, Adventure, Augmentation, FightBoss, Inventory, Misc,
                                BloodMagic, GoldDiggers, NGU, Wandoos, TimeMachine, MoneyPit, Rebirth,
                                Questing, Yggdrasil, Hacks)
from classes.helper     import Helper
# Challenge needed
from classes.challenge  import Challenge
from classes.navigation import Navigation
import coordinates  as coords
import usersettings as userset
from classes.inputs     import Inputs
from classes.challenges import ngu, basic, timemachine, level, blind
from collections import namedtuple

debug = False
farmCurrentZoneOnly = False

# Set these to your own loadouts
ngu_loadout = 1
gold_loadout = 2
respwanDrop_loadout = 3

blood_magic_highest_affordable_level = 7  # 0 basedb

ngu_energy_targets = (list(range(1, 10)) + [5] * 9)
ngu_magic_targets = (list(range(1, 8)) + [5] + [7] * 7)
hacks_targets = (list(range(1, 8)) + [2] * 7)

Helper.init()
Helper.requirements()

curState = ""

zone_after_rebirth = 23  # Pretty
zone_after_training = 23  # Pretty
deadline_before_adv_training = time.strptime("00:13:00", "%H:%M:%S")
deadline_train_power_toughness = time.strptime("01:15:00", "%H:%M:%S")
deadline_augmentation = time.strptime("01:30:00", "%H:%M:%S")  # deadline_train_power_toughness.tm + datetime.timedelta(minutes=15)
deadline_adv_wandoos = time.strptime("01:35:00", "%H:%M:%S")  # deadline_augmentation + datetime.timedelta(minutes=15)
deadline_wandoos = time.strptime("01:55:00", "%H:%M:%S")  # deadline_adv_wandoos + datetime.timedelta(minutes=15)
deadline_gold = time.strptime("02:05:00", "%H:%M:%S")  # for wear gold drop equip for gold drop from titan


def activate_challenge(challenge_id: int) -> None:
    # start the challenge
    Navigation.challenges()
    x = coords.CHALLENGE.x
    y = coords.CHALLENGE.y + challenge_id * coords.CHALLENGEOFFSET
    Inputs.click(x, y)
    time.sleep(userset.LONG_SLEEP)
    Navigation.confirm()


if False:
    # using default speed runs
    challenge_id = 7  # remember to amend the call function too
    challengeTimes = 10

    for x in range(challengeTimes):
        print(f"{x}: challenge: {challenge_id}")
        # running code
        Challenge.start_challenge(challenge_id)  # no time machine challenge

# 20200531 first 3 min rebirth boss 52... 2nd rebirth at 70...
# 20200601 3 min 55,73...
if True:
    # customize speed run length
    challenge_id = 11  # remember to amend the call function too
    challengeClass = timemachine
    challengeTimes = 10

    configTuple = namedtuple('ChallengeConfig', 'times minutes os_level')
    config = [
        configTuple(4, 3, 0),
        configTuple(1, 4, 0),
        configTuple(1, 5, 0),
        configTuple(1, 7, 0),
        configTuple(1, 10, 0),
        configTuple(1, 12, 0),
        configTuple(1, 15, 0),
        configTuple(2, 30, 0),
        configTuple(2, 30, 1),
        configTuple(4, 60, 1),
        configTuple(4, 120, 1),
    ]
    for x in range(challengeTimes):
        print(f"{x+1} out of {challengeTimes}: challenge: {challenge_id}")
        activate_challenge(challenge_id)
        for t in config:
            for y in range(t.times):
                print(f"{y+1} out of {t.times}, Minutes: {t.minutes}, Wandoos: {t.os_level}")
                Wandoos.set_wandoos(t.os_level)
                challengeClass.speedrun(t.minutes)
                #challengeClass.run(t.minutes)
                try:
                    current_boss = int(FightBoss.get_current_boss())
                except ValueError:
                    current_boss = 1
                    print("couldn't get current boss")
                print(f"Current Boss: {current_boss}")
                if not Rebirth.check_challenge():
                    break
            if not Rebirth.check_challenge():
                break


#Adventure.snipe(zone=4, duration=60, manual=True, fast=True)  # snipe for macggufin
#exit(1)
rt = None

if farmCurrentZoneOnly:
    print("Farm Adventure zone only")
while True:
    if farmCurrentZoneOnly:
        # only farm in current zone
        Adventure.snipe(zone=0, duration=30)
        Navigation.menu('inventory')
        continue
    try:
        rt = Rebirth.get_rebirth_time()
    except:
        print("Error in parsing the rebirth time, past rt " + str(rt.days) + " " + str(rt.timestamp))

    try:
        if rt.days == 0 and rt.timestamp < deadline_before_adv_training:
            # before advance training
            # Focus on time machine
            stateName = "Before adv training"
            if curState != stateName:
                print(stateName)
                curState = stateName
                if debug:
                    e_idle = Misc.get_idle_cap(1)
                    m_idle = Misc.get_idle_cap(2)
                    print(f"E: {e_idle} \t M: {m_idle}")
                Misc.reclaim_all()
                if debug:
                    e_idle = Misc.get_idle_cap(1)
                    m_idle = Misc.get_idle_cap(2)
                    print(f"E: {e_idle} \t M: {m_idle}")

                Inventory.loadout(gold_loadout)
            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                TimeMachine.time_machine(e=Misc.get_idle_cap(1), m=Misc.get_idle_cap(2))  # need to keep adding as filling up
            FightBoss.nuke()
            Adventure.snipe(zone=zone_after_rebirth, duration=1, once=True, bosses=True, manual=False)  # auto to be safe
            Adventure.itopod_snipe(60, auto=True)  # may not have skill yet

        elif rt.days == 0 and rt.timestamp < deadline_train_power_toughness:
            # after adv training and < 2hr
            stateName = "Adv training"
            if curState != stateName:
                print(stateName)
                curState = stateName

                if debug:
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                    TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                             m=Misc.get_idle_cap(2))  # force away the resource
                Misc.reclaim_all()
                if debug:
                    while Misc.get_idle_cap(1) == 0 or Misc.get_idle_cap(2) == 0:
                        print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                        Misc.reclaim_all()
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")

                Inventory.loadout(gold_loadout)
            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Focus on adv training power and toughness
                AdvancedTraining.advanced_training(energy=(Misc.get_idle_cap(1) // 2), ability=1)  # Toughness
                AdvancedTraining.advanced_training(energy=Misc.get_idle_cap(1), ability=2)  # Power
                # Continue on magic time machine
                TimeMachine.time_machine(e=0, m=Misc.get_idle_cap(2))
            # Snipe itopod
            Adventure.snipe(zone=zone_after_rebirth, duration=1, once=True, bosses=True, manual=True)  # improve gold
            Adventure.itopod_snipe(60)

        elif rt.days == 0 and rt.timestamp < deadline_augmentation:
            stateName = "Augmentation"
            if curState != stateName:
                print(stateName)
                curState = stateName

                if debug:
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                    TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                             m=Misc.get_idle_cap(2))  # force away the resource
                Misc.reclaim_all()
                if debug:
                    while Misc.get_idle_cap(1) == 0 or Misc.get_idle_cap(2) == 0:
                        print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                        Misc.reclaim_all()
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")

                Inventory.loadout(gold_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[11])  # blood

            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Augmentation
                Augmentation.augments({"MI": 0.34, "DTMT": 0.66}, Misc.get_idle_cap(1))
                # Blood magic for gold
                BloodMagic.toggle_auto_spells(number=False, drop=False, gold=True)
                BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)
                # in case of excess
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))
            Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True, manual=True)
            Adventure.itopod_snipe(60)

        elif rt.days == 0 and rt.timestamp < deadline_adv_wandoos:
            stateName = "Adv wandoos"
            if curState != stateName:
                print(stateName)
                curState = stateName

                if debug:
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                    TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                             m=Misc.get_idle_cap(2))  # force away the resource
                Misc.reclaim_all()
                if debug:
                    while Misc.get_idle_cap(1) == 0 or Misc.get_idle_cap(2) == 0:
                        print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                        Misc.reclaim_all()
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")

                Inventory.loadout(ngu_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[11])  # blood

            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Adv training for wandoos
                AdvancedTraining.advanced_training(energy=(Misc.get_idle_cap(1) // 2), ability=4)  # wandoos energy
                AdvancedTraining.advanced_training(energy=Misc.get_idle_cap(1), ability=5)  # wandoos magic
                # Blood magic for drop
                BloodMagic.toggle_auto_spells(number=False, drop=True, gold=False)
                BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)
                # in case of excess
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))
            # enemies
            Adventure.itopod_snipe(60)

        elif rt.days == 0 and rt.timestamp < deadline_wandoos:
            stateName = "Wandoos"
            if curState != stateName:
                print(stateName)
                curState = stateName

                if debug:
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                    TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                             m=Misc.get_idle_cap(2))  # force away the resource
                Misc.reclaim_all()
                if debug:
                    while Misc.get_idle_cap(1) == 0 or Misc.get_idle_cap(2) == 0:
                        print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                        Misc.reclaim_all()
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")

                Inventory.loadout(ngu_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[2, 11])  # wandoos, blood

            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Wandoos
                Wandoos.wandoos(energy=True, magic=True)
                # Blood magic for number
                BloodMagic.toggle_auto_spells(number=True, drop=False, gold=False)
                BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)

                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))

            # enemies
            Adventure.itopod_snipe(60)

        elif rt.days == 0 and rt.timestamp < deadline_gold:
            stateName = "Gold"
            if curState != stateName:
                print(stateName)
                curState = stateName

                if debug:
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                    TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                             m=Misc.get_idle_cap(2))  # force away the resource
                Misc.reclaim_all()
                if debug:
                    while Misc.get_idle_cap(1) == 0 or Misc.get_idle_cap(2) == 0:
                        print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                        Misc.reclaim_all()
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")

                Inventory.loadout(gold_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[4, 1, 9, 10, 12], deactivate=True)  # add adv stats, drop, pp, day care, exp
            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))  # need to keep adding as filling up
            # enemies
            Adventure.itopod_snipe(60)

        elif rt.days > 0 and rt.timestamp.tm_min > 15:  # 15 min buffer
            stateName = "Pending rebirth"
            if curState != stateName:
                print(stateName)
                curState = stateName

                GoldDiggers.deactivate_all_diggers()
                Yggdrasil.ygg(equip=1)  # harvest with equipment set 1
                Yggdrasil.ygg(eat_all=True)
                GoldDiggers.level_diggers()  # level all diggers
                GoldDiggers.gold_diggers(targets=[3])  # cap for stat
                FightBoss.nuke()
                MoneyPit.spin()
                MoneyPit.pit()

                Rebirth.do_rebirth()
                # activate_challenge(8)
                time.sleep(3)
        else:
            # >=2hr < 1D
            stateName = "NGU"
            if curState != stateName:
                print(stateName)
                curState = stateName

                if debug:
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                    TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                             m=Misc.get_idle_cap(2))  # force away the resource
                Misc.reclaim_all()
                if debug:
                    while Misc.get_idle_cap(1) == 0 or Misc.get_idle_cap(2) == 0:
                        print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")
                        Misc.reclaim_all()
                    print(f"E: {Misc.get_idle_cap(1)} \t M: {Misc.get_idle_cap(2)}")

                Inventory.loadout(ngu_loadout)
                #Inventory.loadout(gold_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers([5, 6, 4, 1, 9, 12], deactivate=True)  # Energy NGU, Magic NGU, Adventure Stat, drop, pp, exp
            if Misc.get_idle_cap(1) > 20:
                NGU.assign_ngu(value=Misc.get_idle_cap(1), targets=ngu_energy_targets, magic=False)
                #NGU.cap_ngu(targets=None, magic=False, cap_all=True)
            if Misc.get_idle_cap(2) > 20:
                NGU.assign_ngu(value=Misc.get_idle_cap(2), targets=ngu_magic_targets, magic=True)
                #NGU.cap_ngu(targets=None, magic=True, cap_all=True)
            if Misc.get_idle_cap(3) > 0:
                Hacks.hacks(hacks_targets, Misc.get_idle_cap(3))
            #Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True, manual=True)
            Adventure.itopod_snipe(60)
            #Adventure.snipe(zone=19, duration=1, once=False, bosses=True, manual=True)
            #Adventure.itopod_snipe(0)

        # common area
        FightBoss.nuke()

        Yggdrasil.ygg()

        Inventory.merge_inventory(slots=6)
        Inventory.merge_equipment()
        Inventory.boost_equipment(boost_cube=True)
        # Inventory.boost_inventory(6)
        Inventory.boost_cube()

        Questing.questing(subcontract=True)

        if Misc.get_idle_cap(3) > 0:
            Hacks.hacks(hacks_targets, Misc.get_idle_cap(3))

        spells = BloodMagic.check_spells_ready()
        if spells:  # check if any spells are off CD
            Misc.reclaim_res(magic=True)
            for spell in spells:
                BloodMagic.cast_spell(spell)
            curState = ""  # let the loop reassign the stuff

        if Inputs.check_pixel_color(*coords.IS_PIT_READY):
            print("Feed money pit")
            GoldDiggers.level_diggers()
            MoneyPit.pit()
            print(stateName)

        Misc.save_check()
    except Exception as e:
        print(e)
        time.sleep(1)
