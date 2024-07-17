from dataclasses import dataclass
from functools import cached_property

from googleapiclient.discovery import build
import requests
import csv


# Your API key goes here
api_key = 'AIzaSyA_vj5yr5hZ2lR96H6GUZdXq8AdJ9PHhU8'

youtube = build('youtube', 'v3', developerKey=api_key)


# Function to get video IDs from a channel
def get_video_ids_from_playlist(playlist_id='PLrJKMagQEL7ljEG9QXPyrXGNuzt_7XBPf'):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids += [item['snippet']['resourceId']['videoId'] for item in response['items']]

        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break

    return video_ids


@dataclass
class Video:
    title: str
    description: str
    video_id: str

    @staticmethod
    def split_by_part(text, split, return_first=True):
        try:
            first, second = text.split(split, 1)
            if return_first:
                return first
            else:
                return second
        except ValueError:
            return text

    @cached_property
    def clean_description(self):
        list = self.split_by_part(self.description, 'Check prices on Amazon below:', False)
        list = self.split_by_part(list, 'Check prices on Amazon:', False)
        list = self.split_by_part(list, '📸  Instagram - https://instagram.com/devyn.johnston')
        list = self.split_by_part(list, '🎥 CAMERA GEAR:')
        list = self.split_by_part(list, 'Checkout the')
        return list

    @cached_property
    def products(self):
        products = []
        for line in self.clean_description.split('\n'):
            if 'http' in line and 'video' not in line:
                products.append(line)
        return products


# Function to get video details
def get_video_details(video_ids):
    videos = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()

        for item in response['items']:
            title = item['snippet']['title']
            description = item['snippet']['description']
            # Transcription is not directly available, but you can download captions if they are available

            videos.append(Video(**{
                'title': title,
                'description': description,
                'video_id': video_id
            }))

    return videos


video_ids = get_video_ids_from_playlist()
videos = get_video_details(video_ids)

max_products = max([len(video.products) for video in videos])
file_list = []
for video in videos:
    products = video.products
    if len(products) < max_products:
        products += ['' for i in range(max_products - len(products))]

    file_list.append([video.title, *products])


with open('build_parts_list.csv', mode='w') as build_list:
    build_writer = csv.writer(build_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in zip(*file_list):
        build_writer.writerow(row)
