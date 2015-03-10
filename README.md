# history
Bash history command colorized on levenshtein distance of last 10 commands

The history command is measured against the previous command in the list and it it's the same or almost the same it's printed in grey. Duplicates are also grey.

###.bash_profile
```bash
# Avoid duplicates
export HISTCONTROL=ignoredups:erasedups

# When the shell exits, append to the history file instead of overwriting it
shopt -s histappend

# After each command, append to the history file and reread it
export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

#alias to script
alias hist='python ~/workspace/history/history.py'
```
  

###screenshot
![history](https://raw.githubusercontent.com/erikdejonge/history/master/res/history.png)
