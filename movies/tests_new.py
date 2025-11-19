from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Media, MediaPlatform, Platform
from .forms import VideoForm
from unittest.mock import patch

User = get_user_model()



class StorageLimitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password", storage_limit=1
        )  # 1GB limit
        from .models import Genre
        self.genre = Genre.objects.create(name="Test Genre")


    def test_upload_within_limit(self):
        # 10MB file
        file = SimpleUploadedFile(
            "test.mp4", b"0" * 10 * 1024 * 1024, content_type="video/mp4"
        )
        form = VideoForm(
            data={"title": "Test Video"},
            files={"video_file": file},
            user=self.user,
        )
        self.assertTrue(form.is_valid())

    def test_upload_exceeds_limit(self):
        # 1.1GB file (simulated size check, actual content is small to save memory)
        # We mock the size attribute since creating a real 1.1GB file is slow/memory intensive
        file = SimpleUploadedFile(
            "large.mp4", b"0", content_type="video/mp4"
        )
        file.size = 1.1 * 1024 * 1024 * 1024  # 1.1 GB

        form = VideoForm(
            data={"title": "Large Video"},
            files={"video_file": file},
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("video_file", form.errors)
        self.assertIn("exceeds your available storage", form.errors["video_file"][0])


class CopyrightSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.media_type = None  # Needs setup if foreign key required, assuming defaults work or mocked

    def test_copyright_flag_sets_private(self):
        # Create media (need minimal fields)
        from .models import MediaType
        mt = MediaType.objects.create(name="TestType")
        media = Media.objects.create(
            title="Copyrighted Video",
            uploader=self.user,
            media_type=mt,
            privacy="public",
            copyright_flagged=False,
        )
        
        # Flag it
        media.copyright_flagged = True
        media.save()
        
        # Refresh and check
        media.refresh_from_db()
        self.assertEqual(media.privacy, "private")


class MultiPlatformTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="mp@example.com", password="password"
        )
        from .models import MediaType
        self.mt = MediaType.objects.create(name="TestType")
        self.platform = Platform.objects.create(name="YouTube", api_key="test_key")

    @patch("movies.services.upload_to_youtube")
    def test_upload_triggered(self, mock_upload):
        mock_upload.return_value = "http://youtube.com/fake"
        
        media = Media.objects.create(
            title="Viral Video",
            uploader=self.user,
            media_type=self.mt,
        )
        
        # Create MediaPlatform link
        mp = MediaPlatform.objects.create(
            media=media,
            platform=self.platform
        )
        
        # Check if upload was called
        mock_upload.assert_called_once()
        
        # Check if model updated
        mp.refresh_from_db()
        self.assertTrue(mp.uploaded)
        self.assertEqual(mp.upload_url, "http://youtube.com/fake")
