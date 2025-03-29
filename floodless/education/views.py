import os
import requests
from django.shortcuts import render
from django.conf import settings
# YouTube API key
YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

def education_view(request):
    disaster_type = request.GET.get('disaster_type', 'Earthquake')  # Default to 'Earthquake'
    videos = []

    if disaster_type:
        # Define search query based on disaster type
        search_query = f"{disaster_type} disaster management life hacks"
        
        # YouTube API endpoint
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': search_query,
            'type': 'video',
            'maxResults': 6,  # Fetch 6 videos
            'key': YOUTUBE_API_KEY,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Extract video details
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                thumbnail = item['snippet']['thumbnails']['medium']['url']
                video_link = f"https://www.youtube.com/watch?v={video_id}"

                videos.append({
                    'title': title,
                    'thumbnail': thumbnail,
                    'link': video_link,
                })

        except requests.exceptions.RequestException as e:
            print(f"Error fetching YouTube videos: {e}")
            videos = []  # Fallback to empty list if API call fails

    context = {
        'disaster_type': disaster_type,
        'videos': videos,
    }
    return render(request, 'education/education.html', context)
