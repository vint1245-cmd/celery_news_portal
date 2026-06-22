from django.urls import path
from .views import IndexView, upgrade_me,PostsList
urlpatterns = [
    path('', IndexView.as_view()),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('logout/', PostsList.as_view()),
]