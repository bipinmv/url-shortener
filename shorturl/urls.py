from django.urls import path
from shorturl import views

urlpatterns = [
    path('',views.index,name="index"),
    path('user/signup/',views.signup,name="signup"),
    path('user/dashboard/',views.dashboard,name="dashboard"),
    path('user/login/',views.userlogin,name="login"),
    path('user/logout/',views.userlogout,name="logout"),
    path('<str:surl>/',views.external,name="external"),
    path('user/shorten/',views.shorten,name="shorten")
]
