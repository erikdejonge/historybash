#!/usr/bin/env python3
# coding=utf-8
"""
History bash command search wrapper
license: gpl2

Usage:
  history.py [options] [<keyword>... ]

Options:
  -f --forcecolor Force colored output
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
from builtins import super
from builtins import open
from builtins import int
from builtins import str
from future import standard_library

import os
import hashlib
import sys
import pickle
from arguments import Arguments
from Levenshtein import distance
from collections import deque
from pygments.lexers import guess_lexer, ClassNotFound
from pygments.lexers.python import PythonLexer
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments import highlight
from pygments.cmdline import main

def isnumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def mystr(s):
    if isnumber(s):
        s = str(s)
    s = s.encode('ascii', 'replace').decode('ascii')
    return s

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
        self.forcecolor = False
        super().__init__(doc)


def get_distance(command, previous_command):
    """
    @type command: mystr, unicode
    @type previous_command: mystr, unicode
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


def handle_history_item(cnt, colorize_from, hcnt, history_item, keyword, prev_cmds, previous_command, runid, samecnt, showid, defcolor, greyed_out_color, forcecolor):
    """
    @type cnt: int
    @type colorize_from: int
    @type hcnt: int
    @type history_item: mystr
    @type keyword: mystr
    @type prev_cmds: list
    @type previous_command: mystr
    @type runid: mystr
    @type samecnt: int
    @type showid: bool
    @type defcolor: int
    @type greyed_out_color: int
    @return: None
    """
    m = hashlib.md5()
    hil = history_item.lstrip().split(" ")
    m.update(mystr(hil[0:][0]).encode())

    # if m.hexdigest() not in st:
    command = " ".join(history_item.lstrip().split(" ")).strip()

    if keyword is not None and runid is False:
        if keyword not in command:
            command = ""

    command = command.strip()
    previous_command = previous_command.strip()

    if len(command.strip()) > 0:
        num = mystr(hcnt)
        dist, _ = get_distance(command, previous_command)
        maxdist = 15

        if len(command) < maxdist + 1:
            maxdist = len(command) // 2

        if " ".join(command.split()[:1]) in prev_cmds:
            samecnt += 1
            if samecnt == 2:
                print("\033[90m...\033[0m")
            elif samecnt < 2:
                print_item(num, command, showid, 93, forcecolor)

        elif 0 < dist < maxdist:
            samecnt = 0
            print_item(num, command, showid, greyed_out_color, forcecolor)
        else:
            samecnt = 0
            print_item(num, command, showid, defcolor, forcecolor)

        previous_command = command

        while len(prev_cmds) > 10:
            prev_cmds.popleft()

        if cnt > colorize_from:
            prev_cmds.append("".join(command.split()[:2]))

    return previous_command


def print_item(mid, command, showmid, colorcode, forcecolor):
    """
    @type mid: mystr
    @type command: mystr
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
        command2 = command[:maxlen] + "..." + mystr(len(command) - maxlen)
    else:
        command2 = command

    if showmid is True:
        print("\033[" + mystr(midcolor) + "m" + mystr(mid) + "  \033[" + mystr(colorcode) + "m" + command2, "\033[0m")
    else:
        if forcecolor:
            print("\033[" + mystr(colorcode) + "m" + command2, "\033[0m")
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

    if not arguments.forcecolor:
        forcecolor = sys.stdout.isatty()
    else:
        forcecolor = True

    if runid is True:
        try:
            keyword = int(keyword)
        except ValueError:

            print("\033[31minvalid number\033[0m", keyword)
            return

    if keyword:
        if len(mystr(keyword)) == 0:
            keyword = None
    previous_command = ""
    prev_cmds = deque()
    try:
        sto = open(os.path.join(os.path.expanduser("~"), ".bash_history"), "rt", encoding='utf-8').read()
    except UnicodeDecodeError:
        raise
        #sto = open(os.path.join(os.path.expanduser("~"), ".bash_history"), "rb").read()
        #sto = sto.decode(errors='replace')
    newstl = []
    stl = []

    for hi in mystr(sto).split("\n"):
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
        config = open(configpath, "rt", encoding='utf-8').read()
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

        config = open(configpath, "wt", encoding='utf-8')
        config.write("default_color=" + mystr(default_color) + "\n")
        config.write("greyed_out_color=" + mystr(greyed_out_color) + "\n")
    hcache = os.path.expanduser("~/.historybashstl")
    if runid is True:
        if os.path.exists(hcache):
            stl = pickle.load(open(hcache, "rb"))

        for cnt, history_item in enumerate(stl):
            if len(history_item.strip()) > 0:
                hcnt += 1

                if hcnt == keyword:
                    print("\033[30m" + history_item + "\033[0m")

                    os.system(history_item)
    else:
        pickle.dump(stl, open(hcache, "wb"))
        samecnt = 0

        for cnt, history_item in enumerate(stl):
            if len(history_item.strip()) > 0:
                hcnt += 1

                previous_command = handle_history_item(cnt, colorize_from, hcnt, history_item, keyword, prev_cmds, previous_command, runid, samecnt, showid, default_color, greyed_out_color, forcecolor)


standard_library.install_aliases()


if __name__ == "__main__":
    main()
