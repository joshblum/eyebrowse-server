import json
import os
import urllib

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from annoying.decorators import ajax_request
from urlparse import urlparse
from common.templatetags.gravatar import gravatar_for_user

from tags.models import Domain, Page, Highlight
from api.models import Tag, Topic, Value, Vote
from accounts.models import UserProfile


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
    description = request.POST.get('description')
    color = request.POST.get('color')
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
        color=color, 
        page=p,
        description=description,
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
def vote(request):
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
def page(request):
  '''
  Adding a page
  '''
  success = False
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

    p = Page.objects.get(url=url)
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


# Helper function to parse urls minus query strings
def process_url(url):
  for i in range(len(url)):
    if url[i] == "?":
      return url[:i]

  return url





