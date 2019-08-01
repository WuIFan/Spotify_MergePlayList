# Spotify_MergePlayList

Merge playlist by added date  

## You need Client_id and Client_secret  

and put config.cfg file in the same directory with main.py  
config.cfg is like this:  

```cfg
[user]
    user_id = 'your_client_id'
    user_secret = 'your_client_secret'
```

## How to use  

```console  
python3 main.py YOURACCOUNT YOURTARGETLIST PLAYLIST1 PLAYLIST2  
```

you may need to install some library  

```console
pip3 install spotipy  
```
