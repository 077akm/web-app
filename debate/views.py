from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from .forms import *
from .models import Debate, Category
from .serializers import DebateSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .utils import *


class DebateAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class DebateAPIList(generics.ListCreateAPIView):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = DebateAPIListPagination


class DebateAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, )


class DebateAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    permission_classes = (IsAdminOrReadOnly, )









class DebateHome(DataMixin, ListView):
    model = Debate
    template_name = 'debate/index.html'
    context_object_name = 'debats'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная Страница")
        return dict(list(context.items())+ list(c_def.items()))

    def get_queryset(self):
        return Debate.objects.filter(is_published=True).select_related('cat')

# def index(request):
#     debats = Debate.objects.all()
#
#     context = {
#         'debats': debats,
#         'menu': menu,
#         'title': 'Главная Страница',
#         'cat_selected': 0,
#     }
#     return render(request, "debate/index.html", context=context)

def about(request):
    contact_list = Debate.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "debate/about.html", {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddDebateForm
    template_name = 'debate/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление Статьи")
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddDebateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddDebateForm()
#     return render(request, 'debate/addpage.html', {'form': form,'menu': menu, 'title': 'Добавление статьи'})

# def contact(request):
#     return HttpResponse("asdasdasd")
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'debate/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
# def login(request):
#     return HttpResponse("asdasdasdas")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def show_page(request, page_slug):
#     debate = get_object_or_404(Debate, slug=page_slug)
#
#     context = {
#         'debate': debate,
#         'menu': menu,
#         'title': debate.title,
#         'cat_selected': debate.cat_id,
#     }
#     return render(request, 'debate/debate.html', context=context)

class ShowPage(DataMixin, DetailView):
    model = Debate
    template_name = 'debate/debate.html'
    slug_url_kwarg = 'page_slug'
    context_object_name = 'debate'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['debate'])
        return dict(list(context.items()) + list(c_def.items()))

class DebateCategory(DataMixin, ListView):
    model = Debate
    template_name = 'debate/index.html'
    context_object_name = 'debats'
    allow_empty = False

    def get_queryset(self):
        return Debate.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published = True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категории - '+ str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items())+ list(c_def.items()))

# def show_category(request, cat_id):
#     debats = Debate.objects.filter(cat_id = cat_id)
#
#     if len(debats) == 0:
#         raise Http404()
#
#     context = {
#         'debats': debats,
#         'menu': menu,
#         'title': 'Categories',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'debate/index.html', context = context)

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'debate/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'debate/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')