from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone

from .models import Article, Reservation, Note, Category, UserProfile, Favorite, Message
from .forms import ReservationForm, UserProfileForm, MessageForm

ITEMS_PER_PAGE = 12


def home(request):
    list_articles = Article.objects.filter(disponible=True).order_by('-created_at')
    paginator = Paginator(list_articles, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()
    return render(request, 'home.html', {"page_obj": page_obj, "categories": categories})


def detail(request, id_article):
    article = get_object_or_404(Article, id=id_article)
    articles_en_relation = Article.objects.filter(category=article.category).exclude(id=article.id)[:5]
    notes = Note.objects.filter(article=article)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, article=article).exists()
    return render(request, 'detail.html', {
        "Article": article,
        "aer": articles_en_relation,
        "notes": notes,
        "is_favorite": is_favorite,
    })


def search(request):
    query = request.GET.get('q', '') or request.GET.get('Article', '')
    articles = Article.objects.all()

    if query:
        articles = articles.filter(nom__icontains=query)

    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)

    prix_min = request.GET.get('prix_min')
    if prix_min:
        articles = articles.filter(prix__gte=prix_min)

    prix_max = request.GET.get('prix_max')
    if prix_max:
        articles = articles.filter(prix__lte=prix_max)

    if request.GET.get('disponible'):
        articles = articles.filter(disponible=True)

    articles = articles.order_by('-created_at')
    paginator = Paginator(articles, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
    })


def reservation_page(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = ReservationForm()
    return render(request, 'reservation_page.html', {'article': article, 'form': form})


@login_required
def confirmation_page(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'confirmation_page.html', {'reservation': reservation})


def generate_invoice(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['date_checkin']
            checkout = form.cleaned_data['date_checkout']
            jours = (checkout - checkin).days
            prix_total = article.prix * jours

            reservation = Reservation(
                article=article,
                user=request.user if request.user.is_authenticated else None,
                nom=form.cleaned_data['nom'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data['telephone'],
                prix_article=article.prix,
                prix_total=prix_total,
                date_checkin=checkin,
                date_checkout=checkout,
                date_reservation=timezone.now(),
                modalites_paiement=form.cleaned_data['modalites_paiement'],
            )
            reservation.save()
            article.disponible = False
            article.save()
            return redirect('confirmation_page', reservation_id=reservation.id)
        else:
            return render(request, 'reservation_page.html', {'form': form, 'article': article})
    else:
        form = ReservationForm()
    return render(request, 'reservation_page.html', {'form': form, 'article': article})


@login_required
def soumettre_note(request, article_id):
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        article = get_object_or_404(Article, id=article_id)
        Note.objects.create(article=article, utilisateur=request.user, note=note, commentaire=commentaire)
        return redirect('detail', id_article=article_id)
    return redirect('home')


def paypal_payment(request):
    return render(request, 'paypal_payment.html', {
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    })


def payment_success(request):
    return render(request, 'payment_success.html')


def articles_by_category(request):
    category_id = request.GET.get('category')
    if category_id:
        articles = Article.objects.filter(category_id=category_id)
    else:
        articles = Article.objects.all()
    articles = articles.order_by('-created_at')
    paginator = Paginator(articles, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = Category.objects.all()
    return render(request, 'articles_by_category.html', {
        'page_obj': page_obj,
        'categories': categories,
        'category_id': int(category_id) if category_id else None,
    })


# --- Favoris ---
@login_required
def toggle_favorite(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, article=article)
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def mes_favoris(request):
    favoris = Favorite.objects.filter(user=request.user).select_related('article')
    return render(request, 'mes_favoris.html', {'favoris': favoris})


# --- Reservations utilisateur ---
@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date_reservation')
    return render(request, 'mes_reservations.html', {'reservations': reservations})


@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if reservation.statut == 'confirmee':
        reservation.statut = 'annulee'
        reservation.save()
        reservation.article.disponible = True
        reservation.article.save()
        messages.success(request, "Votre reservation a ete annulee.")
    else:
        messages.error(request, "Cette reservation ne peut pas etre annulee.")
    return redirect('mes_reservations')


# --- Messagerie ---
@login_required
def envoyer_message(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    receiver = article.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = receiver
            msg.article = article
            msg.save()
            messages.success(request, "Message envoye!")
            return redirect('detail', id_article=article_id)
    else:
        form = MessageForm()
    return render(request, 'envoyer_message.html', {'form': form, 'article': article})


@login_required
def messagerie(request):
    received = Message.objects.filter(receiver=request.user).order_by('-created_at')
    sent = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'messagerie.html', {'received': received, 'sent': sent})


@login_required
def conversation(request, user_id):
    from django.contrib.auth.models import User as AuthUser
    other_user = get_object_or_404(AuthUser, id=user_id)
    msgs = Message.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')
    msgs.filter(receiver=request.user, lu=False).update(lu=True)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('conversation', user_id=user_id)
    return render(request, 'conversation.html', {'msgs': msgs, 'other_user': other_user, 'form': form})


# --- Profil ---
@login_required
def profil(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis a jour!")
            return redirect('profil')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profil.html', {'form': form, 'profile': profile})
