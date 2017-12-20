from django.db import models
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet
from django import forms
from django.contrib.auth.models import User

# Create your models here.
    
# annotation model

class Sentence( models.Model ):
    pmid = models.IntegerField( verbose_name = "pmid" )
    section = models.IntegerField( verbose_name = "section in pmid" ) # 1 = title, 2 = abstract
    text = models.CharField( verbose_name = "sentence text", max_length = 1024 )
    
class Token(models.Model):
    sentence = models.ForeignKey( Sentence )
    seqnr = models.IntegerField( verbose_name = "sequence number token" )
    startpos = models.IntegerField( verbose_name = "start position" ) 
    endpos = models.IntegerField( verbose_name = "end position" ) 
    
    def text(self):
        return self.sentence.text[self.startpos:self.endpos]

class Annotation(models.Model):
    annotation = models.CharField( verbose_name = "give annotation id", max_length = 50 )
    group = models.CharField( verbose_name = "semantic group", max_length = 15 )

class AnnotationToken(models.Model):
    token = models.ForeignKey( Token )
    annotation = models.ForeignKey( Annotation )
