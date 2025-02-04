from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('signin/', views.login_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('emotion-analysis/', views.analyze_emotions, name='analyze_emotions'),
    path('object-detect/', views.object_detect, name='object_detect'),
     path('buttons/', views.buttons, name='buttons'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
