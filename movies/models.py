from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Genre(models.Model):
    """Genre model for categorizing media content"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class MediaType(models.Model):
    """Media type model (e.g., movie, series, documentary)"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Media(models.Model):
    """Base model for all media content"""

    PRIVACY_CHOICES = [
        ("public", "Public"),
        ("unlisted", "Unlisted"),
        ("private", "Private"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=275, unique=True, blank=True)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    poster = models.ImageField(upload_to="media_posters/", blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)

    genres = models.ManyToManyField(Genre, related_name="media")
    media_type = models.ForeignKey(
        MediaType, on_delete=models.CASCADE, related_name="media"
    )
    uploader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_media"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    # New fields for privacy and copyright
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default="public")
    copyright_flagged = models.BooleanField(default=False)
    used_space = models.PositiveIntegerField(
        default=0, help_text="Space used by this media in MB"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.release_year}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Media"


class Movie(models.Model):
    """Movie-specific model"""

    media = models.OneToOneField(
        Media, on_delete=models.CASCADE, primary_key=True, related_name="movie_details"
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes", blank=True, null=True
    )
    director = models.CharField(max_length=255, blank=True)
    cast = models.TextField(
        help_text="Main cast members, separated by commas", blank=True
    )

    def __str__(self):
        return f"Movie: {self.media.title}"


class Series(models.Model):
    """TV Series model"""

    media = models.OneToOneField(
        Media, on_delete=models.CASCADE, primary_key=True, related_name="series_details"
    )
    total_seasons = models.PositiveIntegerField(default=1)
    is_ongoing = models.BooleanField(default=True)

    def __str__(self):
        return f"Series: {self.media.title}"


class Season(models.Model):
    """Season model for TV Series"""

    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="seasons")
    title = models.CharField(max_length=255)
    season_number = models.PositiveIntegerField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    poster = models.ImageField(upload_to="season_posters/", blank=True, null=True)

    def __str__(self):
        return f"{self.series.media.title} - Season {self.season_number}: {self.title}"

    class Meta:
        ordering = ["season_number"]
        unique_together = ["series", "season_number"]


class Episode(models.Model):
    """Episode model for TV Series seasons"""

    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="episodes"
    )
    title = models.CharField(max_length=255)
    episode_number = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes", blank=True, null=True
    )
    release_date = models.DateField(blank=True, null=True)
    video_file = models.FileField(upload_to="episodes/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    file_size = models.PositiveIntegerField(
        help_text="File size in MB", blank=True, null=True
    )

    def __str__(self):
        return f"{self.season.series.media.title} S{self.season.season_number}E{self.episode_number}: {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file_size:
            self.season.series.media.used_space += self.file_size
            self.season.series.media.save()

    class Meta:
        ordering = ["episode_number"]
        unique_together = ["season", "episode_number"]


class VideoFile(models.Model):
    """Video file model for movies"""

    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="video_files"
    )
    quality = models.CharField(
        max_length=50, help_text="e.g., 1080p, 720p, 4K", blank=True
    )
    video_file = models.FileField(upload_to="movies/")
    video_url = models.URLField(blank=True, null=True)
    file_size = models.PositiveIntegerField(
        help_text="File size in MB", blank=True, null=True
    )

    def __str__(self):
        return f"{self.movie.media.title} - {self.quality}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file_size:
            self.movie.media.used_space += self.file_size
            self.movie.media.save()


class Platform(models.Model):
    """Platform model for automatic uploads"""

    name = models.CharField(max_length=100, unique=True)
    api_endpoint = models.URLField(blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class MediaPlatform(models.Model):
    """Link media to platforms for auto-upload"""

    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="platforms")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    uploaded = models.BooleanField(default=False)
    upload_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.media.title} on {self.platform.name}"


class Podcast(models.Model):
    """Podcast-specific model"""

    media = models.OneToOneField(
        Media,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="podcast_details",
    )
    host = models.CharField(max_length=255, blank=True)
    episode_count = models.PositiveIntegerField(default=1)
    is_ongoing = models.BooleanField(default=True)

    def __str__(self):
        return f"Podcast: {self.media.title}"


class Video(models.Model):
    """Video-specific model for normal videos"""

    media = models.OneToOneField(
        Media, on_delete=models.CASCADE, primary_key=True, related_name="video_details"
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds", blank=True, null=True
    )

    def __str__(self):
        return f"Video: {self.media.title}"


class ShortVideo(models.Model):
    """Short video-specific model"""

    media = models.OneToOneField(
        Media,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="short_video_details",
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds, max 60", blank=True, null=True
    )

    def __str__(self):
        return f"Short Video: {self.media.title}"

    def clean(self):
        if self.duration > 60:
            raise ValidationError("Short videos must be 60 seconds or less.")


class Review(models.Model):
    """User reviews for media content"""

    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        help_text="Rating from 1 to 10", choices=[(i, i) for i in range(1, 11)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s review of {self.media.title} - {self.rating}/10"

    class Meta:
        unique_together = ["media", "user"]
        ordering = ["-created_at"]


class Watchlist(models.Model):
    """User's watchlist for media they want to watch later"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    media = models.ForeignKey(
        Media, on_delete=models.CASCADE, related_name="in_watchlists"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s watchlist: {self.media.title}"

    class Meta:
        unique_together = ["user", "media"]
