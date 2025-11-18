from django import forms
from django.forms import inlineformset_factory
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
    Platform,
    MediaPlatform,
    Podcast,
    Video,
    ShortVideo,
)
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
import os


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class MediaTypeForm(forms.ModelForm):
    class Meta:
        model = MediaType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = [
            "title",
            "description",
            "release_year",
            "poster",
            "trailer_url",
            "genres",
            "media_type",
            "is_featured",
            "privacy",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "release_year": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2100}
            ),
            "trailer_url": forms.URLInput(attrs={"class": "form-control"}),
            "genres": forms.SelectMultiple(attrs={"class": "form-select"}),
            "media_type": forms.Select(attrs={"class": "form-select"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "privacy": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap file input styling
        self.fields["poster"].widget.attrs.update({"class": "form-control"})
        # Add custom form-check div around checkboxes for proper styling
        self.fields["is_featured"].widget.attrs.update({"class": "form-check-input"})


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["duration", "director", "cast"]
        widgets = {
            "duration": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "director": forms.TextInput(attrs={"class": "form-control"}),
            "cast": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Actor 1, Actor 2, Actor 3...",
                }
            ),
        }


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ["total_seasons", "is_ongoing"]
        widgets = {
            "total_seasons": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "is_ongoing": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ["title", "season_number", "release_year", "poster"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "season_number": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "release_year": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2100}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap file input styling
        self.fields["poster"].widget.attrs.update({"class": "form-control"})


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = [
            "title",
            "episode_number",
            "description",
            "duration",
            "release_date",
            "video_file",
            "video_url",
            "file_size",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "episode_number": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "duration": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "release_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "video_url": forms.URLInput(attrs={"class": "form-control"}),
            "file_size": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap file input styling
        self.fields["video_file"].widget.attrs.update({"class": "form-control"})


class VideoFileForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ["quality", "video_file", "video_url", "file_size"]
        widgets = {
            "quality": forms.TextInput(attrs={"class": "form-control"}),
            "video_url": forms.URLInput(attrs={"class": "form-control"}),
            "file_size": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap file input styling
        self.fields["video_file"].widget.attrs.update({"class": "form-control"})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-select"}),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your review here...",
                }
            ),
        }


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ["media"]
        widgets = {
            "media": forms.Select(attrs={"class": "form-select"}),
        }


# Form sets for related items
VideoFileFormSet = inlineformset_factory(
    Movie, VideoFile, form=VideoFileForm, extra=1, can_delete=True
)

SeasonFormSet = inlineformset_factory(
    Series, Season, form=SeasonForm, extra=1, can_delete=True
)

EpisodeFormSet = inlineformset_factory(
    Season, Episode, form=EpisodeForm, extra=3, can_delete=True
)


# Combined forms for creating media with its specific type
class MovieWithMediaForm(forms.Form):
    """Combined form for creating a Movie with its Media parent"""

    # Media fields - poster first
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    title = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6})
    )
    release_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1900, "max": 2100}
        )
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    privacy = forms.ChoiceField(
        choices=Media.PRIVACY_CHOICES,
        initial="public",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Movie fields
    duration = forms.IntegerField(
        help_text="Duration in minutes",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    )
    director = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    cast = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Actor 1, Actor 2, Actor 3...",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def extract_metadata(self, file_path):
        """Extract metadata from audio/video file"""
        try:
            if file_path.lower().endswith((".mp3", ".flac", ".ogg", ".m4a")):
                if file_path.lower().endswith(".mp3"):
                    audio = MP3(file_path)
                elif file_path.lower().endswith(".flac"):
                    audio = FLAC(file_path)
                elif file_path.lower().endswith(".ogg"):
                    audio = OggVorbis(file_path)
                elif file_path.lower().endswith(".m4a"):
                    audio = MP4(file_path)

                metadata = {}
                # Extract title
                if hasattr(audio, "tags") and audio.tags:
                    if "TIT2" in audio.tags:  # ID3v2 title
                        metadata["title"] = str(audio.tags["TIT2"])
                    elif "title" in audio.tags:
                        metadata["title"] = (
                            str(audio.tags["title"][0])
                            if isinstance(audio.tags["title"], list)
                            else str(audio.tags["title"])
                        )

                    # Extract date/year
                    if "TDRC" in audio.tags:  # ID3v2 recording date
                        date_str = str(audio.tags["TDRC"])
                        metadata["release_year"] = (
                            int(date_str[:4]) if date_str[:4].isdigit() else None
                        )
                    elif "date" in audio.tags:
                        date_str = (
                            str(audio.tags["date"][0])
                            if isinstance(audio.tags["date"], list)
                            else str(audio.tags["date"])
                        )
                        metadata["release_year"] = (
                            int(date_str[:4]) if date_str[:4].isdigit() else None
                        )

                # Extract duration (for movies/podcasts)
                if hasattr(audio, "info"):
                    metadata["duration"] = int(audio.info.length)

                return metadata
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
        return {}


class SeriesWithMediaForm(forms.Form):
    """Combined form for creating a Series with its Media parent"""

    # Media fields - poster first
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    title = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6})
    )
    release_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1900, "max": 2100}
        )
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    privacy = forms.ChoiceField(
        choices=Media.PRIVACY_CHOICES,
        initial="public",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Series fields
    total_seasons = forms.IntegerField(
        initial=1, widget=forms.NumberInput(attrs={"class": "form-control", "min": 1})
    )
    is_ongoing = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class PodcastWithMediaForm(forms.Form):
    """Combined form for creating a Podcast with its Media parent"""

    # Media fields - poster first
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    title = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6})
    )
    release_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1900, "max": 2100}
        )
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    privacy = forms.ChoiceField(
        choices=Media.PRIVACY_CHOICES,
        initial="public",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Podcast fields
    host = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    episode_count = forms.IntegerField(
        initial=1, widget=forms.NumberInput(attrs={"class": "form-control", "min": 1})
    )
    is_ongoing = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class VideoWithMediaForm(forms.Form):
    """Combined form for creating a Video with its Media parent"""

    # Media fields - poster first
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    title = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6})
    )
    release_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1900, "max": 2100}
        )
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    privacy = forms.ChoiceField(
        choices=Media.PRIVACY_CHOICES,
        initial="public",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # Video fields
    duration = forms.IntegerField(
        help_text="Duration in seconds",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class ShortVideoWithMediaForm(forms.Form):
    """Combined form for creating a ShortVideo with its Media parent"""

    # Media fields - poster first
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    title = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6})
    )
    release_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1900, "max": 2100}
        )
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    privacy = forms.ChoiceField(
        choices=Media.PRIVACY_CHOICES,
        initial="public",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # ShortVideo fields
    duration = forms.IntegerField(
        help_text="Duration in seconds (max 60)",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 60}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration and duration > 60:
            raise forms.ValidationError("Short videos must be 60 seconds or less.")
        return duration
