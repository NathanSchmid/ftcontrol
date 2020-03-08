import logging
import asyncio

from .Positionable import Positionable


class PositionableMotor(Positionable):
    """
    Class to control a motor by coordinates.
    """
    def __init__(self, coordinate_id, motor, init_switch):
        """
        Create a new motor.
        :param coordinate_id: The id of the motor.
        :param motor: The underlying motor.
        :param init_switch: The switch used to initialize the motors. Marks position 0.
        """
        super().__init__(coordinate_id)
        self._motor = motor
        self._init_switch = init_switch
        self._pos = 0

    async def initialize(self, speed=512):
        """
        Initialize the motor by running it with the given speed till the init switch is pressed.
        The hit of thr switch sets the internal coordinate to 0.

        :param speed: The speed at which the motor should run for the initialization
        """
        self._motor.setSpeed(-speed)
        await asyncio.create_task(self._initialize_done())
        self._motor.stop()
        self._pos = 0
        logging.debug("initialized: " + self.id)

    async def goto(self, position=0, speed=512):
        """
        Move the motor to the provided position using the provided speed.
        :param position: The position the motor should navigate to.
        :param speed: The speed at which the motor should run.
        """
        distance = position - self._pos
        if distance < 0:
            distance = -distance
            speed = -speed
        elif distance == 0:
            return

        # start the motor
        self._motor.setDistance(distance)
        self._motor.setSpeed(speed)
        logging.debug(self.id + " going to " + str(position))
        await asyncio.create_task(self._motor_done(position))
        self._motor.stop()

    async def _initialize_done(self):
        while not self._init_switch.state():
            await asyncio.sleep(0.01)

    async def _motor_done(self, position):
        while True:
            # reinitialize every time the init switch is hit.
            if self._pos != 0 and self._init_switch.state():
                logging.debug("reinitialized: " + self.id)
                self._pos = 0
                return
            # set coordinate to position if motor is done.
            if self._motor.finished():
                logging.debug("done: " + self.id)
                self._pos = position
                return
            await asyncio.sleep(0.01)
