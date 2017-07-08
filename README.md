RamboBoxGen
===========

RamboBoxGen is a utility for generating Rambo-style Box Score for NBA games, with ANSI color highlighting optimized for [Ptt BBS](https://www.ptt.cc/).

# Usage

1. Get game ID from [NBA Official Website](https://watch.nba.com/). You can find it from `masterAttribute.game` attribute located at the source of game page (e.g. [https://watch.nba.com/game/20170318/SACOKC](https://watch.nba.com/game/20170318/SACOKC)).

2. Run `python3 box.py [-h] [-s season] [-c {esc,ctrlu}] game_id`. For example,

    ```
    $ python3 box.py -s 2016 0021601028
    ```

    The default value of argument `season` is set based on today's date. For 2016-17 season, please use 2016. July 1st is regarded as the start of the new season.

    Optional argument `-c=ctrlu` will replace ANSI control code `ESC` with `CTRL-U`. For Nally and Welly on macOS, we recommend you to set this option.

    For convenience, you can also pipe the result to clipboard directly,

    ```
    $ python3 box.py 0021601028 -c=ctrlu | pbcopy   # for Welly on macOS
    $ python3 box.py 0021601028 | clip.exe   # for PCMan on Windows
    ```

    Then, paste the result to the BBS.

# Demo

![](https://i.imgur.com/IQwqLxN.png)

![](https://i.imgur.com/RbxJJtw.png)

![](https://i.imgur.com/ox93zIo.png)
