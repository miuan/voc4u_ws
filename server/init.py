'''
Created on 16.1.2012

@author: m1uan
'''

from google.appengine.ext import webapp
from wordcore.word import *
from google.appengine.ext import db

class Init(webapp.RequestHandler):

    def addLangCode(self, code):
        lang = LangId()
        lang.code = code
        lang.put()


    def RemoveAllLocale(self):
        lang = LangId()
        a = lang.all()
        results = a.fetch(10)
        for i in results:
            i.delete()

    def get(self):
        self.response.out.write("ahoj")
        
#        word = Word()
#        a = word.all(   )
#        results = a.fetch(10000)
#        for i in results:
#            i.delete()
##        
#        word = WordEntity(only_keys=True)
#        a = word.all()
#        results = a.fetch(10000)
#        for i in results:
#            i.delete()
#            
#        self.RemoveAllLocale()
            
#        self.addLangCode("CZ")
#        self.addLangCode("EN")
#        self.addLangCode("DE")
#        self.addLangCode("FR")
#        self.addLangCode("IT")
#        self.addLangCode("SP")
#        self.addLangCode("PL")
#        self.addLangCode("PT")
#         self.addLangCode("KR")
#         self.addLangCode("RU")  
