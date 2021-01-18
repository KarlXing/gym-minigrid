from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class FetchColorEnv(MiniGridEnv):
    """
    Environment in which the agent has to fetch a random object
    named using English text strings
    Each object has a unique color
    """

    def __init__(
        self,
        size=8,
        numObjs=3,
        targetColorIdx=0
    ):
        self.numObjs = numObjs
        assert(numObjs < len(COLOR_NAMES)-1)
        self.colors = ['green', 'yellow', 'blue']
        self.targetColor = self.colors[targetColorIdx]

        super().__init__(
            grid_size=size,
            max_steps=5*size**2,
            # Set this to True for maximum speed
            see_through_walls=True
        )

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height-1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width-1, 0)

        types = ['key', 'ball']

        objs = []

        # For each object to be generated
        color_idx = 0
        while len(objs) < self.numObjs:
            objType = self._rand_elem(types)
            objColor = self.colors[color_idx]

            if objType == 'key':
                obj = Key(objColor)
            elif objType == 'ball':
                obj = Ball(objColor)

            self.place_obj(obj)
            objs.append(obj)
            color_idx += 1

        # Randomize the player start position and orientation
        self.place_agent()


        descStr = '%s' % (self.targetColor)

        # Generate the mission string
        idx = self._rand_int(0, 5)
        if idx == 0:
            self.mission = 'get a %s' % descStr
        elif idx == 1:
            self.mission = 'go get a %s' % descStr
        elif idx == 2:
            self.mission = 'fetch a %s' % descStr
        elif idx == 3:
            self.mission = 'go fetch a %s' % descStr
        elif idx == 4:
            self.mission = 'you must fetch a %s' % descStr
        assert hasattr(self, 'mission')

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        if self.carrying:
            if self.carrying.color == self.targetColor:
                print('pick up color', self.carrying.color, self.targetColor)
                reward = 1
                done = True
            else:
                reward = -1
                done = True

        return obs, reward, done, info

class FetchGreenEnv(FetchColorEnv):
    def __init__(self):
        super().__init__(size=8, numObjs=3, targetColorIdx=0)

class FetchYellowEnv(FetchColorEnv):
    def __init__(self):
        super().__init__(size=8, numObjs=3, targetColorIdx=1)

class FetchBlueEnv(FetchColorEnv):
    def __init__(self):
        super().__init__(size=8, numObjs=3, targetColorIdx=2)

register(
    id='MiniGrid-FetchGreen-8x8-v0',
    entry_point='gym_minigrid.envs:FetchGreenEnv'
)

register(
    id='MiniGrid-FetchYellow-8x8-v0',
    entry_point='gym_minigrid.envs:FetchYellowEnv'
)

register(
    id='MiniGrid-FetchBlue-8x8-v0',
    entry_point='gym_minigrid.envs:FetchBlueEnv'
)
