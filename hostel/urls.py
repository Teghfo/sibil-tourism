from rest_framework.routers import SimpleRouter

from hostel.views import ShowHost


router = SimpleRouter()
router.register("host", ShowHost, basename="host")

urlpatterns = router.urls
