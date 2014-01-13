# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'LocationType', fields ['order']
        db.create_unique(u'questionnaire_locationtype', ['order'])


    def backwards(self, orm):
        # Removing unique constraint on 'LocationType', fields ['order']
        db.delete_unique(u'questionnaire_locationtype', ['order'])


    models = {
        'questionnaire.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['questionnaire']