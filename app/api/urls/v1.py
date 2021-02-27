from django.urls import path, include

urlpatterns = [
    path('account/', include(('app.api.account.urls', 'app.account'))),
]
