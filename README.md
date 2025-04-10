# RamJaap - Digital Ram Naam Jaap Application

RamJaap is a web application that enables users to perform digital "Ram Naam Jaap" by typing Ram's name repeatedly. The app tracks user progress, provides timer options, and features a leaderboard of top devotees.

## Features

- User authentication and profiles
- Timer-based Jaap sessions (5, 10, 15, 30, 60 minutes)
- Target-based Jaap counting (e.g., 10,000, 100,000 times)
- Auto-conversion of any variation of "ram" to "Ram"
- Support for Hindi input
- Auto-spacing feature
- Session pause and resume functionality
- Leaderboard of top devotees
- User statistics dashboard
- Mobile responsive design

## Technology Stack

- Backend: Django (Python 3.12)
- Frontend: Tailwind CSS, Alpine.js
- Database: SQLite (local), PostgreSQL (production)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ramjaap.git
   cd ramjaap
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Tailwind CSS dependencies:
   ```
   python manage.py tailwind install
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

8. In a separate terminal, start the Tailwind CSS watcher:
   ```
   python manage.py tailwind start
   ```

## Project Structure

- `accounts/`: User authentication and profile management
- `core/`: Core functionality and shared components
- `jaap/`: Ram Naam Jaap functionality
- `theme/`: Tailwind CSS customization

## Admin Access

The admin interface is available at `/durga/` (e.g., http://127.0.0.1:8000/durga/).

A custom admin dashboard is also available at `/admin/` with specialized views for RamJaap management.

## Testing

To run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test jaap accounts

# Run with coverage (requires coverage package)
coverage run --source='.' manage.py test
coverage report
```

Testing documentation:
- `RESPONSIVE_TESTING.md`: Guidelines for testing mobile responsiveness
- `SECURITY_CHECKLIST.md`: Security testing procedures and best practices
- Model and view tests are included in each app's `tests.py` and `tests_views.py` files

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions.

Key deployment steps:
1. Configure PostgreSQL database
2. Set up environment variables
3. Collect static files
4. Configure a production web server (Gunicorn + Nginx recommended)
5. Enable HTTPS with SSL/TLS certificates

## Future Enhancements (Phase 2)

- Social sharing functionality
- User levels/badges based on Jaap counts
- Notification system for reaching targets

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. # ram
