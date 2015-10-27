from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from news.models import NewsItem


class NewsView(TemplateView):
    template_name = 'news/news.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewsView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        paginator = Paginator(NewsItem.objects.for_user(self.request.user), 20)
        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context
