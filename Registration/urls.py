from django.urls import path
from rest_framework.routers import SimpleRouter
from Registration.views import PlayStoreRegistrationViewSet

app_name = 'Registration'

router = SimpleRouter()
router.register('playstore', PlayStoreRegistrationViewSet, 'playstore')

urlpatterns = router.urls
