# Lineups from flashscore.com
Lineups - GUI application to get a squad information of playing teams from flashscore.com:
 - players are in starting lineup (green color) ;
 - players are on the bench (yellow color) ;
 - missing players (red color).

![Demo 1](https://github.com/nikolaitolmachev/lineups_flashscore/raw/main/Flags/screen_1.jpg)

It can be helpful to rate both teams.

## How to install ?
It is a python (3.6) application, so you need have installed it on your PK.

Clone the repository:
```
https://github.com/nikolaitolmachev/lineups_flashscore.git
```

Upgrade pip:
```
python3 -m pip install --upgrade pip
```

Install libs:
```
pip install -r requirements.txt
```

Also can create exe, for example, using PyInstaller:
```
pyinstaller -F -w --icon=Flags/icon_1.ico --noconsole main.py
```

### Prerequisites

Flashscore.com is protected of simple bots so Lineups uses Selenium (Chrome browser) to scrape a data.
So you need download chrome driver from https://chromedriver.chromium.org/downloads which corresponding version of your Chrome.
Put this file of driver to folder where Chrome is installed.
Copy path to this file of driver and paste in settings.ini.

It must have two folders to correct work:
 - Flags (contains list of flags in png - to show flag of player nationality)
 - Logos (empty by default - to download logos of teams and show it);

And simple file - settings.ini.

## How to use ?

It is easier than you think: just put on text field a URL of match from flashcore.com which you need and enjoy.

![Demo 2](https://github.com/nikolaitolmachev/lineups_flashscore/raw/main/Flags/screen_2.jpg)


## GL!
