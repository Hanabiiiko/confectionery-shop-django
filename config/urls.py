from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from shop.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', include('shop.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
