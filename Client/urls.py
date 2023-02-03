from rest_framework.routers import SimpleRouter
from Client.views import GetAuthToken, ApplicationViewSet
from django.urls import path

app_name = 'Client'

router = SimpleRouter()
router.register('application', ApplicationViewSet, 'application')

urlpatterns = [
    path('token/', GetAuthToken.as_view())
]

urlpatterns += router.urls
