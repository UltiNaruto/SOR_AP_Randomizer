from ...Regions import StreetsOfRageRegion

from BaseClasses import MultiWorld


# noinspection PyShadowingNames
class Menu(StreetsOfRageRegion):
    name = "Menu"

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Shopping Mall Gate': lambda state, player: state.has('Shopping Mall Key', player),
            'Inner City Slums Gate': lambda state, player: state.has('Inner City Slums Key', player),
            'Beachside Gate': lambda state, player: state.has('Beachside Key', player),
            'Bridge Under Construction Gate': lambda state, player: state.has('Bridge Under Construction Key', player),
            'Aboard The Ferry Gate': lambda state, player: state.has('Aboard The Ferry Key', player),
            'Factory Gate': lambda state, player: state.has('Factory Key', player),
            'Elevator Gate': lambda state, player: state.has('Elevator Key', player),
            'Syndicate Mansion Gate': lambda state, player: state.has('Syndicate Mansion Key', player),
        })


# noinspection PyShadowingNames
class ShoppingMallGate(StreetsOfRageRegion):
    name = 'Shopping Mall Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Shopping Mall': lambda state, player: True,
        })


# noinspection PyShadowingNames
class InnerCitySlumsGate(StreetsOfRageRegion):
    name = 'Inner City Slums Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Inner City Slums': lambda state, player: True,
        })


# noinspection PyShadowingNames
class BeachsideGate(StreetsOfRageRegion):
    name = 'Beachside Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Beachside': lambda state, player: True,
        })


# noinspection PyShadowingNames
class BridgeUnderConstructionGate(StreetsOfRageRegion):
    name = 'Bridge Under Construction Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Bridge Under Construction': lambda state, player: True,
        })


# noinspection PyShadowingNames
class AboardTheFerryGate(StreetsOfRageRegion):
    name = 'Aboard The Ferry Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Aboard The Ferry': lambda state, player: True,
        })


# noinspection PyShadowingNames
class FactoryGate(StreetsOfRageRegion):
    name = 'Factory Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Factory': lambda state, player: True,
        })


# noinspection PyShadowingNames
class ElevatorGate(StreetsOfRageRegion):
    name = 'Elevator Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Elevator': lambda state, player: True,
        })


# noinspection PyShadowingNames
class SyndicateMansionGate(StreetsOfRageRegion):
    name = 'Syndicate Mansion Gate'

    def __init__(self, player: int, multiworld: MultiWorld):
        super().__init__(player, multiworld, exits_={
            'Menu': lambda state, player: True,
            'Syndicate Mansion': lambda state, player: True,
        })
