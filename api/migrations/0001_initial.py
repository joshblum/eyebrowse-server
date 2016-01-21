# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MuteList'
        db.create_table('api_mutelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True)),
            ('word', self.gf('django.db.models.fields.URLField')(max_length=300, null=True)),
        ))
        db.send_create_signal('api', ['MuteList'])

        # Adding model 'Tag'
        db.create_table('api_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('domain', self.gf('django.db.models.fields.URLField')(default='', max_length=300)),
        ))
        db.send_create_signal('api', ['Tag'])

        # Adding model 'ChatMessage'
        db.create_table('api_chatmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author', to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
        ))
        db.send_create_signal('api', ['ChatMessage'])

        # Adding model 'WhiteListItem'
        db.create_table('api_whitelistitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=80)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 9, 11, 0, 0))),
        ))
        db.send_create_signal('api', ['WhiteListItem'])

        # Adding unique constraint on 'WhiteListItem', fields ['user', 'url']
        db.create_unique('api_whitelistitem', ['user_id', 'url'])

        # Adding model 'BlackListItem'
        db.create_table('api_blacklistitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=80)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 9, 11, 0, 0))),
        ))
        db.send_create_signal('api', ['BlackListItem'])

        # Adding unique constraint on 'BlackListItem', fields ['user', 'url']
        db.create_unique('api_blacklistitem', ['user_id', 'url'])

        # Adding model 'EyeHistoryRaw'
        db.create_table('api_eyehistoryraw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('src', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('domain', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('favicon_url', self.gf('django.db.models.fields.TextField')(default='')),
            ('favIconUrl', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=2000)),
            ('start_event', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_event', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('total_time', self.gf('django.db.models.fields.IntegerField')()),
            ('humanize_time', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal('api', ['EyeHistoryRaw'])

        # Adding model 'EyeHistory'
        db.create_table('api_eyehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('src', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('domain', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('favicon_url', self.gf('django.db.models.fields.TextField')(default='')),
            ('favIconUrl', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=2000)),
            ('start_event', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_event', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('total_time', self.gf('django.db.models.fields.IntegerField')()),
            ('humanize_time', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal('api', ['EyeHistory'])

        # Adding model 'EyeHistoryMessage'
        db.create_table('api_eyehistorymessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('post_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eyehistory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.EyeHistory'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('api', ['EyeHistoryMessage'])

        # Adding model 'PopularHistoryInfo'
        db.create_table('api_popularhistoryinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=255)),
            ('img_url', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('domain', self.gf('django.db.models.fields.URLField')(default='', max_length=100)),
            ('favicon_url', self.gf('django.db.models.fields.TextField')(default='')),
            ('favIconUrl', self.gf('django.db.models.fields.URLField')(default='', max_length=2000)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=2000)),
        ))
        db.send_create_signal('api', ['PopularHistoryInfo'])

        # Adding model 'PopularHistory'
        db.create_table('api_popularhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('popular_history', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.PopularHistoryInfo'])),
            ('top_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('unique_visitor_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('avg_time_spent_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('num_comment_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('total_time_spent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_time_ago', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('humanize_avg_time', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('avg_time_ago', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('api', ['PopularHistory'])

        # Adding unique constraint on 'PopularHistory', fields ['user', 'popular_history']
        db.create_unique('api_popularhistory', ['user_id', 'popular_history_id'])

        # Adding M2M table for field eye_hists on 'PopularHistory'
        m2m_table_name = db.shorten_name('api_popularhistory_eye_hists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('popularhistory', models.ForeignKey(orm['api.popularhistory'], null=False)),
            ('eyehistory', models.ForeignKey(orm['api.eyehistory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['popularhistory_id', 'eyehistory_id'])

        # Adding M2M table for field visitors on 'PopularHistory'
        m2m_table_name = db.shorten_name('api_popularhistory_visitors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('popularhistory', models.ForeignKey(orm['api.popularhistory'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['popularhistory_id', 'user_id'])

        # Adding M2M table for field messages on 'PopularHistory'
        m2m_table_name = db.shorten_name('api_popularhistory_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('popularhistory', models.ForeignKey(orm['api.popularhistory'], null=False)),
            ('eyehistorymessage', models.ForeignKey(orm['api.eyehistorymessage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['popularhistory_id', 'eyehistorymessage_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PopularHistory', fields ['user', 'popular_history']
        db.delete_unique('api_popularhistory', ['user_id', 'popular_history_id'])

        # Removing unique constraint on 'BlackListItem', fields ['user', 'url']
        db.delete_unique('api_blacklistitem', ['user_id', 'url'])

        # Removing unique constraint on 'WhiteListItem', fields ['user', 'url']
        db.delete_unique('api_whitelistitem', ['user_id', 'url'])

        # Deleting model 'MuteList'
        db.delete_table('api_mutelist')

        # Deleting model 'Tag'
        db.delete_table('api_tag')

        # Deleting model 'ChatMessage'
        db.delete_table('api_chatmessage')

        # Deleting model 'WhiteListItem'
        db.delete_table('api_whitelistitem')

        # Deleting model 'BlackListItem'
        db.delete_table('api_blacklistitem')

        # Deleting model 'EyeHistoryRaw'
        db.delete_table('api_eyehistoryraw')

        # Deleting model 'EyeHistory'
        db.delete_table('api_eyehistory')

        # Deleting model 'EyeHistoryMessage'
        db.delete_table('api_eyehistorymessage')

        # Deleting model 'PopularHistoryInfo'
        db.delete_table('api_popularhistoryinfo')

        # Deleting model 'PopularHistory'
        db.delete_table('api_popularhistory')

        # Removing M2M table for field eye_hists on 'PopularHistory'
        db.delete_table(db.shorten_name('api_popularhistory_eye_hists'))

        # Removing M2M table for field visitors on 'PopularHistory'
        db.delete_table(db.shorten_name('api_popularhistory_visitors'))

        # Removing M2M table for field messages on 'PopularHistory'
        db.delete_table(db.shorten_name('api_popularhistory_messages'))


    models = {
        'api.blacklistitem': {
            'Meta': {'unique_together': "(('user', 'url'),)", 'object_name': 'BlackListItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.chatmessage': {
            'Meta': {'object_name': 'ChatMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        'api.eyehistory': {
            'Meta': {'object_name': 'EyeHistory'},
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'end_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'humanize_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.eyehistorymessage': {
            'Meta': {'ordering': "['-post_time']", 'object_name': 'EyeHistoryMessage'},
            'eyehistory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.EyeHistory']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'api.eyehistoryraw': {
            'Meta': {'object_name': 'EyeHistoryRaw'},
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'end_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'humanize_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_event': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'total_time': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.mutelist': {
            'Meta': {'object_name': 'MuteList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'word': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True'})
        },
        'api.popularhistory': {
            'Meta': {'unique_together': "(('user', 'popular_history'),)", 'object_name': 'PopularHistory'},
            'avg_time_ago': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avg_time_spent_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'eye_hists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['api.EyeHistory']", 'symmetrical': 'False'}),
            'humanize_avg_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['api.EyeHistoryMessage']", 'symmetrical': 'False'}),
            'num_comment_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'popular_history': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.PopularHistoryInfo']"}),
            'top_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_time_ago': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_time_spent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unique_visitor_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'visitors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pophist_visitors'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'api.popularhistoryinfo': {
            'Meta': {'object_name': 'PopularHistoryInfo'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '100'}),
            'favIconUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'favicon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255'})
        },
        'api.tag': {
            'Meta': {'object_name': 'Tag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'domain': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'api.whitelistitem': {
            'Meta': {'unique_together': "(('user', 'url'),)", 'object_name': 'WhiteListItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 11, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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

    complete_apps = ['api']