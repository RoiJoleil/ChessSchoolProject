
from tkinter import filedialog
from typing import TYPE_CHECKING, Dict
import json
from src.util.dictConverter import GameConverter

class Filemanager:
    def __init__(self):
        pass
    def open_file_dialog():
        filepath = filedialog.askopenfilename(
                                              title="Open Game File",
                                              filetypes=[("json file","*.json")])
        if filepath == None:
            return
        
        try:
            buffer = None
            with open(filepath, mode="r") as file:
                buffer = json.load(file)
            GameConverter.load_save_data(buffer) if buffer else print("ERROR")
        except:
            print("open failed")
        
    def save_file_dialog():
        path_of_file = filedialog.asksaveasfilename(
                                                title="Save Game File",
                                                filetypes=[("json file","*.json")],
                                                defaultextension=".json")
        buffer = GameConverter.construct_save_data()

        if buffer == None:
            return
        try:
            with open(path_of_file, mode="w") as file:
                json.dump(buffer, file)
        except Exception as e:
            print(f"Saving File Failed:\t{repr(e)}")
