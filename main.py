import sys
import time
import spotipy
import spotipy.util as util
from configparser import ConfigParser


class MergePlayList():

    def __init__(self, user_name, sp):
        self.username = user_name
        self.sp = sp
        if len(sys.argv) > 3:
            self.target = sys.argv[1]
            self.playlist1 = sys.argv[2]
            self.playlist2 = sys.argv[3]
        else:
            print ("Usage: %s targetplaylist playlist1 playlist2" % (sys.argv[0]))
            sys.exit()

    def getTracks(self,playlistId):
        results = self.sp.user_playlist_tracks(self.username , playlistId)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        print ("track number : ", len(tracks))
        return tracks

    def addTracks(self, sorted_track):
        created_playlist = self.sp.user_playlist_create(self.username, self.target)
        created_playlist_id = created_playlist['id']
        toAdd = []
        for s in sorted_track:
            toAdd.append(s[0])
            if (len(toAdd) >= 1):
                self.sp.user_playlist_add_tracks(self.username, created_playlist_id, toAdd)
                toAdd.clear()
                time.sleep(0.01)

    def merge(self):
        results = self.sp.current_user_playlists()
        playlist1_id = ''
        playlist2_id = ''
        for item in results['items']:
            if (item['name'] == self.playlist1):
                playlist1_id = item['id']
            if (item['name'] == self.playlist2):
                playlist2_id = item['id']
        try:
            tracks = self.getTracks(playlist1_id)
            tracks.extend(self.getTracks(playlist2_id))
        except:
            if not playlist1_id:
                print('The playlist:', self.playlist1, 'not found')
            if not playlist2_id:
                print('The playlist:', self.playlist2, 'not found')
            print('Check yout playlist name, and make sure is set to public')
            sys.exit()

        track_dist = {}
        for track in tracks:
            track_dist[track['track']['id']] = track['added_at']
        sorted_track = sorted(track_dist.items(), key=lambda x: x[1])

        print ("Total tracks : ",len(sorted_track))
        self.addTracks(sorted_track)

def getToken(user_name, user_id, user_secret):
    scope = 'user-library-read playlist-modify-public'
    token = util.prompt_for_user_token(user_name,scope,
        client_id = user_id,
        client_secret = user_secret,
        redirect_uri = 'http://localhost:8888/callback')
    if token:
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        print ("Can't get token for", user_name)
        return NULL

if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('config.cfg')
    sp = getToken(cfg['user']['user_name'],cfg['user']['user_id'],cfg['user']['user_secret'])
    if not sp:
        sys.exit()
    mp = MergePlayList(cfg['user']['user_name'], sp)
    mp.merge()
