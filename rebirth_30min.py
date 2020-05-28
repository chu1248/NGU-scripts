import time
# Helper classes
from classes.features   import (AdvancedTraining, Adventure, Augmentation, FightBoss, Inventory, Misc,
                                BloodMagic, GoldDiggers, NGU, Wandoos, TimeMachine, MoneyPit, Rebirth,
                                Questing, Yggdrasil)
from classes.helper     import Helper
# Challenge needed
from classes.challenge  import Challenge
from classes.navigation import Navigation
import coordinates  as coords
import usersettings as userset
from classes.inputs     import Inputs
from classes.challenges import ngu, basic
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

Helper.init()
Helper.requirements()

curState = ""

#zone_after_rebirth = 23  # Pretty
#zone_after_training = 23  # Pretty
zone_after_rebirth = -1  # Pretty
zone_after_training = -1  # Pretty
deadline_gold = time.strptime("00:05:00", "%H:%M:%S")  # for wear gold drop equip for gold drop from titan
deadline_augmentation = time.strptime("00:15:00", "%H:%M:%S")
deadline_train_power_toughness = time.strptime("00:20:00", "%H:%M:%S")
deadline_adv_wandoos = time.strptime("00:25:00", "%H:%M:%S")  # deadline_augmentation + datetime.timedelta(minutes=15)
deadline_wandoos = time.strptime("04:00:00", "%H:%M:%S")  # deadline_adv_wandoos + datetime.timedelta(minutes=15)

rt = None

while True:
    try:
        rt = Rebirth.get_rebirth_time()
    except:
        print("Error in parsing the rebirth time, past rt " + str(rt.days) + " " + str(rt.timestamp))

    try:
        if rt.days == 0 and rt.timestamp < deadline_gold:
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

                Inventory.loadout(respwanDrop_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[1, 9, 10, 12], deactivate=True)  # drop, pp, day care, exp
            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))  # need to keep adding as filling up
            # enemies
            FightBoss.nuke()
            #Adventure.snipe(zone=zone_after_rebirth, duration=1, once=True, bosses=True, manual=False)  # auto to be safe
            #Adventure.itopod_snipe(60, auto=True)  # may not have skill yet
            if zone_after_training == -1:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, highest=True, bosses=True, manual=False)
            else:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, bosses=True, manual=False)

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

                Inventory.loadout(respwanDrop_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[1, 3, 10, 12])  # blood

            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Augmentation
                Augmentation.augments({"MI": 0.34, "DTMT": 0.66}, Misc.get_idle_cap(1))
                # Blood magic for gold
                BloodMagic.toggle_auto_spells(number=True, drop=False, gold=False)
                BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)
                # in case of excess
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))
            #Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True, manual=True)
            #Adventure.itopod_snipe(60)
            if zone_after_training == -1:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, highest=True, bosses=True, manual=False)
            else:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, bosses=True, manual=False)

        elif rt.days == 0 and rt.timestamp < deadline_train_power_toughness:
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

                Inventory.loadout(respwanDrop_loadout)
            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Focus on adv training power and toughness
                AdvancedTraining.advanced_training(energy=(Misc.get_idle_cap(1) // 2), ability=1)  # Toughness
                AdvancedTraining.advanced_training(energy=Misc.get_idle_cap(1), ability=2)  # Power
                # Continue on magic time machine
                TimeMachine.time_machine(e=0, m=Misc.get_idle_cap(2))
            # Snipe itopod
            #Adventure.snipe(zone=zone_after_rebirth, duration=1, once=True, bosses=True, manual=True)  # improve gold
            #Adventure.itopod_snipe(60)
            if zone_after_training == -1:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, highest=True, bosses=True, manual=False)
            else:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, bosses=True, manual=False)

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

                Inventory.loadout(respwanDrop_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[11])  # blood

            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Adv training for wandoos
                AdvancedTraining.advanced_training(energy=(Misc.get_idle_cap(1) // 2), ability=4)  # wandoos energy
                AdvancedTraining.advanced_training(energy=Misc.get_idle_cap(1), ability=5)  # wandoos magic
                # Blood magic for number
                BloodMagic.toggle_auto_spells(number=True, drop=False, gold=False)
                BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)
                # in case of excess
                Augmentation.augments({"MI": 0.34, "DTMT": 0.66}, Misc.get_idle_cap(1))
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))
            # enemies
            #Adventure.itopod_snipe(60)
            if zone_after_training == -1:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, highest=True, bosses=True, manual=False)
            else:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, bosses=True, manual=False)

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

                Inventory.loadout(respwanDrop_loadout)
                GoldDiggers.deactivate_all_diggers()
                GoldDiggers.gold_diggers(targets=[2, 11])  # wandoos, blood

            if Misc.get_idle_cap(1) > 0 or Misc.get_idle_cap(2) > 0:
                # Wandoos
                Wandoos.wandoos(energy=True, magic=True)
                # Blood magic for number
                BloodMagic.toggle_auto_spells(number=True, drop=False, gold=False)
                BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)

                Augmentation.augments({"MI": 0.34, "DTMT": 0.66}, Misc.get_idle_cap(1))
                TimeMachine.time_machine(e=Misc.get_idle_cap(1),
                                         m=Misc.get_idle_cap(2))

            # enemies
            #Adventure.itopod_snipe(60)
            if zone_after_training == -1:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, highest=True, bosses=True, manual=False)
            else:
                Adventure.snipe(zone=zone_after_training, duration=1, once=False, bosses=True, manual=False)

        #elif rt.days <= 0 and rt.timestamp.tm_hour >= 1:
        #elif rt.days >= 0 and (rt.timestamp.tm_min >= 30 or rt.timestamp.tm_hour >= 1):
        elif rt.days >= 0:
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
                time.sleep(3)
        else:
            # most of the time
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
                #NGU.assign_ngu(value=Misc.get_idle_cap(1), targets=ngu_energy_targets, magic=False)
                NGU.cap_ngu(targets=None, magic=False, cap_all=True)
            if Misc.get_idle_cap(2) > 20:
                #NGU.assign_ngu(value=Misc.get_idle_cap(2), targets=ngu_magic_targets, magic=True)
                NGU.cap_ngu(targets=None, magic=True, cap_all=True)
            #Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True, manual=True)
            Adventure.itopod_snipe(60)
            #Adventure.snipe(zone=19, duration=1, once=False, bosses=True, manual=True)
            #Adventure.itopod_snipe(0)

        # common area
        FightBoss.nuke()

        Yggdrasil.ygg()

        Inventory.merge_inventory(slots=9)
        # Inventory.boost_inventory(6)
        Inventory.boost_equipment(boost_cube=True)
        Inventory.boost_cube()

        Questing.questing(subcontract=True)

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
