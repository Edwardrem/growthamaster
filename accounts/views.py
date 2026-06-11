from django.contrib.auth.views import LoginView, LogoutView


class StaffLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class StaffLogoutView(LogoutView):
    next_page = '/'
