import asyncio


class MultiPositionable:
    def __init__(self, coordinates):
        self._coordinates = coordinates

    @property
    def position(self):
        return tuple(c.position for c in self._coordinates)

    async def initialize(self, speed=None):
        speed = self._speed(speed)
        init_calls = [self._coordinates[i].initialize(speed[i]) for i in range(len(self._coordinates))]
        await asyncio.gather(*init_calls)

    async def goto(self, coordinates, speed=None):
        speed = self._speed(speed)
        goto_calls = [self._coordinates[i].goto(coordinates[i], speed[i]) for i in range(len(self._coordinates))]
        await asyncio.gather(*goto_calls)

    def _speed(self, speed):
        if not speed:
            return tuple(512 for c in self._coordinates)
        return speed
