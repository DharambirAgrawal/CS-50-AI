import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = [[False for _ in range(width)] for _ in range(height)]

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # Player hasn't found any mines yet
        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count and self.count != 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        i, j = cell
        for di in range(-1, 2):
            for dj in range(-1, 2):
                ni, nj = i + di, j + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    neighbor = (ni, nj)
                    if neighbor != cell:
                        if neighbor in self.mines:
                            count -= 1
                        elif neighbor not in self.safes:
                            neighbors.add(neighbor)

        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)
        self.update_knowledge()
        self.infer_new_sentences()

    def update_knowledge(self):
        changed = True
        while changed:
            changed = False
            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes |= sentence.known_safes()
                mines |= sentence.known_mines()

            if safes:
                changed = True
                for cell in safes:
                    self.mark_safe(cell)

            if mines:
                changed = True
                for cell in mines:
                    self.mark_mine(cell)

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

    def infer_new_sentences(self):
        new_sentences = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2 or not s1.cells or not s2.cells:
                    continue
                if s1.cells.issubset(s2.cells):
                    diff_cells = s2.cells - s1.cells
                    diff_count = s2.count - s1.count
                    new_sentence = Sentence(diff_cells, diff_count)
                    if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                        new_sentences.append(new_sentence)
        self.knowledge.extend(new_sentences)
        self.update_knowledge()

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        all_cells = set(itertools.product(range(self.height), range(self.width)))
        choices = list(all_cells - self.moves_made - self.mines)
        if choices:
            return random.choice(choices)
        return None

