import json

from authlib.integrations.django_client import OAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .models import Chatroom
from .forms import CreateChatForm

from django.shortcuts import get_object_or_404


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
    template_name = 'chatroom/chatroom_mine.html'
    paginate_by = 10

    def get_queryset(self):
        return Chatroom.objects.filter(user=self.request.user).order_by('created_at')


def show_chatroom(request, name):
    chatroom = get_object_or_404(Chatroom, name=name)
    if request.user.is_authenticated:
        chatroom.user.add(request.user)
    return render(request, 'chatroom/chatroom_detail.html', {'chatroom': chatroom})


def delete_mine_chatroom(request, name):
    chatroom = get_object_or_404(Chatroom, name=name)

    if request.method == 'POST':
        chatroom.user.remove(request.user)

    return redirect('my-chats')


@login_required
def create_chatroom(request):
    if request.method == "POST":
        form = CreateChatForm(request.POST)
        if form.is_valid():
            chatroom = Chatroom.objects.create(
                name=form.cleaned_data["name"], is_public=False, created_by=request.user)
            return HttpResponseRedirect(reverse('chat-detail', kwargs={"pk": chatroom.id}))
    else:
        form = CreateChatForm()
    return render(request, 'create.html', {'form': form})


@login_required
def update_chatroom(request):
    if request.method == "POST":
        form = CreateChatForm(request.POST)
        pass
    return render(request, 'create.html')


def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'home.html', context={'user': user})
