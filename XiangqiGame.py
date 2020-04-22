# Author: James Tauzin
# Date: 03/11/2020
# Description: XiangQi game portfolio project


# class wide contract variables using all caps nomenclature to denote that this variable does not change
# this method reduces the possibility of typos in programs, especially when accessing databases or in long programs
STATUS_UNFINISHED = 'UNFINISHED'
STATUS_RED_WINS = 'RED_WON'
STATUS_BLACK_WINS = 'BLACK_WON'
FACTION_RED = 'RED'
FACTION_BLACK = 'BLACK'


class GamePiece:
    """Defines the basic functionality of a game piece"""

    def __init__(self, row, column, faction, game_board, ):
        self._row = row
        self._column = column
        self._faction = faction
        self._game_board = game_board
        self._game_board[row][column] = self
        self._screened_moves = []

    def get_row(self):
        """returns the current row occupied by the piece"""
        return self._row

    def get_column(self):
        """returns the current column occupied by the piece"""
        return self._column

    def get_faction(self):
        """returns the pieces' faction"""
        return self._faction

    def update_position(self, row, column):
        """updates the positional tracking of the piece"""
        game_piece = self._game_board[self._row][self._column]
        self._game_board[self._row][self._column] = ""
        self._row = row
        self._column = column
        self._game_board[self._row][self._column] = game_piece

    def move_out_of_bounds(self, row, column):
        """checks to see if a proposed move is out of bounds"""
        if row > 9 or row < 0 or column > 8 or column < 0:
            return True
        else:
            return False

    def position_contains_ally(self, row, column):
        """checks to see if position is occupied by an ally piece"""
        if self._game_board[row][column] == "":
            return False
        elif self._faction == self._game_board[row][column].get_faction():
            return True
        else:
            return False

    def position_contains_enemy(self, row, column):
        """checks to see if position is occupied by an ally piece"""
        if self._game_board[row][column] == "":
            return False
        elif self._faction != self._game_board[row][column].get_faction():
            return True
        else:
            return False

    def get_title(self):
        """returns the title assigned to the child class"""
        return self._title

    def get_screened_moves(self):
        """returns the list of screened moves"""
        return self._screened_moves

    def set_screened_moves(self, moves_list):
        """updates the potential moves list"""
        self._screened_moves = moves_list


# Note, for all game piece child classes, the method for finding moves is to provide a list of all spaces in the
# objects range, then to delete illegal moves
class General(GamePiece):
    """Class General extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = [[self.get_row() + 1, self.get_column() + 0],
                                 [self.get_row() - 1, self.get_column() + 0],
                                 [self.get_row() + 0, self.get_column() + 1],
                                 [self.get_row() + 0, self.get_column() - 1]]
        self._title = "Gen"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves = [[self.get_row() + 1, self.get_column() + 0],
                                 [self.get_row() - 1, self.get_column() + 0],
                                 [self.get_row() + 0, self.get_column() + 1],
                                 [self.get_row() + 0, self.get_column() - 1]]

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        index = 0
        move_adder = []

        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)
            elif self.position_contains_ally(move[0], move[1]):
                moves_to_remove.append(move)
            # cannot leave palace
            elif self.get_faction() == FACTION_RED:
                if move[0] > 2 or move[1] > 5 or move[1] < 3:
                    moves_to_remove.append(move)

            elif self.get_faction() == FACTION_BLACK:
                if move[0] < 7 or move[1] > 5 or move[1] < 3:
                    moves_to_remove.append(move)

            index += 1

        # add rules for flying general, if a general can see another he/she can capture that opposing general
        unit_count = 0
        enemy_gen_in_column = False
        enemy_gen_position = []
        for row in self._game_board:
            for unit in row:
                if unit != "" and self.get_column() == unit.get_column() and unit != self:
                    unit_count += 1
                    if unit.get_title().lower() == "gen" and self.get_faction() != unit.get_faction():
                        enemy_gen_in_column = True
                        enemy_gen_position = [unit.get_row(), unit.get_column()]
        if enemy_gen_in_column and unit_count == 1:
            move_adder.append(enemy_gen_position)

        for move in moves_to_remove:
            potential_moves.remove(move)
        for move in move_adder:
            potential_moves.append(move)
        return potential_moves


class Guard(GamePiece):
    """Class Guard extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = [[self.get_row() + 1, self.get_column() + 1],
                                 [self.get_row() - 1, self.get_column() - 1],
                                 [self.get_row() + 1, self.get_column() - 1],
                                 [self.get_row() - 1, self.get_column() + 1]]
        self._title = "Grd"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves = [[self.get_row() + 1, self.get_column() + 1],
                                 [self.get_row() - 1, self.get_column() - 1],
                                 [self.get_row() + 1, self.get_column() - 1],
                                 [self.get_row() - 1, self.get_column() + 1]]

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        index = 0
        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)
            elif self.position_contains_ally(move[0], move[1]):
                moves_to_remove.append(move)
            # cannot leave palace
            elif self.get_faction() == FACTION_RED:
                if move[0] > 2 or move[1] > 5 or move[1] < 3:
                    moves_to_remove.append(move)
            elif self.get_faction() == FACTION_BLACK:
                if move[0] < 7 or move[1] > 5 or move[1] < 3:
                    moves_to_remove.append(move)
            index += 1

        for move in moves_to_remove:
            potential_moves.remove(move)
        return potential_moves


class Elephant(GamePiece):
    """Class Elephant extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = [[self.get_row() + 2, self.get_column() + 2],
                                 [self.get_row() - 2, self.get_column() - 2],
                                 [self.get_row() + 2, self.get_column() - 2],
                                 [self.get_row() - 2, self.get_column() + 2]]
        # check zone is a list of position coordinates that an opponent can currently attack
        self._title = "Ele"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves = [[self.get_row() + 2, self.get_column() + 2],
                                 [self.get_row() - 2, self.get_column() - 2],
                                 [self.get_row() + 2, self.get_column() - 2],
                                 [self.get_row() - 2, self.get_column() + 2]]

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        index = 0
        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)
            elif self.position_contains_ally(move[0], move[1]):
                moves_to_remove.append(move)
            # Cannot cross the river
            elif self.get_faction() == FACTION_RED:
                if move[0] > 4:
                    moves_to_remove.append(move)
                else:
                    # check to see if the path is blocked
                    if index == 0:
                        if self._game_board[move[0] - 1][move[1] - 1] != "":
                            moves_to_remove.append(move)
                    elif index == 1:
                        if self._game_board[move[0] + 1][move[1] + 1] != "":
                            moves_to_remove.append(move)
                    elif index == 2:
                        if self._game_board[move[0] - 1][move[1] + 1] != "":
                            moves_to_remove.append(move)
                    elif index == 3:
                        if self._game_board[move[0] + 1][move[1] - 1] != "":
                            moves_to_remove.append(move)
            elif self.get_faction() == FACTION_BLACK:
                if move[0] < 5:
                    moves_to_remove.append(move)
                else:
                    # check to see if the path is blocked
                    if index == 0:
                        if self._game_board[move[0] - 1][move[1] - 1] != "":
                            moves_to_remove.append(move)
                    elif index == 1:
                        if self._game_board[move[0] + 1][move[1] + 1] != "":
                            moves_to_remove.append(move)
                    elif index == 2:
                        if self._game_board[move[0] - 1][move[1] + 1] != "":
                            moves_to_remove.append(move)
                    elif index == 3:
                        if self._game_board[move[0] + 1][move[1] - 1] != "":
                            moves_to_remove.append(move)
            index += 1

        for move in moves_to_remove:
            potential_moves.remove(move)
        return potential_moves


class Horse(GamePiece):
    """Class Horse extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = [[self.get_row() + 2, self.get_column() + 1],
                                 [self.get_row() + 2, self.get_column() - 1],
                                 [self.get_row() - 2, self.get_column() + 1],
                                 [self.get_row() - 2, self.get_column() - 1],
                                 [self.get_row() + 1, self.get_column() + 2],
                                 [self.get_row() - 1, self.get_column() + 2],
                                 [self.get_row() + 1, self.get_column() - 2],
                                 [self.get_row() - 1, self.get_column() - 2]]
        self._title = "Hrs"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves = [[self.get_row() + 2, self.get_column() + 1],
                                 [self.get_row() + 2, self.get_column() - 1],
                                 [self.get_row() - 2, self.get_column() + 1],
                                 [self.get_row() - 2, self.get_column() - 1],
                                 [self.get_row() + 1, self.get_column() + 2],
                                 [self.get_row() - 1, self.get_column() + 2],
                                 [self.get_row() + 1, self.get_column() - 2],
                                 [self.get_row() - 1, self.get_column() - 2]]

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        index = 0
        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)
            elif self.position_contains_ally(move[0], move[1]):
                moves_to_remove.append(move)
            # Can be blocked by other units
            else:
                # check to see if the path is blocked
                if (index == 0 or index == 1) and move[0] < 9:
                    if self._game_board[self.get_row() + 1][self.get_column()] != "":
                        moves_to_remove.append(move)
                elif (index == 2 or index == 3) and move[0] > 0:
                    if self._game_board[self.get_row() - 1][self.get_column()] != "":
                        moves_to_remove.append(move)
                elif (index == 4 or index == 5) and move[1] > 0:
                    if self._game_board[self.get_row()][self.get_column() + 1] != "":
                        moves_to_remove.append(move)
                elif (index == 6 or index == 7) and move[1] < 8:
                    if self._game_board[self.get_row()][self.get_column() - 1] != "":
                        moves_to_remove.append(move)
            index += 1

        for move in moves_to_remove:
            potential_moves.remove(move)
        return potential_moves


class Chariot(GamePiece):
    """Class Chariot extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = []
        # for simplicity, fill moves with a loop since there are many possible
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() + row_num, self.get_column()])
            row_num += 1
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() - row_num, self.get_column()])
            row_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() + column_num])
            column_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() - column_num])
            column_num += 1

        self._title = "Chr"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves.clear()
        # for simplicity, fill moves with a loop since there are many possible
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() + row_num, self.get_column()])
            row_num += 1
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() - row_num, self.get_column()])
            row_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() + column_num])
            column_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() - column_num])
            column_num += 1

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        index = 0
        current_column = self.get_column()
        current_row = self.get_row()
        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)

            # if position contains ally, delete all moves behind that position
            elif self.position_contains_ally(move[0], move[1]):
                if current_row < move[0]:
                    row_num = move[0]
                    while row_num <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num += 1

                elif current_row > move[0]:
                    row_num = move[0]
                    while abs(row_num) <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num -= 1

                elif current_column < move[1]:
                    column_num = move[1]
                    while column_num <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num += 1

                elif current_column > move[1]:
                    column_num = move[1]
                    while abs(column_num) <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num -= 1

            elif self.position_contains_enemy(move[0], move[1]):
                # same as before but plus one because it can capture the opponent, just not move past the opponent
                if current_row < move[0]:
                    row_num = move[0] + 1
                    while row_num <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num += 1

                elif current_row > move[0]:
                    row_num = move[0] - 1
                    while abs(row_num) <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num -= 1

                elif current_column < move[1]:
                    column_num = move[1] + 1
                    while column_num <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num += 1

                elif current_column > move[1]:
                    column_num = move[1] - 1
                    while abs(column_num) <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num -= 1

            index += 1
        for move in moves_to_remove:
            if move in potential_moves:
                potential_moves.remove(move)
        return potential_moves


class Cannon(GamePiece):
    """Class Cannon extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = []
        # for simplicity, fill moves with a loop since there are many possible
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() + row_num, self.get_column()])
            row_num += 1
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() - row_num, self.get_column()])
            row_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() + column_num])
            column_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() - column_num])
            column_num += 1

        self._title = "Can"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves.clear()
        # for simplicity, fill moves with a loop since there are many possible
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() + row_num, self.get_column()])
            row_num += 1
        row_num = 1
        while row_num <= len(self._game_board):
            self._potential_moves.append([self.get_row() - row_num, self.get_column()])
            row_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() + column_num])
            column_num += 1
        column_num = 1
        while column_num <= len(self._game_board[0]):
            self._potential_moves.append([self.get_row(), self.get_column() - column_num])
            column_num += 1

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        # for enemies that have one unit between them and the cannon,
        # grant that move back for a capture, otherwise behave as the Chariot
        moves_to_grant = []
        index = 0
        current_column = self.get_column()
        current_row = self.get_row()
        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)

            elif self.position_contains_ally(move[0], move[1]):
                if current_row < move[0]:
                    row_num = move[0]
                    while row_num <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num += 1

                elif current_row > move[0]:
                    row_num = move[0]
                    while abs(row_num) <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num -= 1

                elif current_column < move[1]:
                    column_num = move[1]
                    while column_num <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num += 1

                elif current_column > move[1]:
                    column_num = move[1]
                    while abs(column_num) <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num -= 1

            elif self.position_contains_enemy(move[0], move[1]):
                # Cannot capture like the rook, so no plus one. Instead capture move is added back if conditions are met
                if current_row < move[0]:
                    row_index = move[0] - 1
                    unit_count = 0
                    while row_index > current_row:
                        if self._game_board[row_index][current_column] != "":
                            unit_count += 1
                        row_index -= 1
                    if unit_count == 1:
                        moves_to_grant.append(move)

                    row_num = move[0]
                    while row_num <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num += 1

                # if move contains enemy and the player's unit is in a greater number column than the enemy,
                # scan the spaces between to count how many units there are. If only one, add that move back to
                # possible move list
                elif current_row > move[0]:
                    row_index = move[0] + 1
                    unit_count = 0
                    while row_index < current_row:
                        if self._game_board[row_index][current_column] != "":
                            unit_count += 1
                        row_index += 1
                    if unit_count == 1:
                        moves_to_grant.append(move)
                    # scan like normal, removing all moves that lay behind the occupied space
                    row_num = move[0]
                    while abs(row_num) <= len(self._game_board):
                        next_move = [row_num, current_column]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        row_num -= 1

                elif current_column < move[1]:
                    column_index = move[1] - 1
                    unit_count = 0
                    while column_index > current_column:
                        if self._game_board[current_row][column_index] != "":
                            unit_count += 1
                        column_index -= 1
                    if unit_count == 1:
                        moves_to_grant.append(move)

                    column_num = move[1]
                    while column_num <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num += 1

                elif current_column > move[1]:
                    column_index = move[1] + 1
                    unit_count = 0
                    while column_index < current_column:
                        if self._game_board[current_row][column_index] != "":
                            unit_count += 1
                        column_index += 1
                    if unit_count == 1:
                        moves_to_grant.append(move)

                    column_num = move[1]
                    while abs(column_num) <= len(self._game_board[1]):
                        next_move = [current_row, column_num]
                        if next_move not in moves_to_remove:
                            moves_to_remove.append(next_move)
                        column_num -= 1

            index += 1
        for move in moves_to_remove:
            if move in potential_moves:
                potential_moves.remove(move)
        for move in moves_to_grant:
            potential_moves.append(move)
        return potential_moves


class Pawn(GamePiece):
    """Class Pawn extended from game piece which defines specific moves for this piece"""

    def __init__(self, row, column, faction, game_board):
        """Overrides the init method for special moves for the piece"""
        super().__init__(row, column, faction, game_board)
        self._potential_moves = [[self.get_row() + 1, self.get_column() + 0],
                                 [self.get_row() - 1, self.get_column() + 0],
                                 [self.get_row() + 0, self.get_column() + 1],
                                 [self.get_row() + 0, self.get_column() - 1]]
        # check zone is a list of position coordinates that an opponent can currently attack
        self._title = "Paw"

    def update_position(self, row, column):
        """runs the parent update method and updates the unique move list for the piece"""
        super().update_position(row, column)
        self._potential_moves = [[self.get_row() + 1, self.get_column() + 0],
                                 [self.get_row() - 1, self.get_column() + 0],
                                 [self.get_row() + 0, self.get_column() + 1],
                                 [self.get_row() + 0, self.get_column() - 1]]

    def get_potential_moves(self):
        """Returns a list of potential moves, removing items what will not be valid"""
        # Save to separate list object, so we don't modify our moves list
        potential_moves = list(self._potential_moves)
        moves_to_remove = []
        index = 0
        while index < len(potential_moves):
            move = potential_moves[index]
            if self.move_out_of_bounds(move[0], move[1]):
                moves_to_remove.append(move)
            elif self.position_contains_ally(move[0], move[1]):
                moves_to_remove.append(move)
            # cannot go backwards and can only move sideways if across the river
            elif self.get_faction() == FACTION_RED:
                if move[0] < self.get_row():
                    moves_to_remove.append(move)
                    # can only move sideways if across the river
                if self.get_row() < 5 and self.get_column() < move[1] or move[1] < self.get_column():
                    moves_to_remove.append(move)
            elif self.get_faction() == FACTION_BLACK:
                if move[0] > self.get_row():
                    moves_to_remove.append(move)
                if self.get_row() >= 5 and self.get_column() < move[1] or move[1] < self.get_column():
                    moves_to_remove.append(move)
            index += 1
        for move in moves_to_remove:
            potential_moves.remove(move)
        return potential_moves


class XiangqiGame:
    """Xiangqui game class"""

    def __init__(self):
        """Initializes the game board"""
        # 10 rows by 9 columns
        self._game_board = [["", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", ""]]

        self._game_state = STATUS_UNFINISHED
        self._turn = FACTION_RED

        # We dont need to save these to a variable, but it helps visualize what we are creating
        red_general = General(0, 4, FACTION_RED, self._game_board)
        black_general = General(9, 4, FACTION_BLACK, self._game_board)
        red_guard1 = Guard(0, 3, FACTION_RED, self._game_board)
        red_guard2 = Guard(0, 5, FACTION_RED, self._game_board)
        black_guard1 = Guard(9, 3, FACTION_BLACK, self._game_board)
        black_guard2 = Guard(9, 5, FACTION_BLACK, self._game_board)
        red_elep1 = Elephant(0, 6, FACTION_RED, self._game_board)
        red_elep2 = Elephant(0, 2, FACTION_RED, self._game_board)
        black_elep1 = Elephant(9, 6, FACTION_BLACK, self._game_board)
        black_elep2 = Elephant(9, 2, FACTION_BLACK, self._game_board)
        red_horse1 = Horse(0, 7, FACTION_RED, self._game_board)
        red_horse2 = Horse(0, 1, FACTION_RED, self._game_board)
        black_horse1 = Horse(9, 7, FACTION_BLACK, self._game_board)
        black_horse2 = Horse(9, 1, FACTION_BLACK, self._game_board)
        red_chariot1 = Chariot(0, 8, FACTION_RED, self._game_board)
        red_chariot2 = Chariot(0, 0, FACTION_RED, self._game_board)
        black_chariot1 = Chariot(9, 8, FACTION_BLACK, self._game_board)
        black_chariot2 = Chariot(9, 0, FACTION_BLACK, self._game_board)
        red_cannon1 = Cannon(2, 1, FACTION_RED, self._game_board)
        red_cannon2 = Cannon(2, 7, FACTION_RED, self._game_board)
        black_cannon1 = Cannon(7, 1, FACTION_BLACK, self._game_board)
        black_cannon2 = Cannon(7, 7, FACTION_BLACK, self._game_board)
        red_pawn1 = Pawn(3, 0, FACTION_RED, self._game_board)
        red_pawn2 = Pawn(3, 2, FACTION_RED, self._game_board)
        red_pawn3 = Pawn(3, 4, FACTION_RED, self._game_board)
        red_pawn4 = Pawn(3, 6, FACTION_RED, self._game_board)
        red_pawn5 = Pawn(3, 8, FACTION_RED, self._game_board)
        black_pawn1 = Pawn(6, 0, FACTION_BLACK, self._game_board)
        black_pawn2 = Pawn(6, 2, FACTION_BLACK, self._game_board)
        black_pawn3 = Pawn(6, 4, FACTION_BLACK, self._game_board)
        black_pawn4 = Pawn(6, 6, FACTION_BLACK, self._game_board)
        black_pawn5 = Pawn(6, 8, FACTION_BLACK, self._game_board)

    def get_board(self):
        """Returns the game board"""
        return self._game_board

    def get_game_state(self):
        """Returns the current game state"""
        return self._game_state

    def is_in_check(self, faction):
        """returns true for input 'red' or input 'black' if either faction's general is in check"""
        general_position = []
        if faction == 'black':

            # find black general's position
            black_units = self.get_faction_units(FACTION_BLACK)
            for unit in black_units:
                if unit.get_title().lower() == "gen":
                    general_position.append(unit.get_row())
                    general_position.append(unit.get_column())

            # update screened moves list for red
            self.screen_moves(self._game_board, FACTION_RED)

            # search screened moves for valid moves that can take the opponent's general
            red_units = self.get_faction_units(FACTION_RED)
            for unit in red_units:
                potential_moves = unit.get_screened_moves()
                if general_position in potential_moves:
                    return True
            return False

        elif faction == 'red':

            # find red general's position
            red_units = self.get_faction_units(FACTION_RED)
            for unit in red_units:
                if unit.get_title().lower() == "gen":
                    general_position.append(unit.get_row())
                    general_position.append(unit.get_column())

            # update screened moves list for black
            self.screen_moves(self._game_board, FACTION_BLACK)

            # search screened moves for valid moves that can take the opponent's general
            black_units = self.get_faction_units(FACTION_BLACK)
            for unit in black_units:
                potential_moves = unit.get_screened_moves()
                if general_position in potential_moves:
                    return True
            return False
        else:
            print("Invalid input: please enter 'red' or 'black'")

    def get_faction_units(self, faction):
        """returns a list of the units based on faction"""
        if faction == FACTION_BLACK:
            black_units = []
            for row in self._game_board:
                for unit in row:
                    if unit != "":
                        if unit.get_faction() == FACTION_BLACK:
                            black_units.append(unit)
            return black_units
        elif faction == FACTION_RED:
            red_units = []
            for row in self._game_board:
                for unit in row:
                    if unit != "":
                        if unit.get_faction() == FACTION_RED:
                            red_units.append(unit)
            return red_units

    def get_screened_moves_list(self, unit_list):
        """returns a list of raw screened moves for all units in the input unit list"""
        move_list = []
        for unit in unit_list:
            move_list.append(unit.get_screened_moves())
        return move_list

    def translate_coord(self, coord):
        """translates a coordinate from algebraic notation to usable list coord format"""
        letter_key = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        coord = coord.strip()
        if len(coord) > 3 or len(coord) < 2:
            print("Coordinate " + coord + " invalid. Please try again")
            return None
        elif len(coord) == 3 and int(coord[1:3]) > 10 or int(coord[1]) < 1:
            print("Coordinate " + coord + " invalid. Please try again")
            return None
        elif len(coord) == 2 and int(coord[1]) < 1:
            print("Coordinate " + coord + " invalid. Please try again")
            return None
        else:
            column_string = str(coord[0]).lower()
            try:
                row_string = ""
                if len(coord) == 3:
                    row_string = coord[1:3]
                else:
                    row_string = coord[1]
                row_val = int(row_string) - 1
            except ValueError:
                print("Coordinate " + coord + " invalid. Please try again")
                return None
            if column_string not in letter_key:
                print("Coordinate " + coord + " invalid. Please try again")
                return None
            else:
                column_val = letter_key.index(column_string)
                move = [row_val, column_val]
                return move

    def screen_moves(self, game_board, faction):
        """scans the game board for higher logic illegal moves for a specific faction,
         such as moves that will cause the player to be in check, or stay in check"""
        test_board = list(game_board)
        # create a test board for testing of possible moves without using the real board (for safety)
        red_units = []
        black_units = []

        # Testing Red Pieces
        if faction == FACTION_RED:
            for row in test_board:
                for unit in row:
                    if unit != "":
                        if unit.get_faction() == FACTION_RED:
                            red_units.append(unit)
            general_position = []
            for unit in red_units:
                if unit.get_title().lower() == "gen":
                    general_position.append(unit.get_row())
                    general_position.append(unit.get_column())
            # test all possible moves for legality
            for red_unit in red_units:
                potential_moves = red_unit.get_potential_moves()
                screened_moves = list(potential_moves)
                original_position = [red_unit.get_row(), red_unit.get_column()]
                for move in potential_moves:
                    temp_black_piece = test_board[move[0]][move[1]]
                    red_unit.update_position(move[0], move[1])
                    if red_unit.get_title().lower() == "gen":
                        general_position[0] = red_unit.get_row()
                        general_position[1] = red_unit.get_column()
                    for row in test_board:
                        for black_unit in row:
                            if black_unit != "":
                                if black_unit.get_faction() == FACTION_BLACK:
                                    black_units.append(black_unit)
                    for game_piece in black_units:
                        moves_list = game_piece.get_potential_moves()
                        if general_position in moves_list and move in screened_moves:
                            screened_moves.remove(move)
                    # reset the board after the test
                    red_unit.update_position(original_position[0], original_position[1])
                    if red_unit.get_title().lower() == "gen":
                        general_position[0] = red_unit.get_row()
                        general_position[1] = red_unit.get_column()
                    if temp_black_piece != "":
                        test_board[move[0]][move[1]] = temp_black_piece
                # sets the screened moves of each piece based on if that move would put, or leave the general in check
                self._game_board[original_position[0]][original_position[1]].set_screened_moves(screened_moves)

        # Testing Black Pieces
        if faction == FACTION_BLACK:
            for row in test_board:
                for unit in row:
                    if unit != "":
                        if unit.get_faction() == FACTION_BLACK:
                            black_units.append(unit)
            general_position = []
            for unit in black_units:
                if unit.get_title().lower() == "gen":
                    general_position.append(unit.get_row())
                    general_position.append(unit.get_column())
            # test all possible moves for legality
            for black_unit in black_units:
                potential_moves = black_unit.get_potential_moves()
                screened_moves = list(potential_moves)
                original_position = [black_unit.get_row(), black_unit.get_column()]
                for move in potential_moves:
                    temp_red_piece = test_board[move[0]][move[1]]
                    black_unit.update_position(move[0], move[1])
                    if black_unit.get_title().lower() == "gen":
                        general_position[0] = black_unit.get_row()
                        general_position[1] = black_unit.get_column()
                    for row in test_board:
                        for red_unit in row:
                            if red_unit != "":
                                if red_unit.get_faction() == FACTION_RED:
                                    red_units.append(red_unit)
                    for game_piece in red_units:
                        moves_list = game_piece.get_potential_moves()
                        if general_position in moves_list and move in screened_moves:
                            screened_moves.remove(move)
                    # reset the board after the test
                    black_unit.update_position(original_position[0], original_position[1])
                    if black_unit.get_title().lower() == "gen":
                        general_position[0] = black_unit.get_row()
                        general_position[1] = black_unit.get_column()
                    if temp_red_piece != "":
                        test_board[move[0]][move[1]] = temp_red_piece
                # sets the screened moves of each piece based on if that move would put, or leave the general in check
                self._game_board[original_position[0]][original_position[1]].set_screened_moves(screened_moves)

    def make_move(self, starting_string, move_to_string):
        """Updates the gameplay and moves the game pieces by using 2 input strings as coordinates, the first string is
         the starting position of the unit, the last string is the desired position"""
        starting_move = self.translate_coord(starting_string)
        finishing_move = self.translate_coord(move_to_string)

        # screen moves to ensure potential moves don't cause a check, or to find out if the game is
        # checkmate or a stalemate
        self.screen_moves(self._game_board, FACTION_RED)
        self.screen_moves(self._game_board, FACTION_BLACK)

        # check for invalid input
        if starting_move is None or finishing_move is None:
            print("invalid starting or ending coordinate")
            return False
        elif self._game_board[starting_move[0]][starting_move[1]] == "":
            print("No unit detected")
            return False
        elif self._game_board[starting_move[0]][starting_move[1]].get_faction() != self._turn:
            print("Error: it is not that player's turn, please select another unit")
            return False
        elif self._game_state != STATUS_UNFINISHED:
            print("Error: This game has been completed")
            return False

        # else, make sure that the move is achievable by that unit, and if so, update the position
        else:
            selected_unit = self._game_board[starting_move[0]][starting_move[1]]
            selected_faction = selected_unit.get_faction()
            if finishing_move not in selected_unit.get_screened_moves():
                print("Error: that move is not valid, check your move and/or ensure your"
                      " general is not in check after this move")
                return False
            else:
                selected_unit.update_position(finishing_move[0], finishing_move[1])
                self._game_board[starting_move[0]][starting_move[1]] = ""

                # Update the players turn & scan for check, checkmate, or stalemate conditions
                if selected_faction == FACTION_RED:
                    self._turn = FACTION_BLACK
                    if self.is_in_check('black'):
                        print("Black is in check")
                        self.screen_moves(self._game_board, FACTION_BLACK)
                        black_units = self.get_faction_units(FACTION_BLACK)
                        black_moves = self.get_screened_moves_list(black_units)
                        available_moves = 0
                        for item in black_moves:
                            if len(item) > 0:
                                available_moves += 1
                        if available_moves == 0:
                            print("Checkmate! Red Wins")
                            self._game_state = STATUS_RED_WINS
                        else:
                            print("Black's Turn!")
                    else:
                        self.screen_moves(self._game_board, FACTION_BLACK)
                        black_units = self.get_faction_units(FACTION_BLACK)
                        black_moves = self.get_screened_moves_list(black_units)
                        available_moves = 0
                        for item in black_moves:
                            if len(item) > 0:
                                available_moves += 1
                        if available_moves == 0:
                            print("Stalemate! Red Wins")
                            self._game_state = STATUS_RED_WINS
                        else:
                            print("Black's Turn!")

                else:
                    self._turn = FACTION_RED
                    if self.is_in_check('red'):
                        print("red is in check")
                        self.screen_moves(self._game_board, FACTION_RED)
                        red_units = self.get_faction_units(FACTION_RED)
                        red_moves = self.get_screened_moves_list(red_units)
                        available_moves = 0
                        for item in red_moves:
                            if len(item) > 0:
                                available_moves += 1
                        if available_moves == 0:
                            print("Checkmate! Black Wins")
                            self._game_state = STATUS_BLACK_WINS
                        else:
                            print("Red's Turn!")
                    else:
                        self.screen_moves(self._game_board, FACTION_RED)
                        red_units = self.get_faction_units(FACTION_RED)
                        red_moves = self.get_screened_moves_list(red_units)
                        available_moves = 0
                        for item in red_moves:
                            if len(item) > 0:
                                available_moves += 1
                        if available_moves == 0:
                            print("Stalemate! Black Wins")
                            self._game_state = STATUS_BLACK_WINS
                        else:
                            print("Red's Turn!")
                return True


def print_board(game_board):
    """prints the game board and all pieces in their current position"""
    letter_key = ["-", "  a   ", "  b   ", "  c   ", "  d   ", "  e   ", "  f   ", "  g   ", "  h  ", "  i  "]
    print(letter_key)
    counter = 1
    river_made = False
    for row in game_board:
        print_list = [counter]
        if counter == 6 and not river_made:
            river = ["≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋"]
            print(river)
            river_made = True
        for column in row:
            if column == "":
                column = "______"
            else:
                fac_str = column.get_faction()
                if column.get_faction() == FACTION_BLACK:
                    fac_str = "BLK"
                column = column.get_title() + fac_str
            print_list.append(column)
        counter += 1
        print(print_list)


def main():
    """test code"""
    # Simple game loop for testing. Have fun!
    xiangqiGame = XiangqiGame()
    print("RED GOES FIRST!")
    while xiangqiGame.get_game_state() == STATUS_UNFINISHED:
        if xiangqiGame.is_in_check('red'):
            print("RED IS IN CHECK")
        elif xiangqiGame.is_in_check('black'):
            print("BLACK IS IN CHECK")
        print_board(xiangqiGame.get_board())
        selected_unit = input("please select a unit to move: ")
        move_coordinate = input("please select a place to move that unit: ")
        print(xiangqiGame.make_move(selected_unit, move_coordinate))


if __name__ == '__main__':
    main()
