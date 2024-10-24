from rest_framework.routers import SimpleRouter

from appbase.views.health import HealthView

router = SimpleRouter(False)
router.register("health", HealthView, "health")
urls = router.urls