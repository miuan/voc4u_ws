import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template

from wordctrl import WordCtrl
from wordcore import *
from init import Init
#from test import Test
from view.view import *
from wordcore.word import LangId
#-a 192.168.1.170
class MainPage(webapp.RequestHandler):
    
    
    

    def createLinks(self, idPrefixName, funcName, idOther, langs):
        tempa = '<a href="javascript:" onclick="javascript:%(func)s" id="%(id)s" class="%(class)s" >%(title)s</a>'
        lang1 = ''
        
        
        
        for lg in langs:
            code = lg.code
            id = idPrefixName + code
            func = "%(func)s('#%(id)s', '%(code)s', '%(idOther)s');" % { "func" : funcName, "id": id, "code": code, "idOther" : idOther}
            lang1 += tempa % {"func" : func, "id" : id, "class" : idPrefixName, "title" : code}
                              
        
        return lang1

    def get(self):
        
        langs = LangId.all()
        langs = langs.fetch(8)
       
        lang1 = ''
        lang2= ''
        
        idPrefixName = 'langLearn'
        lang1 = self.createLinks(idPrefixName, 'setTo', 'langNative', langs)
        
        idPrefixName = 'langNative'
        lang2 = self.createLinks(idPrefixName, 'setFrom', 'langLearn', langs)
           
                
        template_values = {
            'greetings': 'greetings',
            'url': self.request.headers['Accept-Language'],
            'url_linktext': lang1,
            'url_linktext2': lang2
        }



        v = View()
        self.response.out.write("milan medlik")
        #self.response.out.write(v.getTemplate('index.html',template_values))

class Guestbook(webapp.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                       ('/wordctrl', WordCtrl),
                                       ('/init', Init),
                                       #('/test', Test)
                                       ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()