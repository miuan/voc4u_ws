'''
Created on 16.1.2012

@author: m1uan
'''

from google.appengine.ext import webapp
from wordcore.word import *
from google.appengine.ext import db

class Test(webapp.RequestHandler):

    

    def get(self):
        self.response.out.write('get')
        
    def post(self):
        self.response.out.write(self.request.POST);
        a = self.request.POST['a'];
        order = self.request.POST['Ordre']
        file = self.request.POST['image']
        #image = self.request.POST['image'];
        self.response.out.write(file);
        self.response.out.write(self.request.arguments())
        #self.response.out.write(image)
#        self.addLangCode("CZ")
#        self.addLangCode("EN")
#        self.addLangCode("DE")
#        self.addLangCode("FR")
#        self.addLangCode("IT")
#        self.addLangCode("SP")
#        self.addLangCode("PL")
#        self.addLangCode("PT")
              
