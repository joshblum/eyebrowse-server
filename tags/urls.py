from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('tags.views',
                        url(r'^value_tag$', 'value_tag'),
                        url(r'^tags/page', 'tags_by_page'),
                        url(r'^tags/highlight', 'tags_by_highlight'),
                        url(r'^vote/add$', 'add_vote'),
                        url(r'^vote/remove$', 'remove_vote'),
                        url(r'^page$', 'page'),
                        url(r'^page/related_stories$', 'related_stories'),
                        url(r'^pages/topic$', 'pages_by_topic'),
                        url(r'^highlight$', 'highlight'),
                        url(r'^highlights$', 'highlights'),
                        url(r'^user/tags$', 'user_value_tags'),
                        url(r'^initialize_page$', 'initialize_page'),
                      )