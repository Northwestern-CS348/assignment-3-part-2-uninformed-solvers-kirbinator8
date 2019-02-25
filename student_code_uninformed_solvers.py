from solver import *
from queue import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables().
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if (self.currentState.state == self.victoryCondition):  # if we're already at the victory state, we're done
            return True

        curr = self.currentState  # set curr node to be the current game state
        movables = self.gm.getMovables()  # get the iterable list of movables

        if (movables):
            for movable in movables:  # iterate through list of movables, adding children to the curr node and adding the curr node as the part of the child state
                self.gm.makeMove(movable)  # make move
                child_state = GameState(self.gm.getGameState(), (curr.depth + 1), movable)  # set child state to be the game state one level deeper than the current game state
                curr.children.append(child_state)  # add the child state to the list of children in the curr node
                child_state.parent = curr  # set curr node to be the parent of the child state
                self.gm.reverseMove(movable)  # reverse the move

            for child in curr.children:
                if child not in self.visited:  # iterate through list of curr node's children, keeping track of which ones we've seen
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    break
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    q = Queue()
    move_counter = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        movables = self.gm.getMovables()
        if self.currentState.state == self.victoryCondition:  # check to make sure we're not already at victory state
            if (self.q != self.q.empty()):
                while not self.q.empty():
                    self.q.get()
            return True

        if (movables):
            for i in movables:
                self.gm.makeMove(i)
                child = GameState(self.gm.getGameState(), 0, i)
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.gm.reverseMove(i)

        for i in self.currentState.children:
            if i not in self.visited:
                self.q.put(i)

        while not self.q.empty():
            child = self.q.get()
            if child not in self.visited:
                curr = self.currentState
                base = []

                while (curr.requiredMovable):
                    base.append(curr.requiredMovable)
                    curr = curr.parent
                curr = child
                branch = []

                while curr.requiredMovable:
                    branch.append(curr.requiredMovable)
                    curr = curr.parent
                branch = reversed(branch)

                for s in base:
                    self.gm.reverseMove(s)

                for s in branch:
                    self.gm.makeMove(s)

                self.visited[child] = True
                self.currentState = child
                self.move_counter = self.move_counter + 1
                self.currentState.depth = self.move_counter
                break

        return False
