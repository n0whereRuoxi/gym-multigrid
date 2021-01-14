from gym_multigrid.multigrid import *

class DoorKeyEnv(MultiGridEnv):
    """
    Environment with a door and key, sparse reward
    """

    def __init__(self, size=8):
        self.world = World
        agents_index = [1,2]
        agents = []
        view_size = 7
        for i in agents_index:
            agents.append(Agent(self.world, i, view_size=view_size))
        super().__init__(
            grid_size=size,
            width=None,
            height=None,
            max_steps= 10000,
            see_through_walls=False,
            agents=agents,
            agent_view_size=view_size
        )


    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(self.world, 0, 0)
        self.grid.horz_wall(self.world, 0, height-1)
        self.grid.vert_wall(self.world, 0, 0)
        self.grid.vert_wall(self.world, width-1, 0)

        # # Place a goal in the bottom-right corner
        # self.put_obj(Goal(), width - 2, height - 2)

        # Create a vertical splitting wall
        splitIdx = self._rand_int(2, width-2)
        self.grid.vert_wall(self.world, splitIdx, 0)

        # Create a random openningIdx on the vertical wall
        openningIdx = self._rand_int(1, width-2)
        self.grid.set(splitIdx, openningIdx, None)

        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        # self.place_agent(size=(splitIdx, height))

        # Randomize the player start position and orientation
        for a in self.agents:
            self.place_agent(a)

        # Place a door in the wall
        # doorIdx = self._rand_int(1, width-2)
        # self.place_obj(Door(self.world, 'yellow', is_locked=False), splitIdx, doorIdx)

        # # Place a yellow key on the left side
        # self.place_obj(
        #     obj=Key('yellow'),
        #     top=(0, 0),
        #     size=(splitIdx, height)
        # )


        self.mission = "use the key to open the door and then get to the goal"

    # def _reward(self, i, rewards, reward=1):
    #     """
    #     Compute the reward to be given upon success
    #     """
    #     for j,a in enumerate(self.agents):
    #         if a.index==i or a.index==0:
    #             rewards[j]+=reward
    #         if self.zero_sum:
    #             if a.index!=i or a.index==0:
    #                 rewards[j] -= reward

    # def _handle_pickup(self, i, rewards, fwd_pos, fwd_cell):
    #     if fwd_cell:
    #         if fwd_cell.can_pickup():
    #             if fwd_cell.index in [0, self.agents[i].index]:
    #                 fwd_cell.cur_pos = np.array([-1, -1])
    #                 self.grid.set(*fwd_pos, None)
    #                 self._reward(i, rewards, fwd_cell.reward)

    # def _handle_drop(self, i, rewards, fwd_pos, fwd_cell):
    #     pass

    def step(self, actions):
        obs, rewards, done, info = MultiGridEnv.step(self, actions)
        return obs, rewards, done, info

