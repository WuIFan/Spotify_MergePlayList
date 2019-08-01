import sys
import time
import spotipy
import spotipy.util as util
from configparser import ConfigParser


class MergePlayList():

    def __init__(self, user_id, user_secret):
        scope = 'user-library-read playlist-modify-public'
        if len(sys.argv) > 4:
            self.username = sys.argv[1]
            self.target = sys.argv[2]
            self.playlist1 = sys.argv[3]
            self.playlist2 = sys.argv[4]
        else:
            print ("Usage: %s username targetplaylist playlist1 playlist2" % (sys.argv[0],))
            sys.exit()

        token = util.prompt_for_user_token(self.username,scope,
            client_id=user_id,
            client_secret=user_secret,
            redirect_uri='http://localhost:8888/callback')
        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            print ("Can't get token for", self.username)

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
        for item in results['items']:
            if (item['name'] == self.playlist1):
                playlist1_id = item['id']
            if (item['name'] == self.playlist2):
                playlist2_id = item['id']

        tracks = self.getTracks(playlist1_id)
        tracks.extend(self.getTracks(playlist2_id))

        track_dist = {}
        for track in tracks:
            track_dist[track['track']['id']] = track['added_at']
        sorted_track = sorted(track_dist.items(), key=lambda x: x[1])

        print ("Total tracks : ",len(sorted_track))
        self.addTracks(sorted_track)

if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('config.cfg')
    mp = MergePlayList(cfg['user']['user_id'],cfg['user']['user_secret'])
    mp.merge()
