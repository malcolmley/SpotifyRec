#!/usr/bin/env python
# coding: utf-8

# # Use python to access Spotify REST API

# ## Set up your Spotify developer account

# Before you start, you have to be registered as a Spotify developer and create an app.
# 
# From https://towardsdatascience.com/get-your-spotify-streaming-history-with-python-d5a208bbcbd3
# 
# Go to your new developer dashboard and click on ‘Create an App’. Don’t worry about the details. Spotify will allow you to create dummy apps as long as you promise not to monetize them. But you should avoid using ‘Spotify’ in the name, or it might get blocked.
# 
# **Authorization Code Flow**
# 
# ...
# 
# We need to provide a ‘redirect link’ that we’ll use to collect the user’s permission. From your app’s panel in the developer dashboard, click on ‘Edit Settings’ and add a link under Redirect URIs. This doesn’t have to be a real link: ... use http://localhost:7777/callback.
# 
# You will also need your app’s Client ID and Client Secret. You’ll find them in the app panel under your app’s name. Now you have all you need to access the Spotify API!

# ## Access Spotify API

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

get_ipython().run_line_magic('matplotlib', 'inline')


# Install requests and spotipy libraries so we can access Spotify API using python.  The requests libarary is for making HTTP calls.  The Spotify API just make it easier to access the Spotify API using python.

# In[77]:


get_ipython().system('pip install requests')


# In[73]:


get_ipython().system('pip install spotipy')


# Set your authorization credentials so we don't have to keep sending this information

# In[74]:


get_ipython().run_line_magic('env', 'SPOTIPY_CLIENT_ID=c07db836d18f4ebe968ce919228c0a08')
get_ipython().run_line_magic('env', 'SPOTIPY_CLIENT_SECRET=3374e32eb8c44b59bcb91c454b9bae84')


# In[492]:


get_ipython().run_line_magic('env', "SPOTIPY_REDIRECT_URI='http://localhost:7777/callback'")


# In[75]:


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


# Do a quick test to make sure everything is working.
# 
# NOTE: We get back a spotify object when we call spotipy.Spotify.  This is a handle to the Spotify web service.

# In[493]:


birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


# ## Getting URIs for artists, tracks and other stuff.

# Whenever we make a request to Spotify for something like an artist, we will need to URI.  The URI is just a unique identifier every entity in Spotify is assigned.
# 
# For example, to get the URI for the Dead Milkmen, I can call search on the spotify object we got above. 

# In[80]:


artist_name = 'Dead Milkmen'
results = spotify.search(q='artist:' + artist_name, type='artist')
deadmilk_uri = results['artists']['items'][0]['uri'];uri
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    deadmilk_uri = artist['uri']
print(deadmilk_uri)


# In[90]:


type(results)


# Now that we have this URI, we can call other methods such as recommendations to get similar artists.

# In[87]:


min_energy = 0.4
min_popularity = 50


# In[91]:


deadmilk_rec_results = spotify.recommendations(seed_artists=[deadmilk_uri],
                                               min_energy=min_energy, min_popularity=min_popularity,
                                               country='US')


# In[93]:


deadmilk_rec_results.keys()


# ## Search

# Spotify has various entities you can search for
# - albums
# - artists
# - tracks
# - playlists
# - shows (i.e. podcasts)
# - show episodes (i.e. podcast episodes)
# - players (i.e. users' devices - in beta)
# - user profiles (for the current user of your app)
# - info used for personalization (ex. user's top artists and tracks in a given time range); updated daily
# - stuff in user's *Your Library*
# - info on what a user follows
# - playlists and new album releases featured on Spotify’s Browse tab
# 
# Their web API lists the details:
# 
# https://developer.spotify.com/documentation/web-api/reference/search/search/
# 
# For most of the calls you would make to the spotify server, you will need to get the URI of the entity first.  The **search** call is used to get these.

# For example, to look for an artist, we can call **search** with just the artist's name.  NOTE: I am using spotipy's library, so this call will look different if I am making the call via curl or using javascript on a webpage.  The concepts will be similar though.

# In[125]:


artist_name = 'Lizzo'
query = f'artist:{artist_name}'
results = spotify.search(q=query, type='artist')


# We will get back a (python) dictionary containing the 'artists' field as a key; the corresponding value is yet another dictionary which contains an entry for 'items' - this contains the list of the artists that matched our query. Yes - there is more than one 'lizzo' - a flippin Xiao Lizzo!

# In[129]:


results


# In[130]:


results.keys()


# In[131]:


results['artists']


# In[132]:


results['artists'].keys()


# In[133]:


results['artists']['items']


# Looks like we got 10 artists back.

# In[134]:


len(results['artists']['items'])


# I just want the first one.

# In[137]:


lizzo = results['artists']['items'][0]; lizzo


# As you can see, you can get the genres associated with her, her popularity and what I really want - her uri.

# In[138]:


lizzo['uri']


# I wrote a function, get_artist_uri, to retrieve the uri associated with the first artist in a list returned by calling search.

# In[117]:


def extract_uri(name, srch_type='artist', search_res=None):
    if search_res is None:
        search_res = spotify.search(q=f'{srch_type}:{name}', type=srch_type)
    items = search_res[f'{srch_type}s']['items']
    if len(items) > 0:
        artist = items[0]
        return artist['uri']
    
def get_artist_uri(name, search_res=None): return extract_uri(name, 'artist', search_res)


# In[139]:


artist_name = 'Lizzo'
lizzo_uri = get_artist_uri(artist_name);lizzo_uri


# ## Artist

# If I know the artist's uri, I can get the corresponding entity directly using the 'artist' method on our spotify object.

# In[141]:


lizzo = spotify.artist(lizzo_uri)


# In[142]:


lizzo


# I can also use that same uri to access albums.

# In[145]:


lizzo_albums = spotify.artist_albums(lizzo_uri)


# In[144]:


lizzo_albums


# In[153]:


lizzo_albums['items'][0]['name']


# In[168]:


album_names = [album['name'] for album in lizzo_albums['items']];album_names


# It looks likes there are dupes, but if we pull up the uris as well, they are not dupes.

# In[169]:


album_names_uris = [(album['name'], album['uri']) for album in lizzo_albums['items']];album_names_uris


# It looks like at least for 'Cuz I Love You (Deluxe)', it was released with different number of tracks.

# In[173]:


lizzo_albums['items'][0]['total_tracks']


# In[174]:


lizzo_albums['items'][2]['total_tracks']


# I can also find other stuff about the artist using their uri.  Note that if you hit tab after 'spotify.', you will see the available methods you can call on the spotify object.  Anything that begins with 'artist_' will mirror the web API calls you see in the Spotify documentation.
# 
# https://developer.spotify.com/documentation/web-api/reference/artists/
# 
# Also note that the same thing applies for other entities - I can hit shift tab and see playist_ methods for example.

# In[175]:


lizzo_top_tracks = spotify.artist_top_tracks(lizzo_uri);lizzo_top_tracks


# Not surprisingly, the top track is 'Truth Hurts'

# In[182]:


lizzo_top_tracks['tracks'][0]


# In[183]:


lizzo_top_tracks['tracks'][0]['name']


# Note that I can get the uri for this track.  This is another important way to get uri references to entities, besides using search.

# In[185]:


truth_hurts_uri = lizzo_top_tracks['tracks'][0]['uri'];truth_hurts_uri


# Then I can use this uri to access calls in the Track API.  For example, I can get the rhythm, pitch and timbre for this track. See more on this below in the Tracks section.

# In[196]:


truth_hurts_audio_asys = spotify.audio_analysis(truth_hurts_uri)


# And finally we can find related artists.

# In[204]:


lizzo_rel_artists = spotify.artist_related_artists(lizzo_uri)


# In[205]:


len(lizzo_rel_artists['artists'])


# In[209]:


related_artists = [(a['name'], a['popularity']) for a in lizzo_rel_artists['artists']];related_artists


# To order these by popularity

# In[213]:


sorted(related_artists, key=lambda x:x[1], reverse=True)


# ## Tracks

# Let's go back to Lizzo's 'Truth Hurts' track.

# In[203]:


truth_hurts_audio_asys = spotify.audio_analysis(truth_hurts_uri)


# In[199]:


truth_hurts_audio_asys.keys()


# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/
# 
# Bars = beats/downbeats

# In[198]:


truth_hurts_audio_asys['bars']


# Tatums relates to rhythm somehow

# In[200]:


truth_hurts_audio_asys['tatums']


# You can also get higher level audio info about track - duration, pitch, tempo, danceability.
# 
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

# In[202]:


truth_hurts_audio_feats = spotify.audio_features(truth_hurts_uri);truth_hurts_audio_feats


# ## Playlists

# I can look at your public playlists.  This only returns 50 at a time because the default limit is 50.  You can change that by passing in the limit parameter.

# In[509]:


playlists = spotify.user_playlists('alenaf11')


# In[510]:


len(playlists['items'])


# In[511]:


playlists['items'][0]


# In[267]:


stay_forever_uri = playlists['items'][0]['uri'];stay_forever_uri


# In[268]:


stay_forever_tracks = spotify.playlist_tracks(stay_forever_uri)


# In[285]:


from datetime import datetime


# In[289]:


x = datetime.strptime('2020-07-30T21:24:41Z', "%Y-%m-%dT%H:%M:%SZ")


# In[292]:


def parse_track(track_item):
    added_at = datetime.strptime(track_item['added_at'], "%Y-%m-%dT%H:%M:%SZ")
    name = track_item['track']['name']
    return added_at, name


# In[294]:


track_info = [parse_track(track_item) for track_item in stay_forever_tracks['items']]


# Tabulate just prints out a two-dimensional array like this in a nice tabular format.

# In[276]:


get_ipython().system('pip install tabulate')


# In[301]:


from tabulate import tabulate


# In[302]:


print(tabulate(sorted(track_info), headers=["Date and Time Added", "Track"]))


# ## Recommendations

# We can get recommended list of tracks from the Spotify API by passing in either a set of tracks, artists and/or genres.  We are limited to a combination of 5, which seems small to me.
# 
# Pick a random sample of 5 tracks from stay_forever_tracks.  We will see if we recover any of the other tracks you have in that playlist.

# In[387]:


import numpy as np


# In[411]:


np.random.seed(42)


# In[412]:


rand_track_idxs = set(np.random.permutation(len(stay_forever_tracks['items']))[:5])


# In[413]:


some_track_names = [track['track']['name']
                    for i, track in enumerate(stay_forever_tracks['items']) if i in rand_track_idxs]


# In[414]:


some_track_names


# Those are the name of the tracks but we need the uris.

# In[419]:


seed_tracks = [track['track']['uri']
               for i, track in enumerate(stay_forever_tracks['items']) if i in rand_track_idxs]


# In[565]:


stay_forever_tracks['items']


# In[420]:


seed_tracks


# Let's use these 'seeds' for Spotify's recommendation engine.

# In[421]:


maybe_similar_tracks = spotify.recommendations(seed_tracks=seed_tracks)


# In[422]:


maybe_similar_tracks['tracks'][0]['album']['name']


# In[423]:


mst = [(track['name'],
        track['album']['name'],
        track['artists'][0]['name']) for track in maybe_similar_tracks['tracks']]


# In[424]:


print(tabulate(mst, headers=["Track Name", "Album", "Artist"]))


# In[425]:


mst_uris = [track['uri'] for track in maybe_similar_tracks['tracks']]


# In[426]:


orig_playlist_uris = set([track['track']['uri'] for track in stay_forever_tracks['items']])


# In[427]:


mst_in_stay_forever_orig = [uri for uri in mst_uris if uri in orig_playlist_uris]


# In[428]:


len(mst_in_stay_forever_orig)


# We got 3!  NOTE: This may differ from what you get.  It seems Spotify has some element of randomness in its recommendation engine.

# In[429]:


mst_in_stay_forever_orig


# In[430]:


songs = [spotify.track(track_uri) for track_uri in mst_in_stay_forever_orig]


# In[431]:


mst_overlap = [(track['name'],
               track['album']['name'],
               track['artists'][0]['name']) for track in songs]


# In[432]:


print(tabulate(mst_overlap, headers=["Track Name", "Album", "Artist"]))


# Let's see if we can do better by passing in a target key for the recommendations (i.e. music key)

# In[433]:


target_key = 1 # C minor


# In[434]:


maybe_similar_tracks2 = spotify.recommendations(seed_tracks=seed_tracks, target_key=target_key)


# In[435]:


mst2 = [(track['name'],
         track['album']['name'],
         track['artists'][0]['name']) for track in maybe_similar_tracks2['tracks']]


# In[436]:


print(tabulate(mst2, headers=["Track Name", "Album", "Artist"]))


# In[437]:


mst_uris2 = [track['uri'] for track in maybe_similar_tracks2['tracks']]


# In[438]:


mst2_in_stay_forever_orig = [uri for uri in mst_uris2 if uri in orig_playlist_uris]


# In[439]:


len(mst2_in_stay_forever_orig)


# Crap - still 3.  Originally when I did this, I started out with 1 but then passed this and got 3.  Oh well.

# In[440]:


songs2 = [spotify.track(track_uri) for track_uri in mst2_in_stay_forever_orig]


# In[441]:


mst_overlap2 = [(track['name'],
                 track['album']['name'],
                 track['artists'][0]['name']) for track in songs2]


# In[442]:


print(tabulate(mst_overlap2, headers=["Track Name", "Album", "Artist"]))


# There are several 'knobs' we can turn to change the recommendations.  See **Tunable Track attributes** defined on https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/

# ### Genres

# Incidentally, if you want to know the genres Spotify 'knows' about and thus potential genre_seeds you can possibly pass in, you call recommendation_genre_seeds() on the spotify object to get them.

# In[443]:


genre_seeds = spotify.recommendation_genre_seeds()


# In[444]:


len(genre_seeds['genres'])


# ## Categories and Browse

# Categories just seem to be tags Spotify has for pre-curated playlists found under *Browse*.

# In[473]:


category_res = spotify.categories(limit=50)


# In[476]:


category_entries = list(category_res['categories'].items())[1][1]


# In[479]:


category_names = [category['name'] for category in category_entries]


# In[480]:


category_names


# Under the 'Browse', we can also get featured lists and new releases, if you are interested in that.
# 
# https://developer.spotify.com/documentation/web-api/reference/browse/

# In[482]:


fp_res = spotify.featured_playlists();fp_res


# In[483]:


nr_res = spotify.new_releases();nr_res


# ## Spotify Authorization (user vs app authorization)

# For any calls you make to Spotify, your application (here it's just our jupyter notebook) must get authorization to do so.  There are 4 different kinds 'authorization' in Spotify:
# 
# - Refreshable user authorization: Authorization Code Flow
# - Refreshable user authorization: Authorization Code Flow With Proof Key for Code Exchange (PKCE)
# - Temporary user authorization: Implicit Grant
# - Refreshable app authorization: Client Credentials Flow
# 
# The gory details are https://developer.spotify.com/documentation/general/guides/authorization-guide/.
# 
# So far, for all the calls above, we have used Client Credentials Flow.

# In[527]:


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# *Client Credentials Flow* authorization (i.e. **app-authorization**) allows you to access most of the API, and is fast (supposedly), but we will need to switch to *Authorization Code Flow* (i.e. **user-authorization**) for accessing other parts of the API that requires explicit authorization from the end-user using your app.  Right now, in my notebook, that would be me (user with ID 9l2enogkai2ymr28fm1n6cu80); for you, that would be alenaf11.
# 
# I suspect you don't have the file .cache-alenaf11 in your current directory.  This is a file used by spotipy to save access information so it can periodically re-connect to Spotify using user-authorization.  But check anyway.

# In[530]:


get_ipython().system('ls .cache-alenaf11')


# If nothing shows up, executing the following cell, but of course updating with your username, client_id and client_secret.

# In[531]:


username = '9l2enogkai2ymr28fm1n6cu80'
client_id ='c07db836d18f4ebe968ce919228c0a08'
client_secret = '3374e32eb8c44b59bcb91c454b9bae84'
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-follow-read'

token = spotipy.util.prompt_for_user_token(username=username, 
                                   scope=scope,
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)


# This should bring up a pop-up page on your web-brower.  Go ahead and agree to any access crap.  Unless it says they are coming to take Peaches away.

# ## Follow

# Follow-related calls need the right kind of authorization (i.e. we need to use user-authorization, not app-authorization.) 
# 
# Also note that we need to set the right 'scope' for the call we want to make.  Scopes are defined at
# 
# https://developer.spotify.com/documentation/general/guides/scopes/
# 
# Here, we will need 'user-follow-read' so we want to see a list of the artists the user (me, or you for you) follow.

# In[532]:


scope = "user-follow-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path='./.cache-9l2enogkai2ymr28fm1n6cu80'))


# In[534]:


artists = sp.current_user_followed_artists()


# In[535]:


artists


# Fascinating - I don't follow anyone.  But I bet you do!  So you will obviously get more results.
# 
# So I will add an artist (Lizzo) to follow (you don't have to here.)  But I also to have change the scope now to 'user-follow-modify'.  If you notice on the web API pages, they usually have a request parameters table with an Authorization row specifying the required scope.  See
# 
# https://developer.spotify.com/documentation/web-api/reference/follow/follow-artists-users/
# 
# for this example.

# In[541]:


scope = "user-follow-modify"

# Also need to specify the redirect_uri here.  At some point, this will be a real website, but we're just
# playing around here so just use a placeholder.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost:7777/callback',
                                               cache_path='./.cache-9l2enogkai2ymr28fm1n6cu80'))


# In[544]:


lizzo['uri']


# Note: we need to get rid of the 'spotify:artist:' part - grrrr.

# In[546]:


lizzo_raw_uri = lizzo['uri'].split(':')[-1];lizzo_raw_uri


# In[545]:


sp.user_follow_artists(ids=[lizzo_raw_uri])


# Let's see if that worked.  It's annoying, you think being able to write would give you access to read, but NO, we have create another spotify request object with the scope "user-follow-read."  Sigh.

# In[551]:


scope = "user-follow-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback',
                                               cache_path='./.cache-9l2enogkai2ymr28fm1n6cu80'))


# In[552]:


artists2 = sp.current_user_followed_artists()


# Ooh - I am now following Lizzo.

# In[553]:


artists2


# It looks like you can follow other users and playlists, and of course unfollow them.  Details are at 
# 
# https://developer.spotify.com/documentation/web-api/reference/follow/

# ## Personalization

# You can the current user's top artists and tracks.

# In[556]:


scope = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback',
                                               cache_path='./.cache-9l2enogkai2ymr28fm1n6cu80'))


# In[561]:


top_artists = sp.current_user_top_artists();top_artists


# I don't have any top artists.  I don't have any top tracks either.  I presume you will get different results.

# In[562]:


top_tracks = sp.current_user_top_tracks();top_tracks


# ## Library

# I don't have anything in my library.  This is really just demonstrating again how to use user-authorization.

# In[563]:


scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback',
                                               cache_path='./.cache-9l2enogkai2ymr28fm1n6cu80'))


# In[564]:


albums = sp.current_user_saved_albums();albums


# ## Ignore below for now 

# We can also scrape web pages but we probably shouldn't do that unless there is something we can't get from the api.

# In[228]:


from bs4 import BeautifulSoup
import requests


# In[229]:


alena_spotify_url = 'https://open.spotify.com/user/alenaf11'
html_text = requests.get(alena_spotify_url).text


# In[230]:


html_text


# In[231]:


soup = BeautifulSoup(html_text, 'html.parser')


# In[240]:


alena_playlist_titles = [span.get_text() for span in soup.find_all('span', attrs={"dir": "auto"})][1:]


# In[260]:


len(alena_playlist_titles)


# In[303]:


alena_playlist_titles


# ## Obscurify

# ### Recommendations

# This is one of Obscurify's network requests which may be seen using Firefox's web developer tools.

# In[622]:


rec_url1 = 'https://api.spotify.com/v1/recommendations?' +     'seed_artists=6l3HvQ5sa6mXTsMTB19rO5,0Y5tJX1MQlPlqiwlOH1tJY&' +     'seed_tracks=2swu91llDBxeb75tMETplV,0wSeTpuEBS5uloIJ9tGhFi' +     '&market=US&max_popularity=55&min_popularity=15&limit=15'


# In[609]:


def get_seeds(rec_url):
    artist_field, track_field, *_ = rec_url.split('&')
    seed_artists = artist_field.split('=')[1].split(',')
    seed_tracks = track_field.split('=')[1].split(',')
    return seed_artists, seed_tracks


# In[652]:


def get_artists_and_tracks(rec_url):
    seed_artists, seed_tracks = get_seeds(rec_url)
    
    # Get artist names
    res_artists = spotify.artists(seed_artists)
    rec_artists = res_artists['artists']
    artist_names = [rec['name'] for rec in rec_artists]
    
    # Get track names
    res_tracks = spotify.tracks(seed_tracks)
    rec_tracks = res_tracks['tracks']
    track_names = [rec['name'] for rec in rec_tracks]
    
    return artist_names, track_names


# In[657]:


artist_names1, track_names1 = get_artists_and_tracks(rec_url1)
artist_names1, track_names1


# In[626]:


rec_url2 = 'https://api.spotify.com/v1/recommendations?' +     'seed_artists=246dkjvS1zLTtiykXe5h60,4NZvixzsSefsNiIqXn0NDe&' +     'seed_tracks=1Bqxj0aH5KewYHKUg1IdrF,6zHyWsqTzT6Fympdy9KQDQ' +     '&market=US&max_popularity=55&min_popularity=15&limit=15'


# In[656]:


artist_names2, track_names2 = get_artists_and_tracks(rec_url2)
artist_names2, track_names2


# In[650]:


rec_url3 = 'https://api.spotify.com/v1/recommendations?' +     'seed_artists=69GGBxA162lTqCwzJG5jLp,1cZQSpDsxgKIX2yW5OR9Ot&' +     'seed_tracks=150zGw0P2EJccYJKnFIler,6UFivO2zqqPFPoQYsEMuCc' +     '&market=US&max_popularity=55&min_popularity=15&limit=15'


# In[658]:


artist_names3, track_names3 = get_artists_and_tracks(rec_url3)
artist_names3, track_names3


# ### Audio features

# Are these calls made to asses mood?

# In[636]:


s = """https://api.spotify.com/v1/audio-features?ids=5cbpoIu3YjoOwbBDGUEp3P,6SahMe6Q2BqUfnDQ2P9Xea,22DKsoYFV5npPXmnPpXL7i,4kRMsLX7bJqjIfK44qJ9h6,4lh1PamTsomWbFpkOPyfrD,3aWhZ1zeqy1kdjXiyMh22T,0CZ8lquoTX2Dkg7Ak2inwA,1gHC5zFCmKnjKDBtDBoUQZ,0wdKiSBUT7aZkXUIdJWcwC,1F7752qVUzbE1OOzxjyHaT,7K4Aq4awgYvDKEJdEvvl4j,4a17WC0Cf5hSKFD6ts57mk,7pqQpjNxOWbdPlwbW6tHGY,275a9yzwGB6ncAW4SxY7q3,0KjTPvyjSz7j2FS4ftKeCq,0kD586ste6xyDRqUYhVlCh,150zGw0P2EJccYJKnFIler,3C3cr2JQwXIhqAHqOardVO,2plFaDNZayLbtA9Ht1yCEo,4rfaoyaZvNa60cj3OKSQV9,1nX9KhK3Fff27SnrIor2Yb,53jbdPQBaH6WaQvW0zmGBs,2swu91llDBxeb75tMETplV,074M4HBIAHQAr3tTGzmdrI,36tghkPg1AO4HsAzo6YpPp,2HEACm14WJGvQZpQ2TKoqK,2Z8WuEywRWYTKe1NybPQEW,1PNfhBdmFikFn4vkrwiq05,3FhzUK2kAWH2bFImnlvkSc,1Bqxj0aH5KewYHKUg1IdrF,7lfADuEexIpuP4EjO46eZW,1jkIErXa3YNUX5QIyO6GGR,1c7btH9MTjdIDaYMsKeTzt,6VCeywT4JeawuZOUkQ1okx,3YbtjYddK11NTDdUpC4nGp,01stPT7J3W6Zx45jj1f4nk,1r1oITz34K73OEbz1ogvxk,2d3Jd9KvMfwhds67Y67RP5,0DsXQUA2OJW70LFmC95C7S,2Ghhdqk3GM9XJ7bNSnCfky,556l9P7WVZVyYUBjT1YFTT,0VzDv4wiuZsLsNOmfaUy2W,4VIAKU13YSnozH0aLh5S81,6Eoz2eZzrDV0AhzJxfqkFg,3ZO6UxR61HavlXuyohc14T,3mbcW1KDbnkdgjq03JHiQ6,2xKx2EMLkXuci86op5QVSZ,4bdJHQp90ymjEIkkYhcENB,5v0C3nNNDMhZ3nWzzP0W4T,6yuraIBlY8JGTVSwt2QSoB"""


# In[640]:


track_ids = s.replace('https://api.spotify.com/v1/audio-features?ids=','').split(',')


# In[641]:


len(track_ids)


# In[642]:


res_aud_feat_tracks = spotify.tracks(track_ids)


# In[643]:


aud_feat_tracks = res_aud_feat_tracks['tracks']
[rec['name'] for rec in aud_feat_tracks]


# Based on the above result it looks like Obscurify is pulling audio-features of your all-time top songs.
# 
# Based on the result below, it looks like Obscurify is also pulling audio-features of your current top songs.

# In[644]:


s2 = """https://api.spotify.com/v1/audio-features?ids=1M4Ud66z18wuIq3oOxqVHa,5uIRujGRZv5t4fGKkUTv4n,1KypMTzxfo8NNIZ30lanZa,6MYJv37Mpj5njLLbxKWNun,4vHNeBWDQpVCmGbaccrRzi,0afGLa6wcYiLLXFZ48ZQpY,3r2TFFPynN97CgmzXKal5X,48XkVAagIoQHCsOlJtXUd5,04oG24PjVs59q72Id8wXFK,2CO1B7lyEs3lf19hM5gn6x,7B3z0ySL9Rr0XvZEAjWZzM,0zms6rKU9lh6BbIrp1gDcZ,35Ki1lvKPC2sFBD3GmKdRG,1pNUmVxDiE8t6P1XxcZAv8,4677jRCDMa05jcA94EQ0hG,6UFivO2zqqPFPoQYsEMuCc,0Jgbauc8Nv2OOjR5ERW28B,11zf7m4vw9Ze7cer9Nyhk1,4BWJGWmzbjsnA94Weyi5j4,7DwaOIkZk8qLJKGX7XTF2l,6zHyWsqTzT6Fympdy9KQDQ,47Bg6IrMed1GPbxRgwH2aC,5mIOsPuQdXchVY0jB5NO9Q,7LBfVMw4MNNGCLGmXeuDv6,2VgQLPaAPaJRIXeL0FIW2q,4PvbbMYL4fkToni5BLaYRb,6R5JpLDVRgRI6P2OQCjA4n,3GCdLUSnKSMJhs4Tj6CV3s,6TMbGrU3ahGh0BaNI1ESWi,6Dvxpqv61hyRZJs4qDfiP3,6KfoDhO4XUWSbnyKjNp9c4,6uaBrivDHCaV0uBTiwHTUi,5hVghJ4KaYES3BFUATCYn0,6PGoSes0D9eUDeeAafB2As,57RA3JGafJm5zRtKJiKPIm,4EpZ4eYuZOwPSSwyqpdHnJ,2zPcVDSpYNVKQ5c7jR7MXj,0APAKxMXB7jdDs4kw1l30y,5oO3drDxtziYU2H1X23ZIp,6SwRhMLwNqEi6alNPVG00n,7MDKvOzNgAJ3KMCtaP2UOa,5EYi2rH4LYs6M21ZLOyQTx,1EaKU4dMbesXXd3BrLCtYG,6Nle9hKrkL1wQpwNfEkxjh,6U0FIYXCQ3TGrk4tFpLrEA,0gV5B7zmJkS1aaH9APokrH,0wSeTpuEBS5uloIJ9tGhFi,3D4uUFRoYDFHbkQlTKL2Om,0N3W5peJUQtI4eyR6GJT5O,0VgkVdmE4gld66l8iyGjgx"""


# In[646]:


track_ids2 = s2.replace('https://api.spotify.com/v1/audio-features?ids=','').split(',')


# In[647]:


res_aud_feat_tracks2 = spotify.tracks(track_ids2)


# In[649]:


aud_feat_tracks2 = res_aud_feat_tracks2['tracks']
[rec['name'] for rec in aud_feat_tracks2]


# In[ ]:




