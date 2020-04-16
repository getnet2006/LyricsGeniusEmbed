# LyricsGeniusEmbed
This repository contain a code which download a song lyrics from genius and embed it to the audio file. It uses beautifulsoup for scraping and eyed3 for embeding the lyrics to audio file.

For downloading an full album songs use:
    python downloadembed.py -n name_artist -a_t song_title -dir_n "album directory" -alb

To download a lyrics of songs in the certain directory and embed it use:
    python downloadembed.py -dir_n "name_directory" -dirc
