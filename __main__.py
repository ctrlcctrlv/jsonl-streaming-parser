from jsonl import *
from log_handler import logger

INPUT = """{}{"alph{a": 3, "king": {"queen": 3}} [][]""{} {"2": []}  {"id": 1} 23 23 "cap\\"n crunch" [1,2, 3] []""3{}2.2""null"""

import sys

readlen = 10
parsebuf = ""
parsed_pos = 0
parsed_count = 0
while len(INPUT) > 0 or parsebuf:
    if len(INPUT) == 0:
        logger.warning("Last iteration!")
    try:
        logger.debug(
            "Buffer status: len {3}, removed in last iteration {0}, have parsed {2} objects; contents are `{1}`".format(
                parsed_pos, parsebuf, parsed_count, len(parsebuf)
            )
        )
        parsed = json_parser.parse(parsebuf)
    except lark.LarkError:
        continue
    finally:
        if len(transformer.json_split) != parsed_count:
            parsed_pos = 0
            for i in range(parsed_count, len(transformer.json_split)):
                parsed_pos += len(transformer.json_split[i])
                logger.info("Got {}".format(transformer.json_split[i]))
            parsed_count = len(transformer.json_split)
            parsebuf = parsebuf[parsed_pos:]
            json_parser = recreate_parser()
        parsebuf += INPUT[:readlen]
        INPUT = INPUT[readlen:]

logger.info(
    "Final list of objects:\n\t\t{},".format(",\n\t\t".join(transformer.json_objects()))
)
