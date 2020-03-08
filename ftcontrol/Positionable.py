from abc import abstractmethod


class Positionable:
    """
    Base class that supports to hold a position and navigation to a position.
    """
    def __init__(self, coordinate_id):
        """
        Create the positionable
        :param coordinate_id: The identification of the coordinate.
        """
        self._id = str(coordinate_id)
        self._pos = 0

    @property
    def id(self):
        return self._id

    @property
    def position(self):
        return self._pos

    @abstractmethod
    async def goto(self, position=0, speed=512):
        pass

