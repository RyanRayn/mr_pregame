from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.profile, name='profile'),
    path('get_membership', views.get_membership, name='get_membership'),
    path('update_membership/<subscription_id>/',
         views.update_membership, name='update_membership'),
    path('cancel_subscription', views.cancel_subscription,
         name='cancel_subscription'),
    path('wh/', webhook, name='webhook'),
]
