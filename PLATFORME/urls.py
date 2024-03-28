"""
URL configuration for PLATFORME project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from biens.views import home,detail,search,reservation_page,generate_invoice,confirmation_page,soumettre_note,paypal_payment,payment_success,articles_by_category

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('article/<int:id_article>', detail,name="detail"),
    path('article/recherche', search, name="search"),
    path('auth/', include("app_auth.urls")),
    path('my-admin/', include("app_admin.urls")),
    path('reservation/<int:article_id>/', reservation_page, name='reservation_page'),
    path('generate_invoice/<int:article_id>/',generate_invoice, name='generate_invoice'),
    path('confirmation/<int:reservation_id>/',confirmation_page, name='confirmation_page'),
    path('soumettre-note/<int:article_id>/', soumettre_note, name='soumettre_note'),
    path('paypal_payment/', paypal_payment, name='paypal_payment'),
    path('payment-success/', payment_success, name='payment_success'),
    path('articles_by_category/', articles_by_category, name='articles_by_category'),
    path('captcha/', include('captcha.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

