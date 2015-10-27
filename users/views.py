# coding=utf-8
from urlparse import urlparse
from urlparse import parse_qs
import datetime
from django.contrib import messages
from django.contrib.auth import BACKEND_SESSION_KEY, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView, View
from users.forms import ProfileSettingsForm, UserChangePasswordForm, UserChangeEmailForm, WallPostForm, SearchPeopleForm
from users.models import User, FriendInvite


class UserProfileView(TemplateView):
    template_name = 'users/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.pk == int(kwargs['user_id']):
            self.user = request.user
        else:
            self.user = get_object_or_404(User, pk=kwargs['user_id'])
        self.wall_post_form = WallPostForm(request.POST or None)
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get_wall_posts(self):
        paginator = Paginator(self.user.wall_posts.select_related('author'), 10)
        page = self.request.GET.get('page')
        try:
            posts_on_wall = paginator.page(page)
        except PageNotAnInteger:
            posts_on_wall = paginator.page(1)
        except EmptyPage:
            posts_on_wall = paginator.page(paginator.num_pages)
        return posts_on_wall

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile_user'] = self.user
        context['posts_on_wall'] = self.get_wall_posts()
        context['wall_post_form'] = self.wall_post_form
        if self.request.user != self.user:
            context['is_my_friend'] = User.friendship.are_friends(self.request.user, self.user)
        return context

    def post(self, request, *args, **kwargs):
        if self.wall_post_form.is_valid():
            post = self.wall_post_form.save(commit=False)
            post.user = self.user
            post.author = request.user
            post.save()
            messages.success(request, _(u'Повідомлення успішно опубліковано'))
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class UserSettings(TemplateView):
    template_name = 'users/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        action = request.POST.get('action')
        self.profile_settings_form = ProfileSettingsForm(
            (request.POST if action == 'profile' else None),
            (request.FILES if action == 'profile' else None),
            prefix='profile', instance=request.user
        )
        self.user_change_password = UserChangePasswordForm(request.user,
                                                           (request.POST if action == 'password' else None),
                                                           prefix='password')
        self.user_change_email = UserChangeEmailForm(request.user, (request.POST if action == 'email' else None),
                                                     prefix='email')
        return super(UserSettings, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserSettings, self).get_context_data(**kwargs)
        context['profile_settings_form'] = self.profile_settings_form
        context['user_change_password'] = self.user_change_password
        context['user_change_email'] = self.user_change_email
        return context

    def post(self, request, *args, **kwargs):
        if self.profile_settings_form.is_valid():
            self.profile_settings_form.save()
            messages.success(request, _(u'Дані успішно змінені та збережені'))
            return redirect(request.path)
        elif self.user_change_password.is_valid():
            self.user_change_password.save()
            request.user.backend = request.session[BACKEND_SESSION_KEY]
            login(request, request.user)
            messages.success(request, _(u'Пароль успішно змінений'))
            return redirect(request.path)
        elif self.user_change_email.is_valid():
            self.user_change_email.save()
            messages.success(request, _(u'Email успішно змінений та збережений'))
            return redirect(request.path)
        return self.get(request, *args, **kwargs)


class UserFriendsView(TemplateView):
    template_name = 'users/friends_base.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserFriendsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserFriendsView, self).get_context_data(**kwargs)
        context['friend_menu'] = 'friends'
        paginator = Paginator(self.request.user.friends.all(), 20)
        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context


class UserFriendsIncomeView(TemplateView):
    template_name = 'users/friends_income.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserFriendsIncomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserFriendsIncomeView, self).get_context_data(**kwargs)
        context['friend_menu'] = 'friends_income'
        paginator = Paginator(self.request.user.in_friend_invites.all(), 20)
        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context


class UserFriendsOutcomeView(TemplateView):
    template_name = 'users/friends_outcome.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserFriendsOutcomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserFriendsOutcomeView, self).get_context_data(**kwargs)
        context['friend_menu'] = 'friends_outcome'
        paginator = Paginator(self.request.user.out_friend_invites.all(), 20)
        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context


class FriendshipAPIView(View):
    @method_decorator(login_required)
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        method_name = '_action_{}'.format(request.POST.get('action', ''))
        if not hasattr(self, method_name):
            raise Http404
        default_url = getattr(self, method_name)()
        return redirect(request.POST.get('next') or default_url or 'main')

    def _get_user_from_post_field(self, field_name):
        try:
            return User.objects.get(pk=self.request.POST.get(field_name))
        except (User.DoesNotExist, ValueError):
            pass

    def _action_add_to_friends(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            try:
                r = FriendInvite.objects.add(self.request.user, user)
            except ValueError, e:
                messages.warning(self.request, e)
            else:
                if r == 1:
                    messages.success(self.request, _(u'Заявка успішно відправлена і очікує розгляду'))
                elif r == 2:
                    messages.success(self.request, _(u'Користувач успішно добавлений'))
                    return 'friends'
        return 'friends_outcome'

    def _action_approve(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            try:
                r = FriendInvite.objects.approve(user, self.request.user)
            except ValueError, e:
                messages.warning(self.request, e)
            else:
                if r:
                    messages.success(self.request, _(u'Заявка успішно підтверджена'))
        return 'friends_income'

    def _action_reject(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            FriendInvite.objects.reject(user, self.request.user)
            messages.success(self.request, _(u'Заявка успішно відхилена'))
        return 'friends_income'

    def _action_cancel_outcome(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            FriendInvite.objects.filter(from_user=self.request.user, to_user=user).delete()
            messages.success(self.request, _(u'Заявка успішно відмінена'))
        return 'friends_outcome'

    def _action_delete_from_friends(self):
        user = self._get_user_from_post_field('user_id')
        if user:
            if User.friendship.delete(self.request.user, user):
                messages.success(self.request, _(u'Користувач успішно видалений'))
        return 'friends'


class UserSearchPeople(TemplateView):
    template_name = 'users/search.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.form = SearchPeopleForm(request.GET or None)
        return super(UserSearchPeople, self).dispatch(request, *args, **kwargs)

    def get_filtered_qs(self, qs):
        self.form.is_valid()
        if not hasattr(self.form, 'cleaned_data'):
            return qs
        if self.form.cleaned_data.get('fname_and_lname'):
            query = None
            for val in self.form.get_values_list('fname_and_lname'):
                print val
                q = Q(first_name__icontains=val) | Q(last_name__icontains=val)
                if query is None:
                    query = q
                else:
                    query |= q
            if query:
                qs = qs.filter(query)
        if self.form.cleaned_data.get('gender'):
            qs = qs.filter(gender=self.form.cleaned_data['gender'])
        if self.form.cleaned_data.get('from_date'):
            qs = qs.filter(birth_date__gte=datetime.datetime(self.form.cleaned_data['from_date'], 1, 1))
        if self.form.cleaned_data.get('to_date'):
            qs = qs.filter(birth_date__lt=datetime.datetime(self.form.cleaned_data['to_date'] + 1, 1, 1))
        for field_name in ('city', 'job', 'about_me', 'interests'):
            query = None
            for val in self.form.get_values_list(field_name):
                q = Q(**{'{}__icontains'.format(field_name): val})
                if query is None:
                    query = q
                else:
                    query |= q
            if query:
                qs = qs.filter(query)
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserSearchPeople, self).get_context_data(**kwargs)
        context['form'] = self.form
        qs = self.get_filtered_qs(User.objects.all())
        paginator = Paginator(qs, 20)
        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context['items'] = items
        return context
