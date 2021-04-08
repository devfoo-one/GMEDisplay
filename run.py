import curses
import datetime

import emoji
import yfinance as yf

tz = datetime.datetime.now().astimezone().tzinfo

def main(stdscr):

    last_price = None
    last_volume = None
    last_update = None

    while True:

        data = yf.download(tickers='GME', period='5m', interval='1m', prepost=True, progress=False)
        price = round(data['Close'][-1], 2)
        volume = data['Volume'][-2]
        update = data.index[-1]

        if last_update != update:
            if last_price is None:
                trend_price = ':rocket:'
            elif last_price < price:
                trend_price = ':up-right_arrow:'
            elif last_price > price:
                trend_price = ':down-right_arrow:'
            else:
                trend_price = ':right_arrow:'

            if last_volume is None:
                trend_volume = ':rocket:'
            elif last_volume < volume:
                trend_volume = ':up-right_arrow:'
            elif last_volume > volume:
                trend_volume = ':down-right_arrow:'
            else:
                trend_volume = ':right_arrow:'
            last_volume = volume

        last_price = price
        last_update = update

        output = "$GME: {:.2f}$ {} \t {} {} \t {}".format(
            price,
            trend_price,
            volume,
            trend_volume,
            update.astimezone(tz),
        )
        output = emoji.emojize(output, use_aliases=True, variant='emoji_type')

        stdscr.clear()
        stdscr.addstr(0, 0, output)
        stdscr.refresh()
        if stdscr.getch() in [ord('q'), ord('Q')]:
            break
        curses.napms(1000)

if __name__ == '__main__':
    stdscr = curses.initscr()
    old_curs = curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    try:
        main(stdscr)
    except Exception:
        pass
    finally:
        curses.curs_set(old_curs)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()