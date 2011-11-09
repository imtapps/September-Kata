from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from bowling import views
urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^bowling/(?P<bowler>\w+)/', views.BowlerScores.as_view(), name='bowling_scores'),
)
