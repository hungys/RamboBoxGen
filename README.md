RamboBoxGen
===========

RamboBoxGen is an utility to generate Rambo-style Box Score for NBA games, with ANSI color highlighting optimized for [Ptt BBS](https://www.ptt.cc/). This project was still in early stage, and we only test it on Python 3.6.0.

# Usage

1. Get game ID from [NBA Official Website](https://watch.nba.com/). You can find it from `masterAttribute.game` attribute located at the source of game page (e.g. [https://watch.nba.com/game/20170318/SACOKC](https://watch.nba.com/game/20170318/SACOKC)).

2. Run `python3 box.py [Game ID]`. For example,

    ```
    $ python3 box.py 0021601028
    ```

    On macOS, you can also pipe the result to clipboard with `pbcopy`,

    ```
    $ python3 box.py 0021601028 | pbcopy
    ```

    Then paste the result to the BBS.

# Demo

![](https://i.imgur.com/IQwqLxN.png)

![](https://i.imgur.com/RbxJJtw.png)

![](https://i.imgur.com/ox93zIo.png)

## Todo

- [ ] Overtime (OT) support
- [ ] Parse game ID from URL automatically