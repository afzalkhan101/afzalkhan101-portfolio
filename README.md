# Afzal Khan Portfolio

A Django-powered portfolio website with a professional Odoo-inspired glassmorphism design.

## Updated features

- Clean, photo-free homepage and dashboard design.
- Odoo primary color `#714B67` and secondary color `#017E84` kept across the full UI.
- Responsive layout for mobile, tablet, laptop and large screens.
- Dynamic project CRUD from the owner dashboard.
- Project tracking for features, tech stack, repository/live links and last commit details.
- Public GitHub latest commit sync for project repository URLs.
- Blog / LinkedIn / external post URL preview sync using OpenGraph metadata.
- Redesigned dashboard, profile editor, forms, login, delete confirmation and project detail pages.
- Dynamic profile settings for name, title, hero text, stats, services, focus areas, skills and links.

## Run locally

```bash
cd afzalkhan101-portfolio-updated
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Portfolio: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Admin: http://127.0.0.1:8000/admin/

## Notes

- The design intentionally uses professional text cards and UI blocks instead of personal photos.
- Project cards are dynamic. Add new projects from the dashboard to show them on the homepage.
- Writing/external link cards use a clean text-first layout. If a site blocks metadata scraping, fields can be edited manually from the dashboard.
- Login to `/dashboard/` and click **Update Profile Content** to edit professional profile text, links, stats, services and skills.
