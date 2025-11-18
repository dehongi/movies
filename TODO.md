# TODO: Add Normal Video and Short Video Uploads to Media Types

## Step 1: Update models.py

- [ ] Add Video model with OneToOneField to Media, duration field
- [ ] Add ShortVideo model with OneToOneField to Media, duration field (max 60 seconds validation)
- [ ] Ensure VideoFile inline can be used for both Video and ShortVideo

## Step 2: Update forms.py

- [ ] Add VideoWithMediaForm combined form
- [ ] Add ShortVideoWithMediaForm combined form with duration validation
- [ ] Update imports to include new models

## Step 3: Create and Run Migrations

- [ ] Generate migrations for new models
- [ ] Run migrations

## Step 4: Update views.py

- [ ] Add views to handle Video and ShortVideo creation (similar to Movie creation)

## Step 5: Update Templates

- [ ] Update movie_form.html or create new templates for Video and ShortVideo forms

## Step 6: Test Uploads

- [ ] Test normal video uploads
- [ ] Test short video uploads
- [ ] Ensure file size and space tracking works
