<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/logo.png" alt="Surf_TG" style="height:20%; width:50%;"><br>
    <i>Python Web App which Indexes a Your Telegram Channel and Serves its Files for Download and Stream.</i>
</div>


<div align="center" >

[![](https://img.shields.io/github/repo-size/weebzone/Surf-TG?color=green&label=Repo%20Size&labelColor=292c3b)](#) [![](https://img.shields.io/github/commit-activity/m/weebzone/Surf-TG?logo=github&labelColor=292c3b&label=Github%20Commits)](#) [![](https://img.shields.io/github/license/weebzone/Surf-TG?style=flat&label=License&labelColor=292c3b)](#)|[![](https://img.shields.io/github/issues-raw/weebzone/Surf-TG?style=flat&label=Open%20Issues&labelColor=292c3b)](#) [![](https://img.shields.io/github/issues-closed-raw/weebzone/Surf-TG?style=flat&label=Closed%20Issues&labelColor=292c3b)](#) [![](https://img.shields.io/github/issues-pr-raw/weebzone/Surf-TG?style=flat&label=Open%20Pull%20Requests&labelColor=292c3b)](#) [![](https://img.shields.io/github/issues-pr-closed-raw/weebzone/Surf-TG?style=flat&label=Closed%20Pull%20Requests&labelColor=292c3b)](#)
:---:|:---:|
[![](https://img.shields.io/github/languages/count/weebzone/Surf-TG?style=flat&label=Total%20Languages&labelColor=292c3b&color=blueviolet)](#) [![](https://img.shields.io/github/languages/top/weebzone/Surf-TG?style=flat&logo=python&labelColor=292c3b)](#) [![](https://img.shields.io/github/last-commit/weebzone/Surf-TG?style=flat&label=Last%20Commit&labelColor=292c3b&color=important)](#) [![](https://badgen.net/github/branches/weebzone/Surf-TG?label=Total%20Branches&labelColor=292c3b)](#)|[![](https://img.shields.io/github/forks/weebzone/Surf-TG?style=flat&logo=github&label=Forks&labelColor=292c3b&color=critical)](#) [![](https://img.shields.io/github/stars/weebzone/Surf-TG?style=flat&logo=github&label=Stars&labelColor=292c3b&color=yellow)](#) |

</div>



## ***Features*** 📑

- Multi Channel Index 📡
- Thumbnail Support (Channel Profile) 🖼️
- Search Support 🔍
- Login support 🔐
- Faster Resumeable Download Link ⏩
- Stream Video Support 📺
- 25 Website Themes (Bootswatch) 🎨

### ***To-Do*** 📦

- [ ] API Support 🛠️
- [ ] Database Support 💾
- [ ] Playlist Creator Support 📀

## ***Website Screenshots*** 🌐

- **Demo Url:** https://surftg-d5bc40cb110d.herokuapp.com/
- **Username:** admin 
- **Password:** admin

<div style="overflow-x: auto; white-space: nowrap;">
  <img src="https://graph.org/file/67c1500ecd0b9eb3a5700.png" style="width: 400px; display: inline-block; margin-right: 10px;" />
  <img src="https://graph.org/file/be9d123ccc341d43431ef.png" style="width: 400px; display: inline-block; margin-right: 10px;" />
  <img src="https://graph.org/file/29fd699758d8ce2da9aff.png" style="width: 400px; display: inline-block; margin-right: 10px;" />
  <img src="https://graph.org/file/5ace6162fd95c1f9432fa.png" style="width: 400px; display: inline-block; margin-right: 10px;" />
</div>


## ***Environment Variables*** 🪧

To run this Surf-TG, you will need to add the following environment variables to your config.env file.

> [!NOTE]
> First, rename the `sample_config.env` to `config.env`.

| Variable Name | Value
|------------- | -------------
| `API_ID` (required) | Telegram api_id obtained from https://my.telegram.org/apps. `int`
| `API_HASH` (required) | Telegram api_hash obtained from https://my.telegram.org/apps. `str`
| `BOT_TOKEN` (required) | The Telegram Bot Token that you got from @BotFather `str`
| `AUTH_CHANNEL` (required) | Chat_ID of the Channel you are using for index (Seperate Multiple Channel By `,` eg- `-100726731829, -10022121832`). `int`
| `SESSION_STRING` (required) | Use same account which is a participant of the `AUTH_CHANNEL`. `str`
| `BASE_URL` (required) | Valid BASE URL where the bot is deployed. Format of URL should be `http://myip`, where myip is the IP/Domain(public) of your bot. For `Heroku` use `App Url`. `str`
| `PORT` | Port on which app should listen to, defaults to `8080`. `int`
| `USERNAME` | default  username is `admin`. `str`
| `PASSWORD` | default  password is `admin`. `str`
| `SLEEP_THRESHOLD` | Set a sleep threshold for flood wait exceptions, defaut is `60`. `int`
| `WORKERS` | Number of maximum concurrent workers for handling incoming updates, default is `10`. `int`
| `MULTI_TOKEN*` | Multi bot token for handing incoming updates. (*)asterisk represents any interger starting from 1. `str`
| `THEME` | Choose any Bootswatch theme for UI, Default is `flatly`. `str`


## ***Themes*** 🎨

* There are 25 Themes from [bootswatch](https://github.com/thomaspark/bootswatch) official [Bootstrap](https://getbootstrap.com) Themes.
* You can check Theme from [bootswatch.com](https://bootswatch.com) before selecting.
* To Change theme, Set Appropriate Theme name in `Theme` Variable.

| **Themes**|         |         |         |        |          |
|:---------:|:-------:|:-------:|:-------:|:------:|:--------:|
| cerulean  | cosmo   | cyborg  | darkly  | flatly | journal  |
| litera    | lumen   | lux     | materia | minty  | pulse    |
| sandstone | simplex | sketchy | slate   | solar  | spacelab |
| superhero | united  | yeti    | vapor   | morph  | quartz   |    
| zephyr    |

### ***Multiple Bots*** 🚀 (Speed Booster)

> [!NOTE]
> **What it multi-client feature and what it does?** <br><br>
> This feature shares the Telegram API requests between worker bots to speed up download speed when many users are using the server and to avoid the flood limits that are set by Telegram. <br>

> [!NOTE]
> You can add up to 50 bots since 50 is the max amount of bot admins you can set in a Telegram Channel.

To enable multi-client, generate new bot tokens and add it as your `config.env` with the following key names. 

`MULTI_TOKEN1`: Add your first bot token here.
`MULTI_TOKEN2`: Add your second bot token here.

you may also add as many as bots you want. (max limit is 50)
`MULTI_TOKEN3`, `MULTI_TOKEN4`, etc.

> [!WARNING]
> Don't forget to add all these worker bots to the `AUTH_CHANNEL` for the proper functioning

### Generate Session String 

> [!NOTE]
> **Why Session String is needed?** <br><br>
> The session string is required to fetch files from the `AUTH_CHANNEL` due to a restriction in the Telegram API. Only users are allowed to fetch files from channels; bots cannot do so.

> [!NOTE]
> **Make Sure that you have to Generate the `Pyrogram Session String`**

To generate the Session String use this [Colab Tool](https://colab.research.google.com/drive/1u4F2CtYU_Q3_rWfjYtt1IvRJfNKmBKyM)


## Deployment

<i>Either you could locally host, VPS, or deploy on [Heroku](https://heroku.com)</i>


### Deploy Locally:

```sh
git clone https://github.com/weebzone/Surf-TG
cd Surf-TG
python3 -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
python3 -m bot
```

- To stop the whole server,
 do <kbd>CTRL</kbd>+<kbd>C</kbd>

- If you want to run this server 24/7 on the VPS, follow these steps.
```sh
sudo apt install tmux -y
tmux
python3 -m bot
```
- now you can close the VPS and the server will run on it.



### Deploy using Docker 

* Clone the Repository:
```sh
git clone https://github.com/weebzone/Surf-TG
cd Surf-TG
```
- Start Docker daemon (SKIP if already running, mostly you don't need to do this):
```sh
sudo dockerd
```
* Build own Docker image:
```sh
sudo docker build -t Surf-TG .
```

* Start Container:
```sh
sudo docker run -p 8080:8080 Surf-TG
```
* To stop the running image:

```sh
sudo docker ps
```
```sh
sudo docker stop id
```

### Deploy on Heroku :

Easily Deploy to Heroku use this [Colab Tool](https://colab.research.google.com/drive/1R5YBUg8TINgxAm4Hvejjy0VgsKGmb8vV)


## Contributing

Feel free to contribute to this project if you have any further ideas

## Credits

- [@TechShreyash](https://github.com/TechShreyash) for [TechZIndex](https://github.com/TechShreyash/TechZIndex) Base repo

## **Contact Info**

[![Telegram Username](https://img.shields.io/static/v1?label=&message=Telegram%20&color=blueviolet&style=for-the-badge&logo=telegram&logoColor=black)](https://t.me/krn_adhikari)

## **Copyright** ©️ 

Copyright (C) 2024-present [Weebzone](https://github.com/weebzone) under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html).

Surf-TG is Free Software: You can use, study share and improve it at your
will. Specifically you can redistribute and/or modify it under the terms of the
[GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) as
published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. Also keep in mind that all the forks of this repository MUST BE OPEN-SOURCE and MUST BE UNDER THE SAME LICENSE.
