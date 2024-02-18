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
    Simulates rolling A dice of X sides each for Savage Worlds, allowing for 'exploding' dice.
    If a die rolls its maximum value, it is rolled again and added to the total.

    Parameters:
    - A: The number of dice to roll.
    - X: The number of sides on each die.
    - C: A constant to add (or subtract) to the total roll.

    Returns:
    The total of the dice rolls plus the constant, including any additional rolls from 'exploding' dice.
    """
    total_roll = 0

    for i in range(A):
        roll = random.randint(1, X)
        total_roll += roll
        print(f"Roll #{i+1}: {roll}")  # Initial roll print

        # Check if the roll is the maximum value, and continue rolling if so
        while roll == X:
            print(f"Dice exploded! Rolling again...")  # Debug print for explosion
            roll = random.randint(1, X)
            total_roll += roll
            print(f"Exploded Roll: {roll}")  # Print the result of the exploded roll

    # Debug prints to show the final total before adding the constant
    print(f"Total before adding constant ({C}): {total_roll}")

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


def determine_attack_outcome(final_damage, selected_character, ap_value):
    print(selected_character.toughness)
    toughness = selected_character.toughness - ap_value  # Apply AP to reduce toughness
    # Ensure toughness doesn't go below some minimum, if applicable
    toughness = max(toughness, 0)
    print(f"Original Toughness: {selected_character.toughness}, AP: {ap_value}, Adjusted Toughness: {toughness}")

    if toughness is None:
        print("Error: Character's toughness not found.")
        return "Error: Character's toughness not found."

    print(f"Character toughness {toughness}, damage is {final_damage}")
    damage_diff = final_damage - toughness

    if damage_diff <= 0:
        outcome = "No effect on the character."
    else:
        # Calculate the number of wounds based on each full or partial increment of 4 points over toughness
        full_increments = damage_diff // 4  # How many full increments of 4 are in the damage difference
        partial_increment = 1 if damage_diff % 4 > 0 else 0  # Check for any partial increment
        total_increments = full_increments + partial_increment

        # Debug output to show calculation of increments
        print(
            f"Damage difference/4 exceeded {full_increments} times with a partial increment of {partial_increment}, total increments: {total_increments}")

        if total_increments == 1:
            outcome = "Character shaken or receives 1 wound if already shaken."
        else:
            outcome = f"Character shaken and receives +{total_increments} wounds."

    return outcome


# Example usage
if __name__ == "__main__":
    selected_attack_value = "2d6+3"  # Example attack value
    damage_dealt = roll_damage(selected_attack_value)
    print(f"Damage Dealt: {damage_dealt}")
