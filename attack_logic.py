import random
import re


def parse_attack_value(attack_value):
    # Initialize default values
    A = 1  # Default multiplier
    X = 0  # Dice value
    C = 0  # Constant

    # Remove spaces to simplify parsing
    attack_value_cleaned = attack_value.replace(' ', '')

    # Regex to find multiplier (A) and dice (X)
    dice_pattern = re.compile(r'(\d*)d(\d+)')
    dice_match = dice_pattern.search(attack_value_cleaned)

    if dice_match:
        A = int(dice_match.group(1)) if dice_match.group(1) else 1
        X = int(dice_match.group(2))

    # Regex to find constants (C)
    constants = re.findall(r'[-+]\d+', attack_value_cleaned)
    if constants:
        C = sum(map(int, constants))

    # Special case handling: constant before dice (e.g., "1+2d6")
    constant_before_dice = re.match(r'^\d+\+', attack_value_cleaned)
    if constant_before_dice:
        C += int(constant_before_dice.group(0)[:-1])
    #print(f"Parsed {A}d{X}+{C}")
    return A, X, C

def calculate_damage(attack_value, selected_monster, selected_player, aim_result):
    # Assuming selected_player has a 'parry' attribute and selected_monster has an 'attacks' dict
    parry_threshold = selected_player.parry + 4
    base_attack = selected_monster.attacks.get(attack_value, "1d6")  # Default to "1d6" if not found
    print(f"Attack value {attack_value}")

    # Roll base damage
    damage = roll_damage(attack_value)

    # If aim result is greater than or equal to parry + 4, add an extra 1d6 to the damage
    if aim_result >= parry_threshold:
        print(f"{aim_result}>{selected_player.parry} more than on 4. It's critical!")
        damage += simulate_dice_roll(1, 6, 0)  # Roll an additional 1d6
    print(f"Finale damage is {damage}")
    return damage

def simulate_dice_roll(A, X, C):
    """
    Simulates rolling A dice of X sides each, and then adds or subtracts a constant C.

    Parameters:
    - A: The number of dice to roll.
    - X: The number of sides on each die.
    - C: A constant to add (or subtract) to the total roll.

    Returns:
    The total of the dice rolls plus the constant.
    """
    rolls = [random.randint(1, X) for _ in range(A)]  # Generate all rolls
    total_roll = sum(rolls)

    # Debug prints
    # print(f"Dice rolls ({A}d{X}): {rolls}")
    # print(f"Total before adding constant ({C}): {total_roll}")

    return total_roll + C


def roll_damage(attack_value):
    """
    Simulates an attack based on the given attack value string.
    Returns the result of the attack (damage dealt).
    """
    A, X, C = parse_attack_value(attack_value)
    damage = simulate_dice_roll(A, X, C)
    print (f"Damage is {damage}")
    return damage


def roll_aim(skill_notation):
    A, X, C = parse_attack_value(skill_notation)  # Reuse your existing parsing logic

    aim_result = simulate_dice_roll(A, X, C)  # Reuse your dice roll simulation
    print (f"Aim roll is {aim_result}")
    return aim_result

def determine_attack_outcome(final_damage, selected_character):
    toughness =  selected_character.toughness
    if toughness is None:
        self.result_label.config(text="Error: Character's toughness not found.")
        return
    print(f"Character toughness {toughness}, damage is {final_damage}")
    damage_diff = final_damage - toughness

    if damage_diff <= 0:
        outcome = "No effect on the character."
    elif 0 < damage_diff < 4:
        outcome = "Character shaken or receives 1 wound if already shaken."
    elif 4 <= damage_diff < 8:
        outcome = "Character shaken and receives +1 wound."
    elif damage_diff >= 8:
        outcome = "Character shaken and receives +2 wounds."

    return outcome


# Example usage
if __name__ == "__main__":
    selected_attack_value = "2d6+3"  # Example attack value
    damage_dealt = roll_damage(selected_attack_value)
    print(f"Damage Dealt: {damage_dealt}")
