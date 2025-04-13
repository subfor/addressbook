Contacts & Notes Help-a-bot
===========================


Installation instructions
-------------------------

Requirements: Python 3.12 or higher

These are the instructions for installing and running the bot

### First run

Here we clone repository into a local folder and install required dependencies before running the bot

```shell
# start a shell in the directory where you will want to have bot files

# clones this repository in directory "./addressbook"
git clone https://github.com/subfor/addressbook.git

# go into directory with cloned repository
cd addressbook

# initialize python virtual environment in "./.venv" directory
python -m venv ./.venv

# activate virtual environment
# Linux/macOS, using Bash
source ./.venv/bin/activate
# activate through PowerShell (Windows)
.\.venv\Scripts\Activate.ps1

# detailed doc on virtual environment is here: https://docs.python.org/3/library/venv.html

# install required dependencies
pip install -r requirements.txt

# run bot
python bot.py
```

### Next runs

We run the bot from a previously cloned directory

```shell
# start a shell in the directory where you cloned the bot file

# activates virtual environment
# Linux/macOS, using Bash
source ./.venv/bin/activate
# Windows, using powershell
.\.venv\Scripts\Activate.ps1

# detailed doc on virtual environment is here: https://docs.python.org/3/library/venv.html

# run bot
python bot.py
```
