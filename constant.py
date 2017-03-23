BOX_URL_TEMPLATE = "https://neulionmdnyc-a.akamaihd.net/fs/nba/feeds_s2012/stats/2016/boxscore/%s.js?%d"

TEAM_DICT = {
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "NYK": "New York Knicks",
    "PHI": "Philadelphia 76ers",
    "TOR": "Toronto Raptors",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DET": "Detroit Pistons",
    "IND": "Indiana Pacers",
    "MIL": "Milwaukee Bucks",
    "ATL": "Atlanta Hawks",
    "CHA": "Charlotte Hornets",
    "MIA": "Miami Heat",
    "ORL": "Orlando Magic",
    "WAS": "Washington Wizards",
    "GSW": "Golden State Warriors",
    "LAC": "LA Clippers",
    "LAL": "Los Angeles Lakers",
    "PHX": "Phoenix Suns",
    "SAC": "Sacramento Kings",
    "DAL": "Dallas Mavericks",
    "HOU": "Houston Rockets",
    "MEM": "Memphis Grizzlies",
    "NOP": "New Orleans Pelicans",
    "SAS": "San Antonio Spurs",
    "DEN": "Denver Nuggets",
    "MIN": "Minnesota Timberwolves",
    "OKC": "Oklahoma City Thunder",
    "POR": "Portland Trail Blazers",
    "UTA": "Utah Jazz"
}

class BoxColors(object):
    CONTROL = '\033'
    ENDC = '\033[0m'
    ESC = '\033'
    CTRLU = '\x15'

    STATS_HEADER = '[1;33;44m'
    HOME_FRAME = '[1;31m'
    HOME_HEADER = '[1;33;41m'
    VISITOR_FRAME = '[1;35m'
    VISITOR_HEADER = '[1;33;45m'
    WHITE = '[1;37m'
    GREEN = '[1;32m'
    YELLOW = '[1;33m'
    CYAN = '[1;36m'
    RED = '[1;31m'
    DARK_GREEN = '[32m'

    END = '[0m'

    @classmethod
    def set_control_code(cls, code):
        if code not in [cls.ESC, cls.CTRLU]:
            return

        cls.CONTROL = code
        cls.ENDC = cls.CONTROL + cls.END

    @classmethod
    def get_color_code(cls, color):
        return cls.CONTROL + color
