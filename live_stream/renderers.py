from django.template.loader import render_to_string

from common.pagination import paginator
from common.constants import *

import urllib

def history_renderer(user, history, return_type, template, get_params=None, following=None):
    """ 
        Can render a history as html block or list of
        html items. User is the user requesting the view.
        History should be paginated before entering.
    """
    
    for hist in history:
        hist.messages = hist.eyehistorymessage_set.all()
        
    if return_type == "html":
        
        empty_search_msg = EMPTY_SEARCH_MSG['home_stream']

        template_values =  {
            'history' : history,
            'user' : user,
            'empty_search_msg': empty_search_msg,
            'following' : following,
        }

        if get_params:
            template_values['link_mod'] = "&" + urllib.urlencode(get_params)
        return render_to_string('live_stream/timeline.html',template_values)

    elif return_type == "list":
        history_list = []

        for h_item in history:
            history_list.append(render_to_string('live_stream/%s.html'% template, 
                {
                    'item' : h_item,
                    'user' : user,
                })
            )

        return history_list