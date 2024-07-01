from django.urls import include, path
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments',
    views.CommentViewSet,
    basename='comments'
)
router_v1.register(
    'users',
    views.UserViewSet,
    basename='users'
)

auth_patterns = [
    path('signup/', views.signup, name='signup'),
    path('token/', views.token, name='token')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
