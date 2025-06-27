import builtins
import types
from unittest.mock import patch

import attack_logic as al


class DummyChar:
    def __init__(self, parry=0, toughness=0, attacks=None):
        self.parry = parry
        self.toughness = toughness
        self.attacks = attacks or {}


def test_parse_attack_value():
    assert al.parse_attack_value("2d6+3") == (2, 6, 3)
    assert al.parse_attack_value("1d8-2") == (1, 8, -2)
    assert al.parse_attack_value("1+2d6") == (2, 6, 3)
    assert al.parse_attack_value("d6") == (1, 6, 0)


def test_simulate_dice_roll_with_explode():
    with patch('attack_logic.random.randint', side_effect=[6, 3]):
        assert al.simulate_dice_roll(1, 6, 0) == 9


def test_simulate_dice_roll_multiple_dice_and_constant():
    with patch('attack_logic.random.randint', side_effect=[2, 1]):
        assert al.simulate_dice_roll(2, 6, 2) == 5


def test_roll_damage_uses_parsed_value():
    with patch('attack_logic.random.randint', return_value=4):
        assert al.roll_damage("1d6+2") == 6


def test_roll_aim():
    with patch('attack_logic.random.randint', return_value=3):
        assert al.roll_aim("d6") == 3


def test_calculate_damage_no_crit():
    monster = DummyChar(attacks={'stab': '1d6'})
    player = DummyChar(parry=5)
    with patch('attack_logic.roll_damage', return_value=4):
        damage = al.calculate_damage('stab', monster, player, aim_result=6)
    assert damage == 4


def test_calculate_damage_with_crit():
    monster = DummyChar(attacks={'stab': '1d6'})
    player = DummyChar(parry=2)
    with patch('attack_logic.roll_damage', return_value=4):
        with patch('attack_logic.simulate_dice_roll', return_value=5):
            damage = al.calculate_damage('stab', monster, player, aim_result=6)
    assert damage == 9


def test_determine_attack_outcome():
    char = DummyChar(toughness=5)
    assert al.determine_attack_outcome(4, char, ap_value=0) == "No effect on the character."
    assert al.determine_attack_outcome(6, char, ap_value=0) == "Character shaken or receives 1 wound if already shaken."
    assert al.determine_attack_outcome(14, char, ap_value=0) == "Character shaken and receives +3 wounds."
