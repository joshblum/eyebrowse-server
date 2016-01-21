from django.contrib.auth.models import User
from django.db import models


class TwitterInfo(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    twitter_username = models.CharField(max_length=40, default='')
    twitter_id = models.IntegerField()
    access_token = models.CharField(max_length=140, default='')
    access_token_secret = models.CharField(max_length=140, default='')

class GoogleInfo(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    access_token = models.CharField(max_length=140, default='')

class DeliciousInfo(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    access_token = models.CharField(max_length=140, default='')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # other fields here

    follows = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    activation_key = models.CharField(max_length=40, default='')
    pic_url = models.CharField(max_length=1000, default='')
    use_tour = models.BooleanField(default=True)
    anon_email = models.BooleanField(default=False)

    location = models.CharField(max_length=1000, default='')
    website = models.CharField(max_length=1000, default='')
    bio = models.CharField(max_length=1000, default='')

    confirmed = models.BooleanField(default=False)

    def get_following_history(self, history=None):
        following = self.follows.all()
        if not history:

            from api.models import EyeHistory
            history = EyeHistory.objects.all()

        query_set = history.filter(user__in=following)
        return query_set

    def get_full_name(self):
        fullname = self.user.get_full_name()
        if fullname:
            return fullname
        return self.user.username

    def __unicode__(self):
        return "%s's profile" % self.user


User.profile = property(lambda u: u.get_profile())

import signals
signals.setup()
