#!/usr/bin/env python3
# coding=utf-8
"""
history.py

Usage:
  history.py [options] [<keyword> <limitnum>]

Options:
  -i --id   Show id
  -h --help  Show this screen.
"""
import docopt
import hashlib

from Levenshtein import distance
from collections import deque
from subprocess import PIPE, Popen, STDOUT


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
    limitnum = arguments["<limitnum>"]
    keyword = arguments["<keyword>"]

    if keyword:
        if len(keyword) == 0:
            keyword = None

    shell_command = 'bash -i -c "history -r; history"'

    if keyword:
        shell_command = 'bash -i -c "history -r; history|grep ' + keyword + '"'
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    sto, ste = event.communicate()
    sto = sto.decode()
    previous_command = ""
    prev_cmds = deque()
    stl = str(sto).split("\n")

    if limitnum is not None:
        if limitnum.isdigit():
            limitnum = int(limitnum)
            stl = stl[len(stl) - limitnum:]

    colorize_from = 0
    if colorize_from < 0:
        colorize_from = 0

    hist_item_cnt = 0

    for cnt, history_item in enumerate(stl):
        hist_item_cnt += 1

        if len(history_item.strip()) > 0:
            m = hashlib.md5()
            hil = history_item.lstrip().split(" ")
            m.update(str(hil[1:][0]).encode())

            # if m.hexdigest() not in st:
            command = " ".join(history_item.lstrip().split(" ")[1:]).strip()
            num = " ".join(history_item.lstrip().split(" ")[:1]).strip()
            dist, diff = get_distance(command, previous_command)
            maxdist = 6

            if len(command) < maxdist + 1:
                maxdist = len(command) // 2

            if "".join(command.split()[:2]) in prev_cmds:
                if prev_cmds.count("".join(command.split()[:2])) < 2:
                    print_item(num, command, showid, 30)

                # if prev_cmds.count(command.split()[:3]) < 6:
                #    print_item(num, command, showid, 90)
                else:
                    pass

            elif 0 < dist < maxdist:
                print_item(num, command, showid, 90)
            else:
                if len(command) > 160:
                    cmdt = ""
                    cnt = 0

                    for command_item in command:
                        if cnt > 100:
                            cnt = 0
                            cmdt += "\\\n"

                        cmdt += command_item

                        # cmdt += " "
                        cnt += 1

                    command = cmdt.replace("\t  \\\n", "")
                    print_item(num, command, showid, 93)
                else:
                    print_item(num, command, showid, 93)

            previous_command = command

            while len(prev_cmds) > 10:
                prev_cmds.popleft()

            if hist_item_cnt > colorize_from:
                prev_cmds.append("".join(command.split()[:2]))


def print_item(id, command, showid, colorcode):
    """
    @type id: str
    @type command: str
    @type showid: bool
    @type colorcode: int
    @return: None
    """
    idcolor = 37
    if colorcode != 93:
        idcolor = 90

    if showid is True:
        print("\033[" + str(idcolor) + "m" + str(id) + "  \033[" + str(colorcode) + "m" + command, "\033[0m")
    else:
        print("\033[" + str(colorcode) + "m" + command, "\033[0m")

# Erik de Jonge
# erik@a8.nl

# license: gpl2


if __name__ == "__main__":
    main()
