import networkx as nx
import numpy as np
from gymnasium import Env

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


"""
[(nrow, ncol), (start_id, end_id), list of wall locations]
[(nrow, ncol), (start_id, end_id), [(id1, id2), (id3, id4) ...]]
"""
WALLS = {
    "4x4": [
        (4, 4),
        (0, 15),
        [(0, 1), (2, 3), (6, 10), (7, 11), (8, 9), (9, 13), (13, 14), (14, 15)],
    ],
}


class MazeEnv(Env):

    def __init__(
        self,
        render_mode: str = None,
        map_name="4x4",
    ):
        (self.nrow, self.ncol), (self.start_id, self.end_id), wall_locs = WALLS[map_name]
        # number of actions, number of states
        self.nA, self.nS = 4, self.nrow * self.ncol

        self.G_wall, self.G_path = self.build_map(wall_locs)

        # Calculate transition probabilities and rewards
        self.P = {}
        for s_id in range(self.nS):
            location = self.to_loc(s_id)
            self.P[s_id] = {a: [] for a in range(self.nA)}
            self.P[s_id][LEFT] = self._calculate_transition_prob(location, (-1, 0))
            self.P[s_id][DOWN] = self._calculate_transition_prob(location, (0, 1))
            self.P[s_id][RIGHT] = self._calculate_transition_prob(location, (1, 0))
            self.P[s_id][UP] = self._calculate_transition_prob(location, (0, -1))

    def to_id(self, row, col) -> int:
        return row * self.ncol + col

    def to_loc(self, id) -> tuple[int, int]:
        return np.unravel_index(id, (self.nrow, self.ncol))

    def _calculate_transition_prob(self, current, delta):
        """Determine the outcome for an action. Transition Prob is always 1.0.

        Args:
            current: Current position on the grid as (row, col)
            delta: Change in position for transition

        Returns:
            Tuple of ``(1.0, new_state, reward, terminated)``
        """

        new_row, new_col = current[0] + delta[0], current[1] + delta[1]

        if self.is_adjacent(current[0], current[1], new_row, new_col):
            return [(1.0, self.to_id(*current), 0.0, False)]
        else:
            new_state = self.to_id(new_row, new_col)

            if new_state == self.end_id:
                return [(1.0, new_state, 1.0, True)]
            else:
                return [(1.0, new_state, 0.0, False)]

    def is_adjacent(self, row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def build_map(self, wall_locs):
        """
        Build a map.

        Returns
            G_path: graph of path
            G_wall: graph of wall
        """

        def clean_links(G):
            """
            Remove links that do not exist (not adjacent).
            """
            for a, b in G.edges:
                row1, col1 = self.to_loc(a)
                row2, col2 = self.to_loc(b)
                if not self.is_adjacent(row1, col1, row2, col2):
                    G.remove_edge(a, b)

        # Load wall & add all nodes
        G_wall = nx.from_edgelist(wall_locs)
        G_wall.add_nodes_from(range(self.nS))

        # Create path graph
        G_path = nx.complement(G_wall)

        clean_links(G_path)
        clean_links(G_wall)

        return G_wall, G_path


if __name__ == "__main__":
    from pprint import pprint

    # print(np.unravel_index(0, (4,4)))
    # exit()

    env = MazeEnv()
    print(env.G_path.edges)
    pprint(env.P)
    # print(env.G_wall.edges)

    exit(0)
    env.reset()
    for _ in range(100):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            env.reset()
