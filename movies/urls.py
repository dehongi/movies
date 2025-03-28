from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    # Home and search
    path("", views.HomeView.as_view(), name="home"),
    path("search/", views.SearchView.as_view(), name="search"),
    # Genre URLs
    path("genres/", views.GenreListView.as_view(), name="genre_list"),
    path("genres/<slug:slug>/", views.GenreDetailView.as_view(), name="genre_detail"),
    path("genres/create/", views.GenreCreateView.as_view(), name="genre_create"),
    path(
        "genres/<slug:slug>/update/",
        views.GenreUpdateView.as_view(),
        name="genre_update",
    ),
    path(
        "genres/<slug:slug>/delete/",
        views.GenreDeleteView.as_view(),
        name="genre_delete",
    ),
    # MediaType URLs
    path("mediatypes/", views.MediaTypeListView.as_view(), name="mediatype_list"),
    path(
        "mediatypes/create/",
        views.MediaTypeCreateView.as_view(),
        name="mediatype_create",
    ),
    path(
        "mediatypes/<int:pk>/update/",
        views.MediaTypeUpdateView.as_view(),
        name="mediatype_update",
    ),
    path(
        "mediatypes/<int:pk>/delete/",
        views.MediaTypeDeleteView.as_view(),
        name="mediatype_delete",
    ),
    # Media URLs
    path("media/", views.MediaListView.as_view(), name="media_list"),
    path("media/<slug:slug>/", views.MediaDetailView.as_view(), name="media_detail"),
    path("media/create/", views.MediaCreateView.as_view(), name="media_create"),
    path(
        "media/<slug:slug>/update/",
        views.MediaUpdateView.as_view(),
        name="media_update",
    ),
    path(
        "media/<slug:slug>/delete/",
        views.MediaDeleteView.as_view(),
        name="media_delete",
    ),
    # Movie URLs
    path("movies/create/", views.MovieCreateView.as_view(), name="movie_create"),
    path(
        "movies/<slug:slug>/update/",
        views.MovieUpdateView.as_view(),
        name="movie_update",
    ),
    # Series URLs
    path("series/create/", views.SeriesCreateView.as_view(), name="series_create"),
    path(
        "series/<slug:slug>/update/",
        views.SeriesUpdateView.as_view(),
        name="series_update",
    ),
    # Season URLs
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/",
        views.SeasonDetailView.as_view(),
        name="season_detail",
    ),
    path(
        "series/<slug:series_slug>/seasons/create/",
        views.SeasonCreateView.as_view(),
        name="season_create",
    ),
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/update/",
        views.SeasonUpdateView.as_view(),
        name="season_update",
    ),
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/delete/",
        views.SeasonDeleteView.as_view(),
        name="season_delete",
    ),
    # Episode URLs
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/episodes/<int:episode_number>/",
        views.EpisodeDetailView.as_view(),
        name="episode_detail",
    ),
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/episodes/create/",
        views.EpisodeCreateView.as_view(),
        name="episode_create",
    ),
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/episodes/<int:episode_number>/update/",
        views.EpisodeUpdateView.as_view(),
        name="episode_update",
    ),
    path(
        "series/<slug:series_slug>/seasons/<int:season_number>/episodes/<int:episode_number>/delete/",
        views.EpisodeDeleteView.as_view(),
        name="episode_delete",
    ),
    # Review URLs
    path(
        "media/<slug:slug>/review/",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "media/<slug:slug>/review/delete/",
        views.ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    # Watchlist URLs
    path("watchlist/", views.WatchlistView.as_view(), name="watchlist"),
    path(
        "media/<slug:slug>/watchlist/toggle/",
        views.WatchlistToggleView.as_view(),
        name="watchlist_toggle",
    ),
]
