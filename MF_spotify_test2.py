#!/usr/bin/env python
# coding: utf-8

# ### Malcolm's Queries

# In[6]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

get_ipython().run_line_magic('matplotlib', 'inline')


# In[7]:


get_ipython().system('pip install requests')


# In[8]:


get_ipython().system('pip install spotipy')


# In[13]:


get_ipython().run_line_magic('env', 'SPOTIPY_CLIENT_ID=7a91b042b72546c2946779a4be23a481')
get_ipython().run_line_magic('env', 'SPOTIPY_CLIENT_SECRET=e7e3ef77c20c4bcead9d9b3e85696db6')


# In[10]:


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


# In[14]:


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# In[21]:


artist_name = 'Mac Miller'
query = f'artist:{artist_name}'
results = spotify.search(q=query, type='artist')


# In[19]:


def extract_uri(name, srch_type='artist', search_res=None):
    if search_res is None:
        search_res = spotify.search(q=f'{srch_type}:{name}', type=srch_type)
    items = search_res[f'{srch_type}s']['items']
    if len(items) > 0:
        artist = items[0]
        return artist['uri']
    
def get_artist_uri(name, search_res=None): return extract_uri(name, 'artist', search_res)


# In[22]:


macmiller_uri = get_artist_uri(artist_name); macmiller_uri


# In[45]:


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(macmiller_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


# In[23]:


macmiller = spotify.artist(macmiller_uri)


# In[24]:


macmiller


# In[25]:


mac_albums = spotify.artist_albums(macmiller_uri)


# In[26]:


mac_albums


# In[27]:


mac_albums['items'][0]['name']


# In[29]:


mac_albums['items'][2]['name']


# In[30]:


mac_top_tracks = spotify.artist_top_tracks(macmiller_uri);mac_top_tracks


# In[32]:


mac_top_tracks['tracks'][0]['name']


# In[62]:


self_care_uri = mac_top_tracks['tracks'][0]['uri'];macmiller_uri


# In[35]:


self_care_audio_asys = spotify.audio_analysis(self_care_uri)


# In[40]:


mac_rel_artists = spotify.artist_related_artists(macmiller_uri)


# In[41]:


len(mac_rel_artists['artists'])


# In[43]:


related_artists = [(a['name'], a['popularity']) for a in mac_rel_artists['artists']];related_artists


# In[44]:


sorted(related_artists, key=lambda x:x[1], reverse=True)


# In[46]:


min_energy = 0.4
min_popularity = 50


# In[48]:


macmiller_rec_results = spotify.recommendations(seed_artists=[macmiller_uri],
                                               min_energy=min_energy, min_popularity=min_popularity,
                                               country='US')


# In[49]:


macmiller_rec_results.keys()


# In[50]:


macmiller = spotify.artist(macmiller_uri)


# In[51]:


macmiller


# In[55]:


macmiller_albums = spotify.artist_albums(macmiller_uri)


# In[56]:


macmiller_albums


# In[57]:


macmiller_albums['items'][0]['name']


# In[58]:


mac_top_tracks['tracks'][0]


# In[59]:


self_care_audio_asys = spotify.audio_analysis(self_care_uri)


# In[67]:


macmiller_rel_artists = spotify.artist_related_artists(macmiller_uri)


# In[68]:


len(macmiller_rel_artists)


# In[87]:


type(macmiller_rel_artists)


# In[88]:


macmiller_rel_artists.keys()


# In[83]:


foo = macmiller_rel_artists['artists']


# In[84]:


type(foo)


# In[85]:


len(foo)


# In[69]:


related_artists = [(a['name'], a['popularity']) for a in macmiller_rel_artists['artists']];related_artists


# ### Tracks

# In[70]:


self_care_audio_asys = spotify.audio_analysis(self_care_uri)


# In[71]:


self_care_audio_asys.keys()


# In[72]:


self_care_audio_feats = spotify.audio_features(self_care_uri);self_care_audio_feats


# ### Playlists

# In[73]:


playlists = spotify.user_playlists('alenaf11')


# In[74]:


len(playlists['items'])


# In[77]:


playlists['items'][3]


# In[78]:


bad_idea_uri = playlists['items'][3]['uri'];bad_idea_uri


# In[80]:


bad_idea_tracks = spotify.playlist_tracks(bad_idea_uri)


# In[81]:


from datetime import datetime


# In[ ]:




