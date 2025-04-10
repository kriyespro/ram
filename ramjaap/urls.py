"""
URL configuration for ramjaap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Change the admin site headers
admin.site.site_header = 'RamJaap Administration'
admin.site.site_title = 'RamJaap Admin'
admin.site.index_title = 'RamJaap Admin Portal'

urlpatterns = [
    # Change default admin path to 'durga'
    path('durga/', admin.site.urls),
    
    # Custom admin dashboard at /admin
    path('admin/', include('admin_dashboard.urls', namespace='admin_dashboard')),
    
    # Include app-specific URLs
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('jaap/', include('jaap.urls')),
]

# Add static and media URLs in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
