import json
from typing import List

from modules.image_processing.ocr.vertex import Vertex
from modules.processor.processor_exceptions import FieldError, BoundError


class BoundingBox:
    def __init__(self, data: json):
        if len(data) != 4:
            raise BoundError(data)
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