class Pion:
    def __init__(self):
        pass

    def symbol(self):
        return " "

    def clone(self):
        raise NotImplementedError()


class PionVide(Pion):
    def symbol(self):
        return " "

    def clone(self):
        return PionVide()


class PionO(Pion):
    def symbol(self):
        return "O"

    def clone(self):
        return PionO()

class PionX(Pion):
    def symbol(self):
        return "X"

    def clone(self):
        return PionX()
