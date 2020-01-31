import math
import random
import time
from sample_players import DataPlayer, BasePlayer

class Node():
    """
        Implement a class for node of a tree:
        * save state of game
        * value of a node (for mcts algorithm)
        * children node
        * parent node
        See: https://github.com/Alfo5123/Connect4/blob/master/game.py
    """

    def __init__(self, state, parent=None):
        self.visits = 0
        self.value = 0.0
        self.state = state
        self.children = []
        self.child_actions = []
        self.parent = parent

    def add_child(self, child_state, action):
        child = Node(child_state, self)
        self.children.append(child)
        self.child_actions.append(action)

    def update_node(self, value):
        self.value += value
        self.visits += 1

    def fully_explored(self):
        if len(self.child_actions) == len(self.state.actions()):
            return True
        return False


class MctsPlayer(BasePlayer):
    """
        Implement a custom player that invokes the Node class and
        uses Monte Carlo Tree Search (MTCS) to play game
        See: https://github.com/Alfo5123/Connect4/blob/master/game.py
    """

    def get_action(self, state):
        """
            Select random move on an empty board to start game,
            otherwise return the MCTS move.
        """
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.mcts(state))

    def expand(self, node):
        """
            Select a legal move and return new state
        """
        possible_actions = node.state.actions()
        for action in possible_actions:
            if action not in node.child_actions: # if action not explored
                new_state = node.state.result(action)
                break
        node.add_child(new_state, action)
        return node.children[-1]

    def best_child(self, node, factor = 1):
        """
            Return best score of children nodes (exploit + factor * explore  scores)
        """
        if node.visits == 0: # if first visit of the node, we want to explore this part of the tree
            return float("inf")
        else:
            return max(node.children, key=lambda child: child.value / child.visits + factor * math.sqrt(2 * math.log(child.parent.visits) / child.visits)) # see https://en.wikipedia.org/wiki/Monte_Carlo_tree_search

    def tree_policy(self, node):
        """
            Expansion of the search tree
            If node fully explored, return best child, if not fully explored return one branch
        """
        while not node.state.terminal_test():
            if not node.fully_explored():
                return self.expand(node)
            node = self.best_child(node)
        return node

    def rollout_policy(self, node, player):
        """
            From the last expanded node, randomly play moves
            until reach end of the game and record a winner
        """
        state = node.state
        while not state.terminal_test():
            action = random.choice(state.actions())
            state = state.result(action)
        if state._has_liberties(node.state.player()):
            return -1
        else:
            return 1

    def backprop(self, node, value):
        """
            Update nodes value after reaching terminal state going
            backward along the search tree
        """
        while node:
            node.update_node(value)
            node = node.parent
            value = -value

    def mcts(self, state):
        """
            Locate and backpropagate nodes along the search tree, corresponding
            to moves which frequently lead to wins in rollout simulation games
        """
        timer_end  = time.time() + 0.1 # 0.1 can be tuned to balance performance and speed
        root = Node(state)
        if root.state.terminal_test():
            return random.choice(state.actions())
        while time.time() < timer_end:
            leaf = self.tree_policy(root)
            value = self.rollout_policy(leaf, state.player())
            self.backprop(leaf, value)
        result = root.children.index(self.best_child(root, factor=1))
        return root.child_actions[result]

CustomPlayer = MctsPlayer
