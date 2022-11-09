from django.http import Http404
from django.shortcuts import render
from django.views import generic
from .models import Chatroom
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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
