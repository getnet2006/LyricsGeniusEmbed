import argparse
import requests
from bs4 import BeautifulSoup
import time
import os
import eyed3

# embed the downloaded lyrics to its respective audio file
def embed_lyrics(lyrics_content,album_directory,song_title):
    try:
        songs_dir = ['{}/{}'.format(album_directory,file_name) for file_name in os.listdir(album_directory)] # full songs file and directory
        songs_t = [i[:-4] for i in os.listdir(album_directory)] # remove file extention
        lyrics_content = '\n'.join(lyrics_content)
        
        lyrics_content = lyrics_content.encode('latin-1', 'ignore')
        lyrics_content = lyrics_content.decode('utf8')

        for song,song_dir in zip(songs_t, songs_dir):
            if song_title in song:
                print(f'Embeding the lyrics to {song_title}')
                track_tag = eyed3.load(song_dir).tag
                track_tag.lyrics.set(lyrics_content)
                track_tag.save()
            else:
                print("Song not found")
    except Exception as ex:
        print(ex)


def main():
    # To download entire album song lyrics and embed the lyrics to audio file use this command
    
    # To download and embed an album lyrics use python downloadembed.py -n name_artist -a_t song_title -dir_n "album directory" -alb
    # To download a lyrics of songs in the certain directory and embed it use python downloadembed.py -dir_n "name_directory" -dirc
    # Surround directory name with quotation 
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name', type=str, nargs='+', help='The artist name')
    parser.add_argument('-a_t','--album_title', type=str,nargs='+', help='The album title')
    parser.add_argument('-dir_n','--directory_name', type=str, help='The directory where songs reside for downloading the lyrics(surround the directory with double quote)')
    
    # If the following two arguments mentioned in the command the argument will be true else it is False
    parser.add_argument('-alb','--album', action='store_true', help='To download lyrics of whole album track default False')
    parser.add_argument('-dirc','--directory', action='store_true', help='Shows if the script going to download lyrics of songs in the directory')
    arg = parser.parse_args()
    
    # Checking if the directory is true or false 
    if arg.directory:
        song_files = ["{}/{}".format(arg.directory_name,i) for i in os.listdir(arg.directory_name) if i.endswith('.mp3')] # songs in the directory and thier full directory
        song_lyrics_urls = []
        for song_file in song_files:
            song_tag = eyed3.load(song_file).tag
            artist_name = song_tag.artist         # artist name 
            song_title = '-'.join(song_tag.title.split(' '))  # song title
            if ',' in artist_name:
                artist_name = '-'.join(artist_name.split(',')[0].split(' '))
            elif '&' in artist_name:
                artist_name = artist_name.split(' ')
                artist_name = ['and' if i=='&' else i for i in artist_name]
                artist_name = '-'.join(artist_name)
            else:
                artist_name = '-'.join(artist_name.split(' '))
            
            artist_title = '-'.join([artist_name,song_title])
            song_lyrics_urls.append('https://genius.com/{}-lyrics'.format(artist_title))
        song_lyrics_urls = [song_lyrics_url.replace("'",'') if "'" in song_lyrics_url else song_lyrics_url for song_lyrics_url in song_lyrics_urls]

        for song_lyrics_url in song_lyrics_urls:
            req = requests.get(song_lyrics_url)
            soup = BeautifulSoup(req.text,'html.parser')
            singer_and_title = ' '.join(song_lyrics_url[song_lyrics_url.index('m/')+2:].split('-'))
            
            if soup.find('title').get_text() == 'Burrr! | Genius':
                print(singer_and_title +" doesn't exists")
            else:
                song_title = soup.find('title').get_text()
                print(f'Downloading {song_title}')
                lyrics = soup.find('div', class_='lyrics').find('p').getText().split('\n')
                embed_lyrics(lyrics, arg.directory_name, song_title[:song_title.index('Lyrics')-1][song_title.index('– ')+2:])
            time.sleep(7)
    else:
        singer_and_title = '-'.join(arg.name+arg.album_title)
        album_location = arg.directory_name # song location to embed the lyrics

        # Checking if the script want to download album lyrics
        if arg.album:
            singer = '-'.join(arg.name)
            album_name = '-'.join(arg.album_title)
            album_site=f'https://genius.com/albums/{singer}/{album_name}'
            req = requests.get(album_site)
            soup = BeautifulSoup(req.text,'html.parser')

            if not soup.find('title').get_text() == 'Burrr! | Genius':
                link_ls = [i.get('href') for i in soup.find_all('a',class_='u-display_block')]
                son_titles = [i.get_text().replace('Lyrics','').strip() for i in soup.find_all('h3',class_='chart_row-content-title')]
                lyrics_and_title = {}
                for link, s_title in zip(link_ls,son_titles):
                    req = requests.get(link)
                    soup = BeautifulSoup(req.text,'html.parser')
                    title_for_dic = soup.find('title').get_text()
                    print(f'Downloading {title_for_dic}')
                    lyrics = soup.find('div', class_='lyrics').find('p').getText().split('\n')
                    lyrics_and_title[title_for_dic] = lyrics
                    embed_lyrics(lyrics,album_location,s_title)
                    time.sleep(7)
            else:
                print(album_name +" doesn't exists")

if __name__ == '__main__':
    main()
        