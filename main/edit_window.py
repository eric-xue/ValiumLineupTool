import os as os
import tkinter as tk
from tkinter import ttk as ttk
from lxml import etree as ET
import glob as glob

class edit_window():
    def __init__(self, master, agent_list, map_list, xml_tree):

        pic_root = xml_tree.getroot()
        side_list = ["Attacker", "Defender"]

        self.xml_root = xml_tree.getroot()
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Edit XML")
        self.side_selection = ["Attacker", "Defender"]
        self.agent_list = agent_list
        self.map_list = map_list

        #   Make frames
        tab_control = ttk.Notebook(self.window)
        tab_control.pack()
        add_tab = tk.Frame(tab_control)
        tab_control.add(add_tab, text="Add")
        edit_tab = tk.Frame(tab_control)
        tab_control.add(edit_tab, text="Edit")
        remove_tab = tk.Frame(tab_control)
        tab_control.add(remove_tab, text="Remove")
        self.selection_frame = tk.Frame(add_tab, width=400, height=20,pady=40)
        self.selection_frame.pack()
        self.button_frame = tk.Frame(add_tab)
        self.button_frame.pack()
        add_win = add_window(add_tab, agent_list, map_list, xml_tree)
        remove_win = remove_window(remove_tab, agent_list, map_list, xml_tree)

        # Tab change handler function
        def update_tab(event):
            if event.widget.index("current") == 0:
                add_win.update_xml(xml_tree)
            elif event.widget.index("current") == 2:
                remove_win.update_xml(xml_tree)
        tab_control.bind("<<NotebookTabChanged>>", update_tab)

class add_window():
    def __init__(self, master, agent_list, map_list, xml_tree):
        self.master = master
        self.side_list = ["Attacker", "Defender"]
        self.pic_root = xml_tree.getroot()
        self.agent_list = agent_list
        self.map_list = map_list
        self.picture_directory = get_picdir()

        self.selection_frame = tk.Frame(master, width=400, height=20, pady=40)
        self.selection_frame.pack()
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.agent = tk.StringVar()
        self.maps = tk.StringVar()
        self.playing_side = tk.StringVar()

        self.spot = tk.StringVar()
        self.spot_list = ["Choose a spot"]
        self.spot_selection = tk.OptionMenu(self.selection_frame, self.spot, *self.spot_list)
        self.curr_pic = tk.StringVar()
        self.pic_list = ["Choose a picture."]
        self.pic_selection = tk.OptionMenu(self.selection_frame, self.curr_pic, *self.pic_list)

        def refresh_pic_list(*args):
            try:
                # Get list of all pictures in xml w/ given combo
                raw_xml_pics = self.pic_root[agent_list.index(self.agent.get())][map_list.index(self.maps.get())][
                    self.side_list.index(self.playing_side.get())][self.spot_list.index(self.spot.get())]
                xml_pictures = []
                for child in raw_xml_pics:
                    xml_pictures.append(child.text)
                # Get all pictures in directory
                orig_path = os.getcwd()
                os.chdir(self.picture_directory + "\\maps\\" + self.maps.get() + "\\")
                folder_pictures = glob.glob("*.*")
                os.chdir(orig_path)
                # Find all unused pictures
                self.pic_list = list(set(folder_pictures) - set(xml_pictures))
                if len(self.pic_list) != 0:
                    self.curr_pic.set(self.pic_list[0])
                else:
                    self.curr_pic.set("No pictures found")
                self.pic_selection["menu"].delete(0, "end")
                for new_pic in self.pic_list:
                    self.pic_selection["menu"].add_command(label=new_pic, command=tk._setit(self.curr_pic, new_pic))
            except ValueError:
                self.curr_pic.set("No pictures found.")
                self.pic_selection["menu"].delete(0, "end")


        def refresh_spot(haselements):
            if haselements:
                self.spot.set(self.spot_list[0])
            else:
                self.spot.set("No lineups found")
            self.spot_selection["menu"].delete(0, "end")
            for new_spot in self.spot_list:
                self.spot_selection["menu"].add_command(label=new_spot, command=tk._setit(self.spot, new_spot))
            refresh_pic_list()

        def updatespot_list(*args):
            self.spot_list.clear()
            try:
                for child in self.pic_root[self.agent_list.index(self.agent.get())][map_list.index(self.maps.get())][
                    self.side_list.index(self.playing_side.get())]:
                    self.spot_list.append(child.get('name'))
            except:
                self.spot_list.clear()

            haselements = False
            if len(self.spot_list) > 0:
                haselements = True
            refresh_spot(haselements)

        updatespot_list()
        self.maps.trace("w", updatespot_list)
        self.agent.trace("w", updatespot_list)
        self.playing_side.trace("w", updatespot_list)
        self.spot.trace("w", refresh_pic_list)

        self.playing_side.set("Attacker")
        self.agent.set(agent_list[0])
        self.maps.set(map_list[0])
        self.agent_selection = tk.OptionMenu(self.selection_frame, self.agent, *agent_list)
        self.map_selection = tk.OptionMenu(self.selection_frame, self.maps, *map_list)
        self.side_selection = tk.OptionMenu(self.selection_frame, self.playing_side, "Attacker", "Defender")
        self.agent_selection.grid(row=0, column=0)
        self.map_selection.grid(row=0, column=1)
        self.side_selection.grid(row=0, column=2)
        self.spot_selection.grid(row=0, column=3)
        self.pic_selection.grid(row=0, column=4)

        # Make input for spot name
        def add_spot_picture(event=None):
            in_xml = False
            spot_name = self.curr_pic.get()
            self.input.delete(0, 'end')
            #Redundant: Keep for now.
            # Get all pictures in directory
            orig_path = os.getcwd()
            os.chdir(self.picture_directory + "\\maps\\" + self.maps.get() + "\\")
            folder_pictures = glob.glob("*.*")
            os.chdir(orig_path)
            # Get all pictures in xml document
            xml_pictures = self.pic_root[agent_list.index(self.agent.get())][map_list.index(self.maps.get())][
                    self.side_list.index(self.playing_side.get())][self.spot_list.index(self.spot.get())]
            # Check if picture exists already in xml w/ given combination
            for child in xml_pictures:
                if child.text == spot_name:
                    in_xml = True

            if (spot_name in folder_pictures) and not in_xml:
                picture_name = ET.SubElement(xml_pictures, "Picture")
                picture_name.text = spot_name
                print(spot_name + " added.")
                xml_tree.write("../pictures/config.xml", encoding='utf8', pretty_print=True, xml_declaration=True)
            elif spot_name not in folder_pictures:
                print("Error: Picture does not exist in folder.")
            else:
                print("Picture already exists in configuration.")
            refresh_pic_list()

        self.add_button = tk.Button(self.selection_frame, text="Add", command=add_spot_picture)
        self.add_button.grid(row=1)
        self.input = tk.Entry(self.selection_frame)
        self.input.grid(row=0, column=5)

    # Function called by tab controller to update xml when switched to this tab
    def update_xml(self, xml_tree):
        self.pic_root = xml_tree.getroot()
        self.refresh_pic_list()
        print("ADD WIN")

    def refresh_pic_list(self):
        try:
            # Get list of all pictures in xml w/ given combo
            raw_xml_pics = self.pic_root[self.agent_list.index(self.agent.get())][self.map_list.index(self.maps.get())][
                self.side_list.index(self.playing_side.get())][self.spot_list.index(self.spot.get())]
            xml_pictures = []
            for child in raw_xml_pics:
                xml_pictures.append(child.text)
            # Get all pictures in directory
            orig_path = os.getcwd()
            os.chdir(self.picture_directory + "\\maps\\" + self.maps.get() + "\\")
            folder_pictures = glob.glob("*.*")
            os.chdir(orig_path)
            # Find all unused pictures
            self.pic_list = list(set(folder_pictures) - set(xml_pictures))
            if len(self.pic_list) != 0:
                self.curr_pic.set(self.pic_list[0])
            else:
                self.curr_pic.set("No pictures found")
            self.pic_selection["menu"].delete(0, "end")
            for new_pic in self.pic_list:
                self.pic_selection["menu"].add_command(label=new_pic, command=tk._setit(self.curr_pic, new_pic))
        except ValueError:
            self.curr_pic.set("No pictures found.")
            self.pic_selection["menu"].delete(0, "end")

class remove_window():
    def __init__(self, master, agent_list, map_list, xml_tree):
        self.master = master
        self.side_list = ["Attacker", "Defender"]
        self.pic_root = xml_tree.getroot()
        self.picture_directory = get_picdir()
        self.agent_list = agent_list
        self.map_list = map_list
        self.xml_tree = xml_tree

        self.selection_frame = tk.Frame(master, width=400, height=20, pady=40)
        self.selection_frame.pack()
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.agent = tk.StringVar()
        self.maps = tk.StringVar()
        self.playing_side = tk.StringVar()

        self.spot = tk.StringVar()
        self.spot_list = ["Choose a spot"]
        self.spot_selection = tk.OptionMenu(self.selection_frame, self.spot, *self.spot_list)
        self.curr_pic = tk.StringVar()
        self.pic_list = ["Choose a picture."]
        self.pic_selection = tk.OptionMenu(self.selection_frame, self.curr_pic, *self.pic_list)

        def refresh_pic_list(*args):
            # Get list of all pictures in xml w/ given combo
            try:
                xml_pictures = self.pic_root[agent_list.index(self.agent.get())][map_list.index(self.maps.get())][
                    self.side_list.index(self.playing_side.get())][self.spot_list.index(self.spot.get())]
                self.pic_list = []
                for child in xml_pictures:
                    self.pic_list.append(child.text)
                if len(self.pic_list) != 0:
                    self.curr_pic.set(self.pic_list[0])
                else:
                    self.curr_pic.set("No pictures found")
                self.pic_selection["menu"].delete(0, "end")
                for new_pic in self.pic_list:
                    self.pic_selection["menu"].add_command(label=new_pic, command=tk._setit(self.curr_pic, new_pic))
            except ValueError:
                self.curr_pic.set("No pictures found.")
                self.pic_selection["menu"].delete(0, "end")

            #Temporary solution to allow updates if picture added in add_window()
            # self.pic_root = xml_tree.getroot()
            # self.master.after(1000, refresh_pic_list)

        def refresh_spot(haselements):
            if haselements:
                self.spot.set(self.spot_list[0])
            else:
                self.spot.set("No lineups found")
            self.spot_selection["menu"].delete(0, "end")
            for new_spot in self.spot_list:
                self.spot_selection["menu"].add_command(label=new_spot, command=tk._setit(self.spot, new_spot))
            refresh_pic_list()

        def updatespot_list(*args):
            self.spot_list.clear()
            try:
                for child in self.pic_root[agent_list.index(self.agent.get())][map_list.index(self.maps.get())][
                    self.side_list.index(self.playing_side.get())]:
                    self.spot_list.append(child.get('name'))
            except:
                self.spot_list.clear()

            haselements = False
            if len(self.spot_list) > 0:
                haselements = True
            refresh_spot(haselements)

        updatespot_list()
        self.maps.trace("w", updatespot_list)
        self.agent.trace("w", updatespot_list)
        self.playing_side.trace("w", updatespot_list)
        self.spot.trace("w", refresh_pic_list)

        self.playing_side.set("Attacker")
        self.agent.set(agent_list[0])
        self.maps.set(map_list[0])
        self.agent_selection = tk.OptionMenu(self.selection_frame, self.agent, *agent_list)
        self.map_selection = tk.OptionMenu(self.selection_frame, self.maps, *map_list)
        self.side_selection = tk.OptionMenu(self.selection_frame, self.playing_side, "Attacker", "Defender")
        self.agent_selection.grid(row=0, column=0)
        self.map_selection.grid(row=0, column=1)
        self.side_selection.grid(row=0, column=2)
        self.spot_selection.grid(row=0, column=3)
        self.pic_selection.grid(row=0, column=4)


        # Make input for spot name
        def remove_spot_picture(event=None):
            in_xml = False
            spot_name = self.curr_pic.get()
            # Get all pictures in directory
            orig_path = os.getcwd()
            os.chdir(self.picture_directory + "\\maps\\" + self.maps.get() + "\\")
            folder_pictures = glob.glob("*.*")
            os.chdir(orig_path)
            # Get all pictures in xml document
            xml_pictures = self.pic_root[agent_list.index(self.agent.get())][map_list.index(self.maps.get())][
                self.side_list.index(self.playing_side.get())][self.spot_list.index(self.spot.get())]
            # Check if picture exists already in xml w/ given combination
            # Maybe redundant but keep for now
            for child in xml_pictures:
                if child.text == spot_name:
                    xml_pictures.remove(child)
                    print(spot_name + " removed.")
                    xml_tree.write("../pictures/config.xml", encoding='utf8', pretty_print=True, xml_declaration=True)
            refresh_pic_list()


        self.remove_button = tk.Button(self.selection_frame, text="Remove", command=remove_spot_picture)
        self.remove_button.grid(row=1)

    # Function called by tab controller to update xml when switched to this tab
    def update_xml(self, xml_tree):
        self.pic_root = xml_tree.getroot()
        self.refresh_pic_list()
        print("REMOVE WIN")

    def refresh_pic_list(self):
        # Get list of all pictures in xml w/ given combo
        try:
            xml_pictures = self.pic_root[self.agent_list.index(self.agent.get())][self.map_list.index(self.maps.get())][
                self.side_list.index(self.playing_side.get())][self.spot_list.index(self.spot.get())]
            self.pic_list = []
            for child in xml_pictures:
                self.pic_list.append(child.text)
            if len(self.pic_list) != 0:
                self.curr_pic.set(self.pic_list[0])
            else:
                self.curr_pic.set("No pictures found")
            self.pic_selection["menu"].delete(0, "end")
            for new_pic in self.pic_list:
                self.pic_selection["menu"].add_command(label=new_pic, command=tk._setit(self.curr_pic, new_pic))
        except ValueError:
            self.curr_pic.set("No pictures found.")
            self.pic_selection["menu"].delete(0, "end")


def get_picdir():
    inital_path = os.getcwd()
    os.chdir("../pictures/")
    picture_directory = os.getcwd()
    os.chdir(inital_path)
    return picture_directory