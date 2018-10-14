class Vertex:
    def __init__(self, x=None, y=None, **extra_v):
        """
        Create a vertex if one of x and y is valid, and there are no extra vertices
        :param x: The x value
        :param y: The y value
        :param extra_v: A keyword argument catch all
        """
        if x is None and y is None or extra_v:
            raise ([x, y, extra_v])
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        If x is none, return a number indicating so
        :return: self._x or -1
        """
        if self._x is not None:
            return self._x
        return -1

    @property
    def y(self):
        """
        If y is none, return a number indicating so
        :return: self._y or -1
        """
        if self._y is not None:
            return self._y
        return -1

    @property
    def values(self):
        """
        Return x and y as a list
        :return: a list of length 2
        """
        return [self.x, self.y]

    def __call__(self, value):
        """
        Legacy reasons
        :param value:
        :return:
        """
        if hasattr(self, value):
            return self.__dict__[value]
        return None