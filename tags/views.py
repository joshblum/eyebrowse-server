import json
import os
import urllib
import requests

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from annoying.decorators import ajax_request
from urlparse import urlparse
from common.templatetags.gravatar import gravatar_for_user

from tags.models import Domain, Page, Highlight
from api.models import Tag, Topic, Value, Vote, UserTagInfo
from accounts.models import UserProfile

TAGS = {
  'fairness': {
    'color': '#bcf0ff',
    'description': 'Fairness is ideas of justice, rights, and autonomy.',
  },
  'cheating': {
    'color': '#feffbc',
    'description': 'Cheating is acting dishonestly or unfairly in order to gain an advantage.',
  },
  'loyalty': {
    'color': '#bcffe2',
    'description': 'Loyalty underlies virtues of patriotism and self-sacrifice for the group.',
  },
  'betrayal': {
    'color': '#ffe5bc',
    'description': 'Betrayal is disloyalty and the destruction of trust.',
  },
  'care': {
    'color': '#bcc1ff',
    'description': 'Care is concern for the well-being of others.',
  },
  'harm': {
    'color': '#ffbcf5',
    'description': 'Harm is something that causes someone or something to be hurt, broken, made less valuable or successful, etc.',
  },
  'authority': {
    'color': '#ffb29e',
    'description': 'Authority underlies virtues of leadership and followership, including deference to legitimate authority and respect for traditions.',
  },
  'subversion': {
    'color' :'#e7bcff',
    'description': 'Subversion is the undermining of the power and authority of an established system or institution.',
  },
  'sanctity': {
    'color': '#d6ffbc',
    'description': 'Sanctity underlies notions of striving to live in an elevated, less carnal, more noble way.',
  },
  'degradation': {
    'color': '#ffbcd1',
    'description': 'Degradation is the process in which the beauty or quality of something is destroyed or spoiled',
  },
  'morality': {
    'color' : '#c1bfc0',
    'description': 'Morality is a particular system of values and principles of conduct.',
  },
};

trie = {u'a': {u'b': {u'a': {u'n': {u'd': {u'o': {u'n': {u'*': {'_end_': ('_end_', u'harm')}}}}}}, u'i': {u'd': {u'e': {'_end_': ('_end_', u'authority')}}}, u's': {u't': {u'i': {u'n': {u'e': {u'n': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}, u'e': {u'm': {u'i': {u'o': {u'u': {u's': {u'n': {u'e': {u's': {u's': {'_end_': ('_end_', u'sanctity')}}}}}}}}}, u'n': {u't': {u'i': {u'o': {u'n': {'_end_': ('_end_', u'sanctity')}}}}}}}}, u'u': {u's': {u'e': {u'*': {'_end_': ('_end_', u'harm')}}}}}, u'd': {u'u': {u'l': {u't': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}}, u'g': {u'i': {u't': {u'a': {u't': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}, u'm': {u'i': {u't': {u'y': {'_end_': ('_end_', u'care')}}}}, u'l': {u'i': {u'e': {u'n': {u'a': {u't': {u'e': {'_end_': ('_end_', u'subversion')}}}}}}, u'l': {u'y': {'_end_': ('_end_', u'loyalty')}, u'e': {u'g': {u'i': {u'a': {u'n': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}}, u'n': {u'n': {u'i': {u'h': {u'i': {u'l': {u'a': {u't': {u'e': {u'*': {'_end_': ('_end_', u'harm')}}}}}}}}}}, u'p': {u'o': {u's': {u't': {u'a': {u's': {u'y': {'_end_': ('_end_', u'subversion')}}, u't': {u'e': {'_end_': ('_end_', u'subversion')}}}}}}}, u'u': {u's': {u't': {u'e': {u'r': {u'i': {u't': {u'y': {'_end_': ('_end_', u'sanctity')}}}}}}}, u't': {u'h': {u'o': {u'r': {u'i': {u't': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}}, u't': {u't': {u'a': {u'c': {u'k': {u'*': {'_end_': ('_end_', u'harm')}}}}}}}, u'c': {u'a': {u's': {u't': {u'e': {u'*': {'_end_': ('_end_', u'authority')}}}}, u'r': {u'i': {u'n': {u'g': {'_end_': ('_end_', u'care')}}}, u'e': {'_end_': ('_end_', u'care')}}, u'd': {u'r': {u'e': {'_end_': ('_end_', u'loyalty')}}}, u'n': {u'o': {u'n': {'_end_': ('_end_', u'morality')}}}}, u'e': {u'l': {u'i': {u'b': {u'a': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}}, u'h': {u'a': {u's': {u't': {u'*': {'_end_': ('_end_', u'sanctity')}}}, u'r': {u'a': {u'c': {u't': {u'e': {u'r': {'_end_': ('_end_', u'morality')}}}}}}}, u'u': {u'r': {u'c': {u'h': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}}, u'l': {u'a': {u's': {u's': {'_end_': ('_end_', u'authority')}}}, u'i': {u'q': {u'u': {u'*': {'_end_': ('_end_', u'loyalty')}}}}, u'e': {u'a': {u'n': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}, u'o': {u'h': {u'o': {u'r': {u't': {'_end_': ('_end_', u'loyalty')}}}}, u'r': {u'r': {u'e': {u'c': {u't': {'_end_': ('_end_', u'morality')}}}}}, u'm': {u'p': {u'a': {u's': {u's': {u'i': {u'o': {u'n': {u'*': {'_end_': ('_end_', u'care')}}}}}}}, u'l': {u'i': {u'a': {u'n': {u'*': {'_end_': ('_end_', u'authority')}}}}, u'y': {'_end_': ('_end_', u'authority')}}}, u'r': {u'a': {u'd': {u'*': {'_end_': ('_end_', u'loyalty')}}}}, u'm': {u'a': {u'n': {u'd': {'_end_': ('_end_', u'authority')}}}, u'u': {u'n': {u'a': {u'l': {'_end_': ('_end_', u'loyalty')}}, u'i': {u's': {u'*': {'_end_': ('_end_', u'loyalty')}}, u't': {u'*': {'_end_': ('_end_', u'loyalty')}}}, u'e': {u'*': {'_end_': ('_end_', u'loyalty')}}}}, u'e': {u'n': {u'd': {u'a': {u'b': {u'l': {u'e': {'_end_': ('_end_', u'morality')}}}}}}}}}, u'l': {u'l': {u'e': {u'c': {u't': {u'i': {u'v': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}}}, u'n': {u's': {u't': {u'a': {u'n': {u't': {'_end_': ('_end_', u'fairness')}}}}}, u't': {u'a': {u'g': {u'i': {u'o': {u'*': {'_end_': ('_end_', u'degradation')}}}}}, u'r': {u'o': {u'l': {'_end_': ('_end_', u'authority')}}}}}}, u'r': {u'u': {u's': {u'h': {u'*': {'_end_': ('_end_', u'harm')}}}, u'e': {u'l': {u'*': {'_end_': ('_end_', u'harm')}}}}}}, u'b': {u'a': {u'd': {'_end_': ('_end_', u'morality')}, u'l': {u'a': {u'n': {u'c': {u'e': {u'*': {'_end_': ('_end_', u'fairness')}}}}}}}, u'e': {u't': {u'r': {u'a': {u'y': {u'*': {'_end_': ('_end_', u'subversion')}}}}}, u'n': {u'e': {u'f': {u'i': {u't': {u'*': {'_end_': ('_end_', u'care')}}}}}}}, u'i': {u'a': {u's': {u'*': {'_end_': ('_end_', u'cheating')}}}, u'g': {u'o': {u't': {u'*': {'_end_': ('_end_', u'cheating')}}}}}, u'l': {u'a': {u'm': {u'e': {u'l': {u'e': {u's': {u's': {'_end_': ('_end_', u'morality')}}}}}}}, u'e': {u'm': {u'i': {u's': {u'h': {'_end_': ('_end_', u'degradation')}}}}}}, u'o': {u'u': {u'r': {u'g': {u'e': {u'o': {u'i': {u's': {u'i': {u'e': {'_end_': ('_end_', u'authority')}}}}}}}}}}, u'r': {u'u': {u't': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'harm')}}}}}}}, u'e': {u'g': {u'a': {u'l': {u'i': {u't': {u'a': {u'r': {u'*': {'_end_': ('_end_', u'fairness')}}}}}}}}, u'm': {u'p': {u'a': {u't': {u'h': {u'*': {'_end_': ('_end_', u'care')}}}}}}, u'n': {u'e': {u'm': {u'*': {'_end_': ('_end_', u'betrayal')}}}, u'd': {u'a': {u'n': {u'g': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'harm')}}}}}}}}, u'q': {u'u': {u'a': {u'b': {u'l': {u'e': {'_end_': ('_end_', u'fairness')}}}, u'l': {u'*': {'_end_': ('_end_', u'fairness')}}}, u'i': {u't': {u'y': {'_end_': ('_end_', u'fairness')}}, u'v': {u'a': {u'l': {u'e': {u'n': {u't': {'_end_': ('_end_', u'fairness')}}}}}}}}}, u't': {u'h': {u'i': {u'c': {u'*': {'_end_': ('_end_', u'morality')}}}}}, u'v': {u'i': {u'l': {'_end_': ('_end_', u'morality')}}, u'e': {u'n': {u'n': {u'e': {u's': {u's': {'_end_': ('_end_', u'fairness')}}}}}}}, u'x': {u'p': {u'l': {u'o': {u'i': {u't': {'_end_': ('_end_', u'harm'), u'i': {u'n': {u'g': {'_end_': ('_end_', u'harm')}}}, u's': {'_end_': ('_end_', u'harm')}, u'e': {u'd': {'_end_': ('_end_', u'harm')}}, u'a': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}}}, u'c': {u'l': {u'u': {u's': {u'i': {u'o': {u'n': {'_end_': ('_end_', u'cheating')}}}}, u'd': {u'*': {'_end_': ('_end_', u'cheating')}}}}}, u'e': {u'm': {u'p': {u'l': {u'a': {u'r': {u'y': {'_end_': ('_end_', u'morality')}}}}}}}}}, u'd': {u'i': {u's': {u'c': {u'r': {u'i': {u'm': {u'i': {u'n': {u'a': {u't': {u'*': {'_end_': ('_end_', u'cheating')}}}}}}}}}, u'e': {u'a': {u's': {u'e': {u'*': {'_end_': ('_end_', u'degradation')}}}}}, u'g': {u'u': {u's': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}}, u'h': {u'o': {u'n': {u'e': {u's': {u't': {'_end_': ('_end_', u'cheating')}}}}}}, u'l': {u'o': {u'y': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}, u'o': {u'b': {u'e': {u'*': {'_end_': ('_end_', u'subversion')}}}}, u'p': {u'r': {u'o': {u'p': {u'o': {u'r': {u't': {u'i': {u'o': {u'n': {u'*': {'_end_': ('_end_', u'cheating')}}}}}}}}}}}, u's': {u'i': {u'd': {u'e': {u'n': {u't': {'_end_': ('_end_', u'subversion')}}}}}, u'e': {u'n': {u't': {u'*': {'_end_': ('_end_', u'subversion')}}}}, u'o': {u'c': {u'i': {u'a': {u't': {u'e': {'_end_': ('_end_', u'cheating')}}}}}}}, u'r': {u'e': {u's': {u'p': {u'e': {u'c': {u't': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}}}}, u'r': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}, u'u': {u't': {u'y': {'_end_': ('_end_', u'authority')}, u'i': {u'*': {'_end_': ('_end_', u'authority')}}}}, u'e': {u'c': {u'e': {u'i': {u'v': {u'*': {'_end_': ('_end_', u'betrayal')}}}, u'n': {u'*': {'_end_': ('_end_', u'sanctity')}}}}, u'b': {u'a': {u's': {u'e': {u'*': {'_end_': ('_end_', u'degradation')}}}, u'u': {u'c': {u'h': {u'e': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}}, u'f': {u'i': {u'a': {u'n': {u'*': {'_end_': ('_end_', u'subversion')}}}, u'l': {u'e': {u'*': {'_end_': ('_end_', u'degradation')}}}}, u'y': {u'*': {'_end_': ('_end_', u'subversion')}}, u'e': {u'c': {u't': {u'o': {u'r': {'_end_': ('_end_', u'subversion')}}}}, u'r': {'_end_': ('_end_', u'authority'), u'e': {u'*': {'_end_': ('_end_', u'authority')}}}, u'n': {u'*': {'_end_': ('_end_', u'care')}}}}, u'n': {u'o': {u'u': {u'n': {u'c': {u'e': {'_end_': ('_end_', u'subversion')}}}}}}, u'p': {u'r': {u'a': {u'v': {u'*': {'_end_': ('_end_', u'degradation')}}}}}, u's': {u'e': {u'c': {u'r': {u'a': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}}, u'r': {u't': {u'i': {u'n': {u'g': {'_end_': ('_end_', u'subversion')}}}, u'e': {u'r': {u'*': {'_end_': ('_end_', u'subversion')}}, u'd': {'_end_': ('_end_', u'subversion')}}}}}, u't': {u'r': {u'o': {u'y': {'_end_': ('_end_', u'harm')}}}}}, u't': {u'r': {u'i': {u'm': {u'e': {u'n': {u't': {u'*': {'_end_': ('_end_', u'harm')}}}}}}}}, u'v': {u'o': {u't': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}, u'a': {u'm': {u'a': {u'g': {u'*': {'_end_': ('_end_', u'harm')}}}}}, u'o': {u'c': {u't': {u'r': {u'i': {u'n': {u'e': {'_end_': ('_end_', u'morality')}}}}}}}}, u'g': {u'r': {u'o': {u's': {u's': {'_end_': ('_end_', u'degradation')}}, u'u': {u'p': {'_end_': ('_end_', u'loyalty')}}}}, u'u': {u'a': {u'r': {u'd': {u'*': {'_end_': ('_end_', u'care')}}}}, u'i': {u'l': {u'd': {'_end_': ('_end_', u'loyalty')}}}}, u'o': {u'o': {u'd': {'_end_': ('_end_', u'morality'), u'n': {u'e': {u's': {u's': {'_end_': ('_end_', u'morality')}}}}}}}}, u'f': {u'i': {u'l': {u't': {u'h': {u'*': {'_end_': ('_end_', u'degradation')}}}}, u'g': {u'h': {u't': {u'*': {'_end_': ('_end_', u'harm')}}}}}, u'a': {u'i': {u'r': {u'*': {'_end_': ('_end_', u'fairness')}, u'm': {u'i': {u'n': {u'd': {u'*': {'_end_': ('_end_', u'fairness')}}}}}, u'l': {u'y': {'_end_': ('_end_', u'fairness')}}, u'n': {u'e': {u's': {u's': {'_end_': ('_end_', u'fairness')}}}}, u'p': {u'l': {u'a': {u'y': {'_end_': ('_end_', u'fairness')}}}}, '_end_': ('_end_', u'fairness')}}, u'm': {u'i': {u'l': {u'y': {'_end_': ('_end_', u'loyalty')}, u'i': {u'a': {u'l': {'_end_': ('_end_', u'loyalty')}}, u'e': {u's': {'_end_': ('_end_', u'loyalty')}}}}}}, u't': {u'h': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'authority')}}}}}, u'v': {u'o': {u'r': {u'i': {u't': {u'i': {u's': {u'm': {'_end_': ('_end_', u'cheating')}}}}}}}}}, u'e': {u'l': {u'l': {u'o': {u'w': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}, u'o': {u'r': {u'e': {u'i': {u'g': {u'n': {u'*': {'_end_': ('_end_', u'betrayal')}}}}}}}}, u'i': {u'l': {u'l': {u'e': {u'g': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}}, u'm': {u'p': {u'i': {u'e': {u't': {u'y': {'_end_': ('_end_', u'degradation')}}}, u'o': {u'u': {u's': {'_end_': ('_end_', u'degradation')}}}}, u'a': {u'i': {u'r': {'_end_': ('_end_', u'harm')}}, u'r': {u't': {u'i': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'fairness')}}}}}}}, u'o': {u's': {u't': {u'e': {u'r': {'_end_': ('_end_', u'betrayal')}}}}}}, u'm': {u'i': {u'g': {u'r': {u'a': {u'*': {'_end_': ('_end_', u'betrayal')}}}}}, u'a': {u'c': {u'u': {u'l': {u'a': {u't': {u'e': {'_end_': ('_end_', u'sanctity')}}}}}}}, u'o': {u'r': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'morality')}}}}}}}, u'd': {u'e': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'morality')}}}}}, u'n': {u'e': {u'q': {u'u': {u'i': {u't': {u'a': {u'b': {u'l': {u'e': {'_end_': ('_end_', u'cheating')}}}}}}}}}, u'd': {u'i': {u'v': {u'i': {u'd': {u'u': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'betrayal')}}}}}}}}, u'e': {u'c': {u'e': {u'n': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}, u'j': {u'u': {u's': {u't': {u'*': {'_end_': ('_end_', u'cheating')}}}}}, u'n': {u'o': {u'c': {u'e': {u'n': {u't': {'_end_': ('_end_', u'sanctity')}}}}}}, u's': {u'i': {u'd': {u'e': {u'r': {'_end_': ('_end_', u'loyalty')}}}}, u'u': {u'r': {u'g': {u'e': {u'n': {u't': {'_end_': ('_end_', u'subversion')}}}}}, u'b': {u'o': {u'r': {u'd': {u'i': {u'n': {u'a': {u't': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}}}}}}, u't': {u'e': {u'm': {u'p': {u'e': {u'r': {u'a': {u't': {u'e': {'_end_': ('_end_', u'degradation')}}}}}}}, u'g': {u'r': {u'i': {u't': {u'y': {'_end_': ('_end_', u'sanctity')}}}}}}}}}, u'h': {u'i': {u'e': {u'r': {u'a': {u'r': {u'c': {u'h': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}}, u'a': {u'r': {u'm': {u'*': {'_end_': ('_end_', u'harm')}}}}, u'e': {u'r': {u'e': {u't': {u'i': {u'c': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}}, u'u': {u'r': {u't': {u'*': {'_end_': ('_end_', u'harm')}}}}, u'o': {u'm': {u'e': {u'l': {u'a': {u'n': {u'd': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}, u'o': {u'l': {u'o': {u'g': {u'o': {u'u': {u's': {'_end_': ('_end_', u'fairness')}}}}}}}}, u'l': {u'y': {'_end_': ('_end_', u'sanctity')}, u'i': {u'n': {u'e': {u's': {u's': {'_end_': ('_end_', u'sanctity')}}}}}}, u'n': {u'e': {u's': {u't': {u'*': {'_end_': ('_end_', u'fairness')}}}}, u'o': {u'r': {u'*': {'_end_': ('_end_', u'authority')}}}}}}, u'k': {u'i': {u'l': {u'l': {'_end_': ('_end_', u'harm'), u'i': {u'n': {u'g': {'_end_': ('_end_', u'harm')}}}, u's': {'_end_': ('_end_', u'harm')}, u'e': {u'r': {u'*': {'_end_': ('_end_', u'harm')}}, u'd': {'_end_': ('_end_', u'harm')}}}}}}, u'j': {u'i': {u'l': {u't': {u'*': {'_end_': ('_end_', u'betrayal')}}}}, u'u': {u's': {u't': {u'i': {u'c': {u'e': {'_end_': ('_end_', u'fairness')}}, u'f': {u'i': {u'*': {'_end_': ('_end_', u'fairness')}}}}, u'n': {u'e': {u's': {u's': {'_end_': ('_end_', u'fairness')}}}}}}}, u'o': {u'i': {u'n': {u't': {'_end_': ('_end_', u'loyalty')}}}}}, u'm': {u'i': {u's': {u'c': {u'r': {u'e': {u'a': {u'n': {u't': {'_end_': ('_end_', u'betrayal')}}}}}}}}, u'a': {u'i': {u'd': {u'e': {u'n': {'_end_': ('_end_', u'sanctity')}}}}}, u'u': {u't': {u'i': {u'n': {u'o': {u'u': {u's': {'_end_': ('_end_', u'subversion')}}}}}}}, u'e': {u'm': {u'b': {u'e': {u'r': {'_end_': ('_end_', u'loyalty')}}}}}, u'o': {u'r': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'morality')}}}}, u't': {u'h': {u'e': {u'r': {'_end_': ('_end_', u'authority'), u'i': {u'n': {u'g': {'_end_': ('_end_', u'authority')}}}, u's': {'_end_': ('_end_', u'authority')}, u'l': {u'*': {'_end_': ('_end_', u'authority')}}}}}}, u'd': {u'e': {u's': {u't': {u'y': {'_end_': ('_end_', u'sanctity')}}}}}}}, u'l': {u'a': {u'x': {'_end_': ('_end_', u'degradation')}, u'u': {u'd': {u'a': {u'b': {u'l': {u'e': {'_end_': ('_end_', u'morality')}}}}}}, u'w': {'_end_': ('_end_', u'authority'), u'l': {u'e': {u's': {u's': {u'*': {'_end_': ('_end_', u'subversion')}}}}}, u'f': {u'u': {u'l': {u'*': {'_end_': ('_end_', u'authority')}}}}}}, u'i': {u'm': {u'p': {u'i': {u'd': {'_end_': ('_end_', u'sanctity')}}}}}, u'e': {u'a': {u'd': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'authority')}}}}}, u's': {u's': {u'o': {u'n': {'_end_': ('_end_', u'morality')}}}}, u'w': {u'd': {u'*': {'_end_': ('_end_', u'degradation')}}}, u'g': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'authority')}}}}}, u'o': {u'y': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}, u'o': {u'p': {u'p': {u'o': {u's': {u'e': {'_end_': ('_end_', u'subversion')}}}}}, u'r': {u'd': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'authority')}}}}}, u'b': {u's': {u'c': {u'e': {u'n': {u'*': {'_end_': ('_end_', u'degradation')}}}}, u't': {u'r': {u'u': {u'c': {u't': {'_end_': ('_end_', u'subversion')}}}}}}, u'e': {u'y': {u'*': {'_end_': ('_end_', u'authority')}}, u'd': {u'i': {u'e': {u'n': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}, u'f': {u'f': {u'e': {u'n': {u's': {u'i': {u'v': {u'e': {u'*': {'_end_': ('_end_', u'morality')}}}}}, u'd': {u'*': {'_end_': ('_end_', u'morality')}}}}}}}, u'n': {u'a': {u't': {u'i': {u'o': {u'n': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}, u'o': {u'b': {u'l': {u'e': {'_end_': ('_end_', u'morality')}}}, u'n': {u'c': {u'o': {u'n': {u'f': {u'o': {u'r': {u'm': {u'i': {u's': {u't': {'_end_': ('_end_', u'subversion')}}}}}}}}}}}}}, u'p': {u'a': {u't': {u'r': {u'i': {u'o': {u't': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}}, u'e': {u'a': {u'c': {u'e': {u'*': {'_end_': ('_end_', u'care')}}}}, u'r': {u'm': {u'i': {u's': {u's': {u'i': {u'o': {u'n': {'_end_': ('_end_', u'authority')}}}}}, u't': {'_end_': ('_end_', u'authority')}}}, u'v': {u'e': {u'r': {u't': {'_end_': ('_end_', u'degradation')}}}}}}, u'i': {u'e': {u't': {u'y': {'_end_': ('_end_', u'sanctity')}}}, u'o': {u'u': {u's': {'_end_': ('_end_', u'sanctity')}}}}, u'o': {u's': {u'i': {u't': {u'i': {u'o': {u'n': {'_end_': ('_end_', u'authority')}}}}}}}, u'r': {u'i': {u's': {u't': {u'i': {u'n': {u'e': {'_end_': ('_end_', u'sanctity')}}}}}, u'n': {u'c': {u'i': {u'p': {u'l': {u'e': {u'*': {'_end_': ('_end_', u'morality')}}}}}}}}, u'a': {u'i': {u's': {u'e': {u'w': {u'o': {u'r': {u't': {u'h': {u'y': {'_end_': ('_end_', u'morality')}}}}}}}}}}, u'e': {u's': {u'e': {u'r': {u'v': {u'e': {'_end_': ('_end_', u'sanctity')}}}}}, u'j': {u'u': {u'd': {u'*': {'_end_': ('_end_', u'cheating')}}}}, u'f': {u'e': {u'r': {u'e': {u'n': {u'c': {u'e': {'_end_': ('_end_', u'cheating')}}}}}}}}, u'o': {u'p': {u'e': {u'r': {'_end_': ('_end_', u'morality')}}}, u's': {u't': {u'i': {u't': {u'u': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}}, u'm': {u'i': {u's': {u'c': {u'u': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}, u't': {u'e': {u'c': {u't': {u'*': {'_end_': ('_end_', u'care')}}}, u's': {u't': {'_end_': ('_end_', u'subversion')}}}}, u'f': {u'a': {u'n': {u'*': {'_end_': ('_end_', u'degradation')}}}, u'l': {u'i': {u'g': {u'a': {u't': {u'e': {'_end_': ('_end_', u'degradation')}}}}}}}}}, u'u': {u'r': {u'i': {u't': {u'y': {'_end_': ('_end_', u'sanctity')}}}, u'e': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}, u's': {u'a': {u'i': {u'n': {u't': {u'*': {'_end_': ('_end_', u'sanctity')}}}}, u'c': {u'r': {u'e': {u'd': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}, u'f': {u'e': {u'*': {'_end_': ('_end_', u'care')}}}}, u'e': {u'q': {u'u': {u'e': {u's': {u't': {u'e': {u'r': {'_end_': ('_end_', u'betrayal')}}}}}}}, u'c': {u'u': {u'r': {u'*': {'_end_': ('_end_', u'care')}}}}, u'r': {u'v': {u'e': {'_end_': ('_end_', u'authority')}}}, u'd': {u'i': {u't': {u'i': {u'*': {'_end_': ('_end_', u'subversion')}}}}}, u'g': {u'r': {u'e': {u'g': {u'a': {u't': {u'*': {'_end_': ('_end_', u'loyalty')}}}}}}}}, u'i': {u'c': {u'k': {u'*': {'_end_': ('_end_', u'degradation')}}}, u'n': {'_end_': ('_end_', u'degradation'), u's': {'_end_': ('_end_', u'degradation')}, u'n': {u'i': {u'n': {u'g': {'_end_': ('_end_', u'degradation')}}}, u'e': {u'r': {u'*': {'_end_': ('_end_', u'degradation')}}, u'd': {'_end_': ('_end_', u'degradation')}}}, u'f': {u'u': {u'l': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}, u'h': {u'i': {u'e': {u'l': {u'd': {'_end_': ('_end_', u'care')}}}}, u'e': {u'l': {u't': {u'e': {u'r': {'_end_': ('_end_', u'care')}}}}}}, u'l': {u'u': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}, u'o': {u'l': {u'i': {u'd': {u'a': {u'r': {u'i': {u't': {u'y': {'_end_': ('_end_', u'loyalty')}}}}}}}}}, u'p': {u'y': {'_end_': ('_end_', u'betrayal')}, u'u': {u'r': {u'n': {'_end_': ('_end_', u'harm')}}}}, u'u': {u'p': {u'r': {u'e': {u'm': {u'a': {u'c': {u'y': {'_end_': ('_end_', u'authority')}}}}}}}, u'b': {u'm': {u'i': {u'*': {'_end_': ('_end_', u'authority')}}}, u'v': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'subversion')}}}}}, u'f': {u'f': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'harm')}}}}}}, u't': {u'a': {u'i': {u'n': {u'*': {'_end_': ('_end_', u'degradation')}}}, u't': {u'u': {u's': {u'*': {'_end_': ('_end_', u'authority')}}}}}, u'e': {u'r': {u'i': {u'l': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}, u'o': {u'm': {u'p': {'_end_': ('_end_', u'harm')}}}}, u'y': {u'm': {u'p': {u'a': {u't': {u'h': {u'*': {'_end_': ('_end_', u'care')}}}}}}}}, u'r': {u'i': {u'o': {u't': {u'*': {'_end_': ('_end_', u'subversion')}}}, u'g': {u'h': {u't': {u's': {'_end_': ('_end_', u'fairness')}, u'e': {u'o': {u'u': {u's': {u'*': {'_end_': ('_end_', u'morality')}}}}}}}}}, u'e': {u'a': {u's': {u'o': {u'n': {u'a': {u'b': {u'l': {u'e': {'_end_': ('_end_', u'fairness')}}}}}}}}, u'c': {u'i': {u'p': {u'r': {u'o': {u'c': {u'*': {'_end_': ('_end_', u'fairness')}}}}}}}, u'b': {u'e': {u'l': {u'*': {'_end_': ('_end_', u'subversion')}}}}, u'f': {u'i': {u'n': {u'e': {u'd': {'_end_': ('_end_', u'sanctity')}}}}, u'u': {u's': {u'e': {'_end_': ('_end_', u'subversion')}}}}, u'm': {u'o': {u'n': {u's': {u't': {u'r': {u'a': {u't': {u'e': {'_end_': ('_end_', u'subversion')}}}}}}}}}, u'n': {u'e': {u'g': {u'a': {u'd': {u'e': {'_end_': ('_end_', u'betrayal')}}}}}}, u'p': {u'u': {u'l': {u's': {u'*': {'_end_': ('_end_', u'degradation')}}}}}, u's': {u'p': {u'e': {u'c': {u't': {'_end_': ('_end_', u'authority'), u's': {'_end_': ('_end_', u'authority')}, u'e': {u'd': {'_end_': ('_end_', u'authority')}}, u'f': {u'u': {u'l': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}}}, u'v': {u'e': {u'r': {u'e': {u'*': {'_end_': ('_end_', u'authority')}}}}}}, u'u': {u'i': {u'n': {u'*': {'_end_': ('_end_', u'harm')}}}}, u'a': {u'v': {u'a': {u'g': {u'e': {'_end_': ('_end_', u'harm')}}}}, u'n': {u'k': {u'*': {'_end_': ('_end_', u'authority')}}}}}, u'u': {u'p': {u's': {u't': {u'a': {u'n': {u'd': {u'i': {u'n': {u'g': {'_end_': ('_end_', u'morality')}}}}}}}}, u'r': {u'i': {u'g': {u'h': {u't': {'_end_': ('_end_', u'sanctity')}}}}}}, u'n': {u'a': {u'd': {u'u': {u'l': {u't': {u'e': {u'r': {u'a': {u't': {u'e': {u'd': {'_end_': ('_end_', u'sanctity')}}}}}}}}}}}, u'c': {u'h': {u'a': {u's': {u't': {u'e': {'_end_': ('_end_', u'degradation')}}}}}, u'l': {u'e': {u'a': {u'n': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}, u'b': {u'i': {u'a': {u's': {u'*': {'_end_': ('_end_', u'fairness')}}}}}, u'e': {u'q': {u'u': {u'a': {u'l': {u'*': {'_end_': ('_end_', u'cheating')}}}}}}, u'f': {u'a': {u'i': {u'r': {u'*': {'_end_': ('_end_', u'cheating')}}, u't': {u'h': {u'f': {u'u': {u'l': {'_end_': ('_end_', u'subversion')}}}}}}}}, u'i': {u's': {u'o': {u'n': {'_end_': ('_end_', u'loyalty')}}}, u't': {u'e': {u'*': {'_end_': ('_end_', u'loyalty')}}}}, u'j': {u'u': {u's': {u't': {u'*': {'_end_': ('_end_', u'cheating')}}}}}, u'p': {u'r': {u'e': {u'j': {u'u': {u'd': {u'i': {u'c': {u'e': {u'*': {'_end_': ('_end_', u'fairness')}}}}}}}}}}, u's': {u'c': {u'r': {u'u': {u'p': {u'u': {u'l': {u'o': {u'u': {u's': {'_end_': ('_end_', u'cheating')}}}}}}}}}}}}, u't': {u'a': {u'i': {u'n': {u't': {u'*': {'_end_': ('_end_', u'degradation')}}}}, u'r': {u'n': {u'i': {u's': {u'h': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}}, u'r': {u'a': {u'i': {u't': {u'o': {u'r': {u'*': {'_end_': ('_end_', u'subversion')}}}}}, u's': {u'h': {u'y': {'_end_': ('_end_', u'degradation')}}}, u'm': {u'p': {'_end_': ('_end_', u'degradation')}}, u'd': {u'i': {u't': {u'i': {u'o': {u'n': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}, u'n': {u's': {u'g': {u'r': {u'e': {u's': {u's': {u'*': {'_end_': ('_end_', u'morality')}}}}}}}}}, u'e': {u'a': {u's': {u'o': {u'n': {u'*': {'_end_': ('_end_', u'subversion')}}}}, u'c': {u'h': {u'e': {u'r': {u'*': {'_end_': ('_end_', u'subversion')}}}}}}}}, u'e': {u'r': {u'r': {u'o': {u'r': {u'i': {u's': {u'*': {'_end_': ('_end_', u'betrayal')}}}}}}}}, u'o': {u'l': {u'e': {u'r': {u'a': {u'n': {u't': {'_end_': ('_end_', u'fairness')}}}}}}, u'g': {u'e': {u't': {u'h': {u'e': {u'r': {'_end_': ('_end_', u'loyalty')}}}}}}}}, u'w': {u'i': {u'c': {u'k': {u'e': {u'd': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}, u'h': {u'o': {u'r': {u'e': {'_end_': ('_end_', u'degradation')}}, u'l': {u'e': {u's': {u'o': {u'm': {u'e': {u'*': {'_end_': ('_end_', u'sanctity')}}}}}}}}}, u'r': {u'e': {u't': {u'c': {u'h': {u'e': {u'd': {u'*': {'_end_': ('_end_', u'degradation')}}}}}}}, u'o': {u'n': {u'g': {u'*': {'_end_': ('_end_', u'morality')}}}}}, u'a': {u'r': {'_end_': ('_end_', u'harm'), u's': {'_end_': ('_end_', u'harm')}, u'r': {u'i': {u'n': {u'g': {'_end_': ('_end_', u'harm')}}}}, u'l': {u'*': {'_end_': ('_end_', u'harm')}}}, u'n': {u't': {u'o': {u'n': {'_end_': ('_end_', u'degradation')}}}}}, u'o': {u'r': {u't': {u'h': {u'*': {'_end_': ('_end_', u'morality')}}}}, u'u': {u'n': {u'd': {u'*': {'_end_': ('_end_', u'harm')}}}}}}, u'v': {u'a': {u'l': {u'u': {u'e': {u'*': {'_end_': ('_end_', u'morality')}}}}}, u'i': {u'r': {u't': {u'u': {u'o': {u'u': {u's': {'_end_': ('_end_', u'sanctity')}}}}}, u'g': {u'i': {u'n': {'_end_': ('_end_', u'sanctity'), u'i': {u't': {u'y': {'_end_': ('_end_', u'sanctity')}}}, u's': {'_end_': ('_end_', u'sanctity')}, u'a': {u'l': {'_end_': ('_end_', u'sanctity')}}}}}}, u'o': {u'l': {u'e': {u'n': {u'*': {'_end_': ('_end_', u'harm')}}}}}}, u'e': {u'n': {u'e': {u'r': {u'a': {u't': {u'*': {'_end_': ('_end_', u'authority')}}}}}}}}}


@login_required
@ajax_request
def value_tag(request):
  '''
  Adding and getting a value tag
  request requirements: 
   - tag name
   - tag description
   - tag color
   - tag url
  '''
  user = request.user
  success = False
  errors = {}

  # Add a new tag
  if request.POST:
    tag_name = request.POST.get('name')
    url = process_url(request.POST.get('url'))
    errors['add_tag'] = []

    p = Page.objects.get(url=url)
    if not p:
      errors['add_tag'].append("Page " + url + " doesn't exist")

    if len(Value.objects.filter(name=tag_name, page__url=url)) > 0:
      errors['add_tag'].append("Tag " + tag_name + " already exists")

    if len(errors['add_tag']) == 0:
      new_tag = Value(
        name=tag_name, 
        user=user, 
        color=TAGS[tag_name]["color"], 
        page=p,
        description=TAGS[tag_name]["description"],
      )
      new_tag.save()
      success = True

  elif request.GET:
    # TODO: get a tag?
    pass

  return {
      'success': success,
      'errors': errors,
    }

@login_required
@ajax_request
def add_vote(request):
  '''
  Adding a vote to a value tag
  '''
  user = request.user
  success = False
  errors = {}
  data = {}
  vote_count = 0

  if request.POST:
    tag_name = request.POST.get('valuetag')
    url = process_url(request.POST.get('url'))
    highlight = urllib.unquote(request.POST.get('highlight')).decode('utf8')
    errors['add_vote'] = []

    if not len(errors['add_vote']):
      vt = Value.objects.get(
        name=tag_name, 
        highlight__highlight=highlight, 
        page__url=url,
      )

      vote_count = len(Vote.objects.filter(tag=vt, voter=user))
      
      # Ensure user hasn't already voted
      if vote_count == 0:
        vt.vote_count += 1
        vt.save()

        vote = Vote(tag=vt, voter=user)
        vote.save()
        success = True

  vote_count = len(Vote.objects.filter(tag=vt))

  return {
    'success': success,
    'errors': errors,
    'vote_count': vote_count
  }

@login_required
@ajax_request
def remove_vote(request):
  '''
  Removing a vote from a value tag
  '''
  user = request.user
  success = False
  errors = {}
  data = {}
  vote_count = 0

  if request.POST:
    tag_name = request.POST.get('valuetag')
    url = process_url(request.POST.get('url'))
    highlight = urllib.unquote(request.POST.get('highlight')).decode('utf8')
    errors['remove_vote'] = []

    if not len(errors['remove_vote']):
      vt = Value.objects.get(
        name=tag_name, 
        highlight__highlight=highlight, 
        page__url=url,
      )
      old_votes = Vote.objects.filter(tag=vt, voter=user)

      if len(old_votes) > 0:
        vt.vote_count -= len(old_votes)
        old_votes.delete()
        success = True

  vote_count = len(Vote.objects.filter(tag=vt))

  return {
    'success': success,
    'errors': errors,
    'vote_count': vote_count
  }

@login_required
@ajax_request
def related_stories(request):
  success = False
  errors = {}
  page_info = {}
  data = {}

  if request.GET:
    url = process_url(request.GET.get('url'))

    api_url = "https://api.newsapi.aylien.com/api/v1/related_stories"

    payload = {
      "story_url": url,
      "return[]": ["id", "summary", "title", "source", "links", "body"],
      "source.rankings.alexa.rank.max": 2000,
      "language": ["en"],
      "per_page": 5,
    }

    headers = {
      "Access-Control-Allow-Origin": "*",
      "X-AYLIEN-NewsAPI-Application-ID": "6373daf3",
      "X-AYLIEN-NewsAPI-Application-Key": "5dd8483b654cbba292494175cfa601e9",
    }

    r = requests.get(api_url, params=payload, headers=headers)

    if r.status_code == 200:
      for item in r.json()["related_stories"]:
        if "logo_url" in item["source"]:
          logo = item["source"]["logo_url"]
        else:
          logo = ""

        data[item["id"]] = {
          "title": item["title"],
          "link": item["links"]["permalink"],
          "source": item["source"]["name"],
          "domain": item["source"]["domain"],
          "logo": logo,
          "summary": item["body"]
        }

      success = True

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

@login_required
@ajax_request
def page(request):
  '''
  Adding a page
  '''
  success = False
  user = request.user
  errors = {}
  page_info = {}

  if request.POST:
    url = process_url(request.POST.get('url'))
    domain_name = request.POST.get('domain_name')
    title = request.POST.get('title')
    parsed_url = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
    errors['page'] = []

    if len(Page.objects.filter(url=url)) != 0:
      errors['page'].append("Page already exists!")

    else: 
      if domain_name == "":
        domain_name = domain
      if title == "":
        title = url

      d, created = Domain.objects.get_or_create(url=domain, name=domain_name)
      d.save()
      p = Page(url=url, domain=d, title=title)
      p.save()
      success = True

  elif request.GET:
    url = process_url(request.GET.get('url'))
    parsed_url = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
    errors['page'] = []

    try: 
      p = Page.objects.get(url=url)
    except Page.DoesNotExist:  
      success = False
      errors['page'].append("Page does not exist")

      return {
        'success': success,
        'errors': errors,
        'page': None,
      }

    d = p.domain
    page_info = {
      "url": url,
      "title": p.title,
      "favicon_url": p.favicon_url,
      "domain": {
        "name": d.name,
        "url": d.url,
      } 
    }

  return {
    'success': success,
    'errors': errors,
    'page': page_info,
  }

@login_required
@ajax_request
def pages_by_topic(request):
  success = False
  errors = {}
  data = {}
  errors['pages_by_topic'] = []

  if request.GET:
    topic = request.GET.get('topic')

    ts = Topic.objects.filter(name=topic)
    pages = {}

    if not len(ts):
      for t in ts:
        pages[t.page.url] = {
          'domain': t.page.domain,
          'favicon': t.page.favIconUrl,
          'description': t.page.description,
          'title': t.page.title,
        }
      data['pages'] = pages
    else:
      errors['pages_by_topic'].append('No topics ' + topic + ' found')

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }


@login_required
@ajax_request
def highlight(request):
  '''
  Adding a highlight
  '''
  success = False
  user = request.user
  errors = {}
  data = {}

  if request.POST:
    url = process_url(request.POST.get('url'))
    highlight = request.POST.get('highlight')
    tags = json.loads(request.POST.get('tags'))
    errors['add_highlight'] = []

    if not len(errors['add_highlight']) and highlight != "":
      p = Page.objects.get(url=url)

      if not len(Highlight.objects.filter(page=p, highlight=highlight)):
        h = Highlight(page=p, highlight=highlight)
        h.save()

        for tag in tags:
          vt = Value(
            page=p, 
            highlight=h, 
            name=tag, 
            description=tags[tag]['description'], 
            user=user, 
            color=tags[tag]['color'],
          )
          vt.save()

        success = True

  return {
    'success': success,
    'errors': errors,
  }

@login_required
@ajax_request
def highlights(request):
  '''
  Getting all highlights
  '''
  success = False
  errors = {}
  data = {}
  highlights = {}
  max_tag = ()
  max_tag_count = 0

  if request.GET:
    url = process_url(request.GET.get('url'))
    errors['get_highlights'] = []

    if not len(errors['get_highlights']):
      hs = Highlight.objects.filter(page__url=url)
      for h in hs:
        max_tag = ()
        max_tag_count = 0

        vts = Value.objects.filter(highlight=h, page__url=url)
        for vt in vts:
          if vt.vote_count >= max_tag_count:
            max_tag_count = vt.vote_count
            max_tag = (vt.name, vt.color)
        highlights[h.highlight] = max_tag
      success = True

  return {
    'success': success,
    'errors': errors,
    'highlights': highlights,
  }

@login_required
@ajax_request
def add_topic(request):
  # TODO: topic api
  pass

@login_required
@ajax_request
def tags_by_page(request):
  '''
  Getting all tags for a page
  '''
  success = False
  errors = {}
  value_tags = {}
  user = request.user

  if request.GET:
    url = process_url(request.GET.get('url'))
    errors['get_tags'] = []

    if not len(errors['get_tags']):
      vts = Value.objects.filter(page__url=url, highlight=None)

      try:
        page = Page.objects.get(url=url)

        # get relevant info for each value tag
        for vt in vts:
          vt_info = {
            'user_voted': False,
            'name': vt.name,
            'color': vt.color,
            'domain': vt.domain,
            'description': vt.description,
            'is_private': vt.is_private,
            'vote_count': vt.vote_count,
          }

          value_tags[vt.name] = vt_info
          success = True

        if success == False:
          errors['get_tags'].append("No tags for page " + url)
      except Page.DoesNotExist:
        errors['get_tags'].append("Page " + url + " does not exist")

  return {
    'success': success,
    'errors': errors,
    'value_tags': value_tags,
  }

@login_required
@ajax_request
def tags_by_highlight(request):
  '''
  Getting all tags for a highlight
  '''
  success = False
  errors = {}
  value_tags = {}
  user = request.user

  if request.GET:
    highlight = urllib.unquote(request.GET.get('highlight')).decode('utf8')
    url = process_url(request.GET.get('url'))
    errors['get_tags'] = []

    h = Highlight.objects.get(highlight=highlight, page__url=url)
    if not h:
      errors['get_tags'].append("Highlight " + highlight + "doesn't exist!")

    if not len(errors['get_tags']):
      vts = Value.objects.filter(highlight=h, page__url=url)

      # get relevant info for each value tag
      for vt in vts:
        vt_info = {
          'user_voted': False,
          'name': vt.name,
          'color': vt.color,
          'domain': vt.domain,
          'description': vt.description,
          'is_private': vt.is_private,
          'vote_count': vt.vote_count,
        }

        votes = []
        vs = Vote.objects.filter(tag=vt)

        # get vote info
        for v in vs:
          if user == v.voter:
            vt_info['user_voted'] = True
          user_profile = UserProfile.objects.get(user=v.voter)
          pic = user_profile.pic_url
          if not pic:
            pic = gravatar_for_user(v.voter)
          votes.append({
            'name': user_profile.get_full_name(),
            'pic': pic,
          })
        vt_info['votes'] = votes

        value_tags[vt.name] = vt_info

  return {
    'success': success,
    'errors': errors,
    'value_tags': value_tags,
  }


@login_required
@ajax_request
def user_value_tags(request):
  success = False
  errors = {}
  data = {}
  user = request.user
  errors['user_value_tags'] = []

  if request.GET:
    tag_counts = {}
    uts = UserTagInfo.objects.filter(user=user)

    if len(uts) != 0:
      for ut in uts:
        if ut.tag.name in tag_counts:
          tag_counts[ut.tag.name] += 1
        else:
          tag_counts[ut.tag.name] = 1
      data['tag_counts'] = tag_counts
      success = True

    else:
      errors['user_value_tags'].append("No user tag info")

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

# add domain
      # if already exists, pass
    # add page
      # if already exists, get value tags for page
    # count value tags for page
    # add value tags to page
    # add value tags to user

    # return value tags
@login_required
@ajax_request
def initialize_page(request):
  success = False
  value_tags = {}
  errors = {}
  user = request.user

  if request.POST:
    url = process_url(request.POST.get('url'))
    domain_name = request.POST.get('domain_name')
    title = request.POST.get('title')
    add_usertags = request.POST.get('add_usertags')

    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))

    errors['add_page'] = []

    if len(Page.objects.filter(url=url)) != 0:
      errors['add_page'].append("Page already exists!")

      # Get value tags for page
      vts = Value.objects.filter(page__url=url, highlight=None)

      for vt in vts:
        vt_info = {
          'user_voted': False,
          'name': vt.name,
          'color': vt.color,
          'domain': vt.domain,
          'description': vt.description,
          'is_private': vt.is_private,
          'vote_count': vt.vote_count,
        }

        value_tags[vt.name] = vt_info

    else: 
      if domain_name == "":
        domain_name = domain
      if title == "":
        title = url

      # Add domain
      d, created = Domain.objects.get_or_create(url=domain, name=domain_name)
      d.save()

      if not created:
        errors['add_domain'] = ["Domain already exists"]

      # Add page
      try:
        page = Page(url=url, domain=d, title=title)
        page.save()

        # Count value tags for page
        r = requests.get(url)
        emotes = start(r.text, trie)
        tags = [(e, emotes[e]) for e in emotes if e]
        sorted(tags, key=lambda x: x[1], reverse=True)

        for tag in tags:
          if tag[1] > 2:
            name = tag[0]
            value_tags[name] = {
              'name': name,
              'color': TAGS[name]['color'],
              'description': TAGS[name]['description'],
            }

            # Add tag to page
            try:
              vt = Tag.objects.get(page__url=url, name=name, highlight=None)
            except:
              vt = Value(
                name=name, 
                user=user, 
                color=TAGS[name]["color"], 
                page=page,
                description=TAGS[name]["description"],
              )
              vt.save()

            # Add tag to user
            if add_usertags == "true":
              try:
                UserTagInfo.objects.get(user=user, page=page, tag=vt)
              except UserTagInfo.DoesNotExist:  
                uto = UserTagInfo(user=user, page=page, tag=vt)
                uto.save()
            success = True

      except:
        errors['add_page'].append("Could not create page")

    return {
      'success': success,
      'errors': errors,
      'value_tags': value_tags,
    }


# Helper function to parse urls minus query strings
def process_url(url):
  for i in range(len(url)):
    if url[i] == "?":
      return url[:i]

  return url

# Trie variable
_end = '_end_'

# Helper trie functions
def in_trie(trie, word):
  current_dict = trie
  for letter in word: 
    if letter in current_dict:
      current_dict = current_dict[letter]
    elif "*" in current_dict:
      return current_dict["*"][_end][1]
    else:
      return False
  else:
    if _end in current_dict:
      return current_dict[_end][1]
    elif "*" in current_dict:
      return current_dict["*"][_end][1]
    else:
      return False

def countEmote(text, trie):
  emote_dict = {}
  for word in text:
    state = in_trie(trie, word)
    if state in emote_dict:
      emote_dict[state] += 1
    else:
      emote_dict[state] = 1
  return emote_dict

def start(text, trie):
  content = []
  for word in text.split(" "):
    if word.isalpha():
      content.append(word)

  return countEmote(content, trie)





