"""YouTube Discovery MCP server.

Returns curated educational video recommendations using YouTube Data API.
"""
from typing import List, Dict, Any
import os
from googleapiclient.discovery import build


class YouTubeMCP:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key) if self.api_key else None
    
    def is_available(self) -> bool:
        """Check if YouTube API is available."""
        return bool(self.api_key)
    
    async def find_tutorials(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Find tutorial videos for a topic."""
        if not self.is_available():
            # Fallback to stub
            return [
                {
                    "title": f"{topic} - Tutorial",
                    "channel": "EduChannel",
                    "url": f"https://youtube.com/watch?v=example",
                    "duration": 600,
                    "thumbnail": "https://img.youtube.com/vi/example/default.jpg"
                }
            ]
        
        try:
            search_response = self.youtube.search().list(
                q=f"{topic} tutorial educational",
                part='id,snippet',
                maxResults=min(max_results, 10),
                type='video',
                order='relevance',
                videoDuration='medium'
            ).execute()
            
            videos = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                videos.append({
                    "title": snippet['title'],
                    "channel": snippet['channelTitle'],
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "duration": 0,  # Would need additional API call to get duration
                    "thumbnail": snippet['thumbnails']['default']['url'],
                    "description": snippet.get('description', '')[:200]
                })
            return videos
        except Exception as e:
            print(f"YouTube search failed: {e}")
            return []

    async def find_revision_videos(self, topic: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Find revision/crash course videos for a topic."""
        if not self.is_available():
            # Fallback to stub
            return [
                {
                    "title": f"{topic} - Revision",
                    "channel": "RevisionChannel",
                    "url": f"https://youtube.com/watch?v=revision",
                    "duration": 300,
                    "thumbnail": "https://img.youtube.com/vi/revision/default.jpg"
                }
            ]
        
        try:
            search_response = self.youtube.search().list(
                q=f"{topic} crash course revision summary",
                part='id,snippet',
                maxResults=min(max_results, 5),
                type='video',
                order='relevance',
                videoDuration='short'
            ).execute()
            
            videos = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                videos.append({
                    "title": snippet['title'],
                    "channel": snippet['channelTitle'],
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "duration": 0,
                    "thumbnail": snippet['thumbnails']['default']['url'],
                    "description": snippet.get('description', '')[:200]
                })
            return videos
        except Exception as e:
            print(f"YouTube revision search failed: {e}")
            return []
