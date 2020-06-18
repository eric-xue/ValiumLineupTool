import tkinter as tk
from PIL import ImageTk, Image
import glob as glob
import os as os
import xml.etree.ElementTree as ET
from enum import Enum

agent_list = ["Sova", "Viper", "Brimstone", "Cypher"]
map_list = ["Bind", "Haven", "Split", "Ascent"]
side_list = ["Attacker", "Defender"]
spot_list = []

inital_path = os.getcwd()
os.chdir("../pictures/")
picture_directory = os.getcwd()
os.chdir(inital_path)

map_dictionary = {}
pic_tree = ET.parse(picture_directory + "\\config.xml")
pic_root = pic_tree.getroot()
image_list = []



class CharMapKey:
    def __init__(self, agent, chosenmap, side):
        self.agent = agent
        self.chosenmap = chosenmap
        self.side = side

    def __hash__(self):
        return hash((self.agent, self.chosenmap, self.side))

    def __eq__(self, other):
        return (self.agent, self.chosenmap, self.side) == (other.character, other.chosenmap, other.side)

    def __ne__(self, other):
        return not (self == other)


def init_charkey():
    charkey_dict = {}
    for agents in agent_list:
        for maps in map_list:
            for sides in side_list:
                charkey_dict[CharMapKey(agents, maps, sides)] = "../pictures/{agent}/{map}/{side}".format(
                    agent=agents, map=maps, side=sides)
    return charkey_dict


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()
        # Create child frames
        selection_frame = tk.Frame(self.main_frame, width=400, height=20)
        selection_frame.grid(row=0, column=0)
        spot_frame = tk.Frame(self.main_frame)
        spot_frame.grid(row=1, column=0)
        map_frame = tk.Frame(self.main_frame)
        map_frame.grid(row=0, column=1)
        lineup_frame = tk.Frame(self.main_frame)
        lineup_frame.grid(row=1, column=1)

        # Option menu using above char list
        agent = tk.StringVar()
        agent.set(agent_list[0])
        agent_selection = tk.OptionMenu(selection_frame, agent, *agent_list)
        agent_selection.grid(row=0, column=0)
        agent_selection.configure(width=15, height=2)

        # Option menu using above defined maps list
        maps = tk.StringVar()
        maps.set(map_list[0])
        map_selection = tk.OptionMenu(selection_frame, maps, *map_list)
        map_selection.grid(row=0, column=1)
        map_selection.configure(width=15, height=2)

        # Option menu w/ hard coded sides
        playing_side = tk.StringVar()
        playing_side.set("Attacker")
        side_selection = tk.OptionMenu(selection_frame, playing_side, "Attacker", "Defender")
        side_selection.grid(row=0, column=2)
        side_selection.configure(width=15, height=2)

        # Option menu for possible spots
        orig_path = os.getcwd()
        os.chdir(picture_directory + "\\maps\\" + maps.get() + "\\")
        spot_list = glob.glob("*.jpg")
        os.chdir(orig_path)
        spot = tk.StringVar()
        spot.set("Choose a spot")
        spot_selection = tk.OptionMenu(spot_frame, spot, *spot_list)

        def refresh_spot(haselements):
            global spot_list
            if haselements:
                spot.set("Choose a spot")
            else:
                spot.set("No lineups found")
            spot_selection["menu"].delete(0, "end")
            for new_spot in spot_list:
                spot_selection["menu"].add_command(label=new_spot, command=tk._setit(spot, new_spot))
        # Callback function to update when spot inputs change
        def updatespot_list(*args):
            # Save original pathname to restore later
            orig_path = os.getcwd()
            os.chdir(picture_directory + "\\maps\\" + maps.get() + "\\")
            global spot_list
            spot_list = glob.glob("*.jpg")
            spot_list = [x.split(".jpg", 1)[0] for x in spot_list]
            haselements = False
            if len(spot_list) > 0:
                haselements = True
            os.chdir(orig_path)
            refresh_spot(haselements)

        updatespot_list()
        spot_selection.grid(row=0)
        spot_selection.configure(width=15, height=2)
        maps.trace("w", updatespot_list)
        agent.trace("w", updatespot_list)
        playing_side.trace("w", updatespot_list)

        # Map Image
        # Callback function to update when map changed from dropdown
        def updatemap(*args):
            map_path.set(picture_directory + "\\maps\\" + maps.get() + "\\" + maps.get() + ".png")
            map_image = Image.open(map_path.get())
            map_image = map_image.resize((500, 500))
            map_img = ImageTk.PhotoImage(map_image)
            map_label.configure(image=map_img)
            map_label.image = map_img

        map_path = tk.StringVar()
        map_path.set(picture_directory + "\\maps\\" + maps.get() + "\\" + maps.get() + ".png")
        map_image = Image.open(map_path.get())
        map_image = map_image.resize((500, 500))
        map_img = ImageTk.PhotoImage(map_image)
        map_label = tk.Label(map_frame, image=map_img)
        map_label.image = map_img  # Keep reference https://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        map_label.pack()
        maps.trace("w", updatemap)

        # Spot Image
        # Callback function to update when spot changes
        def updatelineup(*args):
            lineupfound = False
            try:
                lineup_path.set(picture_directory + "\\maps\\" + maps.get() + "\\" + spot.get() + ".jpg")
                lineup_image = Image.open(lineup_path.get())
                lineupfound = True
            except FileNotFoundError:
                print("File not found at " + lineup_path.get())
                lineup_path.set(picture_directory + "\\placeholder.jpg")
                lineup_image = Image.open(lineup_path.get())
            # If lineup found, look @ xml and insert all images associated w/ lineup into array
            if lineupfound:
                image_list.clear()
                print("The current spot is :" + spot.get() + " with spots")
                for child in pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][side_list.index(playing_side.get())]:
                    if child.get('name') == spot.get():
                        for grandchild in child:
                            formatted_grandchild = grandchild.text.strip()
                            formatted_grandchild.split("\n", 1)[0]
                            image_list.append(formatted_grandchild)
                        break
                print(image_list)
            lineup_image = lineup_image.resize((848, 480))
            lineup_img = ImageTk.PhotoImage(lineup_image)
            lineup.configure(image=lineup_img)
            lineup.image = lineup_img
            print(lineup_path.get())

        lineup_path = tk.StringVar()
        lineup_path.set(picture_directory + "\\placeholder.jpg")
        lineup_image = Image.open(picture_directory + "\\placeholder.jpg")
        lineup_image = lineup_image.resize((848, 480))
        lineup_img = ImageTk.PhotoImage(lineup_image)
        lineup = tk.Label(lineup_frame, image=lineup_img)
        lineup.image = lineup_img
        lineup.grid(row=0)
        spot.trace("w", updatelineup)
        maps.trace("w", updatelineup)
        agent.trace("w", updatelineup)
        playing_side.trace("w", updatelineup)

        # Button for next image if multiple
        lineup_imgarr = []

        def updatelineup():
            pass

        def prev_lineimage():
            pass

        def next_lineimage():
            pass

        lineup_buttonframe = tk.Frame(lineup_frame)
        lineup_buttonframe.grid(row=1)

        lineup_button_back = tk.Button(lineup_buttonframe, text="Back", command=prev_lineimage)
        lineup_button_back.grid(row=0, column=0, padx=10)
        lineup_button_next = tk.Button(lineup_buttonframe, text="Next", command=next_lineimage)
        lineup_button_next.grid(row=0, column=1, padx=10)


def main():
    # charkeydict = init_charkey()
    # print(charkeydict)
    root = tk.Tk();
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
