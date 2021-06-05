#! /usr/bin/env python3
import json

from frozeindea.bot_api import BotAPI
from frozeindea.bot_api import get_args_parser
from frozeindea.bot_api import get_rotating_logger

logger = get_rotating_logger()


class WednesdayBot(BotAPI):
    def __init__(self, nickname, chans, server, msgs, port=6667):
        super().__init__(nickname, chans, server, port, logger=logger)
        self.msgs = msgs

    def send_update(self, to=None):
        logger.debug("Sending update to %s", str(to))

        for chan in self.chans.keys():
            for msg in self.msgs:
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


if __name__ == "__main__":
    parser = get_args_parser("Wednesday miracle bot.")

    parser._actions = [
        action for action in parser._actions
        if "--nick" not in action.option_strings
    ]

    args = parser.parse_args()

    yt_link = consume_one_video()
    msgs = ["It is Wednesday MY DUDES!", yt_link]
    nick = "Wednesdaytest"

    bot = WednesdayBot(nick, args.channels, args.server, msgs, port=args.port)
    bot.verbose = not args.quiet

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Clean exit.")
