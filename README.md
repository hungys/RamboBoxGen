RamboBoxGen
===========

RamboBoxGen is a utility for generating Rambo-style Box Score for NBA games, with ANSI color highlighting optimized for [Ptt BBS](https://www.ptt.cc/).

# Usage

1. Get game ID from [NBA Official Website](https://watch.nba.com/). You can find it from `masterAttribute.game` attribute located at the source of game page (e.g. [https://watch.nba.com/game/20170318/SACOKC](https://watch.nba.com/game/20170318/SACOKC)).

2. Run `python3 box.py [-h] [-c {esc,ctrlu}] game_id`. For example,

    ```
    $ python3 box.py 0021601028
    ```

    Optional argument `-c=ctrlu` will replace ANSI control code `ESC` with `CTRL-U`. For Nally and Welly on macOS, we recommend you to set this option.

    For convenience, you can also pipe the result to clipboard directly,

    ```
    $ python3 box.py 0021601028 -c=ctrlu | pbcopy   # for macOS
    $ python3 box.py 0021601028 | clip.exe   # for Windows
    ```

    Then paste the result to the BBS.

# Demo

![](https://i.imgur.com/IQwqLxN.png)

![](https://i.imgur.com/RbxJJtw.png)

![](https://i.imgur.com/ox93zIo.png)
