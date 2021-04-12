import curses
import datetime
import time

import emoji
import numpy as np
import yfinance as yf
from pandas import Series

tz = datetime.datetime.now().astimezone().tzinfo


class Ticker():

    def __init__(self, name: str):
        self.name = name
        self.last_update = 0
        self.update()

    def get_trend_emoji(self, data: Series) -> str:
        a, _ = np.polyfit(data, range(len(data)), 1)
        if a > 0:
            return ':up-right_arrow:'
        elif a < 0:
            return ':down-right_arrow:'
        else:
            return ':right_arrow:'

    def update(self):
        if abs(self.last_update - time.time()) > 15:
            self.data = yf.download(tickers=self.name, period='10m', interval='1m', prepost=True, progress=False)
            self.last_update = time.time()

    def __str__(self):
        self.update()
        price = round(self.data['Close'][-1], 2)
        volume = self.data['Volume'][-2]
        update = self.data.index[-1]
        output = "${}: {:.2f}$ {} \t {} {} \t {}".format(
            self.name,
            price,
            self.get_trend_emoji(self.data['Close']),
            volume,
            self.get_trend_emoji(self.data['Volume'][:-1]),
            update.astimezone(tz),
        )
        return emoji.emojize(output, use_aliases=True, variant='emoji_type')


def main(stdscr):
    gme = Ticker('GME')

    while True:

        output = str(gme)

        stdscr.clear()
        stdscr.addstr(0, 0, output)
        stdscr.refresh()
        if stdscr.getch() in [ord('q'), ord('Q')]:
            break
        curses.napms(500)


if __name__ == '__main__':
    stdscr = curses.initscr()
    old_curs = curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    try:
        main(stdscr)
    except KeyboardInterrupt:
        pass
    finally:
        curses.curs_set(old_curs)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
