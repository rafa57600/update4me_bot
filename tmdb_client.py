"""
TMDB API Client - Async wrapper for The Movie Database API - Localized
"""

import aiohttp
from typing import Optional, Dict, Any
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE


class TMDBClient:
    """Async client for TMDB API"""
    
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base = TMDB_IMAGE_BASE
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def _request(self, endpoint: str, params: Optional[Dict] = None, language: str = "en-US") -> Dict[str, Any]:
        """Make a request to TMDB API"""
        session = await self._get_session()
        
        url = f"{self.base_url}{endpoint}"
        request_params = {
            "api_key": self.api_key,
            "language": language,
            **(params or {})
        }
        
        async with session.get(url, params=request_params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"results": [], "error": f"API Error: {response.status}"}
    
    async def get_now_playing_movies(self, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Get movies currently in theaters"""
        return await self._request("/movie/now_playing", {"page": page}, language=language)
    
    async def get_popular_movies(self, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Get popular movies"""
        return await self._request("/movie/popular", {"page": page}, language=language)
    
    async def get_latest_series(self, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Get latest TV series (airing today)"""
        return await self._request("/tv/airing_today", {"page": page}, language=language)
    
    async def get_popular_series(self, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Get popular TV series"""
        return await self._request("/tv/popular", {"page": page}, language=language)
    
    async def get_trending(self, media_type: str = "all", time_window: str = "week", page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Get trending movies/series"""
        return await self._request(f"/trending/{media_type}/{time_window}", {"page": page}, language=language)
    
    async def search_movies(self, query: str, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Search for movies"""
        return await self._request("/search/movie", {"query": query, "page": page}, language=language)
    
    async def search_series(self, query: str, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Search for TV series"""
        return await self._request("/search/tv", {"query": query, "page": page}, language=language)
    
    async def search_multi(self, query: str, page: int = 1, language: str = "en-US") -> Dict[str, Any]:
        """Search for movies and TV series"""
        return await self._request("/search/multi", {"query": query, "page": page}, language=language)
    
    async def get_movie_details(self, movie_id: int, language: str = "en-US") -> Dict[str, Any]:
        """Get movie details"""
        return await self._request(f"/movie/{movie_id}", language=language)
    
    async def get_series_details(self, series_id: int, language: str = "en-US") -> Dict[str, Any]:
        """Get TV series details"""
        return await self._request(f"/tv/{series_id}", language=language)
    
    async def get_movie_videos(self, movie_id: int, language: str = "en-US") -> Dict[str, Any]:
        """Get movie videos (trailers)"""
        return await self._request(f"/movie/{movie_id}/videos", language=language)
    
    async def get_series_videos(self, series_id: int, language: str = "en-US") -> Dict[str, Any]:
        """Get series videos (trailers)"""
        return await self._request(f"/tv/{series_id}/videos", language=language)
    
    def get_poster_url(self, poster_path: Optional[str]) -> Optional[str]:
        """Get full poster URL"""
        if poster_path:
            return f"{self.image_base}{poster_path}"
        return None
    
    def format_movie(self, movie: Dict[str, Any], lang: str = "en") -> str:
        """Format movie data for display"""
        title = movie.get("title", "Unknown")
        rating = movie.get("vote_average", 0)
        release_date = movie.get("release_date", "N/A")[:10] if movie.get("release_date") else "N/A"
        overview = movie.get("overview", "No description available.")
        
        # Truncate overview if too long
        if len(overview) > 300:
            overview = overview[:297] + "..."
        
        return (
            f"<b>{title}</b>\n"
            f"⭐ {rating:.1f}/10 | 📅 {release_date}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{overview}"
        )
    
    def format_series(self, series: Dict[str, Any], lang: str = "en") -> str:
        """Format series data for display"""
        title = series.get("name", "Unknown")
        rating = series.get("vote_average", 0)
        first_air_date = series.get("first_air_date", "N/A")[:10] if series.get("first_air_date") else "N/A"
        overview = series.get("overview", "No description available.")
        
        # Truncate overview if too long
        if len(overview) > 300:
            overview = overview[:297] + "..."
        
        return (
            f"<b>{title}</b>\n"
            f"⭐ {rating:.1f}/10 | 📅 {first_air_date}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{overview}"
        )
    
    def format_trending_item(self, item: Dict[str, Any], lang: str = "en") -> str:
        """Format trending item (movie or series)"""
        media_type = item.get("media_type", "movie")
        
        if media_type == "movie":
            return self.format_movie(item, lang)
        elif media_type == "tv":
            return self.format_series(item, lang)
        else:
            title = item.get("title") or item.get("name", "Unknown")
            return f"🔥 <b>{title}</b>"


# Global client instance
tmdb = TMDBClient()
