
from tkinter import filedialog
from typing import TYPE_CHECKING, Dict
import json

class Convert:
    def tupleKeyDict_to_intKeyDict(tDict:Dict[tuple, object], ) -> Dict[int, object]:
        if tDict == None:
            return None
        result = {}
        for ele_key in tDict:
            result[ele_key[0] + ele_key[1] * 8] = tDict[ele_key]
        return result
    def intKeyDict_to_tupleKeyDict(iDict:Dict[int, object], ) -> Dict[tuple, object]:
        if iDict == None:
            return None
        result = {}
        for ele_key in iDict:
            key = int(ele_key)            
            result[(key % 8, key // 8)] = iDict[ele_key]
        return result

class Filemanager:
    def __init__(self):
        pass
    def open_file_dialog():
        filepath = filedialog.askopenfilename(
                                              title="Open Game File",
                                              filetypes=[("json file","*.json")])
        try:
            buffer = None
            with open(filepath, mode="r") as file:
                buffer = json.load(file)
            return Convert.intKeyDict_to_tupleKeyDict(buffer)
        except:
            return None
        
    def save_file_dialog(dict:Dict):
        filepath = filedialog.asksaveasfilename(
                                                title="Save Game File",
                                                filetypes=[("json file","*.json")],
                                                defaultextension=".json")
        try:
            buffer = Convert.tupleKeyDict_to_intKeyDict(dict)
            with open(filepath, mode="w") as file:
                json.dump(buffer, file)
        except:
            pass