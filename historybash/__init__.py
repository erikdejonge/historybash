#!/usr/bin/env python3
# coding=utf-8
"""
History bash command search wrapper
license: gpl2

Usage:
  history.py [options] [<keyword>... ]

Options:
  -i --id       Show id
  -r --run      Run id
  -l --limitnum Limit results
  -h --help     Show this screen.
  -c --config   Show config

author  : rabshakeh (erik@a8.nl)
project : historybash
created : 29-06-15 / 14:53
"""
from __future__ import division, print_function, absolute_import, unicode_literals
from future import standard_library

import os
import hashlib
import sys
from arguments import Arguments
from Levenshtein import distance
from collections import deque
from pygments.lexers import guess_lexer, ClassNotFound
from pygments.lexers.python import PythonLexer
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments import highlight
from pygments.cmdline import main


class IArguments(Arguments):
    """
    IArguments
    """
    def __init__(self, doc):
        """
        __init__
        """
        self.config = False
        self.help = False
        self.id = False
        self.keyword = ""
        self.limitnum = False
        self.run = False
        super().__init__(doc)


def get_distance(command, previous_command):
    """
    @type command: str, unicode
    @type previous_command: str, unicode
    @return: None
    """
    previous_command = previous_command.strip()
    command = command.strip()

    # print("----")
    # print(previous_command)
    # print(command)
    dist = distance(previous_command, command)

    # print(dist)
    # print("----")
    diff = len(command) - len(previous_command)
    return dist, diff


def handle_history_item(cnt, colorize_from, hcnt, history_item, keyword, prev_cmds, previous_command, runid, samecnt, showid, defcolor, greyed_out_color):
    """
    @type cnt: int
    @type colorize_from: int
    @type hcnt: int
    @type history_item: str
    @type keyword: str
    @type prev_cmds: list
    @type previous_command: str
    @type runid: str
    @type samecnt: int
    @type showid: bool
    @type defcolor: int
    @type greyed_out_color: int
    @return: None
    """
    m = hashlib.md5()
    hil = history_item.lstrip().split(" ")
    m.update(str(hil[0:][0]).encode())

    # if m.hexdigest() not in st:
    command = " ".join(history_item.lstrip().split(" ")).strip()

    if keyword is not None and runid is False:
        if keyword not in command:
            command = ""

    command = command.strip()
    previous_command = previous_command.strip()

    if len(command.strip()) > 0:
        num = str(hcnt)
        dist, _ = get_distance(command, previous_command)
        maxdist = 15

        if len(command) < maxdist + 1:
            maxdist = len(command) // 2

        if " ".join(command.split()[:1]) in prev_cmds:
            samecnt += 1
            if samecnt == 2:
                print("\033[90m...\033[0m")
            elif samecnt < 2:
                print_item(num, command, showid, 93)

        elif 0 < dist < maxdist:
            samecnt = 0
            print_item(num, command, showid, greyed_out_color)
        else:
            samecnt = 0
            print_item(num, command, showid, defcolor)

        previous_command = command

        while len(prev_cmds) > 10:
            prev_cmds.popleft()

        if cnt > colorize_from:
            prev_cmds.append("".join(command.split()[:2]))

    return previous_command


def print_item(mid, command, showmid, colorcode):
    """
    @type mid: str
    @type command: str
    @type showmid: bool
    @type colorcode: int
    @return: None
    """
    command = command.replace("    ", " ")
    command = command.replace("   ", " ")
    command = command.replace("  ", " ")
    midcolor = 37
    if colorcode != 93:
        midcolor = 90

    maxlen = 500

    if len(command) >= maxlen:
        command2 = command[:maxlen] + "..." + str(len(command) - maxlen)
    else:
        command2 = command

    if showmid is True:
        print("\033[" + str(midcolor) + "m" + str(mid) + "  \033[" + str(colorcode) + "m" + command2, "\033[0m")
    else:
        if sys.stdout.isatty():

            print("\033[" + str(colorcode) + "m" + command2, "\033[0m")
        else:
            print(command2)


def main():
    """
    main
    """
    arguments = IArguments(__doc__)
    showid = arguments.id
    runid = arguments.run
    limitnum = arguments.limitnum
    keyword = " ".join(arguments.keyword).strip()

    if runid is True:
        try:
            keyword = int(keyword)
        except ValueError:

            print("\033[31minvalid number\033[0m", keyword)
            return

    if keyword:
        if len(str(keyword)) == 0:
            keyword = None
    if keyword:
        print(keyword)
    previous_command = ""
    prev_cmds = deque()
    try:
        sto = open(os.path.join(os.path.expanduser("~"), ".bash_history"), "rt").read()
    except UnicodeDecodeError:
        sto = open(os.path.join(os.path.expanduser("~"), ".bash_history"), "rb").read()
        sto = sto.decode(errors='replace')
    newstl = []
    stl = []

    for hi in str(sto).split("\n"):
        stl.append(hi)

    for hi in stl:
        if hi not in newstl:
            newstl.append(hi)

    stl = newstl

    if limitnum is not None:
        limitnum = int(limitnum)
        stl = stl[len(stl) - limitnum:]

    colorize_from = 0
    if colorize_from < 0:
        colorize_from = 0

    hcnt = 0
    default_color = 34
    greyed_out_color = 90
    configpath = os.path.join(os.path.expanduser("~"), ".historybashconfig")

    if os.path.exists(configpath):
        config = open(configpath, "rt").read()
        config = "#"+configpath+"\n"+config

        if arguments.config is True:
            try:
                lexer = guess_lexer(config)
            except ClassNotFound:
                lexer = PythonLexer()
            config = highlight(config, lexer, Terminal256Formatter(style='colorful'))
            for line in config.split("\n"):
               if line.strip():
                   print("\033[33m"+line.strip()+"\033[0m")

            return

        config = config.strip().split("\n")

        for line in config:
            if "default_color" in line:
                default_color = int(line.split("=")[-1])
            elif "greyed_out_color" in line:
                greyed_out_color = int(line.split("=")[-1])
    else:
        if arguments.config is True:
            print("\033[31m" + "no config found at", configpath, "\033[0m")

        config = open(configpath, "wt")
        config.write("default_color=" + str(default_color) + "\n")
        config.write("greyed_out_color=" + str(greyed_out_color) + "\n")

    if runid is True:
        for cnt, history_item in enumerate(stl):
            if len(history_item.strip()) > 0:
                hcnt += 1

                if hcnt == keyword:
                    print("\033[30m" + history_item + "\033[0m")

                    os.system(history_item)
    else:
        samecnt = 0

        for cnt, history_item in enumerate(stl):
            if len(history_item.strip()) > 0:
                hcnt += 1
                previous_command = handle_history_item(cnt, colorize_from, hcnt, history_item, keyword, prev_cmds, previous_command, runid, samecnt, showid, default_color, greyed_out_color)


standard_library.install_aliases()


if __name__ == "__main__":
    main()
