#!/usr/bin/env python3
# coding=utf-8
"""
history.py

Usage:
  history.py [options] [<keyword> <limitnum>]

Options:
  -i --id    Show id
  -r --run   Run id
  -h --help  Show this screen.
"""
import hashlib

from collections import deque

import os
import docopt
import stat
from Levenshtein import distance

from consoleprinter import forceascii
def get_distance(command, previous_command):
    """
    @type command: str, unicode
    @type previous_command: str, unicode
    @return: None
    """
    dist = distance(previous_command, command)
    diff = len(command) - len(previous_command)
    return dist, diff


def main():
    """
    main
    """
    arguments = docopt.docopt(__doc__)
    showid = arguments["--id"]
    runid = arguments["--run"]
    limitnum = arguments["<limitnum>"]
    keyword = arguments["<keyword>"]

    if runid is True:
        try:
            keyword = int(keyword)
        except ValueError:
            print("\033[31minvalid number\033[0m", keyword)
            return

    if keyword:
        if len(str(keyword)) == 0:
            keyword = None

    previous_command = ""
    prev_cmds = deque()
    sto = open(os.path.join(os.path.expanduser("~"), ".bash_history"), "rt").read()

    stl = str(sto).split("\n")

    if limitnum is not None:
        if limitnum.isdigit():
            limitnum = int(limitnum)
            stl = stl[len(stl) - limitnum:]

    colorize_from = 0
    if colorize_from < 0:
        colorize_from = 0

    hcnt = 0
    if runid is True:
        for cnt, history_item in enumerate(stl):
            if len(history_item.strip()) > 0:
                hcnt += 1
                if hcnt == keyword:
                    print("\033[30m" + history_item + "\033[0m")
                    # script = """
                    #     shopt -s expand_aliases
                    #     source ~/.bash_profile
                    #     """
                    # script += history_item
                    # script = "".join([x.strip()+"\n" for x in script.split("\n")]).strip()
                    # f = open("hscript.sh", "w")
                    # f.write(script)
                    # f.close()
                    #os.chmod("hscript.sh", stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
                    #os.system("./hscript.sh; rm ./hscript.sh")
                    os.system(history_item)


    else:
        for cnt, history_item in enumerate(stl):
            if len(history_item.strip()) > 0:
                hcnt += 1
                m = hashlib.md5()
                hil = history_item.lstrip().split(" ")
                m.update(str(hil[0:][0]).encode())

                # if m.hexdigest() not in st:
                command = " ".join(history_item.lstrip().split(" ")).strip()

                if keyword is not None and runid is False:
                    if keyword not in command:
                        command = ""

                if len(command.strip()) > 0:
                    num = str(hcnt)
                    dist, diff = get_distance(command, previous_command)
                    maxdist = 6

                    if len(command) < maxdist + 1:
                        maxdist = len(command) // 2

                    if "".join(command.split()[:2]) in prev_cmds:
                        if prev_cmds.count("".join(command.split()[:2])) < 2:
                            print_item(num, command, showid, 30)
                        else:
                            pass

                    elif 0 < dist < maxdist:
                        print_item(num, command, showid, 90)
                    else:
                        if len(command) > 160:
                            cmdt = ""
                            linebreakcnt = 0

                            for command_item in command:
                                if linebreakcnt > 100:
                                    linebreakcnt = 0
                                    cmdt += "\\\n"

                                cmdt += command_item

                                # cmdt += " "
                                linebreakcnt += 1

                            command = cmdt.replace("\t  \\\n", "")
                            print_item(num, command, showid, 93)
                        else:
                            print_item(num, command, showid, 93)

                    previous_command = command

                    while len(prev_cmds) > 10:
                        prev_cmds.popleft()

                    if cnt > colorize_from:
                        prev_cmds.append("".join(command.split()[:2]))


def print_item(mid, command, showmid, colorcode):
    """
    @type mid: str
    @type command: str
    @type showmid: bool
    @type colorcode: int
    @return: None
    """
    midcolor = 37
    if colorcode != 93:
        midcolor = 90

    if showmid is True:
        print("\033[" + str(midcolor) + "m" + str(mid) + "  \033[" + str(colorcode) + "m" + command, "\033[0m")
    else:
        print("\033[" + str(colorcode) + "m" + command, "\033[0m")

# Erik de Jonge
# erik@a8.nl

# license: gpl2


if __name__ == "__main__":
    main()
