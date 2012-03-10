
import os
from google.appengine.ext.webapp import template



class View():
    def getTemplate(self, file_path, values = {}):
        f = "content/en/" + file_path
        
        path = os.path.join(os.path.dirname(__file__), file_path)
        return template.render(f, values)

