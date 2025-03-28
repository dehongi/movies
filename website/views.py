from django.shortcuts import render
from movies.models import Media, Genre

# Create your views here.


def home(request):
    context = {
        "featured_media": Media.objects.filter(is_featured=True)[:8],
        "latest_movies": Media.objects.filter(media_type__name="Movie").order_by(
            "-created_at"
        )[:6],
        "latest_series": Media.objects.filter(media_type__name="Series").order_by(
            "-created_at"
        )[:6],
        "popular_media": Media.objects.order_by("-views_count")[:6],
        "genres": Genre.objects.all(),
    }
    return render(request, "website/home.html", context)


def about(request):
    return render(request, "website/about.html")


def contact(request):
    return render(request, "website/contact.html")


def faq(request):
    return render(request, "website/faq.html")


def terms(request):
    return render(request, "website/terms.html")


def privacy(request):
    return render(request, "website/privacy.html")
