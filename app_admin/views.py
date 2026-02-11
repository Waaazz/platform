from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from biens.models import Article, Reservation
from biens.forms import ArticleForm


@login_required
def dashboard(request):
    return render(request, 'db.html')


@login_required
def user_articles(request):
    list_articles = Article.objects.filter(user=request.user)
    return render(request, 'my-articles.html', {'list_articles': list_articles})


class AddArticle(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "add-article.html"
    success_url = "/my-admin/my-articles"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateArticle(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'app_admin/article_form.html'
    success_url = "/my-admin/my-articles"

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.user


class DeleteArticle(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = "/my-admin/my-articles"

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.user


@login_required
def articles_reserves(request):
    reservations = Reservation.objects.filter(article__user=request.user)
    return render(request, 'app_admin/articles_reserves.html', {'reservations': reservations})
