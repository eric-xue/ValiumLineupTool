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

        add_window(add_tab, agent_list, map_list, xml_tree)
        remove_window(remove_tab, agent_list, map_list, xml_tree)


        #   Setup selection boxes
        # agent = tk.StringVar()
        # maps = tk.StringVar()
        # playing_side = tk.StringVar()
        #
        # spot = tk.StringVar()
        # spot.set("Choose a spot")
        # self.spot_list = ["Choose a spot"]
        # self.spot_selection = tk.OptionMenu(self.selection_frame, spot, *self.spot_list)
        #
        # def refresh_spot(haselements):
        #     if haselements:
        #         spot.set("Choose a spot")
        #     else:
        #         spot.set("No lineups found")
        #     self.spot_selection["menu"].delete(0, "end")
        #     for new_spot in self.spot_list:
        #         self.spot_selection["menu"].add_command(label=new_spot, command=tk._setit(spot, new_spot))
        #     print(self.spot_list)
        #
        # def updatespot_list(*args):
        #     self.spot_list.clear()
        #     try:
        #         for child in pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][
        #             side_list.index(playing_side.get())]:
        #             self.spot_list.append(child.get('name'))
        #     except:
        #         self.spot_list.clear()
        #
        #     haselements = False
        #     if len(self.spot_list) > 0:
        #         haselements = True
        #     refresh_spot(haselements)
        #
        # updatespot_list()
        # maps.trace("w", updatespot_list)
        # agent.trace("w", updatespot_list)
        # playing_side.trace("w", updatespot_list)
        #
        # playing_side.set("Attacker")
        # agent.set(agent_list[0])
        # maps.set(map_list[0])
        # self.agent_selection = tk.OptionMenu(self.selection_frame, agent, *self.agent_list)
        # self.map_selection = tk.OptionMenu(self.selection_frame, maps, *self.map_list)
        # self.side_selection = tk.OptionMenu(self.selection_frame, playing_side, "Attacker", "Defender")
        # self.agent_selection.grid(row=0, column=0)
        # self.map_selection.grid(row=0, column=1)
        # self.side_selection.grid(row=0, column=2)
        # self.spot_selection.grid(row=0, column=3)
        #
        # # Make input for lineup name
        #
        # # Make input for spot name
        # def add_spot_picture(event=None):
        #     spot_name = self.input.get()
        #     self.input.delete(0, 'end')
        #     print(spot.get())
        #
        #     lineup_node = pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][
        #         side_list.index(playing_side.get())][self.spot_list.index(spot.get())]
        #     picture_name = ET.SubElement(lineup_node, "Picture").text = spot_name
        #     xml_tree.write("../pictures/config.xml", encoding='utf8')
        #
        #
        # self.input = tk.Entry(self.selection_frame)
        # self.input.bind('<Return>', add_spot_picture)
        # self.input.grid(row=0,column=4)

        #   Add edit box


        # for child in self.xml_root.findall('Agent'):
        #     name = child.get("name")
        #     if name == "Sova":
        #         self.xml_root.remove(child)
        #         print("Removed")

        # a_l, m_l, s_l = init_lists(xml_tree)
        # print(a_l)
        #
        # xml_tree.write("file_edit.xml", encoding='utf8')

class add_window():
    def __init__(self, master, agent_list, map_list, xml_tree):
        self.master = master
        self.side_list = ["Attacker", "Defender"]
        pic_root = xml_tree.getroot()
        picture_directory = get_picdir()

        self.selection_frame = tk.Frame(master, width=400, height=20, pady=40)
        self.selection_frame.pack()
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        agent = tk.StringVar()
        maps = tk.StringVar()
        playing_side = tk.StringVar()

        spot = tk.StringVar()
        self.spot_list = ["Choose a spot"]
        self.spot_selection = tk.OptionMenu(self.selection_frame, spot, *self.spot_list)

        def refresh_spot(haselements):
            if haselements:
                spot.set(self.spot_list[0])
            else:
                spot.set("No lineups found")
            self.spot_selection["menu"].delete(0, "end")
            for new_spot in self.spot_list:
                self.spot_selection["menu"].add_command(label=new_spot, command=tk._setit(spot, new_spot))
            print(self.spot_list)

        def updatespot_list(*args):
            self.spot_list.clear()
            try:
                for child in pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][
                    self.side_list.index(playing_side.get())]:
                    self.spot_list.append(child.get('name'))
            except:
                self.spot_list.clear()

            haselements = False
            if len(self.spot_list) > 0:
                haselements = True
            refresh_spot(haselements)

        updatespot_list()
        maps.trace("w", updatespot_list)
        agent.trace("w", updatespot_list)
        playing_side.trace("w", updatespot_list)

        playing_side.set("Attacker")
        agent.set(agent_list[0])
        maps.set(map_list[0])
        self.agent_selection = tk.OptionMenu(self.selection_frame, agent, *agent_list)
        self.map_selection = tk.OptionMenu(self.selection_frame, maps, *map_list)
        self.side_selection = tk.OptionMenu(self.selection_frame, playing_side, "Attacker", "Defender")
        self.agent_selection.grid(row=0, column=0)
        self.map_selection.grid(row=0, column=1)
        self.side_selection.grid(row=0, column=2)
        self.spot_selection.grid(row=0, column=3)

        # Make input for spot name
        def add_spot_picture(event=None):
            in_xml = False
            spot_name = self.input.get()
            self.input.delete(0, 'end')
            # Get all pictures in directory
            orig_path = os.getcwd()
            os.chdir(picture_directory + "\\maps\\" + maps.get() + "\\")
            folder_pictures = glob.glob("*.*")
            os.chdir(orig_path)
            # Get all pictures in xml document
            xml_pictures = pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][
                    self.side_list.index(playing_side.get())][self.spot_list.index(spot.get())]
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

        self.add_button = tk.Button(self.selection_frame, text="Add", command=add_spot_picture
                                    )
        self.add_button.grid(row=1)
        self.input = tk.Entry(self.selection_frame)
        self.input.grid(row=0, column=4)

class remove_window():
    def __init__(self, master, agent_list, map_list, xml_tree):
        self.master = master
        self.side_list = ["Attacker", "Defender"]
        pic_root = xml_tree.getroot()
        picture_directory = get_picdir()

        self.selection_frame = tk.Frame(master, width=400, height=20, pady=40)
        self.selection_frame.pack()
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        agent = tk.StringVar()
        maps = tk.StringVar()
        playing_side = tk.StringVar()

        spot = tk.StringVar()
        self.spot_list = ["Choose a spot"]
        self.spot_selection = tk.OptionMenu(self.selection_frame, spot, *self.spot_list)

        def refresh_spot(haselements):
            if haselements:
                spot.set(self.spot_list[0])
            else:
                spot.set("No lineups found")
            self.spot_selection["menu"].delete(0, "end")
            for new_spot in self.spot_list:
                self.spot_selection["menu"].add_command(label=new_spot, command=tk._setit(spot, new_spot))
            print(self.spot_list)

        def updatespot_list(*args):
            self.spot_list.clear()
            try:
                for child in pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][
                    self.side_list.index(playing_side.get())]:
                    self.spot_list.append(child.get('name'))
            except:
                self.spot_list.clear()

            haselements = False
            if len(self.spot_list) > 0:
                haselements = True
            refresh_spot(haselements)

        updatespot_list()
        maps.trace("w", updatespot_list)
        agent.trace("w", updatespot_list)
        playing_side.trace("w", updatespot_list)

        playing_side.set("Attacker")
        agent.set(agent_list[0])
        maps.set(map_list[0])
        self.agent_selection = tk.OptionMenu(self.selection_frame, agent, *agent_list)
        self.map_selection = tk.OptionMenu(self.selection_frame, maps, *map_list)
        self.side_selection = tk.OptionMenu(self.selection_frame, playing_side, "Attacker", "Defender")
        self.agent_selection.grid(row=0, column=0)
        self.map_selection.grid(row=0, column=1)
        self.side_selection.grid(row=0, column=2)
        self.spot_selection.grid(row=0, column=3)

        # Make input for spot name
        def remove_spot_picture(event=None):
            in_xml = False
            spot_name = self.input.get()
            self.input.delete(0, 'end')
            # Get all pictures in directory
            orig_path = os.getcwd()
            os.chdir(picture_directory + "\\maps\\" + maps.get() + "\\")
            folder_pictures = glob.glob("*.*")
            os.chdir(orig_path)
            # Get all pictures in xml document
            xml_pictures = pic_root[agent_list.index(agent.get())][map_list.index(maps.get())][
                self.side_list.index(playing_side.get())][self.spot_list.index(spot.get())]
            # Check if picture exists already in xml w/ given combination
            all_pics = []
            for child in xml_pictures:
                if child.text == spot_name:
                    xml_pictures.remove(child)
                    print(spot_name + " removed.")
                    xml_tree.write("../pictures/config.xml", encoding='utf8', pretty_print=True, xml_declaration=True)
                else:
                    print("NOTHING")
                all_pics.append(child.text)
            print(all_pics)

        self.remove_button = tk.Button(self.selection_frame, text="Remove", command=remove_spot_picture)
        self.remove_button.grid(row=1)
        self.input = tk.Entry(self.selection_frame)
        self.input.grid(row=0, column=4)


def get_picdir():
    inital_path = os.getcwd()
    os.chdir("../pictures/")
    picture_directory = os.getcwd()
    os.chdir(inital_path)
    return picture_directory