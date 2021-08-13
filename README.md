<h1>Ohto Ai Plays <a href='https://github.com/tgcalls/awesome-tgcalls'><img src='https://awesome.re/mentioned-badge-flat.svg'></a></h1>

<p align='center'>
<img src="https://i.ibb.co/R0Vh3rW/IMG-20210808-131839-removebg-preview.png" alt="ohto-ai-kawaaii-pic" border="0" widht='223.5' height='176'>
</p>

An awesome, deployable, simple, non spammy, auth-system enabled, multi-chat music bot!

---

## Requirements 📝
- `API_ID` :  API_ID as from [telegram apps](https://my.telegram.org/).
- `API_HASH` :  API_HASH as from [telegram apps](https://my.telegram.org/).
- `SESSION_NAME` :  Make a string session of the alternate account that will be used by the bot to play music, (this account will not be able to hear music) [here](https://repl.it/@subinps/getStringName).
- `BOT_TOKEN` :  Make a Bot from [@Botfather](https://t.me/botfather) and fill it's bot token.
- `BOT_USERNAME` : Your bot username, to help create handlers.
- `OWNER_ID` : Needed sometimes, so fill it.
- `START_PIC` : The pic displayed when a person starts your bot, use telegraph for it.
- `PLAY_PIC` : The pic to show playing message and stop message.
- `SUDO_USERS` :  Fill the userids of the users who will have full control over bot at any group, with spaces between them (dont forget to add your own id kek!).
- `PROXY`: A proxy to use for youtube-dl, if you dont know, leave it.

---

### Deploy to railways:

I recommend deploying on railways, because it lags relatively less than heroku (almost lagless)

<details>
<summary>Steps to Deploy on Railway</summary>
<ol>
<li>Fork This Repo, to your github account</li>
<li>Create an account at <a href='https://railway.app'>Railway</a>
<li>Create an app at railway with a postgresql addon</li>
<li>Gather all the requirements mentioned above in the following manner in your notes app, and then after finishing copy the whole thing to your clipboard
<img src='https://telegra.ph/file/4c45814b6ec4e96b686a2.jpg'>
</li>
<li>Go to railway, to the app you created, and then go to the tab <code>variables</code></li>
<li>Click on bulk import, a dialogue box would open up, now paste the whole copied vars that we copied in step 4</li>
<li>Now go to the Deployment tab and then connect your github</li>
<li>After connecting your github, connect the forked repo that you forked from me</li>
<li>Now deploy it, wait until it comes online and enjoy lagless music!</li>
</ol>
</details>

### Deploy to Heroku: 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Zack-Bloodshot/Ohto-Ai)

---

## Credits

- [Zack-Bloodshot](https://github.com/Zack-Bloodshot) A.K.A [A B H I](https://t.me/DontKnowWhoRU): Main Dev
- [MarshalX](https://github.com/MarshalX) for [tgcalls](https://github.com/MarshalX/tgcalls)
- [delivrance](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram)