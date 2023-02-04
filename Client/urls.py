from rest_framework.routers import SimpleRouter
from Client.views import GetAuthToken, ApplicationViewSet, RegisterUser
from django.urls import path

app_name = 'Client'

router = SimpleRouter()
router.register('application', ApplicationViewSet, 'application')

urlpatterns = [
    path('token/', GetAuthToken.as_view()),
    path('register/', RegisterUser.as_view()),
]

urlpatterns += router.urls
