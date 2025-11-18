# TODO: Simplify Video Models for Simple Uploads

## Steps to Complete

- [x] Add SimpleVideo model to movies/models.py with fields: uploader, video_file, title, thumbnail, duration, upload_date
- [x] Implement metadata extraction logic using a library (e.g., moviepy or ffprobe) to extract title, thumbnail, duration from uploaded file
- [x] Update forms.py to include SimpleVideoForm for uploads
- [x] Update views.py to handle SimpleVideo creation and display
- [x] Update admin.py to register SimpleVideo
- [x] Create and run migrations for the new model
- [x] Test the upload and metadata extraction functionality
- [x] Update templates if necessary for SimpleVideo display
