import GameConfig
from PionFactory import PionFactory
import copy

class Plateau:
    def __init__(self):
        self.grid = [[PionFactory.create_pion(" ") for _ in range(GameConfig.TAILLE_PLATEAU)] for _ in range(GameConfig.TAILLE_PLATEAU)]

    def place_pion(self, x, y, pion):
        self.grid[x][y] = pion

    def get_pion(self, x, y):
        return self.grid[x][y]

    def shift_insert(self, direction, x, y, pion):
        placement_x = 0
        placement_y = 0

        if direction == "up":
            for row in range(x, 0, -1):
                self.grid[row][y] = self.grid[row - 1][y]
            placement_x = 0
            placement_y = y

        elif direction == "down":
            for row in range(x, len(self.grid) - 1):
                self.grid[row][y] = self.grid[row + 1][y]
            placement_x = len(self.grid) - 1
            placement_y = y

        elif direction == "left":
            for col in range(y, 0, -1):
                self.grid[x][col] = self.grid[x][col - 1]
            placement_x = x
            placement_y = 0

        elif direction == "right":
            for col in range(y, len(self.grid[x]) - 1):
                self.grid[x][col] = self.grid[x][col + 1]
            placement_x = x
            placement_y = len(self.grid[x]) - 1
            
        self.place_pion(placement_x, placement_y, pion)

    def clone(self):
        new_plateau = Plateau()
        for i in range(GameConfig.TAILLE_PLATEAU):
            for j in range(GameConfig.TAILLE_PLATEAU):
                new_plateau.grid[i][j] = self.grid[i][j].clone()
        return new_plateau
