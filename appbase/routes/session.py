from rest_framework.routers import SimpleRouter

from appbase.views.session import SessionView

router = SimpleRouter(False)
router.register("session", SessionView, "session")
urls = router.urls