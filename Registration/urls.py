from django.urls import path
from rest_framework.routers import SimpleRouter
from Registration.views import PlayStoreRegistrationViewSet, TwitterRegistrationViewSet, DiscourseRegistrationViewSet, IntercomRegistrationViewSet

app_name = 'Registration'

router = SimpleRouter()
router.register('playstore', PlayStoreRegistrationViewSet, 'playstore')
router.register('twitter', TwitterRegistrationViewSet, 'twitter')
router.register('discourse', DiscourseRegistrationViewSet, 'discourse')
router.register('intercom', IntercomRegistrationViewSet, 'intercom')

urlpatterns = router.urls
