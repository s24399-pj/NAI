import asyncio
import sys

import numpy as np
import pygame
import skfuzzy as fuzz
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from skfuzzy import control as ctrl

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Fuzzy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )

        self.initialize_fuzzy_controller()

    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Player(self.config)
            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    def check_quit_event(self, event):
        if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
                event.key == pygame.K_SPACE or event.key == pygame.K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        asyncio.create_task(self.flap_every_frame())

        while True:
            if self.player.collided(self.pipes, self.floor):
                return

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def flap_every_frame(self):
        """Continuously evaluate and decide whether the bird should flap in each frame using the fuzzy logic controller.

        This method runs asynchronously during gameplay, retrieving current state parameters,
        computing the action using the fuzzy logic controller, and making the bird flap if necessary.
        """
        while not self.player.crashed:
            bird_y = self.player.y
            bird_vel_y = self.player.vel_y
            distance_to_pipe, pipe_gap_y = self.get_next_pipe_data()
            height_difference = pipe_gap_y - bird_y

            should_flap = self.fuzzy_logic_controller(bird_y, bird_vel_y, distance_to_pipe, height_difference)
            if should_flap:
                self.player.flap()

            print(
                f"bird_y: {bird_y}, bird_vel_y: {bird_vel_y}, distance_to_pipe: {distance_to_pipe}, height_difference: {height_difference}, should_flap: {should_flap}"
            )
            await asyncio.sleep(0)

    def get_next_pipe_data(self):
        """Get the distance to the next pipe and the vertical position of the next pipe's gap.

        Returns:
            tuple: A tuple containing:
            - distance_to_pipe (float): The horizontal distance from the bird to the next pipe.
            - pipe_gap_y (float): The vertical position of the middle of the gap in the next pipe.
        """
        for pipe_upper in self.pipes.upper:
            if pipe_upper.x + pipe_upper.w > self.player.x:
                distance_to_pipe = pipe_upper.x - self.player.x
                pipe_gap_y = pipe_upper.y + pipe_upper.h + self.pipes.pipe_gap / 2
                return distance_to_pipe, pipe_gap_y
        return 300, self.config.window.height / 2

    async def game_over(self):
        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)

    def initialize_fuzzy_controller(self):
        """Initialize the fuzzy logic controller with membership functions and rules."""
        self.bird_y = ctrl.Antecedent(np.arange(0, 513, 1), 'bird_y')
        self.bird_vel_y = ctrl.Antecedent(np.arange(-15, 16, 1), 'bird_vel_y')
        self.distance_to_pipe = ctrl.Antecedent(np.arange(0, 501, 1), 'distance_to_pipe')
        self.height_difference = ctrl.Antecedent(np.arange(-512, 513, 1), 'height_difference')

        self.action = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'action')

        self.bird_y['high'] = fuzz.trimf(self.bird_y.universe, [0, 0, 200])
        self.bird_y['medium'] = fuzz.trimf(self.bird_y.universe, [150, 256, 362])
        self.bird_y['low'] = fuzz.trimf(self.bird_y.universe, [300, 512, 512])

        self.bird_vel_y['rising_fast'] = fuzz.trimf(self.bird_vel_y.universe, [-15, -15, -5])
        self.bird_vel_y['rising_slowly'] = fuzz.trimf(self.bird_vel_y.universe, [-10, -5, 0])
        self.bird_vel_y['stable'] = fuzz.trimf(self.bird_vel_y.universe, [-2, 0, 2])
        self.bird_vel_y['falling_slowly'] = fuzz.trimf(self.bird_vel_y.universe, [0, 5, 10])
        self.bird_vel_y['falling_fast'] = fuzz.trimf(self.bird_vel_y.universe, [5, 15, 15])

        self.distance_to_pipe['close'] = fuzz.trimf(self.distance_to_pipe.universe, [0, 0, 150])
        self.distance_to_pipe['medium'] = fuzz.trimf(self.distance_to_pipe.universe, [100, 250, 400])
        self.distance_to_pipe['far'] = fuzz.trimf(self.distance_to_pipe.universe, [350, 500, 500])

        self.height_difference['much_below'] = fuzz.trimf(self.height_difference.universe, [-512, -512, -100])
        self.height_difference['below'] = fuzz.trimf(self.height_difference.universe, [-150, -50, 0])
        self.height_difference['level'] = fuzz.trimf(self.height_difference.universe, [-25, 0, 25])
        self.height_difference['above'] = fuzz.trimf(self.height_difference.universe, [0, 50, 150])
        self.height_difference['much_above'] = fuzz.trimf(self.height_difference.universe, [100, 512, 512])

        self.action["don't_flap"] = fuzz.trimf(self.action.universe, [0, 0, 0.5])
        self.action['flap'] = fuzz.trimf(self.action.universe, [0.5, 1, 1])

        rule1 = ctrl.Rule(
            self.bird_y['low'] & self.bird_vel_y['falling_fast'] & self.distance_to_pipe['close'],
            self.action['flap']
        )
        rule2 = ctrl.Rule(
            self.bird_y['high'] & self.bird_vel_y['rising_fast'],
            self.action["don't_flap"]
        )
        rule3 = ctrl.Rule(
            self.distance_to_pipe['far'],
            self.action["don't_flap"]
        )
        rule4 = ctrl.Rule(
            self.bird_y['medium'] & self.bird_vel_y['falling_slowly'] & self.distance_to_pipe['medium'],
            self.action['flap']
        )
        rule5 = ctrl.Rule(
            self.bird_vel_y['stable'],
            self.action["don't_flap"]
        )
        rule6 = ctrl.Rule(
            self.height_difference['much_below'] | self.height_difference['below'],
            self.action['flap']
        )
        rule7 = ctrl.Rule(
            self.height_difference['much_above'] | self.height_difference['above'],
            self.action["don't_flap"]
        )
        rule8 = ctrl.Rule(
            self.height_difference['level'] & self.bird_vel_y['stable'],
            self.action["don't_flap"]
        )

        self.flappy_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
        self.flappy_simulation = ctrl.ControlSystemSimulation(self.flappy_ctrl)

    def fuzzy_logic_controller(self, bird_y_value, bird_vel_y_value, distance_to_pipe_value, height_difference_value):
        """Compute the action (whether to flap or not) using the fuzzy logic controller.
                Args:
                    bird_y_value (float): The vertical position of the bird.
                    bird_vel_y_value (float): The vertical velocity of the bird.
                    distance_to_pipe_value (float): The horizontal distance to the next pipe.
                    height_difference_value (float): The vertical difference between the bird and the pipe gap.

                Returns:
                    bool: True if the bird should flap, False otherwise.
        """
        self.flappy_simulation.input['bird_y'] = bird_y_value
        self.flappy_simulation.input['bird_vel_y'] = bird_vel_y_value
        self.flappy_simulation.input['distance_to_pipe'] = distance_to_pipe_value
        self.flappy_simulation.input['height_difference'] = height_difference_value

        try:
            self.flappy_simulation.compute()
        except Exception as e:
            print(f"Error in fuzzy controller calculations: {e}")
            self.flappy_simulation.print_state()
            return False

        action_value = self.flappy_simulation.output.get('action', 0)

        return action_value > 0.5
