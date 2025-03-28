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
)


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
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "release_year": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2100}
            ),
            "trailer_url": forms.URLInput(attrs={"class": "form-control"}),
            "genres": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
            "media_type": forms.Select(attrs={"class": "form-select"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
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

    # Media fields
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
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
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


class SeriesWithMediaForm(forms.Form):
    """Combined form for creating a Series with its Media parent"""

    # Media fields
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
    poster = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    trailer_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    is_featured = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
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
