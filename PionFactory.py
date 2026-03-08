from Pion import Pion, PionO, PionX, PionVide

class PionFactory:
    @staticmethod
    def create_pion(type):
        if type == "O":
            return PionO()
        elif type == "X":
            return PionX()
        else:
            return PionVide()