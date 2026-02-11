import re
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from biens.views import (
    home, detail, search, reservation_page, generate_invoice,
    confirmation_page, soumettre_note, paypal_payment, payment_success,
    articles_by_category, toggle_favorite, mes_favoris, mes_reservations,
    annuler_reservation, envoyer_message, messagerie, conversation, profil
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('article/<int:id_article>', detail, name="detail"),
    path('article/recherche', search, name="search"),
    path('auth/', include("app_auth.urls")),
    path('my-admin/', include("app_admin.urls")),
    path('reservation/<int:article_id>/', reservation_page, name='reservation_page'),
    path('generate_invoice/<int:article_id>/', generate_invoice, name='generate_invoice'),
    path('confirmation/<int:reservation_id>/', confirmation_page, name='confirmation_page'),
    path('soumettre-note/<int:article_id>/', soumettre_note, name='soumettre_note'),
    path('paypal_payment/', paypal_payment, name='paypal_payment'),
    path('payment-success/', payment_success, name='payment_success'),
    path('articles_by_category/', articles_by_category, name='articles_by_category'),
    path('captcha/', include('captcha.urls')),
    # Nouvelles routes
    path('favoris/toggle/<int:article_id>/', toggle_favorite, name='toggle_favorite'),
    path('mes-favoris/', mes_favoris, name='mes_favoris'),
    path('mes-reservations/', mes_reservations, name='mes_reservations'),
    path('annuler-reservation/<int:reservation_id>/', annuler_reservation, name='annuler_reservation'),
    path('message/<int:article_id>/', envoyer_message, name='envoyer_message'),
    path('messagerie/', messagerie, name='messagerie'),
    path('conversation/<int:user_id>/', conversation, name='conversation'),
    path('profil/', profil, name='profil'),
]

# Servir les fichiers media (uploads) en dev et en production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
