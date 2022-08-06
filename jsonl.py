#!/usr/bin/env python3
from json_interpreter import JsonInterpreter

from lark import Lark
from lark.reconstruct import Reconstructor
import lark

import tempfile

TEMP = tempfile.NamedTemporaryFile()

with open("jsonl.lark") as f:
    GRAMMAR = f.read()
parser = Lark(GRAMMAR, parser="lalr", maybe_placeholders=False)
reconstructor = Reconstructor(parser)
transformer = JsonInterpreter(reconstructor)


def recreate_parser():
    return Lark(
        GRAMMAR,
        parser="lalr",
        maybe_placeholders=False,
        transformer=transformer,
        cache=TEMP.name,
    )


json_parser = recreate_parser()
