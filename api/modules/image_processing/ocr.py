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


class BoundingBox:
    def __init__(self, data: json):
        if len(data) != 4:
            raise BadBoundingException(data)
        self._points = [Vertex(**v) for v in data]

    @property
    def points(self) -> List[List[int]]:
        return [point.values for point in self._points]

    @property
    def tl(self) -> Vertex:
        return self._points[0]

    @property
    def tr(self) -> Vertex:
        return self._points[1]

    @property
    def br(self) -> Vertex:
        return self._points[2]

    @property
    def bl(self) -> Vertex:
        return self._points[3]

    @staticmethod
    def _safely_get_param(param: dict, value: str = None) -> int or List[int]:
        if value != 'x' and value != 'y':
            return param
        if type(param) is not dict or len(param) != 2:
            raise TypeError(param)
        if value not in param:
            return param[0]
        return param[value]

    def __str__(self):
        return "Box%s" % (str(self.points))


class TextField:
    matcher = None

    def __init__(self, data: json, type: str):
        self.raw = data
        self.bounds = BoundingBox(self.raw["boundingPoly"]["vertices"])
        self.type = type

    def get_value(self) -> str:
        return self.raw["description"]

    def get_field_type(self) -> str:
        return self.type

    def is_valid_field(self):
        if self.matcher is None:
            raise NotImplementedError()
        match = self.matcher.match(self.get_value())
        if match is None:
            return False
        return match

    def is_directly_above(self, field):
        bounds = self.bounds
        min_x = bounds.bl.x - Config.word_leniency
        max_x = bounds.bl.x + Config.word_leniency
        return min_x <= field.bounds.tl.x <= max_x and bounds.bl.y < field.bounds.tl.y

    def is_above(self, field):
        bounds = self.bounds
        min_x = bounds.bl.x - Config.word_leniency
        max_x = bounds.bl.x + Config.word_leniency
        return min_x <= field.bounds.tl.x <= max_x

    def v_distance_to(self, field):
        """
        Calculates and returns the closest of two fields to this field
        :param field:
        :return: TextField
        """
        origin = self.bounds
        return origin.br.y - field.bounds.tr.y

    def adjacent_to(self, field):
        """
        Calculates whether this text field is adjacent (to the left of) another text field
        :param field: An instance of Textfield
        :return: boolean, whether or not this is true
        """
        bounds = self.bounds
        min_y_1 = bounds.tr.y - Config.word_leniency / 2
        max_y_1 = bounds.tr.y + Config.word_leniency / 2
        min_y_2 = bounds.br.y - Config.word_leniency / 2
        max_y_2 = bounds.br.y + Config.word_leniency / 2

        return bounds.tr.x < field.bounds.tl.x < bounds.tr.x + Config.word_leniency and \
               min_y_1 < field.bounds.tl.y < max_y_1 and min_y_2 < field.bounds.bl.y < max_y_2

    def __str__(self):
        return self.get_value()

    def __repr__(self):
        return "%s(%s) at %s" % (self.get_field_type(), self.get_value(), self.bounds)
