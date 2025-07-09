from django.urls import path
from .views import signup_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True,
        next_page='article_list'
    ), name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='article_list'), name='logout'),
]
