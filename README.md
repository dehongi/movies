# Movies - Media Management Platform

A comprehensive Django-based web application for managing and streaming various types of media content including movies, TV series, podcasts, videos, and short videos. Features user accounts with subscription plans, storage management, reviews, watchlists, and more.

## Features

### Media Management

- **Movies**: Full movie catalog with details like director, cast, duration, and multiple video quality options
- **TV Series**: Complete series management with seasons and episodes
- **Podcasts**: Podcast episodes with host information and episode tracking
- **Videos**: Standalone video uploads with automatic metadata extraction
- **Short Videos**: Vertical short-form videos (up to 3 minutes) with validation

### User Management

- Email-based authentication (no usernames required)
- Custom user profiles with bio and profile pictures
- Subscription plans: Free (5GB), Premium, Pro
- Storage limit management and usage tracking
- Payment history tracking

### Content Features

- Genre categorization
- Privacy settings (public, unlisted, private)
- Copyright flagging system
- Review and rating system (1-10 scale)
- Personal watchlists
- View count tracking
- Featured content highlighting

### Technical Features

- Automatic thumbnail generation for videos
- Metadata extraction from uploaded files
- Platform integration for automatic uploads
- Responsive web interface
- File size and storage space management

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd movies
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

### For Users

- **Sign up/Login**: Create an account or log in with your email
- **Upload Content**: Add movies, videos, or podcasts through the web interface
- **Manage Media**: Edit details, set privacy, add to genres
- **Watch & Review**: Browse content, add to watchlist, leave reviews
- **Storage Management**: Monitor your storage usage and upgrade plans

### For Administrators

- Access the Django admin at `/admin` to manage all content and users
- Moderate content, manage user accounts, view analytics

## Project Structure

```
movies/
├── accounts/          # User management app
├── movies/            # Main media management app
├── website/           # Static pages and landing
├── django_project/    # Django project settings
├── templates/         # HTML templates
├── media/             # User-uploaded files
├── static/            # Static assets (CSS, JS)
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Key Models

- **Media**: Base model for all content types
- **Movie/Series/Podcast**: Specific content type models
- **Video/ShortVideo**: Video file models with metadata
- **CustomUser**: Extended user model with subscriptions
- **Review/Watchlist**: User interaction models
- **Genre/MediaType**: Content categorization

## Dependencies

- Django 5.1.7 - Web framework
- Pillow 11.1.0 - Image processing
- mutagen 1.47.0 - Audio metadata extraction

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

Follow Django's coding standards and use meaningful variable names.

### Database

Uses SQLite for development. Configure PostgreSQL or MySQL for production.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on the GitHub repository.
