import time
# Helper classes
from classes.features   import (AdvancedTraining, Adventure, Augmentation, FightBoss, Inventory, Misc,
                                BloodMagic, GoldDiggers, NGU, Wandoos, TimeMachine, MoneyPit, Rebirth,
                                Questing, Yggdrasil)
from classes.helper     import Helper

# Set these to your own loadouts

blood_magic_highest_affordable_level = 6  # 0 based

Helper.init()
Helper.requirements()

curState = ""

while False:
    rt = Rebirth.get_rebirth_time()

    Yggdrasil.ygg()

    Adventure.snipe(zone=16, duration=20, once=True, bosses=True, manual=True)
    Adventure.itopod_snipe(60)
    Inventory.boost_cube()

    spells = BloodMagic.check_spells_ready()
    if spells:  # check if any spells are off CD
        Misc.reclaim_ngu(magic=True)  # take all magic from magic NGUs
        for spell in spells:
            BloodMagic.cast_spell(spell)
        Misc.reclaim_bm()
        NGU.assign_ngu(Misc.get_idle_cap(2), range(1, 7), magic=True)  # magic idle for magic ngu

    continue

zone_after_rebirth = 14
zone_after_training = 16
deadline_before_adv_training = time.strptime("00:25:00", "%H:%M:%S")
deadline_train_power_toughness = time.strptime("01:30:00", "%H:%M:%S")
deadline_augmentation = time.strptime("02:00:00", "%H:%M:%S")  # deadline_train_power_toughness.tm + datetime.timedelta(minutes=30)
deadline_adv_wandoos = time.strptime("02:15:00", "%H:%M:%S")  # deadline_augmentation + datetime.timedelta(minutes=15)
deadline_wandoos = time.strptime("02:45:00", "%H:%M:%S")  # deadline_adv_wandoos + datetime.timedelta(minutes=30)

while True:
    rt = Rebirth.get_rebirth_time()

    if rt.days == 0 and rt.timestamp < deadline_before_adv_training:
        # before advance training
        # Focus on time machine
        stateName = "Before adv training"
        if curState != stateName:
            print(stateName)
            curState = stateName
            Misc.reclaim_all()
        TimeMachine.time_machine(e=Misc.get_idle_cap(1), m=Misc.get_idle_cap(2))  # need to keep adding as filling up
        FightBoss.nuke()
        Adventure.snipe(zone=zone_after_rebirth, duration=1, once=True, bosses=True, manual=False)  # Mega land, auto to be safe
        Adventure.itopod_snipe(60, auto=True)  # may not have skill yet

    elif rt.days == 0 and rt.timestamp < deadline_train_power_toughness:
        # after adv training and < 2hr
        stateName = "Adv training"
        if curState != stateName:
            print(stateName)
            curState = stateName
            Misc.reclaim_all()
        # Focus on adv training power and toughness
        AdvancedTraining.advanced_training(value=(Misc.get_idle_cap(1) // 2), ability=1)  # Toughness
        AdvancedTraining.advanced_training(value=Misc.get_idle_cap(1), ability=2)  # Power
        # Continue on magic time machine
        TimeMachine.time_machine(e=0, m=Misc.get_idle_cap(2))
        # Snipe itopod
        Adventure.itopod_snipe(60)

    elif rt.days == 0 and rt.timestamp < deadline_augmentation:
        stateName = "Augmentation"
        if curState != stateName:
            print(stateName)
            curState = stateName
            Misc.reclaim_all()
        # Augmentation
        Augmentation.augments({"CI": 0.7, "ML": 0.3}, Misc.get_idle_cap(1))
        # Blood magic for gold
        BloodMagic.toggle_auto_spells(number=False, drop=False, gold=True)
        BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)

        Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True,
                    manual=True)  # Mega land, auto to be safe
        Adventure.itopod_snipe(60)

    elif rt.days == 0 and rt.timestamp < deadline_adv_wandoos:
        stateName = "Adv wandoos"
        if curState != stateName:
            print(stateName)
            curState = stateName
            Misc.reclaim_all()
        # Adv training for power and toughness
        AdvancedTraining.advanced_training(value=(Misc.get_idle_cap(1) // 2), ability=4)  # wandoos energy
        AdvancedTraining.advanced_training(value=Misc.get_idle_cap(1), ability=5)  # wandoos magic
        # Blood magic for drop
        BloodMagic.toggle_auto_spells(number=False, drop=True, gold=False)
        BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)
        # enemies
        Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True,
                        manual=True)
        Adventure.itopod_snipe(60)

    elif rt.days == 0 and rt.timestamp < deadline_wandoos:
        stateName = "Wandoos"
        if curState != stateName:
            print(stateName)
            curState = stateName
            Misc.reclaim_all()
        # Wandoos
        Wandoos.wandoos(energy=True, magic=True)
        # Blood magic for number
        BloodMagic.toggle_auto_spells(number=True, drop=False, gold=False)
        BloodMagic.blood_magic_reverse(blood_magic_highest_affordable_level)
        # enemies
        Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True,
                        manual=True)
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
            GoldDiggers.gold_diggers(targets=[3])  # stat digger for stat
            FightBoss.nuke()
            MoneyPit.spin()
            MoneyPit.pit()

            Rebirth.do_rebirth()
            time.sleep(3)
    else:
        # >=2hr < 1D
        stateName = "NGU"
        if curState != stateName:
            print(stateName)
            curState = stateName
            Misc.reclaim_all()
        GoldDiggers.deactivate_all_diggers()
        GoldDiggers.gold_diggers([5, 6], deactivate=True)  # toggle the active, to use preset level
        NGU.assign_ngu(value=Misc.get_idle_cap(1), targets=range(1, 10), magic=False)
        NGU.assign_ngu(value=Misc.get_idle_cap(2), targets=range(1, 8), magic=True)
        Adventure.snipe(zone=zone_after_training, duration=1, once=True, bosses=True, manual=True)  # Beardverse
        Adventure.itopod_snipe(60)
        #Adventure.snipe(zone=16, duration=1, bosses=True, manual=True)  # Beardverse

    # common area
    FightBoss.nuke()

    Yggdrasil.ygg()

    Inventory.boost_cube()

    spells = BloodMagic.check_spells_ready()
    if spells:  # check if any spells are off CD
        Misc.reclaim_ngu(magic=True)  # take all magic from magic NGUs
        for spell in spells:
            BloodMagic.cast_spell(spell)
        curState = ""  # let the loop reassign the stuff
