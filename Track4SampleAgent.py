import scipy.misc
import carla
from srunner.challenge.autoagents.autonomous_agent import AutonomousAgent

try:
    import pygame
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_c
    from pygame.locals import K_d
    from pygame.locals import K_h
    from pygame.locals import K_m
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

import carla
import time

from srunner.challenge.autoagents.autonomous_agent import AutonomousAgent

class KeyboardControl(object):
    def __init__(self):
        self._control = carla.VehicleControl()
        self._steer_cache = 0.0

    def parse_events(self, control, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            self._parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time())
            control.steer = self._control.steer
            control.throttle = self._control.throttle
            control.brake = self._control.brake
            control.hand_brake = self._control.hand_brake

    def _parse_vehicle_keys(self, keys, milliseconds):
        self._control.throttle = 0.6 if keys[K_UP] or keys[K_w] else 0.0
        steer_increment = 15.0 * 5e-4 * milliseconds
        if keys[K_LEFT] or keys[K_a]:
            self._steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            self._steer_cache += steer_increment
        else:
            self._steer_cache = 0.0

        self._steer_cache = min(0.95, max(-0.95, self._steer_cache))
        self._control.steer = round(self._steer_cache, 1)
        self._control.brake = 1.0 if keys[K_DOWN] or keys[K_s] else 0.0
        self._control.hand_brake = keys[K_SPACE]


class HumanTextInterface():
    """
    Class to control a vehicle manually for debugging purposes
    """
    def __init__(self, parent):
        self.quit = False
        self._parent = parent
        self.WIDTH = 800
        self.HEIGHT = 600
        self.THROTTLE_DELTA = 0.05
        self.STEERING_DELTA = 0.01

        pygame.init()
        pygame.font.init()
        self._clock = pygame.time.Clock()
        self._display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Human Agent")

    def run(self):
        while not self._parent.agent_engaged:
            time.sleep(0.5)

        controller = KeyboardControl()
        while not self.quit:
            self._clock.tick_busy_loop(20)
            controller.parse_events(self._parent.current_control, self._clock)
            # Process events
            pygame.event.pump()  # to get all the keyboard control

            # process sensor data
            input_data = self._parent.sensor_interface.get_data()

            # merge your position with the input data and inform the client
            # Your position

            print (input_data['GPS'])

            # Then we print how this relates with all the other positions



        pygame.quit()


class Track4SampleAgent(AutonomousAgent):
    """
    THis is a human controlled agent with track 4 access for testing
    """
    def setup(self, path_to_conf_file):
        pass

    def sensors(self):

        """
        Define the sensor suite required by the agent

        :return: a list containing the required sensors in the following format:

        """
        sensors = [
                   {'type': 'sensor.other.gnss', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'GPS'},
                   {'type': 'sensor.scene_layout', 'id': 'scene_layout'},
                   {'type': 'sensor.object_finder', 'reading_frequency': 20, 'id': 'object_finder'}

                  ]

        return sensors

    def run_step(self, input_data):

        self.agent_engaged = True
        return self.current_control

