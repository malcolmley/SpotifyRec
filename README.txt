The focus of your app is on customizing recommendations,

For recommendations, allow user to control by
- genre
- time (emphasize current playlists, all-time, custom time-range)
- spotify popularity rating (right now this is hard-coded to a max of 55)
- your personal popularity rating - this may be a combination of your top artists and tracks and some other info we can get via Spotify API
mood?
- obscurify rating

Initially, I focused on getting recommended tracks and then add in artists, albums, etc.

Spotify has 'showcase' apps to see what other developers have done with the API.  For example
Dubolt: you select the artists/tracks and then you can filter recommendations by popularity and music features
Magic Playlist: you pick the song, gets related artists

Some technical notes
Obscurify uses Angular for web app - never used it but maybe I will play around with it.
I can see the the Spotify calls Obscurify makes using Firefox's Web Developer Tools. 
