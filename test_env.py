import gym
import time
from gym.envs.registration import register
import argparse
from gym_multigrid.window import Window

parser = argparse.ArgumentParser(description=None)
parser.add_argument('-e', '--env', default='doorkey', type=str)

args = parser.parse_args()

if args.env == 'doorkey':
    register(
        id='multigrid-doorkey-v0',
        entry_point='gym_multigrid.envs:DoorKeyEnv',
    )
    env = gym.make('multigrid-doorkey-v0')

elif args.env == 'soccer':
    register(
        id='multigrid-soccer-v0',
        entry_point='gym_multigrid.envs:SoccerGame4HEnv10x15N2',
    )
    env = gym.make('multigrid-soccer-v0')

else:
    register(
        id='multigrid-collect-v0',
        entry_point='gym_multigrid.envs:CollectGame4HEnv10x10N2',
    )
    env = gym.make('multigrid-collect-v0')

# env.reset()

nb_agents = len(env.agents)
active_agent = 0
def key_handler(event):
    global active_agent
    if event.key == 'escape':
        window.close()
        return
    if event.key == 'backspace':
        reset()
        return
    if event.key == 'left':
        step(env.actions.left)
        return
    if event.key == 'right':
        step(env.actions.right)
        return
    if event.key == 'up':
        step(env.actions.forward)
        return
    if event.key == '1':
        print('set agent 1 to be active')
        active_agent = 0
        return
    if event.key == '2':
        print('set agent 2 to be active')
        active_agent = 1
        return
    # if event.key == ' ':
    #     step(env.actions.toggle)
    #     return
    # if event.key == 'pageup':
    #     step(env.actions.pickup)
    #     return
    # if event.key == 'pagedown':
    #     step(env.actions.drop)
    #     return
    # if event.key == 'enter':
    #     step(env.actions.done)
    #     return

def redraw(img):
    img = env.render(mode='human', highlight=True)
    window.show_img(img)

def reset():
    obs = env.reset()
    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)
    redraw(obs)

def step(action):
    if active_agent == 0:
        ac = [action, None]
    else:
        ac = [None, action]

    obs, reward, done, info = env.step(ac)
    # print('step=%s, reward=%.2f' % (env.step_count, reward))

    if done:
        print('done!')
        reset()
    else:
        redraw(obs)

window = Window('gym_multigrid')
window.reg_key_handler(key_handler)
reset()
# Blocking event loop
window.show(block=True)
# while True:
#     env.render(mode='human', highlight=True)
#     time.sleep(0.1)

#     ac = [env.action_space.sample() for _ in range(nb_agents)]

#     obs, _, done, _ = env.step(ac)

#     if done:
#         break

