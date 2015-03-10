#!/usr/bin/env python3
# coding=utf-8
"""
history.py

Usage:
  history.py [<keyword> <limitnum>]

Options:
  -h --help             Show this screen.
"""

# Erik de Jonge
# erik@a8.nl
# license: gpl2

import hashlib
import docopt
from subprocess import Popen, PIPE, STDOUT
from Levenshtein import distance
from collections import deque


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
    sto = sto.decode("utf-8")
    previous_command = ""
    prev_cmds = deque()
    stl = str(sto).split("\n")

    if limitnum is not None:
        if limitnum.isdigit():
            limitnum = int(limitnum)
            stl = stl[len(stl) - limitnum:]

    colorize_from = len(stl) - 40
    if colorize_from < 0:
        colorize_from = 0

    hist_item_cnt = 0

    for history_item in stl:
        hist_item_cnt += 1

        if len(history_item.strip()) > 0:
            m = hashlib.md5()
            m.update(str(history_item.split(" ")[4:][0]).encode())

            # if m.hexdigest() not in st:
            command = " ".join(history_item.split(" ")[4:]).strip()
            num = " ".join(history_item.split(" ")[:4]).strip()
            dist, diff = get_distance(command, previous_command)

            for prevcmd in prev_cmds:
                dist2, diff2 = get_distance(command, prevcmd)

                if dist2 < dist:
                    dist = dist2
                    diff = diff2

            maxdist = 3

            if len(command) < maxdist:
                maxdist = len(command)
                dist += 1

            prev_cmds_digest = [hashlib.md5(str(x.split(" ")[4:][0]).encode()).hexdigest() for x in prev_cmds if len(x.split(" ")) > 4]

            # print dist, maxdist, m.hexdigest(), prev_cmds_digest
            prev_cmds_parsed = [" ".join(x.split(" ")[4:]) for x in prev_cmds if len(x.split(" ")) > 4]

            # print command, prev_cmds_parsed[len(prev_cmds_parsed)//2:]

            if dist < maxdist:
                print("\033[90m" + command, "\033[0m")
            elif command in prev_cmds_parsed[len(prev_cmds_parsed) // 2:]:
                print("\033[30m" + command, "\033[0m")  # , dist, diff, m.hexdigest() not in st
            else:
                if len(command) > 100:
                    cmdt = ""
                    cnt = 0

                    for command_item in command:
                        if cnt > 100:
                            cnt = 0
                            cmdt += "\\\n"

                        cmdt += command_item
                        #cmdt += " "
                        cnt += 1

                    command = cmdt.replace("\t  \\\n", "")

                print("\033[33m" + command, "\033[0m")  # , dist, diff, m.hexdigest()

            previous_command = command

            while len(prev_cmds) > 30:
                prev_cmds.popleft()

            if hist_item_cnt > colorize_from:
                prev_cmds.append(history_item)


if __name__ == "__main__":
    main()
