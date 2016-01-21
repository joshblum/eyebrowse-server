# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterInfo'
        db.create_table('accounts_twitterinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('twitter_id', self.gf('django.db.models.fields.IntegerField')()),
            ('access_token', self.gf('django.db.models.fields.CharField')(default='', max_length=140)),
            ('access_token_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=140)),
        ))
        db.send_create_signal('accounts', ['TwitterInfo'])

        # Adding model 'DeliciousInfo'
        db.create_table('accounts_deliciousinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('access_token', self.gf('django.db.models.fields.CharField')(default='', max_length=140)),
        ))
        db.send_create_signal('accounts', ['DeliciousInfo'])
        
        # Adding model 'GoogleInfo'
        db.create_table('accounts_googleinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('access_token', self.gf('django.db.models.fields.CharField')(default='', max_length=140)),
        ))
        db.send_create_signal('accounts', ['GoogleInfo'])
        
        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('pic_url', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('use_tour', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('anon_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('website', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('bio', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding M2M table for field follows on 'UserProfile'
        m2m_table_name = db.shorten_name('accounts_userprofile_follows')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_userprofile_id', 'to_userprofile_id'])


    def backwards(self, orm):
        # Deleting model 'TwitterInfo'
        db.delete_table('accounts_twitterinfo')

        # Deleting model 'DeliciousInfo'
        db.delete_table('accounts_deliciousinfo')
        
        # Deleting model 'GoogleInfo'
        db.delete_table('accounts_googleinfo')

        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Removing M2M table for field follows on 'UserProfile'
        db.delete_table(db.shorten_name('accounts_userprofile_follows'))


    models = {
        'accounts.deliciousinfo': {
            'Meta': {'object_name': 'DeliciousInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.twitterinfo': {
            'Meta': {'object_name': 'TwitterInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'access_token_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'twitter_id': ('django.db.models.fields.IntegerField', [], {}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.googleinfo': {
            'Meta': {'object_name': 'GoogleInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'anon_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followed_by'", 'symmetrical': 'False', 'to': "orm['accounts.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'pic_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'use_tour': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']