import json

from authlib.integrations.django_client import OAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .models import Chatroom

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

def createChatroom(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        pass
    return render(request, 'create.html')


#     try:
#         book = Chatroom.objects.get(pk=primary_key)
#     except Chatroom.DoesNotExist:
#         raise Http404('Book does not exist')
#
#     # from django.shortcuts import get_object_or_404
#     # book = get_object_or_404(Book, pk=primary_key)


# @login_required
# def my_view(request):
#     pass

def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'home.html', context={'user': user})
