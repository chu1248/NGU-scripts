import time
# Helper classes
from classes.features   import (AdvancedTraining, Adventure, Augmentation, FightBoss, Inventory, Misc,
                                BloodMagic, GoldDiggers, NGU, Wandoos, TimeMachine, MoneyPit, Rebirth,
                                Questing, Yggdrasil)
from classes.helper     import Helper

# Set these to your own loadouts

Helper.init()
Helper.requirements()

while True:
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


