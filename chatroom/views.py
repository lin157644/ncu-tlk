from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from .models import Chatroom
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import json

from authlib.integrations.django_client import OAuth

# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='ncu',
    client_id='20221108123625JOZFR9IRPbxH',
    client_secret='dJZFdqzT4sSOMXIKQowzQTKJMTWmxazMiW5pDN9VLESWmV0bQV3',
    # (採用 POST Method, 需要以 Client Id/Client Secret 做為 Basic Auth 的帳號密碼, 另外在 request header 上要 Accept: application/json)
    access_token_url='https://portal.ncu.edu.tw/oauth2/token',
    access_token_params=None,
    authorize_url='https://portal.ncu.edu.tw/oauth2/authorization',
    authorize_params=None,
    api_base_url='https://portal.ncu.edu.tw/apis/oauth/v1/info',
    client_kwargs={'scope': 'id, identifier, chinese-name',
                   'token_endpoint_auth_method': 'client_secret_post'
                   },
    # server_metadata_url=CONF_URL,
)

# ncu = oauth.create_client('ncu')


def index(request):
    return render(request, 'index.html')


class ChatroomListView(generic.ListView):
    """Generic class-based view listing chatroom joined by current user."""
    model = Chatroom
    # Not needed
    # template_name = 'chatroom/chatroom_list.html'
    # context_object_name = 'my_book_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(ChatroomListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class ChatroomDetailView(LoginRequiredMixin, generic.DetailView):
    model = Chatroom


class ChatroomOfUserListView(LoginRequiredMixin, generic.ListView):
    model = Chatroom
    template_name = 'chatroom/templates/chatroom/chatroom_mine.html'
    paginate_by = 10

    def get_queryset(self):
        return Chatroom.objects.filter(user=self.request.user).order_by('created_at')


# def chatroom_detail_view(request, primary_key):
#     try:
#         book = Chatroom.objects.get(pk=primary_key)
#     except Chatroom.DoesNotExist:
#         raise Http404('Book does not exist')
#
#     # from django.shortcuts import get_object_or_404
#     # book = get_object_or_404(Book, pk=primary_key)
#
#     return render(request, 'catalog/book_detail.html', context={'book': book})


@login_required
def my_view(request):
    pass


def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'home.html', context={'user': user})


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.ncu.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.ncu.authorize_access_token(request)
    resp = oauth.ncu.get('info', token=token)
    resp.raise_for_status()
    data = resp.json()
    print(data)
    id = data["id"]
    print(token)
    # request.session['user'] = token['access_token']
    print(f"requset: {request}")
    print(f"resp= {resp}")
    return redirect('/')


def logout(request):
    request.session.pop('user', None)
    return redirect('/')
