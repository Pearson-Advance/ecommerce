"""Settings used only to run `compilemessages` during Docker build.

This imports the normal settings but removes Oscar dashboard apps so that
we avoid app label collisions during the translation compilation step.
"""
"""Minimal settings to run `compilemessages` during Docker build.

This intentionally avoids loading Oscar and other heavy apps which trigger
model imports. It collects all `conf/locale` directories under the project
and sets them in `LOCALE_PATHS` so `compilemessages` can find and compile
translations without registering app models.
"""
import os
from pathlib import Path

from .base import DJANGO_APPS, SITE_ROOT  # noqa: F401

# Use a minimal installed apps list so Django does not import Oscar models.
# Keep only essential Django apps required for translations.
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

# Build LOCALE_PATHS by finding all `conf/locale` directories in the project
repo_root = Path(__file__).resolve().parents[2]
locale_paths = []
for p in repo_root.rglob('conf/locale'):
	if p.is_dir():
		locale_paths.append(str(p))

# Ensure the project's main locale dir is included
main_locale = os.path.join(repo_root, 'ecommerce', 'conf', 'locale')
if os.path.isdir(main_locale) and main_locale not in locale_paths:
	locale_paths.append(main_locale)

LOCALE_PATHS = tuple(locale_paths)

# Minimal i18n settings required by compilemessages
USE_I18N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (('en', 'English'),)
