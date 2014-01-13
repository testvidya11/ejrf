# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationType'
        db.create_table(u'questionnaire_locationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=2, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('questionnaire', ['LocationType'])


    def backwards(self, orm):
        # Deleting model 'LocationType'
        db.delete_table(u'questionnaire_locationtype')


    models = {
        'questionnaire.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'null': 'True'})
        }
    }

    complete_apps = ['questionnaire']