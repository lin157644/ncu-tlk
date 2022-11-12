import json

from authlib.integrations.django_client import OAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .models import Chatroom
from .forms import CreateChatForm, UpdateChatFrom

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
            chatroom = Chatroom.objects.create(is_anonymous=form.cleaned_data.get("anonymous"),
                                               name=form.cleaned_data["name"], is_public=False, created_by=request.user)
            return HttpResponseRedirect(chatroom.get_absolute_url())
    else:
        form = CreateChatForm()
    return render(request, 'create.html', {'form': form})


@login_required
def update_chatroom(request, name):
    # TODO: Very bad code
    if Chatroom.objects.filter(name=name, created_by=request.user).exists():
        if request.method == "POST":
            form = UpdateChatFrom(request.POST)
            if form.is_valid():
                if form.cleaned_data['name'] != name and Chatroom.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    raise ValidationError(_('Chat name already exist'))
                Chatroom.objects.filter(name=name, created_by=request.user).update(
                    name=form.cleaned_data["name"], summary=form.cleaned_data["summary"],
                    is_public=form.cleaned_data["public"])
                chatroom = Chatroom.objects.get(name=form.cleaned_data["name"], created_by=request.user)
                return HttpResponseRedirect(chatroom.get_absolute_url())
        else:
            chatroom = Chatroom.objects.get(name=name, created_by=request.user)
            form = UpdateChatFrom(initial={"name": name, "summary": chatroom.summary, "public": chatroom.is_public})

        return render(request, 'update.html', {'form': form, 'name': name})
    else:
        return redirect('index')


def home(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'home.html', context={'user': user})
