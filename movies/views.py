from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    View,
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect

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
    ShortVideo,
    Video,
    SimpleVideo,
)
from .forms import (
    GenreForm,
    MediaTypeForm,
    MediaForm,
    MovieForm,
    SeriesForm,
    SeasonForm,
    EpisodeForm,
    VideoFileForm,
    ReviewForm,
    WatchlistForm,
    VideoFileFormSet,
    SeasonFormSet,
    EpisodeFormSet,
    MovieWithMediaForm,
    SeriesWithMediaForm,
    PodcastWithMediaForm,
    VideoWithMediaForm,
    ShortVideoWithMediaForm,
    SimpleVideoForm,
)


# Genre Views
class GenreListView(ListView):
    model = Genre
    template_name = "movies/genre_list.html"
    context_object_name = "genres"
    paginate_by = 20


class GenreDetailView(DetailView):
    model = Genre
    template_name = "movies/genre_detail.html"
    context_object_name = "genre"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_list"] = self.object.media.all()
        return context


@method_decorator(login_required, name="dispatch")
class GenreCreateView(LoginRequiredMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = "movies/genre_form.html"
    success_url = reverse_lazy("movies:genre_list")


@method_decorator(login_required, name="dispatch")
class GenreUpdateView(LoginRequiredMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = "movies/genre_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse("movies:genre_detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name="dispatch")
class GenreDeleteView(LoginRequiredMixin, DeleteView):
    model = Genre
    template_name = "movies/genre_confirm_delete.html"
    success_url = reverse_lazy("movies:genre_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


# Media Type Views
class MediaTypeListView(ListView):
    model = MediaType
    template_name = "movies/mediatype_list.html"
    context_object_name = "mediatypes"


@method_decorator(login_required, name="dispatch")
class MediaTypeCreateView(LoginRequiredMixin, CreateView):
    model = MediaType
    form_class = MediaTypeForm
    template_name = "movies/mediatype_form.html"
    success_url = reverse_lazy("movies:mediatype_list")


@method_decorator(login_required, name="dispatch")
class MediaTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = MediaType
    form_class = MediaTypeForm
    template_name = "movies/mediatype_form.html"
    success_url = reverse_lazy("movies:mediatype_list")


@method_decorator(login_required, name="dispatch")
class MediaTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = MediaType
    template_name = "movies/mediatype_confirm_delete.html"
    success_url = reverse_lazy("movies:mediatype_list")


# Media Views
class MediaListView(ListView):
    model = Media
    template_name = "movies/media_list.html"
    context_object_name = "media_list"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.GET.get("genre")
        media_type = self.request.GET.get("type")
        year = self.request.GET.get("year")

        if genre:
            queryset = queryset.filter(genres__slug=genre)
        if media_type:
            queryset = queryset.filter(media_type__name=media_type)
        if year:
            queryset = queryset.filter(release_year=year)

        # Filter by privacy: only show public and unlisted, unless user is uploader
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(privacy__in=["public", "unlisted"]) | Q(uploader=self.request.user)
            )
        else:
            queryset = queryset.filter(privacy__in=["public", "unlisted"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["media_types"] = MediaType.objects.all()
        return context


class MediaDetailView(DetailView):
    model = Media
    template_name = "movies/media_detail.html"
    context_object_name = "media"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media = self.get_object()

        # Increment view count
        media.views_count += 1
        media.save()

        # Add review form
        context["review_form"] = ReviewForm()

        # Add related media
        context["related_media"] = (
            Media.objects.filter(genres__in=media.genres.all())
            .exclude(id=media.id)
            .distinct()[:4]
        )

        # Check if in user's watchlist
        if self.request.user.is_authenticated:
            context["in_watchlist"] = Watchlist.objects.filter(
                user=self.request.user, media=media
            ).exists()

        # Check if it's a movie, series, or podcast and add the appropriate details
        try:
            context["movie"] = media.movie_details
            context["video_files"] = media.movie_details.video_files.all()
        except Movie.DoesNotExist:
            pass

        try:
            context["series"] = media.series_details
            context["seasons"] = media.series_details.seasons.all()
        except Series.DoesNotExist:
            pass

        try:
            context["podcast"] = media.podcast_details
        except Podcast.DoesNotExist:
            pass

        return context


@method_decorator(login_required, name="dispatch")
class MediaCreateView(LoginRequiredMixin, CreateView):
    model = Media
    form_class = MediaForm
    template_name = "movies/media_form.html"

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("movies:media_detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name="dispatch")
class MediaUpdateView(LoginRequiredMixin, UpdateView):
    model = Media
    form_class = MediaForm
    template_name = "movies/media_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse("movies:media_detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name="dispatch")
class MediaDeleteView(LoginRequiredMixin, DeleteView):
    model = Media
    template_name = "movies/media_confirm_delete.html"
    success_url = reverse_lazy("movies:media_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"


# Movie Views
@method_decorator(login_required, name="dispatch")
class MovieCreateView(LoginRequiredMixin, FormView):
    form_class = MovieWithMediaForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movies:media_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Extract metadata if poster file is provided
            metadata = {}
            if form.cleaned_data.get("poster"):
                # Get the file path temporarily
                temp_file_path = form.cleaned_data["poster"].temporary_file_path()
                metadata = form.extract_metadata(temp_file_path)

            # Create Media object
            media_type, _ = MediaType.objects.get_or_create(name="Movie")

            # Use extracted metadata if available, otherwise use form data
            title = metadata.get("title") or form.cleaned_data["title"]
            release_year = (
                metadata.get("release_year") or form.cleaned_data["release_year"]
            )
            duration = metadata.get("duration") or form.cleaned_data["duration"]

            media = Media.objects.create(
                title=title,
                description=form.cleaned_data["description"],
                release_year=release_year,
                poster=(
                    form.cleaned_data["poster"]
                    if "poster" in form.cleaned_data
                    else None
                ),
                trailer_url=form.cleaned_data["trailer_url"],
                media_type=media_type,
                uploader=self.request.user,
                is_featured=form.cleaned_data["is_featured"],
                privacy=form.cleaned_data["privacy"],
            )

            # Add genres
            media.genres.set(form.cleaned_data["genres"])

            # Create Movie object
            movie = Movie.objects.create(
                media=media,
                duration=duration,
                director=form.cleaned_data["director"],
                cast=form.cleaned_data["cast"],
            )

            messages.success(
                self.request, f'Movie "{media.title}" has been created successfully!'
            )
            self.success_url = reverse(
                "movies:media_detail", kwargs={"slug": media.slug}
            )

        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MovieUpdateView(LoginRequiredMixin, View):
    template_name = "movies/movie_update_form.html"

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, media__slug=kwargs["slug"])
        media = movie.media

        # Initialize both forms with instance data
        media_form = MediaForm(instance=media)
        movie_form = MovieForm(instance=movie)
        video_formset = VideoFileFormSet(instance=movie)

        return render(
            request,
            self.template_name,
            {
                "media_form": media_form,
                "movie_form": movie_form,
                "video_formset": video_formset,
                "movie": movie,
            },
        )

    def post(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, media__slug=kwargs["slug"])
        media = movie.media

        media_form = MediaForm(request.POST, request.FILES, instance=media)
        movie_form = MovieForm(request.POST, instance=movie)
        video_formset = VideoFileFormSet(request.POST, request.FILES, instance=movie)

        if media_form.is_valid() and movie_form.is_valid() and video_formset.is_valid():
            with transaction.atomic():
                media_form.save()
                movie_form.save()
                video_formset.save()

            messages.success(
                request, f'Movie "{media.title}" has been updated successfully!'
            )
            return redirect("movies:media_detail", slug=media.slug)

        return render(
            request,
            self.template_name,
            {
                "media_form": media_form,
                "movie_form": movie_form,
                "video_formset": video_formset,
                "movie": movie,
            },
        )


# Series Views
@method_decorator(login_required, name="dispatch")
class SeriesCreateView(LoginRequiredMixin, FormView):
    form_class = SeriesWithMediaForm
    template_name = "movies/series_form.html"
    success_url = reverse_lazy("movies:media_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Create Media object
            media_type, _ = MediaType.objects.get_or_create(name="Series")

            media = Media.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                release_year=form.cleaned_data["release_year"],
                poster=(
                    form.cleaned_data["poster"]
                    if "poster" in form.cleaned_data
                    else None
                ),
                trailer_url=form.cleaned_data["trailer_url"],
                media_type=media_type,
                uploader=self.request.user,
                is_featured=form.cleaned_data["is_featured"],
                privacy=form.cleaned_data["privacy"],
            )

            # Add genres
            media.genres.set(form.cleaned_data["genres"])

            # Create Series object
            series = Series.objects.create(
                media=media,
                total_seasons=form.cleaned_data["total_seasons"],
                is_ongoing=form.cleaned_data["is_ongoing"],
            )

            messages.success(
                self.request, f'Series "{media.title}" has been created successfully!'
            )
            self.success_url = reverse(
                "movies:media_detail", kwargs={"slug": media.slug}
            )

        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class PodcastCreateView(LoginRequiredMixin, FormView):
    form_class = PodcastWithMediaForm
    template_name = "movies/podcast_form.html"
    success_url = reverse_lazy("movies:media_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Extract metadata if poster file is provided
            metadata = {}
            if form.cleaned_data.get("poster"):
                # Get the file path temporarily
                temp_file_path = form.cleaned_data["poster"].temporary_file_path()
                metadata = form.extract_metadata(temp_file_path)

            # Create Media object
            media_type, _ = MediaType.objects.get_or_create(name="Podcast")

            # Use extracted metadata if available, otherwise use form data
            title = metadata.get("title") or form.cleaned_data["title"]
            release_year = (
                metadata.get("release_year") or form.cleaned_data["release_year"]
            )

            media = Media.objects.create(
                title=title,
                description=form.cleaned_data["description"],
                release_year=release_year,
                poster=(
                    form.cleaned_data["poster"]
                    if "poster" in form.cleaned_data
                    else None
                ),
                trailer_url=form.cleaned_data["trailer_url"],
                media_type=media_type,
                uploader=self.request.user,
                is_featured=form.cleaned_data["is_featured"],
                privacy=form.cleaned_data["privacy"],
            )

            # Add genres
            media.genres.set(form.cleaned_data["genres"])

            # Create Podcast object
            podcast = Podcast.objects.create(
                media=media,
                host=form.cleaned_data["host"],
                episode_count=form.cleaned_data["episode_count"],
                is_ongoing=form.cleaned_data["is_ongoing"],
            )

            messages.success(
                self.request, f'Podcast "{media.title}" has been created successfully!'
            )
            self.success_url = reverse(
                "movies:media_detail", kwargs={"slug": media.slug}
            )

        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class VideoCreateView(LoginRequiredMixin, FormView):
    form_class = VideoWithMediaForm
    template_name = "movies/video_form.html"
    success_url = reverse_lazy("movies:media_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Create Media object
            media_type, _ = MediaType.objects.get_or_create(name="Video")

            media = Media.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                release_year=form.cleaned_data["release_year"],
                poster=(
                    form.cleaned_data["poster"]
                    if "poster" in form.cleaned_data
                    else None
                ),
                trailer_url=form.cleaned_data["trailer_url"],
                media_type=media_type,
                uploader=self.request.user,
                is_featured=form.cleaned_data["is_featured"],
                privacy=form.cleaned_data["privacy"],
            )

            # Add genres
            media.genres.set(form.cleaned_data["genres"])

            # Create Video object
            video = Video.objects.create(
                media=media,
                duration=form.cleaned_data["duration"],
            )

            messages.success(
                self.request, f'Video "{media.title}" has been created successfully!'
            )
            self.success_url = reverse(
                "movies:media_detail", kwargs={"slug": media.slug}
            )

        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ShortVideoCreateView(LoginRequiredMixin, FormView):
    form_class = ShortVideoWithMediaForm
    template_name = "movies/shortvideo_form.html"
    success_url = reverse_lazy("movies:media_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Create Media object
            media_type, _ = MediaType.objects.get_or_create(name="ShortVideo")

            media = Media.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                release_year=form.cleaned_data["release_year"],
                poster=(
                    form.cleaned_data["poster"]
                    if "poster" in form.cleaned_data
                    else None
                ),
                trailer_url=form.cleaned_data["trailer_url"],
                media_type=media_type,
                uploader=self.request.user,
                is_featured=form.cleaned_data["is_featured"],
                privacy=form.cleaned_data["privacy"],
            )

            # Add genres
            media.genres.set(form.cleaned_data["genres"])

            # Create ShortVideo object
            shortvideo = ShortVideo.objects.create(
                media=media,
                duration=form.cleaned_data["duration"],
            )

            messages.success(
                self.request,
                f'Short video "{media.title}" has been created successfully!',
            )
            self.success_url = reverse(
                "movies:media_detail", kwargs={"slug": media.slug}
            )

        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class SeriesUpdateView(LoginRequiredMixin, View):
    template_name = "movies/series_update_form.html"

    def get(self, request, *args, **kwargs):
        series = get_object_or_404(Series, media__slug=kwargs["slug"])
        media = series.media

        media_form = MediaForm(instance=media)
        series_form = SeriesForm(instance=series)
        season_formset = SeasonFormSet(instance=series)

        return render(
            request,
            self.template_name,
            {
                "media_form": media_form,
                "series_form": series_form,
                "season_formset": season_formset,
                "series": series,
            },
        )

    def post(self, request, *args, **kwargs):
        series = get_object_or_404(Series, media__slug=kwargs["slug"])
        media = series.media

        media_form = MediaForm(request.POST, request.FILES, instance=media)
        series_form = SeriesForm(request.POST, instance=series)
        season_formset = SeasonFormSet(request.POST, request.FILES, instance=series)

        if (
            media_form.is_valid()
            and series_form.is_valid()
            and season_formset.is_valid()
        ):
            with transaction.atomic():
                media_form.save()
                series_form.save()
                season_formset.save()

            messages.success(
                request, f'Series "{media.title}" has been updated successfully!'
            )
            return redirect("movies:media_detail", slug=media.slug)

        return render(
            request,
            self.template_name,
            {
                "media_form": media_form,
                "series_form": series_form,
                "season_formset": season_formset,
                "series": series,
            },
        )


# Season Views
class SeasonDetailView(DetailView):
    model = Season
    template_name = "movies/season_detail.html"
    context_object_name = "season"

    def get_object(self, queryset=None):
        series_slug = self.kwargs.get("series_slug")
        season_number = self.kwargs.get("season_number")
        return get_object_or_404(
            Season, series__media__slug=series_slug, season_number=season_number
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = self.object.episodes.all().order_by("episode_number")
        context["series"] = self.object.series
        return context


@method_decorator(login_required, name="dispatch")
class SeasonCreateView(LoginRequiredMixin, CreateView):
    model = Season
    form_class = SeasonForm
    template_name = "movies/season_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.series = get_object_or_404(Series, media__slug=self.kwargs["series_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.series = self.series
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["series"] = self.series
        return context

    def get_success_url(self):
        return reverse("movies:media_detail", kwargs={"slug": self.series.media.slug})


@method_decorator(login_required, name="dispatch")
class SeasonUpdateView(LoginRequiredMixin, View):
    template_name = "movies/season_update_form.html"

    def get(self, request, *args, **kwargs):
        series_slug = kwargs.get("series_slug")
        season_number = kwargs.get("season_number")
        season = get_object_or_404(
            Season, series__media__slug=series_slug, season_number=season_number
        )

        season_form = SeasonForm(instance=season)
        episode_formset = EpisodeFormSet(instance=season)

        return render(
            request,
            self.template_name,
            {
                "season_form": season_form,
                "episode_formset": episode_formset,
                "season": season,
            },
        )

    def post(self, request, *args, **kwargs):
        series_slug = kwargs.get("series_slug")
        season_number = kwargs.get("season_number")
        season = get_object_or_404(
            Season, series__media__slug=series_slug, season_number=season_number
        )

        season_form = SeasonForm(request.POST, request.FILES, instance=season)
        episode_formset = EpisodeFormSet(request.POST, request.FILES, instance=season)

        if season_form.is_valid() and episode_formset.is_valid():
            with transaction.atomic():
                season_form.save()
                episode_formset.save()

            messages.success(
                request, f"Season {season.season_number} has been updated successfully!"
            )
            return redirect(
                "movies:season_detail",
                series_slug=series_slug,
                season_number=season.season_number,
            )

        return render(
            request,
            self.template_name,
            {
                "season_form": season_form,
                "episode_formset": episode_formset,
                "season": season,
            },
        )


@method_decorator(login_required, name="dispatch")
class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    model = Season
    template_name = "movies/season_confirm_delete.html"

    def get_object(self, queryset=None):
        series_slug = self.kwargs.get("series_slug")
        season_number = self.kwargs.get("season_number")
        return get_object_or_404(
            Season, series__media__slug=series_slug, season_number=season_number
        )

    def get_success_url(self):
        return reverse(
            "movies:media_detail", kwargs={"slug": self.object.series.media.slug}
        )


# Episode Views
class EpisodeDetailView(DetailView):
    model = Episode
    template_name = "movies/episode_detail.html"
    context_object_name = "episode"

    def get_object(self, queryset=None):
        series_slug = self.kwargs.get("series_slug")
        season_number = self.kwargs.get("season_number")
        episode_number = self.kwargs.get("episode_number")
        return get_object_or_404(
            Episode,
            season__series__media__slug=series_slug,
            season__season_number=season_number,
            episode_number=episode_number,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["season"] = self.object.season
        context["series"] = self.object.season.series

        # Get next and previous episodes
        try:
            context["next_episode"] = Episode.objects.get(
                season=self.object.season, episode_number=self.object.episode_number + 1
            )
        except Episode.DoesNotExist:
            context["next_episode"] = None

        try:
            context["prev_episode"] = Episode.objects.get(
                season=self.object.season, episode_number=self.object.episode_number - 1
            )
        except Episode.DoesNotExist:
            context["prev_episode"] = None

        return context


@method_decorator(login_required, name="dispatch")
class EpisodeCreateView(LoginRequiredMixin, CreateView):
    model = Episode
    form_class = EpisodeForm
    template_name = "movies/episode_form.html"

    def dispatch(self, request, *args, **kwargs):
        series_slug = self.kwargs.get("series_slug")
        season_number = self.kwargs.get("season_number")
        self.season = get_object_or_404(
            Season, series__media__slug=series_slug, season_number=season_number
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.season = self.season
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["season"] = self.season
        context["series"] = self.season.series
        return context

    def get_success_url(self):
        return reverse(
            "movies:season_detail",
            kwargs={
                "series_slug": self.season.series.media.slug,
                "season_number": self.season.season_number,
            },
        )


@method_decorator(login_required, name="dispatch")
class EpisodeUpdateView(LoginRequiredMixin, UpdateView):
    model = Episode
    form_class = EpisodeForm
    template_name = "movies/episode_form.html"

    def get_object(self, queryset=None):
        series_slug = self.kwargs.get("series_slug")
        season_number = self.kwargs.get("season_number")
        episode_number = self.kwargs.get("episode_number")
        return get_object_or_404(
            Episode,
            season__series__media__slug=series_slug,
            season__season_number=season_number,
            episode_number=episode_number,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["season"] = self.object.season
        context["series"] = self.object.season.series
        return context

    def get_success_url(self):
        return reverse(
            "movies:episode_detail",
            kwargs={
                "series_slug": self.object.season.series.media.slug,
                "season_number": self.object.season.season_number,
                "episode_number": self.object.episode_number,
            },
        )


@method_decorator(login_required, name="dispatch")
class EpisodeDeleteView(LoginRequiredMixin, DeleteView):
    model = Episode
    template_name = "movies/episode_confirm_delete.html"

    def get_object(self, queryset=None):
        series_slug = self.kwargs.get("series_slug")
        season_number = self.kwargs.get("season_number")
        episode_number = self.kwargs.get("episode_number")
        return get_object_or_404(
            Episode,
            season__series__media__slug=series_slug,
            season__season_number=season_number,
            episode_number=episode_number,
        )

    def get_success_url(self):
        return reverse(
            "movies:season_detail",
            kwargs={
                "series_slug": self.object.season.series.media.slug,
                "season_number": self.object.season.season_number,
            },
        )


# Review Views
@method_decorator(login_required, name="dispatch")
class ReviewCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        media_slug = kwargs.get("slug")
        media = get_object_or_404(Media, slug=media_slug)

        # Check if user already has a review for this media
        existing_review = Review.objects.filter(media=media, user=request.user).first()

        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            if not existing_review:
                review.media = media
                review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted!")
        else:
            messages.error(request, "There was an error with your review submission.")

        return redirect("movies:media_detail", slug=media_slug)


@method_decorator(login_required, name="dispatch")
class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "movies/review_confirm_delete.html"

    def get_object(self, queryset=None):
        media_slug = self.kwargs.get("slug")
        return get_object_or_404(Review, media__slug=media_slug, user=self.request.user)

    def get_success_url(self):
        return reverse("movies:media_detail", kwargs={"slug": self.object.media.slug})


# Watchlist Views
@method_decorator(login_required, name="dispatch")
class WatchlistView(LoginRequiredMixin, ListView):
    model = Watchlist
    template_name = "movies/watchlist.html"
    context_object_name = "watchlist_items"

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class WatchlistToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        media_slug = kwargs.get("slug")
        media = get_object_or_404(Media, slug=media_slug)

        # Check if already in watchlist
        existing_item = Watchlist.objects.filter(media=media, user=request.user).first()

        if existing_item:
            # Remove from watchlist
            existing_item.delete()
            messages.success(
                request, f'"{media.title}" has been removed from your watchlist.'
            )
        else:
            # Add to watchlist
            Watchlist.objects.create(media=media, user=request.user)
            messages.success(
                request, f'"{media.title}" has been added to your watchlist.'
            )

        return redirect("movies:media_detail", slug=media_slug)


# Home page view with featured content
class HomeView(ListView):
    model = Media
    template_name = "website/home.html"
    context_object_name = "featured_media"

    def get_queryset(self):
        queryset = Media.objects.filter(is_featured=True)
        # Filter by privacy
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(privacy__in=["public", "unlisted"]) | Q(uploader=self.request.user)
            )
        else:
            queryset = queryset.filter(privacy__in=["public", "unlisted"])
        return queryset[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Base queryset with privacy filter
        base_qs = Media.objects.all()
        if self.request.user.is_authenticated:
            base_qs = base_qs.filter(
                Q(privacy__in=["public", "unlisted"]) | Q(uploader=self.request.user)
            )
        else:
            base_qs = base_qs.filter(privacy__in=["public", "unlisted"])

        context["latest_movies"] = base_qs.filter(media_type__name="Movie").order_by(
            "-created_at"
        )[:6]

        context["latest_series"] = base_qs.filter(media_type__name="Series").order_by(
            "-created_at"
        )[:6]

        context["latest_podcasts"] = base_qs.filter(
            media_type__name="Podcast"
        ).order_by("-created_at")[:6]

        context["popular_media"] = base_qs.order_by("-views_count")[:6]

        # Add genres to the context
        context["genres"] = Genre.objects.all()

        return context


# Search functionality
class SearchView(ListView):
    model = Media
    template_name = "movies/search_results.html"
    context_object_name = "results"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            queryset = Media.objects.filter(title__icontains=query)
            # Filter by privacy
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    Q(privacy__in=["public", "unlisted"])
                    | Q(uploader=self.request.user)
                )
            else:
                queryset = queryset.filter(privacy__in=["public", "unlisted"])
            return queryset
        return Media.objects.none()


# SimpleVideo Views
class SimpleVideoListView(ListView):
    model = SimpleVideo
    template_name = "movies/simplevideo_list.html"
    context_object_name = "simple_videos"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user if needed, but for now show all
        return queryset.order_by("-upload_date")


class SimpleVideoDetailView(DetailView):
    model = SimpleVideo
    template_name = "movies/simplevideo_detail.html"
    context_object_name = "simple_video"


@method_decorator(login_required, name="dispatch")
class SimpleVideoCreateView(LoginRequiredMixin, CreateView):
    model = SimpleVideo
    form_class = SimpleVideoForm
    template_name = "movies/simplevideo_form.html"
    success_url = reverse_lazy("movies:simplevideo_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Simple video "{form.instance.title or form.instance.video_file.name}" has been uploaded successfully!',
        )
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class SimpleVideoUpdateView(LoginRequiredMixin, UpdateView):
    model = SimpleVideo
    form_class = SimpleVideoForm
    template_name = "movies/simplevideo_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("movies:simplevideo_detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required, name="dispatch")
class SimpleVideoDeleteView(LoginRequiredMixin, DeleteView):
    model = SimpleVideo
    template_name = "movies/simplevideo_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("movies:simplevideo_list")
