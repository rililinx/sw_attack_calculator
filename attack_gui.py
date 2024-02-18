from load_fighters import *
import tkinter as tk
from tkinter import ttk
from attack_logic import *


# Assuming Character class and load_characters_from_folder function are defined as before

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Savage Worlds Attack Calculator")
        self.attack_type_var = tk.StringVar(value="melee")  # Default to melee
        self.defense_var = tk.StringVar(value="none")  # Default to none

        # Labels for displaying Shooting and Fighting
        self.shooting_label = tk.Label(self, text="Shooting: N/A")
        self.shooting_label.pack(padx=10, pady=5)

        self.fighting_label = tk.Label(self, text="Fighting: N/A")
        self.fighting_label.pack(padx=10, pady=5)
        # In the __init__ method of the Application class
        self.ap_var = tk.StringVar(value="0")
        ttk.Label(self, text="Armor Piercing (AP):").pack(anchor=tk.W)
        ap_entry = ttk.Entry(self, textvariable=self.ap_var)
        ap_entry.pack(anchor=tk.W)

        self.monster_var = tk.StringVar()
        self.attack_var = tk.StringVar()
        self.player_var = tk.StringVar()
        self.result_text = tk.StringVar()
        # Attack type selection

        self.result_label = tk.Label(self, text="Attack result will be shown here", bg="lightgray")
        self.result_label.pack(padx=10, pady=10, fill=tk.X)
        # Initialize empty lists for monsters and players
        self.monsters = []
        self.players = []
        # Example of adding radio buttons for attack type
        ttk.Label(self, text="Attack Type:").pack(anchor=tk.W)
        ttk.Radiobutton(self, text="Melee", variable=self.attack_type_var, value="melee").pack(anchor=tk.W)
        ttk.Radiobutton(self, text="Ranged", variable=self.attack_type_var, value="ranged").pack(anchor=tk.W)

        # Defense option selection
        ttk.Label(self, text="Defense:").pack(anchor=tk.W)
        ttk.Radiobutton(self, text="None", variable=self.defense_var, value="none").pack(anchor=tk.W)
        ttk.Radiobutton(self, text="Cover", variable=self.defense_var, value="cover").pack(anchor=tk.W)
        ttk.Radiobutton(self, text="Shield", variable=self.defense_var, value="shield").pack(anchor=tk.W)

        self.create_widgets()
        self.load_data()

    def update_skill_labels(self, monster_name):
        selected_monster = self.monsters_dict.get(monster_name)

        if selected_monster:
            # Update labels with the selected monster's Shooting and Fighting skills
            shooting_text = f"Shooting: {selected_monster.Shooting}" if selected_monster.Shooting else "Shooting: N/A"
            self.shooting_label.config(text=shooting_text)

            fighting_text = f"Fighting: {selected_monster.Fight}" if selected_monster.Fight else "Fighting: N/A"
            self.fighting_label.config(text=fighting_text)
        else:
            # Reset labels if for some reason the monster is not found
            self.shooting_label.config(text="Shooting: N/A")
            self.fighting_label.config(text="Fighting: N/A")


    def create_widgets(self):
        # Monster selection frame
        self.monster_frame = ttk.LabelFrame(self, text="Monsters")
        self.monster_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Attack selection frame (initially empty)
        self.attack_frame = ttk.LabelFrame(self, text="Attacks")
        self.attack_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Player selection frame
        self.player_frame = ttk.LabelFrame(self, text="Players")
        self.player_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Attack button and result display
        attack_button = ttk.Button(self, text="Attack", command=self.attack)
        attack_button.pack(pady=5)

        result_label = ttk.Label(self, textvariable=self.result_text)
        result_label.pack(pady=5)

    def on_monster_select(self, event=None):
        # Get selected index
        selection = self.monster_listbox.curselection()
        if not selection:
            return

        selected_index = selection[0]
        selected_monster = self.monsters[selected_index]

        # Update Shooting and Fighting labels
        self.label_shooting.config(text=f"Shooting: {selected_monster.Shooting}")
        self.label_fighting.config(text=f"Fighting: {selected_monster.Fight}")


    def load_data(self):
        # Load characters and monsters as instance variables
        self.players = load_characters_from_folder('players')
        self.monsters = load_characters_from_folder('monsters')

        for monster in self.monsters:
            ttk.Radiobutton(self.monster_frame, text=monster.name, variable=self.monster_var, value=monster.name,
                            command=self.update_attacks).pack(anchor=tk.W)

        for player in self.players:
            ttk.Radiobutton(self.player_frame, text=player.name, variable=self.player_var, value=player.name).pack(
                anchor=tk.W)

    def get_selected_attack_value(self):
        selected_monster_name = self.monster_var.get()
        selected_attack_name = self.attack_var.get()

        # Find the selected monster
        selected_monster = next((monster for monster in self.monsters if monster.name == selected_monster_name), None)

        if not selected_monster:
            print("Selected monster not found.")
            return None

        # Get the attack value from the selected monster's attacks
        attack_value = selected_monster.attacks.get(selected_attack_name)

        if not attack_value:
            print(f"No attack value found for {selected_attack_name}.")
            return None

        return attack_value

    def update_attacks(self):
        # Clear current attacks
        for widget in self.attack_frame.winfo_children():
            widget.destroy()

        # Load selected monster's attacks
        selected_monster_name = self.monster_var.get()
        for monster in self.monsters:
            if monster.name == selected_monster_name:
                # Update attacks
                for attack_name, attack_value in monster.attacks.items():
                    # Include both attack name and its value in the radio button label
                    attack_label = f"{attack_name} - {attack_value}"
                    ttk.Radiobutton(self.attack_frame, text=attack_label, variable=self.attack_var,
                                    value=attack_name).pack(anchor=tk.W)

                # Update Shooting and Fighting labels
                shooting_text = f"Shooting: {monster.Shooting}" if monster.Shooting else "Shooting: N/A"
                self.shooting_label.config(text=shooting_text)

                fighting_text = f"Fighting: {monster.Fight}" if monster.Fight else "Fighting: N/A"
                self.fighting_label.config(text=fighting_text)

                break

    def attack(self):
        try:
            ap_value = int(self.ap_var.get())
            assert ap_value >= 0
        except (ValueError, AssertionError):
            self.result_text.set("Invalid AP value. Please enter a positive number or 0.")
            return

        # Continue with the attack logic...

        attack_type = self.attack_type_var.get()  # Melee or ranged
        defense_type = self.defense_var.get()  # None, cover, shield

        # Fetch selected monster and player as before
        monster_name = self.monster_var.get()
        player_name = self.player_var.get()
        selected_monster = next((monster for monster in self.monsters if monster.name == monster_name), None)
        selected_player = next((player for player in self.players if player.name == player_name), None)

        if not selected_monster or not selected_player:
            self.result_text.set("Monster or player not found.")
            return

        # Determine the skill to use based on the attack type and roll for aim
        skill_notation = selected_monster.Fight if attack_type == "melee" else selected_monster.Shooting
        aim_result = roll_aim(skill_notation)

        # Check aim roll against conditions
        if attack_type == "melee" and aim_result < selected_player.parry:
            self.result_text.set(f"{monster_name} attacks {player_name} on {aim_result} with a melee attack and misses.")
            return
        elif attack_type == "ranged" and (defense_type in ["cover", "shield"]) and aim_result < 6:
            self.result_text.set(
                f"{monster_name} attacks {player_name}  on {aim_result} with a ranged attack and misses due to {defense_type}.")
            return

        self.result_text.set(
            f"{monster_name} attacks {player_name}  on {aim_result} with a attack and hit.")
        attack_value = self.get_selected_attack_value()
        if attack_value:
            # Proceed to damage calculation if not missed
            final_damage=calculate_damage(attack_value, selected_monster, selected_player, aim_result)
            ap_value = int(self.ap_var.get() or 0)  # Get AP value, defaulting to 0 if not provided

            outcome=determine_attack_outcome(final_damage,selected_player, ap_value)
            self.result_label.config(text=outcome)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
