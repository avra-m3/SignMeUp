from typing import List


class Vertex:
    x: float
    y: float

    def __str__(self):
        return "Vertex(x: {}, y: {})".format(self.x, self.y)


class Bounds:
    _values: List[Vertex]

    class Row:
        left: Vertex
        right: Vertex

        def __str__(self):
            return "Row(Left: {}, Right: {})".format(str(self.left), str(self.right))

    @property
    def top(self) -> Row:
        result = Bounds.Row()
        result.left = self._values[0]
        result.right = self._values[1]
        return result

    @property
    def bottom(self) -> Row:
        result = Bounds.Row()
        result.left = self._values[2]
        result.right = self._values[3]
        return result

    @property
    def values(self) -> List[Vertex]:
        return self._values.copy()

    @values.setter
    def values(self, new: List[Vertex]):
        self._values = new

    def __getitem__(self, item):
        return self._values[item]

    def __str__(self):
        return "Bounds(top: {}, bottom: {})".format(str(self.top), str(self.bottom))

    def __repr__(self):
        return ",".join([str(vertex) for vertex in self._values])


class ResponseField:
    _text: str
    _bounds: Bounds

    @property
    def bounds(self):
        return self._bounds

    @property
    def text(self):
        return self._text

    def __str__(self):
        return "Response(text: {}, bounds: {})".format(self.text, self.bounds)