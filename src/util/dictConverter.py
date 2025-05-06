from src.chess import board
from src.chess import cell

class GameConverter:
    def Board_to_HexString():
        result = ""
        for i in range(64):
            temp = cell.get_cell((i % 8, i // 8)).piece
            result += (hex((temp.identity)).removeprefix("0x") if temp else "0")
        return result
    
    def HexString_to_Board(hexString:str):
        for i in range(64):
            id = int(hexString, base=16)
            temp = cell.get_cell((i % 8, i // 8))
            temp.set_piece(temp, id // 8)
        
    def construct_save_data():
        result = {
            "current_turn" : board.get_player_turn(),
            "board" : GameConverter.Board_to_HexString()
        }
        return result
    
    def load_save_data(data:dict):
        GameConverter.HexString_to_Board(data["board"])
        board.set_player_turn(data["current_turn"])