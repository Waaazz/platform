from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Article,Reservation,Note,Category
from .forms import ReservationForm
from django.utils import timezone


def paypal_payment(request):
    return render(request, 'paypal_payment.html')
                               
def home(request):
    list_articles =  Article.objects.all()
    context = {"list_articles": list_articles}
    
    if request.method == 'POST':
            article_id = request.POST.get('article_id')  # Assurez-vous que 'article_id' est le nom de votre champ d'ID d'article dans le formulaire
            article = Article.objects.get(pk=article_id)
            if not article.can_reserve():
                    messages.error(request, "Cet article est indisponible pour le moment.")
                    return redirect('home')
    return render(request, 'home.html',context)

def detail(request,id_article):
    article=Article.objects.get(id=id_article)      
    category=article.category
    articles_en_relation=Article.objects.filter(category=category)[:5]
    notes = Note.objects.filter(article=article)
    return render(request, 'detail.html',{"Article":article,"aer":articles_en_relation,"notes": notes})

def search(request): 
    query=request.GET["Article"]
    liste_article= Article.objects.filter(nom__icontains=query)
    return render(request, 'search.html',{"liste_article":liste_article})

def reservation_page(request, article_id):
    article = Article.objects.get(id=article_id)
    form = ReservationForm()
    context = {'article': article, 'form': form}
    return render(request, 'reservation_page.html', context)


def confirmation_page(request, reservation_id):
    # Récupérer la réservation à partir de son ID
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'confirmation_page.html', {'reservation': reservation})

def generate_invoice(request, article_id):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            article_id = article_id  # Utilisez l'ID de l'article transmis dans l'URL
            article = Article.objects.get(id=article_id)
            reservation = Reservation(
                article=article, 
                nom=form.cleaned_data['nom'], 
                email=form.cleaned_data['email'], 
                telephone=form.cleaned_data['telephone'],
                prix_article=article.prix,  # Utilisation du prix de l'article
                date_reservation=timezone.now(),
                modalites_paiement=form.cleaned_data['modalites_paiement']
            )
            reservation.save()
            article.disponible = False
            article.save()
            return redirect('confirmation_page', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    return render(request, 'reservation_page.html', {'form': form})

def soumettre_note(request, article_id):
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        article = Article.objects.get(id=article_id)
        Note.objects.create(article=article, utilisateur=request.user, note=note, commentaire=commentaire)
        return redirect('detail', id_article=article_id)
    else:
        return redirect('home')

def payment_success(request):
    # Vous pouvez ajouter du code ici pour générer la facture en fonction des détails de la réservation
    return render(request, 'payment_success.html')

def articles_by_category(request):
    category_id = request.GET.get('category')
    if category_id:
        articles = Article.objects.filter(category_id=category_id)
    else:
        articles = Article.objects.all()
    categories = Category.objects.all()
    return render(request, 'articles_by_category.html', {'articles': articles, 'categories': categories})