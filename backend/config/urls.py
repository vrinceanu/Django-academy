"""URL map. API routes are grouped by caller (design doc, "API"), never by app.

Groups filled in later milestones:
  me/ (M1)  learn/ (M4)  attempts/ submissions/ (M5)  teach/ (M4-M5)
  studio/ (M2-M3)  manage/ (M1+)  public/ (M2, M6)  media/ (M3)
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.accounts.api.views import MeView
from apps.core.api.views import HealthView

api_v1 = [
    path("health/", HealthView.as_view(), name="health"),
    path("me/", MeView.as_view(), name="me"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="api-docs"),
]

admin.site.site_header = "CHIPS Academy operations"
admin.site.site_title = "CHIPS Academy ops"

urlpatterns = [
    path("api/v1/", include(api_v1)),
    path("ops/admin/", admin.site.urls),
]
