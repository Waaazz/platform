from django.shortcuts import render,redirect
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from biens.models import Article
from biens.forms import ArticleForm
from biens.models import Reservation

def dashboard(request):
    return render(request,'db.html')

def user_articles(request):
    if not request.user.is_authenticated:
        return redirect('login-blog')
    
    list_articles= Article.objects.filter(user=request.user)
    return render(request,'my-articles.html',{'list_articles':list_articles})

class AddArticle(LoginRequiredMixin,CreateView):
    model = Article
    form_class = ArticleForm
    template_name= "add-article.html"
    success_url= "my-articles"
    
    
    
    def form_valid(self, form):
        # Assurez-vous que le formulaire est associé à l'utilisateur actuel
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class UpdateArticle(LoginRequiredMixin,UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'app_admin/article_form.html'
    
class DeleteArticle(LoginRequiredMixin,DeleteView):
    model = Article
    success_url = "/my-admin/my-articles"
    

def articles_reserves(request):
    reservations = Reservation.objects.all()
    return render(request, 'app_admin/articles_reserves.html', {'reservations': reservations})  
