from lark import Tree, Token
from lark.visitors import Transformer


class JsonInterpreter(Transformer):
    json_split = []
    _json_objects = []

    """
    We do it this way because there is a possibility that the buffer may land
    between two valid objects if it's an integer.
    """

    def json_objects(self):
        for i, s in enumerate(self.json_split, start=0):
            candidate = None
            on_space = all(c.isspace() for c in s)
            prev_is_space = all(c.isspace() for c in self.json_split[i - 1])
            if i > 0 and not prev_is_space and not on_space:
                candidate = False
            elif not on_space:
                candidate = s

            if candidate is None:
                continue
            elif isinstance(candidate, bool):
                self._json_objects[-1] += s
            else:
                self._json_objects.append(s)

        return self._json_objects

    def __init__(self, reconstructor):
        self.reconstructor = reconstructor
        super().__init__()

    def jsonl(self, odata):
        reconstructed = self.reconstructor.reconstruct(odata[0])
        if len(reconstructed) > 0:
            self.json_split.append(reconstructed)

        return odata
