"""
Translations for bot UI messages
Supports multiple languages
"""

# Supported languages with their TMDB codes
SUPPORTED_LANGUAGES = {
    "en": {"name": "🇬🇧 English", "tmdb_code": "en-US"},
    "fr": {"name": "🇫🇷 Français", "tmdb_code": "fr-FR"},
    "es": {"name": "🇪🇸 Español", "tmdb_code": "es-ES"},
    "de": {"name": "🇩🇪 Deutsch", "tmdb_code": "de-DE"},
    "it": {"name": "🇮🇹 Italiano", "tmdb_code": "it-IT"},
    "pt": {"name": "🇵🇹 Português", "tmdb_code": "pt-PT"},
    "ar": {"name": "🇸🇦 العربية", "tmdb_code": "ar-SA"},
    "ja": {"name": "🇯🇵 日本語", "tmdb_code": "ja-JP"},
    "ko": {"name": "🇰🇷 한국어", "tmdb_code": "ko-KR"},
    "zh": {"name": "🇨🇳 中文", "tmdb_code": "zh-CN"},
    "ru": {"name": "🇷🇺 Русский", "tmdb_code": "ru-RU"},
    "tr": {"name": "🇹🇷 Türkçe", "tmdb_code": "tr-TR"},
    "hi": {"name": "🇮🇳 हिन्दी", "tmdb_code": "hi-IN"},
    "nl": {"name": "🇳🇱 Nederlands", "tmdb_code": "nl-NL"},
    "pl": {"name": "🇵🇱 Polski", "tmdb_code": "pl-PL"},
}

# UI translations
TRANSLATIONS = {
    "en": {
        "welcome": """
🎬 <b>Welcome to Movie & Series Bot!</b> 🎬

Your personal guide to the latest movies and TV series!

<b>What I can do:</b>
• 🎬 Show latest movies in theaters
• 📺 Show latest TV series episodes
• 🔥 Show what's trending this week
• 🔍 Search for any movie or series
• ⭐ Show popular content

<b>Commands:</b>
/movies - Latest movies
/series - Latest TV series
/trending - Trending now
/search [query] - Search
/language - Change language

Use the buttons below to get started! 👇
""",
        "latest_movies": "🎬 Latest Movies",
        "latest_series": "📺 Latest Series",
        "trending": "🔥 Trending Now",
        "search": "🔍 Search",
        "popular_movies": "⭐ Popular Movies",
        "popular_series": "⭐ Popular Series",
        "language": "🌍 Language",
        "main_menu": "🏠 Main Menu",
        "previous": "⬅️ Previous",
        "next": "Next ➡️",
        "details": "📖 Details",
        "trailer": "▶️ Trailer",
        "now_playing": "🎬 <b>NOW PLAYING</b> 🎬",
        "airing_today": "📺 <b>AIRING TODAY</b> 📺",
        "trending_week": "🔥 <b>TRENDING THIS WEEK</b> 🔥",
        "popular_movies_title": "⭐ <b>POPULAR MOVIES</b> ⭐",
        "popular_series_title": "⭐ <b>POPULAR SERIES</b> ⭐",
        "search_title": "🔍 <b>Search:</b>",
        "no_results": "❌ No results found.",
        "no_movies": "❌ No movies found.",
        "no_series": "❌ No TV series found.",
        "no_trailer": "❌ No trailer available",
        "opening_trailer": "▶️ Opening trailer...",
        "select_language": "🌍 <b>Select your language:</b>",
        "language_set": "✅ Language set to English!",
        "rating": "⭐ Rating",
        "release": "📅 Release",
        "first_aired": "📅 First Aired",
        "runtime": "⏱️ Runtime",
        "seasons": "🎬 Seasons",
        "episodes": "Episodes",
        "status": "📊 Status",
        "genres": "🎭 Genres",
        "overview": "📝 <b>Overview:</b>",
        "how_to_search": "🔍 <b>How to search:</b>\n\n1️⃣ Use command: <code>/search Movie Name</code>\n\n2️⃣ Or use inline mode:\nType <code>@YourBotName query</code> in any chat",
        "back": "Back",
        # Favorites
        "favorites": "Favorites",
        "fav_description": "Manage your favorite movies and series",
        "fav_movies": "Movies",
        "fav_series": "Series",
        "fav_empty": "No favorites yet. Browse movies/series and add some!",
        "fav_count": "You have {count} item(s)",
        "fav_added": "Added to favorites!",
        "fav_removed": "Removed from favorites",
        "fav_already": "Already in favorites",
        "fav_remove_btn": "Remove",
        # Subscriptions
        "subscriptions": "Subscriptions",
        "sub_description": "Subscribe to topics and get notified about new content!",
        "sub_active": "Active subscriptions",
        "my_subscriptions": "My Subscriptions",
        "sub_manage": "Tap to unsubscribe:",
        "sub_empty": "You have no active subscriptions.",
        "subscribed": "Subscribed!",
        "unsubscribed": "Unsubscribed",
        "unsubscribe": "Unsubscribe",
        # Subscription topics
        "sub_new_movies": "New Movies",
        "sub_new_series": "New Series",
        "sub_trending": "Trending",
        "sub_action": "Action",
        "sub_comedy": "Comedy",
        "sub_drama": "Drama",
        "sub_horror": "Horror",
        "sub_scifi": "Sci-Fi",
        "sub_romance": "Romance",
        "sub_animation": "Animation",
    },
    "fr": {
        "welcome": """
🎬 <b>Bienvenue sur Movie & Series Bot!</b> 🎬

Votre guide personnel pour les derniers films et séries TV!

<b>Ce que je peux faire:</b>
• 🎬 Afficher les derniers films au cinéma
• 📺 Afficher les derniers épisodes de séries
• 🔥 Afficher les tendances de la semaine
• 🔍 Rechercher n'importe quel film ou série
• ⭐ Afficher le contenu populaire

<b>Commandes:</b>
/movies - Derniers films
/series - Dernières séries
/trending - Tendances
/search [requête] - Rechercher
/language - Changer de langue

Utilisez les boutons ci-dessous pour commencer! 👇
""",
        "latest_movies": "🎬 Derniers Films",
        "latest_series": "📺 Dernières Séries",
        "trending": "🔥 Tendances",
        "search": "🔍 Rechercher",
        "popular_movies": "⭐ Films Populaires",
        "popular_series": "⭐ Séries Populaires",
        "language": "🌍 Langue",
        "main_menu": "🏠 Menu Principal",
        "previous": "⬅️ Précédent",
        "next": "Suivant ➡️",
        "details": "📖 Détails",
        "trailer": "▶️ Bande-annonce",
        "now_playing": "🎬 <b>À L'AFFICHE</b> 🎬",
        "airing_today": "📺 <b>DIFFUSÉ AUJOURD'HUI</b> 📺",
        "trending_week": "🔥 <b>TENDANCES DE LA SEMAINE</b> 🔥",
        "popular_movies_title": "⭐ <b>FILMS POPULAIRES</b> ⭐",
        "popular_series_title": "⭐ <b>SÉRIES POPULAIRES</b> ⭐",
        "search_title": "🔍 <b>Recherche:</b>",
        "no_results": "❌ Aucun résultat trouvé.",
        "no_movies": "❌ Aucun film trouvé.",
        "no_series": "❌ Aucune série trouvée.",
        "no_trailer": "❌ Pas de bande-annonce disponible",
        "opening_trailer": "▶️ Ouverture de la bande-annonce...",
        "select_language": "🌍 <b>Choisissez votre langue:</b>",
        "language_set": "✅ Langue définie sur Français!",
        "rating": "⭐ Note",
        "release": "📅 Sortie",
        "first_aired": "📅 Première diffusion",
        "runtime": "⏱️ Durée",
        "seasons": "🎬 Saisons",
        "episodes": "Épisodes",
        "status": "📊 Statut",
        "genres": "🎭 Genres",
        "overview": "📝 <b>Synopsis:</b>",
        "how_to_search": "🔍 <b>Comment rechercher:</b>\n\n1️⃣ Utilisez la commande: <code>/search Nom du film</code>\n\n2️⃣ Ou utilisez le mode inline:\nTapez <code>@VotreBot requête</code> dans n'importe quel chat",
    },
    "es": {
        "welcome": """
🎬 <b>¡Bienvenido a Movie & Series Bot!</b> 🎬

¡Tu guía personal para las últimas películas y series de TV!

<b>Lo que puedo hacer:</b>
• 🎬 Mostrar las últimas películas en cartelera
• 📺 Mostrar los últimos episodios de series
• 🔥 Mostrar las tendencias de la semana
• 🔍 Buscar cualquier película o serie
• ⭐ Mostrar contenido popular

<b>Comandos:</b>
/movies - Últimas películas
/series - Últimas series
/trending - Tendencias
/search [consulta] - Buscar
/language - Cambiar idioma

¡Usa los botones de abajo para comenzar! 👇
""",
        "latest_movies": "🎬 Últimas Películas",
        "latest_series": "📺 Últimas Series",
        "trending": "🔥 Tendencias",
        "search": "🔍 Buscar",
        "popular_movies": "⭐ Películas Populares",
        "popular_series": "⭐ Series Populares",
        "language": "🌍 Idioma",
        "main_menu": "🏠 Menú Principal",
        "previous": "⬅️ Anterior",
        "next": "Siguiente ➡️",
        "details": "📖 Detalles",
        "trailer": "▶️ Tráiler",
        "now_playing": "🎬 <b>EN CARTELERA</b> 🎬",
        "airing_today": "📺 <b>EN EMISIÓN HOY</b> 📺",
        "trending_week": "🔥 <b>TENDENCIAS DE LA SEMANA</b> 🔥",
        "popular_movies_title": "⭐ <b>PELÍCULAS POPULARES</b> ⭐",
        "popular_series_title": "⭐ <b>SERIES POPULARES</b> ⭐",
        "search_title": "🔍 <b>Búsqueda:</b>",
        "no_results": "❌ No se encontraron resultados.",
        "no_movies": "❌ No se encontraron películas.",
        "no_series": "❌ No se encontraron series.",
        "no_trailer": "❌ No hay tráiler disponible",
        "opening_trailer": "▶️ Abriendo tráiler...",
        "select_language": "🌍 <b>Selecciona tu idioma:</b>",
        "language_set": "✅ ¡Idioma configurado a Español!",
        "rating": "⭐ Puntuación",
        "release": "📅 Estreno",
        "first_aired": "📅 Primera emisión",
        "runtime": "⏱️ Duración",
        "seasons": "🎬 Temporadas",
        "episodes": "Episodios",
        "status": "📊 Estado",
        "genres": "🎭 Géneros",
        "overview": "📝 <b>Sinopsis:</b>",
        "how_to_search": "🔍 <b>Cómo buscar:</b>\n\n1️⃣ Usa el comando: <code>/search Nombre de película</code>\n\n2️⃣ O usa el modo inline:\nEscribe <code>@TuBot consulta</code> en cualquier chat",
    },
    "ar": {
        "welcome": """
🎬 <b>مرحباً بك في بوت الأفلام والمسلسلات!</b> 🎬

دليلك الشخصي لأحدث الأفلام والمسلسلات!

<b>ما يمكنني فعله:</b>
• 🎬 عرض أحدث الأفلام في السينما
• 📺 عرض أحدث حلقات المسلسلات
• 🔥 عرض الأكثر رواجاً هذا الأسبوع
• 🔍 البحث عن أي فيلم أو مسلسل
• ⭐ عرض المحتوى الشائع

<b>الأوامر:</b>
/movies - أحدث الأفلام
/series - أحدث المسلسلات
/trending - الرائج
/search [بحث] - بحث
/language - تغيير اللغة

استخدم الأزرار أدناه للبدء! 👇
""",
        "latest_movies": "🎬 أحدث الأفلام",
        "latest_series": "📺 أحدث المسلسلات",
        "trending": "🔥 الرائج",
        "search": "🔍 بحث",
        "popular_movies": "⭐ أفلام شائعة",
        "popular_series": "⭐ مسلسلات شائعة",
        "language": "🌍 اللغة",
        "main_menu": "🏠 القائمة الرئيسية",
        "previous": "⬅️ السابق",
        "next": "التالي ➡️",
        "details": "📖 تفاصيل",
        "trailer": "▶️ إعلان",
        "now_playing": "🎬 <b>يُعرض الآن</b> 🎬",
        "airing_today": "📺 <b>يُبث اليوم</b> 📺",
        "trending_week": "🔥 <b>الأكثر رواجاً هذا الأسبوع</b> 🔥",
        "popular_movies_title": "⭐ <b>الأفلام الشائعة</b> ⭐",
        "popular_series_title": "⭐ <b>المسلسلات الشائعة</b> ⭐",
        "search_title": "🔍 <b>بحث:</b>",
        "no_results": "❌ لم يتم العثور على نتائج.",
        "no_movies": "❌ لم يتم العثور على أفلام.",
        "no_series": "❌ لم يتم العثور على مسلسلات.",
        "no_trailer": "❌ لا يوجد إعلان متاح",
        "opening_trailer": "▶️ جاري فتح الإعلان...",
        "select_language": "🌍 <b>اختر لغتك:</b>",
        "language_set": "✅ تم تعيين اللغة إلى العربية!",
        "rating": "⭐ التقييم",
        "release": "📅 الإصدار",
        "first_aired": "📅 أول بث",
        "runtime": "⏱️ المدة",
        "seasons": "🎬 المواسم",
        "episodes": "الحلقات",
        "status": "📊 الحالة",
        "genres": "🎭 الأنواع",
        "overview": "📝 <b>نظرة عامة:</b>",
        "how_to_search": "🔍 <b>كيفية البحث:</b>\n\n1️⃣ استخدم الأمر: <code>/search اسم الفيلم</code>\n\n2️⃣ أو استخدم الوضع المضمن:\nاكتب <code>@اسم_البوت بحث</code> في أي محادثة",
    },
}

# Default to English for unsupported languages
def get_text(lang_code: str, key: str) -> str:
    """Get translated text for a key"""
    lang = lang_code if lang_code in TRANSLATIONS else "en"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["en"].get(key, key))

def get_tmdb_language(lang_code: str) -> str:
    """Get TMDB language code"""
    lang = lang_code if lang_code in SUPPORTED_LANGUAGES else "en"
    return SUPPORTED_LANGUAGES[lang]["tmdb_code"]
