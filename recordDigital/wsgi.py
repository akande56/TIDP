"""
WSGI config for recordDigital project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior
# voteme directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "recordDigital"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recordDigital.production')

application = get_wsgi_application()
