#! /usr/bin/env python3
import sys
import json
import random

from frozeindea.bot_api import BotAPI
from frozeindea.bot_api import get_args_parser
from frozeindea.bot_api import get_rotating_logger

logger = get_rotating_logger()


class WednesdayBot(BotAPI):
    def __init__(self, nickname, chans, server, msgs, port=6667):
        super().__init__(nickname, chans, server, port, logger=logger)
        self.msgs = msgs

    def send_update(self, to=None):
        for chan in self.chans.keys():
            for msg in self.msgs:
                logger.debug(f"{chan} {msg}")
                self.send_msg(chan, msg)

        self.quit()


def consume_one_video(fn="wednesdays.json", video_list=None):
    with open(fn) as f:
        video_list = json.loads(f.read())

    if not video_list:
        return None

    first = video_list.pop(0)

    with open(fn, "wt") as f:
        data = json.dumps(video_list, indent=4)
        f.write(data)

    return first


def get_wednesday_name():
    tokens = [
        "Day",
        "Dude",
        "Spook",
        "Dudes",
        "Duden",
        "Many",
        "Bot",
        "Art",
        "Frog",
        "Ancient",
        "Prophet",
        "Tactic",
        "Mutate",
        "Look",
        "Witness",
        "Miracle",
        "TheDay",
        "Frogs",
        "Bros",
        "Friends",
        "Alien",
        "Cat",
        "Mother",
        "Father",
        "Sun",
        "Moon",
        "Idiot",
        "Sea",
        "Fart",
    ]

    rand_nick = random.choice(tokens)
    if random.choice([True, False]):
        return rand_nick + "Wednesday"
    else:
        return "Wednesday" + rand_nick


if __name__ == "__main__":
    parser = get_args_parser("Wednesday miracle bot.")
    parser._actions = [
        action for action in parser._actions if "--nick" not in action.option_strings
    ]
    args = parser.parse_args()

    video_url = consume_one_video()
    if not video_url:
        logger.error("No more wednesdays.")
        sys.exit(1)

    msgs = ["It is Wednesday MY DUDES!", video_url]

    bot = WednesdayBot(
        get_wednesday_name(), args.channels, args.server, msgs, port=args.port
    )
    bot.verbose = not args.quiet

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Clean exit.")
