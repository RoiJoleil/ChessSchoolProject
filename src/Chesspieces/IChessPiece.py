from abc import ABC, abstractmethod

class IChessPieces:
    @abstractmethod
    def move(posX:int, posY:int):
        pass