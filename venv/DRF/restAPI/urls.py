from rest_framework import routers
from restAPI.api.views import UserAuthAPIView

router = routers.DefaultRouter()
router.register(r'', UserAuthAPIView, base_name='user')

urlpatterns = [
    #url(r'user/', UserAuthAPIView.as_view()),
]

urlpatterns += router.urls