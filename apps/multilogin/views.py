# === django import === #
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

# === app import === #
from apps.multilogin.forms import MultiloginForm
from apps.multilogin.models import Account, Profile
from apps.multilogin.heplers import signin, profile_search
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper


class LoginView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        form = MultiloginForm(request.POST)
        if form.is_valid():
            # sign in multilogin and store current token
            token = signin(
                form.cleaned_data['email'], form.cleaned_data['password'])
            if not token:
                messages.error(
                    request, "Access multilogin fail. Please try again!")
                return redirect("index")
            account, created = Account.objects.update_or_create(
                user=request.user, email=form.cleaned_data['email'],
                default={'password': form.cleaned_data['password']}
            )
            for profile in profile_search():
                obj, created = Profile.objects.update_or_create(
                    account=account,
                    profile=profile['id'],
                    defaults={
                        'folder': profile['folder_id'],
                        'profile_name': profile['name']
                    }
                )
            messages.success(request, "Access multilogin success")
            return redirect("index")
        messages.error(request, "Access multilogin fail. Please try again!")
        return redirect("index")


class ProfileListView(TemplateView):
    def get_context_data(self, **kwargs) -> TemplateHelper:
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


class ProfileDataView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        data = list(Profile.objects.select_related('account').\
            filter(account__user=request.user).values(
            'id', 'name', 'profile', 'folder', 'account__email'
        ))
        return JsonResponse(data, safe=False)
