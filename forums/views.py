from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .forms import DiscussionForm
from .models import Forum, Discussion
from django.db.models import F


class ForumsView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'forums/forums.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(forums=Forum.objects.all())

        return ctx


class DiscussionCreateView(LoginRequiredMixin, CreateView):
    form_class = DiscussionForm
    template_name = 'forums/new_discussion.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.forum = Forum.objects.get(id=self.kwargs.get('forum_id'))
        if self.request.user.has_perm('forums.denied_to_add_safe_discussion') and not self.request.user.is_superuser:
            instance.safe = False
        instance.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        url = reverse_lazy('discussion_list_view', kwargs={'forum_id': self.kwargs.get('forum_id')})
        return url


class DiscussionListView(LoginRequiredMixin, ListView):
    model = Discussion
    template_name = 'forums/discussion_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(forum_id=self.kwargs.get('forum_id'))
        return ctx

    def get_queryset(self):
        queryset = super().get_queryset()
        forum_id = self.kwargs.get('forum_id')
        return queryset.filter(forum=forum_id, safe=True).order_by('-at_date_time')
    

class DiscussionListViewByTag(LoginRequiredMixin, ListView):
    model = Discussion
    template_name = 'forums/discussion_tag_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        return queryset.filter(tags__slug=tag_slug, safe=True).order_by('-at_date_time')


class DiscussionDetailView(LoginRequiredMixin, DetailView):
    model = Discussion
    template_name = 'forums/discussion_detail.html'
    pk_url_kwarg = 'discussion_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(id=self.kwargs.get(self.pk_url_kwarg)).update(view=F('view') + 1)
        return queryset
    
    

    
