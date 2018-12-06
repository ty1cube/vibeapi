
from django.conf.urls import url, include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('user', views.UserView)
# router.register('profile', views.ProfileView)



urlpatterns = [
    url(r'^login/?$', views.CustomAuthToken.as_view()),
    # url(r'^countries/?$', views.CountryView.as_view()),
    url(r'^member/user/?$', views.UserDefaultMemberView.as_view()),
    url(r'^member/user/artist/?$', views.GetUserArtistMemberView.as_view()),
    url(r'^member/user/manager/?$', views.GetUserRecordMemberView.as_view()),
    url(r'^member/create/artist/?$', views.CreateArtistMemberView.as_view()),
    # url(r'^member/join/artist/(?P<name>\w+)/?$', views.JoinArtistMemberView.as_view()),
    url(r'^member/create/manager/?$', views.CreateRecordMemberView.as_view()),
    # url(r'^member/join/record/(?P<name>\w+)/?$', views.JoinRecordMemberView.as_view()),
    url(r'^logout/?$', views.Logout.as_view(), name='authemail-logout'),
    url(r'^signup/verify/?$', views.SignupVerify.as_view(),name='signup-verify'),
    url(r'^password/reset/?$', views.PasswordReset.as_view(), name='password-reset'),
    url(r'^password/reset/verify/?$', views.PasswordResetVerify.as_view(), name='password-reset-verify'),
    url(r'^password/reset/verified/?$', views.PasswordResetVerified.as_view(), name='password-reset-verified'),
    url(r'^password/change/?$', views.PasswordChange.as_view(), name='password-change'),
    # url('', include(router.urls))
]

# urlpatterns.extend(router.urls)
