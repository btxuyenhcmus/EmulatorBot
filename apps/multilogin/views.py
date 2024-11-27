from django.shortcuts import render, redirect
from .multilogindriver import signin, profile_search
from .forms import MultiloginForm
from .models import MultiloginAccount
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def login(request):
    if request.method == 'POST':
        form = MultiloginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Đăng nhập vào Multilogin và lấy token
            token = signin(email, password)
            if token:
                data = profile_search()
                for profile in data:
                    multilogin_account, created = MultiloginAccount.objects.get_or_create(
                        user=request.user,
                        profile_id=profile.get('id', ''),
                        defaults={
                            'email': email,
                            'password': password,
                            'folder_id': profile.get('folder_id', ''),
                            'profile_name': profile.get('name', '')
                        }
                    )
                    if not created:
                        # Cập nhật thông tin nếu tài khoản đã tồn tại
                        multilogin_account.email = email
                        multilogin_account.password = password
                        multilogin_account.folder_id = profile.get(
                            'folder_id', '')
                        # multilogin_account.multilogin_profile_id = profile.get('id', '')
                        multilogin_account.profile_name = profile.get(
                            'name', '')
                        multilogin_account.save()

                messages.success(request, 'Login success')
                return redirect('user')
            else:
                messages.error(
                    request, 'Login failed. Please check infomation again')
    else:
        form = MultiloginForm()
    return render(request, 'multilogin.html', {'form': form})
