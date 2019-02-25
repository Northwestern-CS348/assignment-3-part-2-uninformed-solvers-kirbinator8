from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?d ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the ds on the peg. ds
        should be represented by integers, with the smallest d
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest d onTop on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        result = []
        for i in range(0, 3):
            p = []
            my_bindings = self.kb.kb_ask(parse_input("fact: (on ?x peg" + str(i + 1) + ")"))
            if my_bindings:
                for j in my_bindings:
                    p.append(int(j['?x'][-1]))
            p.sort()
            result.append(tuple(p))
        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable d1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        # Student code goes here
        d = str(movable_statement.terms[0])  # store the disk
        ps = str(movable_statement.terms[1])  # store the peg source
        pd = str(movable_statement.terms[2])  # store the peg destination

        if (self.kb.kb_ask(parse_input("fact: (onTop " + d + " ?y)"))):
            top2 = self.kb.kb_ask(parse_input("fact: (onTop " + d + " ?y)"))[0]
            self.kb.kb_retract(parse_input("fact: (onTop " + d + " " + top2['?y'] + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + top2['?y'] + " " + ps + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + ps + ")"))

        if (self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pd + ")"))):
            top1 = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pd + ")"))[0]
            self.kb.kb_retract(parse_input("fact: (top " + top1['?x'] + " " + pd + ")"))
            self.kb.kb_assert(parse_input("fact: (onTop " + d + " " + top1['?x'] + ")"))
        else:
            self.kb.kb_retract(parse_input("fact: (empty " + pd + ")"))

        parsed = parse_input("fact: (on " + d + " " + ps + ")")
        parsed1 = parse_input("fact: (on " + d + " " + pd + ")")
        parsed2 = parse_input("fact: (top " + d + " " + ps + ")")
        parsed3 = parse_input("fact: (top " + d + " " + pd + ")")

        self.kb.kb_retract(parsed)
        self.kb.kb_assert(parsed1)
        self.kb.kb_retract(parsed2)
        self.kb.kb_assert(parsed3)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here ... I wanted to have a nested loop for aesthetics but couldn't figure out a good way to do it, so I left it as three for-loops instead. With more time, I'm sure I could figure out the nested loop

        tuple_1 = []
        tuple_2 = []
        tuple_3 = []
        result = []
        for i in range(1, 4):
            my_bindings = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos1)"))
            if (my_bindings):
                tbind = my_bindings[0]
                tstr = tbind['?tile']
                if (tstr == "empty"):
                    tint = -1
                elif (tstr != "empty"):
                    tint = int(tstr[-1])
                tuple_1.append(tint)

        for i in range(1, 4):
            my_bindings = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos2)"))
            if (my_bindings):
                tbind = my_bindings[0]
                tstr = tbind['?tile']
                if (tstr == "empty"):
                    tint = -1
                elif (tstr != "empty"):
                    tint = int(tstr[-1])
                tuple_2.append(tint)

        for i in range(1, 4):
            my_bindings = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos3)"))
            if (my_bindings):
                tbind = my_bindings[0]
                tstr = tbind['?tile']
                if (tstr == "empty"):
                    tint = -1
                elif (tstr != "empty"):
                    tint = int(tstr[-1])
                tuple_3.append(tint)

        result.append(tuple(tuple_1))
        result.append(tuple(tuple_2))
        result.append(tuple(tuple_3))
        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        # Student code goes here

        tile = str(movable_statement.terms[0])
        x1 = str(movable_statement.terms[1])
        y1 = str(movable_statement.terms[2])
        x2 = str(movable_statement.terms[3])
        y2 = str(movable_statement.terms[4])

        parsed = parse_input("fact: (loc " + tile + " " + x1 + " " + y1 + ")")
        parsed1 = parse_input("fact: (loc  empty " + x2 + " " + y2 + ")")
        parsed2 = parse_input("fact: (loc " + tile + " " + x2 + " " + y2 + ")")
        parsed3 = parse_input("fact: (loc  empty " + x1 + " " + y1 + ")")

        self.kb.kb_retract(parsed)
        self.kb.kb_retract(parsed1)
        self.kb.kb_assert(parsed2)
        self.kb.kb_assert(parsed3)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
