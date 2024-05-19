![Static Badge](https://img.shields.io/badge/Please_star_this-7289DA?style=for-the-badge)
<div align="center">
	<img src="src\images\logo.png" width="100">
</div>
# ShellScord

ShellScord is a Discord Client in your shell written in python powered by [Textual](https://github.com/Textualize/textual).

> [!CAUTION]
> Discord is trademark of Discord Inc. and solely mentioned for the sake of descriptivity. Mention of it does not imply any affiliation with or endorsement by Discord Inc.
> 
> Client modifications are **against Discord’s Terms of Service**.
>
> However, Discord is pretty indifferent about them and there are no known cases of users getting banned for using client mods! So generally you should be fine as long as you don't misuse ShellScord. But no worries, ShellScord is safe to use!
>
> Regardless, if your account is very important to you and it getting disabled would be a disaster for you, you should probably not use any client mods, just to be safe
>
> Additionally, make sure not to post screenshots with ShellScord in a server where you might get banned for it

# Changelog
Changelog can be found in the root directory of this repo as `CHANGELOG.md`.

# Contributing
Contributing guide can be found in the root directory of this repo as `CONTRIBUTORS.md`.

## Installation

Download the zip file from the latest release and extract it, or simply clone the repository using git.

> [!NOTE]  
> I only tested this project on Windows for now, but it should work on Linux and MacOS as well. If you encounter any issues, please let me know by creating an issue.

Using a Virtual Environment is recommended.

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

```bash
python .\src\main.py
```

To run textual in `dev mode`, you can use the following command:

```bash
# in a different terminal, to see the logs
textual console -x SYSTEM -x DEBUG -x EVENT

textual run --dev .\src\main.py
``` 

## How to login

1- Login to Discord on any web browser

2- Refresh the page (F5)

3- Do `Ctrl + Shift + I` (Or just right click and inspect element)

4- Go to Responsive Design Mode (Or if you're on Chrome, it's "Toggle
Device Toolbar") On Firefox it should be an icon with a phone and a
tablet, on Chrome a phone with a laptop

5- Go to local storage (on Chrome, go to Application and there should be
local storage)

6- In the filter tab, search "token"

<img src="src\images\token.png">

7- create a `.env` file in the root directory of the project and add the token:
    
```env
TOKEN=your_token_here
```

# Screenshots

<img src="src\images\screenshot.png">

# Thanks:

This project idea was given to me by [n1d3v/naticord](https://github.com/n1d3v/naticord), from which I based the discord requests and the form of the readme.

Please go look at his work 🙏