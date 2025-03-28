from django.contrib import admin
from .models import (
    Genre,
    MediaType,
    Media,
    Movie,
    Series,
    Season,
    Episode,
    VideoFile,
    Review,
    Watchlist,
)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class VideoFileInline(admin.TabularInline):
    model = VideoFile
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    list_display = ("__str__", "director", "duration")
    inlines = [VideoFileInline]
    search_fields = ("media__title", "director")


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    show_change_link = True


class SeriesAdmin(admin.ModelAdmin):
    list_display = ("__str__", "total_seasons", "is_ongoing")
    inlines = [SeasonInline]
    search_fields = ("media__title",)


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 3
    show_change_link = True


class SeasonAdmin(admin.ModelAdmin):
    list_display = ("__str__", "series", "season_number", "release_year")
    list_filter = ("series", "release_year")
    inlines = [EpisodeInline]
    search_fields = ("title", "series__media__title")


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "season", "episode_number", "duration", "release_date")
    list_filter = ("season", "release_date")
    search_fields = ("title", "season__series__media__title")
    date_hierarchy = "release_date"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__email", "media__title", "comment")
    date_hierarchy = "created_at"


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__email", "media__title")
    date_hierarchy = "added_at"


class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "media_type",
        "release_year",
        "uploader",
        "is_featured",
        "views_count",
        "created_at",
    )
    list_filter = ("media_type", "release_year", "is_featured", "genres")
    search_fields = ("title", "description", "uploader__email")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    filter_horizontal = ("genres",)
    list_editable = ("is_featured",)
    readonly_fields = ("views_count",)
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "release_year",
                    "media_type",
                    "uploader",
                )
            },
        ),
        ("Media Content", {"fields": ("poster", "trailer_url")}),
        ("Classification", {"fields": ("genres",)}),
        ("Statistics", {"fields": ("is_featured", "views_count")}),
    )


# Register models
admin.site.register(Genre, GenreAdmin)
admin.site.register(MediaType, MediaTypeAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(VideoFile)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
