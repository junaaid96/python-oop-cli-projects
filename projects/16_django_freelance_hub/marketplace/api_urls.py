from rest_framework.routers import DefaultRouter

from .api_views import ProjectViewSet, ProposalViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("proposals", ProposalViewSet, basename="proposal")

urlpatterns = router.urls
