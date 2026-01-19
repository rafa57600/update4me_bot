"""
User preferences storage - Extended with Favorites and Subscriptions
Stores user language preferences, favorites, and subscriptions in a JSON file
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

# File path for storing user preferences
PREFS_FILE = os.path.join(os.path.dirname(__file__), "user_prefs.json")


def _load_prefs() -> Dict:
    """Load preferences from file"""
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_prefs(prefs: Dict) -> None:
    """Save preferences to file"""
    try:
        with open(PREFS_FILE, "w", encoding="utf-8") as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _get_user_data(user_id: int) -> Dict:
    """Get user data, creating if not exists"""
    prefs = _load_prefs()
    user_key = str(user_id)
    if user_key not in prefs:
        prefs[user_key] = {
            "language": "en",
            "favorites": {"movies": [], "series": []},
            "subscriptions": []
        }
        _save_prefs(prefs)
    return prefs[user_key]


# ============ Language Functions ============

def get_user_language(user_id: int) -> str:
    """Get user's preferred language (default: en)"""
    return _get_user_data(user_id).get("language", "en")


def set_user_language(user_id: int, language: str) -> None:
    """Set user's preferred language"""
    prefs = _load_prefs()
    user_key = str(user_id)
    if user_key not in prefs:
        prefs[user_key] = {"language": "en", "favorites": {"movies": [], "series": []}, "subscriptions": []}
    prefs[user_key]["language"] = language
    _save_prefs(prefs)


# ============ Favorites Functions ============

def get_favorites(user_id: int, media_type: str = "movies") -> List[Dict]:
    """Get user's favorite movies or series"""
    user_data = _get_user_data(user_id)
    favorites = user_data.get("favorites", {"movies": [], "series": []})
    return favorites.get(media_type, [])


def add_favorite(user_id: int, media_type: str, item_id: int, title: str, poster_path: Optional[str] = None) -> bool:
    """Add item to favorites. Returns True if added, False if already exists."""
    prefs = _load_prefs()
    user_key = str(user_id)
    
    if user_key not in prefs:
        prefs[user_key] = {"language": "en", "favorites": {"movies": [], "series": []}, "subscriptions": []}
    
    if "favorites" not in prefs[user_key]:
        prefs[user_key]["favorites"] = {"movies": [], "series": []}
    
    if media_type not in prefs[user_key]["favorites"]:
        prefs[user_key]["favorites"][media_type] = []
    
    # Check if already in favorites
    for fav in prefs[user_key]["favorites"][media_type]:
        if fav.get("id") == item_id:
            return False
    
    # Add to favorites
    prefs[user_key]["favorites"][media_type].append({
        "id": item_id,
        "title": title,
        "poster_path": poster_path,
        "added_at": datetime.now().isoformat()
    })
    
    _save_prefs(prefs)
    return True


def remove_favorite(user_id: int, media_type: str, item_id: int) -> bool:
    """Remove item from favorites. Returns True if removed, False if not found."""
    prefs = _load_prefs()
    user_key = str(user_id)
    
    if user_key not in prefs:
        return False
    
    if "favorites" not in prefs[user_key]:
        return False
    
    if media_type not in prefs[user_key]["favorites"]:
        return False
    
    # Find and remove
    for i, fav in enumerate(prefs[user_key]["favorites"][media_type]):
        if fav.get("id") == item_id:
            prefs[user_key]["favorites"][media_type].pop(i)
            _save_prefs(prefs)
            return True
    
    return False


def is_favorite(user_id: int, media_type: str, item_id: int) -> bool:
    """Check if item is in favorites"""
    favorites = get_favorites(user_id, media_type)
    for fav in favorites:
        if fav.get("id") == item_id:
            return True
    return False


# ============ Subscription Functions ============

# Available subscription topics
SUBSCRIPTION_TOPICS = {
    "new_movies": {"emoji": "🎬", "name_key": "sub_new_movies"},
    "new_series": {"emoji": "📺", "name_key": "sub_new_series"},
    "trending": {"emoji": "🔥", "name_key": "sub_trending"},
    "action": {"emoji": "💥", "name_key": "sub_action"},
    "comedy": {"emoji": "😂", "name_key": "sub_comedy"},
    "drama": {"emoji": "🎭", "name_key": "sub_drama"},
    "horror": {"emoji": "👻", "name_key": "sub_horror"},
    "scifi": {"emoji": "🚀", "name_key": "sub_scifi"},
    "romance": {"emoji": "💕", "name_key": "sub_romance"},
    "animation": {"emoji": "🎨", "name_key": "sub_animation"},
}


def get_subscriptions(user_id: int) -> List[str]:
    """Get user's subscription topics"""
    user_data = _get_user_data(user_id)
    return user_data.get("subscriptions", [])


def add_subscription(user_id: int, topic: str) -> bool:
    """Subscribe to a topic. Returns True if subscribed, False if already subscribed."""
    if topic not in SUBSCRIPTION_TOPICS:
        return False
    
    prefs = _load_prefs()
    user_key = str(user_id)
    
    if user_key not in prefs:
        prefs[user_key] = {"language": "en", "favorites": {"movies": [], "series": []}, "subscriptions": []}
    
    if "subscriptions" not in prefs[user_key]:
        prefs[user_key]["subscriptions"] = []
    
    if topic in prefs[user_key]["subscriptions"]:
        return False
    
    prefs[user_key]["subscriptions"].append(topic)
    _save_prefs(prefs)
    return True


def remove_subscription(user_id: int, topic: str) -> bool:
    """Unsubscribe from a topic. Returns True if unsubscribed, False if not found."""
    prefs = _load_prefs()
    user_key = str(user_id)
    
    if user_key not in prefs:
        return False
    
    if "subscriptions" not in prefs[user_key]:
        return False
    
    if topic not in prefs[user_key]["subscriptions"]:
        return False
    
    prefs[user_key]["subscriptions"].remove(topic)
    _save_prefs(prefs)
    return True


def is_subscribed(user_id: int, topic: str) -> bool:
    """Check if user is subscribed to a topic"""
    subscriptions = get_subscriptions(user_id)
    return topic in subscriptions


def get_all_subscribers(topic: str) -> List[int]:
    """Get all user IDs subscribed to a topic"""
    prefs = _load_prefs()
    subscribers = []
    
    for user_key, user_data in prefs.items():
        if topic in user_data.get("subscriptions", []):
            try:
                subscribers.append(int(user_key))
            except ValueError:
                pass
    
    return subscribers
