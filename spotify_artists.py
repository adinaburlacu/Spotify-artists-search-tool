from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv


# Replace with your Spotify API credentials
load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


# Authentication with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



#Function to search for artists by genre and popularity

def artists_by_genre(genre, popularity_threshold):
    artists = []
    offset = 0 

    while True:
        #Response from the API in JSON format
        results = sp.search(q=f'genre:"{genre}"', type='artist', offset=offset)
        #Within the 'artists' section, there is another key called 'items' which contains the artists info
        items = results['artists']['items']  

        if not items: # If there are no more items, break the loop
            break

        for artist in items:
            if artist['popularity'] < popularity_threshold:
                artists.append(artist)  # Append the artist to the 'artists' list
        
        offset += len(items) # increment the offset variable by the number of items retrieved in the current API request

    return artists






# Function to extract the artist's information
def artist_info(artist):
    artist_info = {
        'Artist_ID': artist['id'],
        'Name': artist['name'],
        'Genres': ', '.join(artist['genres']),  # Join the genres into a comma-separated string
        'Popularity': artist['popularity']
    }
    return artist_info





#The main function

if __name__ == '__main__':
    genre = input('Enter a genre => ').lower()
    popularity_threshold = int(input('On a scale of 1 to 100, how popular? => '))

    artists = artists_by_genre(genre, popularity_threshold)

    if not artists:
        print('No artist found.')
    
    else:
        print('Artists found.')

         # Specify the CSV file name
        csv_file_name = f'artists_genre_{genre}.csv'

        # Define the fieldnames in the same order as in your CSV
        fieldnames = ['Artist_ID', 'Name', 'Genres', 'Popularity']

        # Write artist information to a CSV file
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()  # Write CSV header

            for artist in artists:
                artist_information = artist_info(artist)
                writer.writerow(artist_information)

            print(f"Artist information saved to {csv_file_name}")