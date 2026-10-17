# Kumaran's Gallery

A Django photo portfolio with session-protected gallery collections, friend profiles, and a contact form.

## Local setup (Windows PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to add content. Install dependencies first with `python -m pip install -r requirements.txt` if needed.

In the admin, create **Gallery categories** and set a password; category passwords are hashed before they are stored. Add gallery images within each category. Add **Friend profiles** and their photos using the inline photo editor. Contact form submissions are stored in the admin under **Contact messages**.

For code-created categories, use `category.set_password("your password")` before saving. Do not assign a raw password directly to the `password` field.

## Production notes

The settings are configured for local development (`DEBUG = True`, SQLite, and local media serving). Before deployment, set a unique `DJANGO_SECRET_KEY` environment variable, set `DEBUG = False`, configure `ALLOWED_HOSTS`, use HTTPS, and serve uploaded media through a production storage/web server rather than Django's development media route. Do not commit `.env`, uploaded images, or the local SQLite database.

## Project layout

```text
myportfolio/          Django project settings and root URL configuration
main/                  Gallery app, models, forms, views, and admin
main/migrations/       Database schema migrations
main/templates/main/   Shared layout and page templates
main/static/main/      Responsive styles and navigation script
media/                 Uploaded images (created at runtime; ignored by Git)
manage.py
requirements.txt
```
