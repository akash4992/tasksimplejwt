from accounts import views
from django.urls import path,include
app_name = 'accounts'
urlpatterns = [
    path('register/',views.RegisterAPI.as_view(),name='register_user'),
    path('login/', views.LoginView.as_view(),name='login'),
    path('user-list/', views.UserListApiView.as_view(), name='user_list'),
    path('salary/', views.SalaryList.as_view(), name='salary'),

]