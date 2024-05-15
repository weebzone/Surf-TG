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
- Playlist Creator Support 📀
- Database Support 💾
- Cache System 🔄

### ***To-Do*** 📦

- [ ] API Support 🛠️
- [ ] Admin Pannel Support 👑

## ***Website Screenshots*** 🌐


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
| `DATABASE_URL` (required) | Your Mongo Database URL (Connection string). Follow this [Guide](https://github.com/weebzone/Surf-TG/tree/main#generate-database-) to generate database. `str`
| `SESSION_STRING` | Use same account which is a participant of the `AUTH_CHANNEL` Use this [Tool](https://github.com/weebzone/Surf-TG/tree/main#generate-session-string) to generate Session String. `str`
| `BASE_URL` (required) | Valid BASE URL where the bot is deployed. Format of URL should be `http://myip`, where myip is the IP/Domain(public) of your bot. For `Heroku` use `App Url`. `str`
| `PORT` | Port on which app should listen to, defaults to `8080`. `int`
| `USERNAME` | default  username is `admin`. `str`
| `PASSWORD` | default  password is `admin`. `str`
| `ADMIN_USERNAME` | Set the admin username so that the admin can log in to [Playlist Creator](https://github.com/weebzone/Surf-TG/tree/main#playlist-creator-). Make it different from `USERNAME`. The default admin username is `surfTG`. `str`
| `ADMIN_PASSWORD` | Set the admin password so that the admin can log in to [Playlist Creator](https://github.com/weebzone/Surf-TG/tree/main#playlist-creator-). Make it different from `PASSWORD`. The default admin password is `surfTG`. `str`
| `SLEEP_THRESHOLD` | Set a sleep threshold for flood wait exceptions, defaut is `60`. `int`
| `WORKERS` | Number of maximum concurrent workers for handling incoming updates, default is `10`. `int`
| `MULTI_TOKEN*` | Multi bot token for handing incoming updates. (*)asterisk represents any interger starting from 1. `str`
| `THEME` | Choose any Bootswatch theme for UI, Default is `flatly`. `str`
| `MULTI_CLIENT` | Set this `True` if using `MULTI_TOKEN`, Default is `False`. `bool`
| `HIDE_CHANNEL` | Set this `True` to hide the Channel Card in Public Web, Default is `False`. `bool`

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


### ***Generate Database*** 💾

> [!NOTE]
> **Why Database is Required** <br><br>
> In Playlist Creator, the folder and file data are stored. As of now, the session string is not required in Surf-TG, so to store these files, the database is necessary. <br>


1. Go to `https://mongodb.com/` and sign-up.
2. Create Shared Cluster.
3. Press on `Database` under `Deployment` Header, your created cluster will be there.
5. Press on connect, choose `Allow Access From Anywhere` and press on `Add IP Address` without editing the ip, then
   create user.
6. After creating user press on `Choose a connection`, then press on `Connect your application`. Choose `Driver` 
   **python** and `version` **3.6 or later**.
7. Copy your `connection string` and replace `<password>` with the password of your user, then press close.

### Generate Session String 

> [!NOTE]
> **Make Sure that you have to Generate the `Pyrofork Session String`**

To generate the Session String use this [Colab Tool](https://colab.research.google.com/drive/1F3cRAdgvFSenOoVSxJFxP-356pE4sWOL)


### ***Playlist Creator*** 📀

> [!NOTE]
> **Login With `ADMIN_USERNAME` and `ADMIN_PASSWORD`** <br><br>

- 📁 Create Folder/Subfolder
- ✏️ Edit the Folder Name
- 🖼️ Edit the Folder Thumbnail
- 📥 Directly Store File in folder from `AUTH_CHANNEL`
- 🔍 Search Support of file in Playlist folder (limited to the folder which is open in the browser)
- ✏️ Edit Filename of File
- 🖼️ Edit Thumbnail of File

### Bot Commands

```
index - store files in Database
```

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


## FAQ 🤔


#### Question 1: Is a session string required in Surf-TG?

**Answer:** No, it is not required.

#### Question 2: I am using Surf-TG without a session string, but my channel files are not showing on the web.

**Answer:** To initially index your files, use the `/index` command in `AUTH_CHANNEL`. This command stores all your files in the database. Please ensure that you use the `/index` command only in one channel at a time. Once the channel indexing is complete, you can proceed to index the next channel.

#### Question 3: Do I need to use the `/index` command every time the bot restarts or is deployed again?

**Answer:** No, whether you restart the bot or deploy it again, you don't need to perform initial indexing unless you change the database.

#### Question 4: Do I have to use the `/index` command every time I upload a file to the channel to index it?

**Answer:** No, the `/index` command is only used once initially. Subsequently, any files you send will automatically be stored in the database.

#### Question 5: When will be the cache system work?
**Answer:** It work only when you use the `Session String.`

#### Question 6: How are posts updated on the web when using Session String?

**Answer:** Login with `ADMIN_USERNAME` and `ADMIN_PASSWORD`, then clicking the reload option in the Homepage navbar clears all channel caches, to showing new posts. To clear a specific channel's cache, open the channel and click its reload option.

#### Question 7: How to change theme and add/remove Channel without restart?

**Answer:** Login with `ADMIN_USERNAME` and `ADMIN_PASSWORD`, then clicking the Edit option in the Homepage navbar from there you can change theme and add/remove channel. Make sure that channel must be seperated by `,`

#### Question 8: Can anyone create or edit folders/files in Playlist Creator?

**Answer:** No, only admins with `ADMIN_USERNAME` and `ADMIN_PASSWORD` can log in to Playlist Creator.

#### Question 9: If i delete the mongoDb database then my playlist also deleted?

**Answer:** Yes, Your all the playlist will be deleted.

#### Question 10: If i delete the file from `AUTH_CHANNEL` still then it will be played in Surf-TG?

**Answer:** No, Once the file is deleted it will be no more playable.

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
