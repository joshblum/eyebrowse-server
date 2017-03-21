from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('tags.views',
                        url(r'^value_tag$', 'value_tag'),
                        url(r'^tags/page', 'tags_by_page'),
                        url(r'^tags/highlight', 'tags_by_highlight'),
                        url(r'^vote$', 'vote'),
                        url(r'^remove_vote$', 'remove_vote'),
                        url(r'^page$', 'page'),
                        url(r'^highlight$', 'highlight'),
                        url(r'^highlights$', 'highlights'),
                      )