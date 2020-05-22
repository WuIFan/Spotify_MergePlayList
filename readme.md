# Spotify_MergePlayList

Merge playlist by added date  

## Introduction  

Due to the Spotify app can only copy playlists to a new playlist one by one, and the sort rule I prefer to use is "date" which the app doesn't provide, so this script is used to add tracks to a new playlist from two old playlists by added date.  

## You need Client_id and Client_secret  

1. Go to <https://developer.spotify.com/dashboard/applications>
2. Log in and Create a client id.
3. Enter your app and you will see the Client_id and Client_secret
4. Click Edit setting and add <http://localhost:8888/callback> in Redirect URIs
5. Save
6. And put config.cfg file in the same directory with main.py  
config.cfg is like [this](./config_demo.cfg):  

```cfg
[user]
    user_name = your_user_name
    user_id = your_client_id
    user_secret = your_client_secret
```

## How to use  

1. python3 required  
2. you may need to install some library  

```console
pip install spotipy  
```

3. start (Make sure your playlist is public)
   
```console  
python main.py YOURTARGETLIST PLAYLIST1 PLAYLIST2  
```

4. After authentication your web browser will redirected to a url.  Paste that url you were directed to to complete the authorization.  
5. And finished :)
