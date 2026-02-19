import traci
import numpy as np
from gymnasium import Env
from gymnasium.spaces import Discrete, Box
from stable_baselines3 import DQN
import uuid

class TrafficLightEnv(Env):
    def __init__(self, config_file, max_steps=1000):
        super().__init__()
        self.config_file = config_file
        self.max_steps = max_steps
        self.step_count = 0
        self.connection_label = str(uuid.uuid4())
        self.is_connected = False
        
        # Initialize traffic lights and lanes in __init__
        self.tl_ids = []
        self.controlled_lanes = {}
        traci.start(["sumo", "-c", self.config_file, "--no-step-log", "true"], label=self.connection_label)
        self.is_connected = True
        traci.simulationStep()
        
        self.tl_ids = traci.trafficlight.getIDList()
        if not self.tl_ids:
            raise ValueError("No traffic lights found in the network.")
        for tl_id in self.tl_ids:
            lanes = traci.trafficlight.getControlledLanes(tl_id)
            self.controlled_lanes[tl_id] = list(dict.fromkeys(lanes))
        
        self.action_space = Discrete(3)
        obs_size = sum(len(lanes) for lanes in self.controlled_lanes.values()) + 2 * len(self.tl_ids)
        self.observation_space = Box(low=0, high=1000, shape=(obs_size,), dtype=np.float32)
        
        traci.close()
        self.is_connected = False

    def reset(self, seed=None, options=None):
        if self.is_connected:
            try:
                traci.close()
                self.is_connected = False
            except traci.exceptions.TraCIException:
                pass
        traci.start(["sumo-gui", "-c", self.config_file], label=self.connection_label)
        self.is_connected = True
        traci.simulationStep()
        self.step_count = 0
        return self._get_state(), {}

    def step(self, action):
        self._take_action(action)
        traci.simulationStep()
        self.step_count += 1
        state = self._get_state()
        reward = self._get_reward()
        done = self.step_count >= self.max_steps or traci.simulation.getMinExpectedNumber() == 0
        truncated = False
        return state, reward, done, truncated, {}

    def _get_state(self):
        try:
            state = []
            for tl_id in self.tl_ids:
                waiting = [traci.lane.getLastStepHaltingNumber(lane) for lane in self.controlled_lanes[tl_id]]
                phase = traci.trafficlight.getPhase(tl_id)
                current_time = traci.simulation.getTime()
                time_remaining = traci.trafficlight.getPhaseDuration(tl_id) - \
                                 (traci.trafficlight.getNextSwitch(tl_id) - current_time)
                time_remaining = np.clip(time_remaining, 0, 1000)
                state.extend(waiting + [phase, time_remaining])
            return np.array(state, dtype=np.float32)
        except traci.exceptions.TraCIException as e:
            print(f"TraCI error in _get_state: {e}")
            return np.zeros(self.observation_space.shape[0], dtype=np.float32)

    def _take_action(self, action):
        for tl_id in self.tl_ids:
            current_phase = traci.trafficlight.getPhase(tl_id)
            current_duration = traci.trafficlight.getPhaseDuration(tl_id)
            green_phases = [i for i, state in enumerate(traci.trafficlight.getCompleteRedYellowGreenDefinition(tl_id)[0].phases)
                            if 'G' in state.state]
            if action == 0 and current_phase in green_phases:
                traci.trafficlight.setPhaseDuration(tl_id, current_duration + 5)
            elif action == 1:
                traci.trafficlight.setPhase(tl_id, (current_phase + 1) % len(traci.trafficlight.getAllProgramLogics(tl_id)[0].phases))

    def _get_reward(self):
        total_waiting = sum(traci.lane.getWaitingTime(lane) for lane in traci.lane.getIDList())
        return -total_waiting

    def close(self):
        if self.is_connected:
            try:
                traci.close()
                self.is_connected = False
            except traci.exceptions.TraCIException:
                pass

# Test the trained model with SUMO-GUI
config_file = "intersection.sumocfg"
env = TrafficLightEnv(config_file)
model = DQN.load("models/kingcircle")

obs, _ = env.reset()q
total_reward = 0
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, _ = env.step(action)
    total_reward += reward
    if done or truncated:
        obs, _ = env.reset()

env.close()
print(f"Total Reward: {total_reward}")