# Best Instagram Downloader

## How to run guide
- clone repo
- set these to `.env` file in the root folder of repo
```
BEST_INSTAGRAM_DOWNLOADER_BOT_API
LOG_CHANNEL_ID
INSTAGRAM_USER_1
INSTAGRAM_PASS_1
```
- install required python modules:
```
pip3 install -r requirements.txt
```
- run the main file with:
```
nohup python3 best_instagram_downloader.py &
```

## to-do next:
- [x] handle expired session


-------------------------------------------------

found this:
https://github.com/riad-azz/instagram-video-downloader

the main file for it is:
src/app/api/instagram/p/[shortcode]

my python equivalent of it which works fine:
riad-azz.py