import sys
import time
import json
import argparse
import urllib.request
from constant import BOX_URL_TEMPLATE, TEAM_DICT, BoxColors

def download_box_json(gameid):
    url = BOX_URL_TEMPLATE % (gameid, int(time.time() * 1000.0))
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode("utf-8")

    return json.loads(text[15:])

def colorize(content, color):
    return BoxColors.get_color_code(color) + content + BoxColors.ENDC

def print_blank_line(count=1):
    print("\n" * count, end='')

def print_box(box):
    quarters = ["1st", "2nd", "3rd", "4th"]
    for i in range(box["score"]["periodTime"]["period"] - 4):
        quarters.append("OT" + str(i + 1))

    print("      " + "   ".join(quarters) + "   FINAL")
    print_box_team(box, home=False)
    print_box_team(box, home=True)

def print_box_team(box, home=True):
    team = "home" if home else "visitor"
    line = box["score"][team]["id"].ljust(6)
    line += "   ".join(list(map(lambda s: str(s).rjust(3), box["score"][team]["qScore"])))
    line += "    "
    line += str(box["score"][team]["score"]).rjust(3)

    if home:
        print(colorize(line, BoxColors.YELLOW))
    else:
        print(colorize(line, BoxColors.GREEN))

def print_arena_stats(box):
    print(colorize("ARENA STATS                   ", BoxColors.STATS_HEADER))
    print("Arena: " + colorize(box["arena"], BoxColors.CYAN))
    print("       " + colorize(box["location"], BoxColors.CYAN))
    print("Attendance: " + colorize(str(box["attendance"]), BoxColors.CYAN))
    print("Duration:   " + colorize(box["duration"], BoxColors.CYAN))

def print_scoring_stats(box):
    print(colorize("SCORING                       ", BoxColors.STATS_HEADER))
    print("Lead Changes: " + colorize(str(box["score"]["stats"]["leadChanges"]), BoxColors.CYAN))
    print("Times Tied:   " + colorize(str(box["score"]["stats"]["tied"]), BoxColors.CYAN))

def print_frame(line, home=True):
    if home:
        print(colorize(line, BoxColors.HOME_FRAME))
    else:
        print(colorize(line, BoxColors.VISITOR_FRAME))

def print_top_frame(home=True):
    print_frame("┌─────────────────────────────────────┐", home)

def print_divider(home=True):
    print_frame("├─────────────────────────────────────┤", home)

def print_bottom_frame(home=True):
    print_frame("└─────────────────────────────────────┘", home)

def print_with_side_frame(line, home=True):
    frame = ""
    if home:
        frame = colorize("│", BoxColors.HOME_FRAME)
    else:
        frame = colorize("│", BoxColors.VISITOR_FRAME)

    print(frame + line + frame)

def print_header_team(box, home):
    team = "home" if home else "visitor"
    line = get_team_name(box["score"][team]["id"])

    if home:
        line += (" (" + box["stats"]["home"]["hr"] + ")")
    else:
        line += (" (" + box["stats"]["visitor"]["vr"] + ")")

    line = line.ljust(34) + "◢███████████████████"
    line = colorize(line, BoxColors.YELLOW)

    print_with_side_frame(line, home)

def print_header_players(home):
    line = "PLAYERS      MIN  FGM-A 3PM-A FTM-A +/- OR DR TR AS PF ST TO BS BA PTS EFF"
    if home:
        line = colorize(line, BoxColors.HOME_HEADER)
    else:
        line = colorize(line, BoxColors.VISITOR_HEADER)

    print_with_side_frame(line, home)

def print_header_total(home):
    line = " MIN  FGM-A 3PM-A FTM-A     OR DR TR AS PF ST TO BS BA PTS    "
    if home:
        line = colorize(line, BoxColors.HOME_HEADER)
    else:
        line = colorize(line, BoxColors.VISITOR_HEADER)
    line = "            " + line

    print_with_side_frame(line, home)

def print_player_stats(box, home):
    team = "home" if home else "visitor"

    for player in box["stats"][team]["players"]:
        if is_player_dnp(player):
            content = get_player_name(player, True)
            content += " "
            content += (" " + colorize("DNP", BoxColors.DARK_GREEN) + " ")
            content = content.ljust(92)
            print_with_side_frame(content, home)
            continue

        content = " ".join([
            get_player_name(player),
            get_player_minutes(player),
            get_player_fg(player),
            get_player_3pt(player),
            get_player_ft(player),
            get_player_pm(player),
            get_player_oreb(player),
            get_player_dreb(player),
            get_player_treb(player),
            get_player_ast(player),
            get_player_pf(player),
            get_player_stl(player),
            get_player_to(player),
            get_player_bs(player),
            get_player_ba(player),
            get_player_pts(player),
            get_player_eff(player)
        ])

        print_with_side_frame(content, home)

def print_total_stats(box, home):
    team = "home" if home else "visitor"
    team = box["stats"][team]["team"]

    content = ""
    if home:
        content = colorize("TOTAL", BoxColors.HOME_HEADER)
    else:
        content = colorize("TOTAL", BoxColors.VISITOR_HEADER)
    content += "       "
    content += " ".join([
        get_team_minutes(team),
        get_team_fg(team),
        get_team_3pt(team),
        get_team_ft(team),
        "   ",
        get_team_oreb(team),
        get_team_dreb(team),
        get_team_treb(team),
        get_team_ast(team),
        get_team_pf(team),
        get_team_stl(team),
        get_team_to(team),
        get_team_bs(team),
        get_team_ba(team),
        get_team_pts(team)
    ])
    content += "    "

    print_with_side_frame(content, home)

    content = "                  "
    content += " ".join([
        get_team_fg_percentage(team),
        get_team_3pt_percentage(team),
        get_team_ft_percentage(team)
    ])
    content += "                                       "

    print_with_side_frame(content, home)

def get_player_name(player, dnp=False):
    name = ""
    is_starter = True if player["spos"] != "" else False
    name_limit = 9 if is_starter else 11

    if player["fn"] != "" and len(player["ln"]) <= name_limit - 2:
        name = player["fn"][0] + "." + player["ln"]
    else:
        name = player["ln"]

    name = name.ljust(name_limit) if len(name) <= name_limit else name[:name_limit]

    if is_starter:
        name = colorize(name, BoxColors.WHITE) + " " + player["spos"]
    elif dnp:
        name = colorize(name, BoxColors.DARK_GREEN)

    return name

def get_player_minutes(player):
    return str(player["min"]).zfill(2) + ":" + str(player["sec"]).zfill(2)

def get_player_fg(player):
    fg = str(player["fgm"]) + "-" + str(player["fga"])
    fg = fg.rjust(5)

    if player["fga"] == 0:
        return fg

    fgp = player["fgm"] / player["fga"]
    if player["fgm"] == player["fga"]:
        fg = colorize(fg, BoxColors.RED)
    elif fgp >= 0.67:
        fg = colorize(fg, BoxColors.YELLOW)
    elif fgp <= 0.33:
        fg = colorize(fg, BoxColors.GREEN)

    return fg

def get_player_3pt(player):
    tp = str(player["tm"]) + "-" + str(player["ta"])
    tp = tp.rjust(5)

    if player["ta"] == 0:
        return tp

    tpp = player["tm"] / player["ta"]
    if player["tm"] == player["ta"]:
        tp = colorize(tp, BoxColors.RED)
    elif tpp >= 0.6:
        tp = colorize(tp, BoxColors.YELLOW)
    elif tpp <= 0.25:
        tp = colorize(tp, BoxColors.GREEN)

    return tp

def get_player_ft(player):
    ft = str(player["ftm"]) + "-" + str(player["fta"])
    ft = ft.rjust(5)

    if player["fta"] == 0:
        return ft

    ftp = player["ftm"] / player["fta"]
    if player["ftm"] == player["fta"]:
        ft = colorize(ft, BoxColors.RED)
    elif ftp < 0.5:
        ft = colorize(ft, BoxColors.YELLOW)
    elif player["ftm"] == 0:
        ft = colorize(ft, BoxColors.GREEN)

    return ft

def get_player_pm(player):
    sign = "+" if player["pm"] >= 0 else "-"
    pm = str(abs(player["pm"])).rjust(2)
    return sign + pm

def get_player_oreb(player):
    return str(player["or"]).rjust(2)

def get_player_dreb(player):
    return str(player["dr"]).rjust(2)

def get_player_treb(player):
    treb = str(player["or"] + player["dr"])
    treb = treb.rjust(2)

    if player["or"] + player["dr"] >= 10:
        treb = colorize(treb, BoxColors.RED)

    return treb

def get_player_ast(player):
    ast = str(player["a"])
    ast = ast.rjust(2)

    if player["a"] >= 10:
        ast = colorize(ast, BoxColors.RED)

    return ast

def get_player_pf(player):
    pf = str(player["f"]).rjust(2)

    if player["f"] == 6:
        pf = colorize(pf, BoxColors.GREEN)

    return pf

def get_player_stl(player):
    stl = str(player["s"]).rjust(2)
    if player["s"] >= 4:
        stl = colorize(stl, BoxColors.RED)

    return stl

def get_player_to(player):
    to = str(player["to"]).rjust(2)

    if player["to"] == 0:
        to = colorize(to, BoxColors.RED)
    elif player["to"] >= 10:
        to = colorize(to, BoxColors.GREEN)

    return to

def get_player_bs(player):
    bs = str(player["b"]).rjust(2)

    if player["b"] >= 4:
        bs = colorize(bs, BoxColors.RED)

    return bs

def get_player_ba(player):
    ba = str(player["ba"]).rjust(2)

    if player["ba"] >= 4:
        ba = colorize(ba, BoxColors.GREEN)

    return ba

def get_player_pts(player):
    pts = str(player["p"])
    pts = pts.rjust(3)

    if player["p"] >= 30:
        pts = colorize(pts, BoxColors.RED)
    elif player["p"] >= 20:
        pts = colorize(pts, BoxColors.YELLOW)

    return pts

def get_player_eff(player):
    val = (player["p"] + player["or"] + player["dr"] + player["a"] + player["s"] + player["b"]) - (player["fga"] - player["fgm"]) - (player["fta"] - player["ftm"]) - player["to"]
    eff = str(val).rjust(3)

    if val >= 20:
        eff = colorize(eff, BoxColors.RED)
    elif val < 0:
        eff = colorize(eff, BoxColors.GREEN)

    return eff

def get_team_minutes(team):
    return " " + str(team["min"]) + " "

def get_team_fg(team):
    return str(team["fgm"]) + "-" + str(team["fga"])

def get_team_3pt(team):
    tp = str(team["tm"]) + "-" + str(team["ta"])
    return colorize(tp.rjust(5), BoxColors.GREEN)

def get_team_ft(team):
    ft = str(team["ftm"]) + "-" + str(team["fta"])
    return colorize(ft.rjust(5), BoxColors.CYAN)

def get_team_oreb(team):
    oreb = str(team["or"])
    return colorize(oreb.rjust(2), BoxColors.YELLOW)

def get_team_dreb(team):
    dreb = str(team["dr"])
    return colorize(dreb.rjust(2), BoxColors.YELLOW)

def get_team_treb(team):
    treb = str(team["or"] + team["dr"])
    return colorize(treb.rjust(2), BoxColors.YELLOW)

def get_team_ast(team):
    ast = str(team["a"])
    return colorize(ast.rjust(2), BoxColors.CYAN)

def get_team_pf(team):
    return str(team["f"]).rjust(2)

def get_team_stl(team):
    return str(team["s"]).rjust(2)

def get_team_to(team):
    return str(team["to"]).rjust(2)

def get_team_bs(team):
    return str(team["b"]).rjust(2)

def get_team_ba(team):
    return str(team["ba"]).rjust(2)

def get_team_pts(team):
    return str(team["p"]).rjust(3)

def get_team_fg_percentage(team):
    p = team["fgm"] / team["fga"] * 100.0
    return colorize(("%.1f" % (p)).ljust(4) + "%", BoxColors.RED)

def get_team_3pt_percentage(team):
    p = team["tm"] / team["ta"] * 100.0
    return colorize(("%.1f" % (p)).ljust(4) + "%", BoxColors.GREEN)

def get_team_ft_percentage(team):
    p = team["ftm"] / team["fta"] * 100.0
    return colorize(("%.1f" % (p)).ljust(4) + "%", BoxColors.YELLOW)

def get_team_name(team):
    if team in TEAM_DICT:
        return TEAM_DICT[team]
    else:
        return team

def is_player_dnp(player):
    return player["min"] == 0 and player["sec"] == 0

def print_team_box(box, home=True):
    print_top_frame(home)
    print_header_team(box, home)
    print_header_players(home)
    print_divider(home)
    print_player_stats(box, home)
    print_divider(home)
    print_header_total(home)
    print_total_stats(box, home)
    print_bottom_frame(home)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("game_id", help="Game ID from https://watch.nba.com")
    parser.add_argument("--bbs", help="Use CTRL-U for ANSI color control", action="store_true")
    args = parser.parse_args()

    if args.bbs:
        BoxColors.set_control_code(BoxColors.CTRLU)

    try:
        box_json = download_box_json(args.game_id)
    except:
        print("Error: cannot download the box")
        sys.exit()

    print_blank_line(3)
    print_box(box_json)
    print_blank_line(3)

    print_arena_stats(box_json)
    print_blank_line(2)
    print_scoring_stats(box_json)
    print_blank_line(4)

    print_team_box(box_json, home=False)
    print_blank_line()
    print_team_box(box_json, home=True)
