from processor.modules.ocr.bounding import BoundingBox


class TextField:
    FLEX = 27

    def __init__(self, data: dict, type: str, matcher=None):
        self.raw = data
        self.bounds = BoundingBox(self.raw["bounding_poly"]["vertices"])
        self.type = type
        self.matcher = matcher

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
        min_x = bounds.bl.x - TextField.FLEX
        max_x = bounds.bl.x + TextField.FLEX
        return min_x <= field.bounds.tl.x <= max_x and bounds.bl.y < field.bounds.tl.y

    def is_above(self, field):
        bounds = self.bounds
        min_x = bounds.bl.x - TextField.FLEX
        max_x = bounds.bl.x + TextField.FLEX
        return min_x <= field.bounds.tl.x <= max_x

    def v_distance_to(self, field):
        """
        Calculates and returns the closest of two fields to this field
        :param field:
        :return: TextField
        """
        origin = self.bounds
        return abs(origin.br.y - field.bounds.tr.y)

    def adjacent_to(self, field):
        """
        Calculates whether this text field is adjacent (to the left of) another text field
        :param field: An instance of Textfield
        :return: boolean, whether or not this is true
        """
        bounds = self.bounds
        min_y_1 = bounds.tr.y - TextField.FLEX / 2
        max_y_1 = bounds.tr.y + TextField.FLEX / 2
        min_y_2 = bounds.br.y - TextField.FLEX / 2
        max_y_2 = bounds.br.y + TextField.FLEX / 2

        return bounds.tr.x < field.bounds.tl.x < bounds.tr.x + TextField.FLEX and \
               min_y_1 < field.bounds.tl.y < max_y_1 and min_y_2 < field.bounds.bl.y < max_y_2

    def __str__(self):
        return self.get_value()

    def __repr__(self):
        return "%s(%s) at %s" % (self.get_field_type(), self.get_value(), self.bounds)
