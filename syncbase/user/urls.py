from django.conf.urls import url, include
from django.contrib.auth import views as auth

from user.forms import NewAccountForm
from user import views

app_name = 'user'
urlpatterns = [
    # auth

    url(r'^create/$', views.UserCreate.as_view(), name='create'),

    url(r'^login/$', auth.login,
        {'template_name':'user/login.html'},
        name='login'),

    url(r'^logout/$', auth.logout,
        {'template_name':'user/logout.html'},
        name='logout'),

    url(r'^password_change/$', auth.password_change,
        {'template_name':'user/password_change_form.html',
            'post_change_redirect':'user:password_change_done'},
        name='password_change'),

    url(r'^password_change/done/$', auth.password_change_done,
        {'template_name':'user/password_change_done.html'},
        name='password_change_done'),

    url(r'^password_reset/$', auth.password_reset,
        {'post_reset_redirect': 'user:password_reset_done',
            'template_name': 'user/password_reset_form.html',
            'email_template_name': 'user/password_reset_email.html',
            'subject_template_name': 'user/password_reset_subject.txt'},
        name='password_reset'),

    url(r'^password_reset/done/$', auth.password_reset_done,
        {'template_name': 'user/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.password_reset_confirm,
        {'post_reset_redirect':'user:password_reset_complete',
            'template_name': "user/password_reset_confirm.html"},
        name='password_reset_confirm'),

    url(r'^reset/done/$', auth.password_reset_complete,
        {'template_name': 'user/password_reset_complete.html'},
        name='password_reset_complete'),

    # profile

    url(r'^basic/$', views.BasicInfo.as_view(), name="basic"),
]
