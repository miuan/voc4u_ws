'''
Created on 16.1.2012

@author: m1uan
'''

from google.appengine.ext import db

class LangId(db.Model):
    code = db.StringProperty(multiline=False)
    #flag = db.StringProperty(multiline=False)

class WordEntity(db.Model):
    word = db.StringProperty()
    pronouc = db.StringProperty()
    desc = db.StringProperty()
    
    lang = db.Reference(LangId, collection_name="lang")
    vote = db.IntegerProperty()
    
    lastChange = db.DateTimeProperty(auto_now=True)
    
class Word(db.Model):
    word1 = db.Reference(WordEntity, collection_name="word1")
    # the same as in learn.lang
    # is for quickly search
    word1LangId = db.Reference(LangId, collection_name="word1Code")
    word1Lang = db.StringProperty()
    
    special1 = db.StringProperty()
    
    
    word2 = db.Reference(WordEntity, collection_name="word2")
    # the same as in learn.lang
    # is for quickly search
    word2LangId = db.Reference(LangId, collection_name="word2Code")
    word2Lang = db.StringProperty()
    
    special2 = db.StringProperty()
    vote = db.IntegerProperty()
    
    lastChange = db.DateTimeProperty(auto_now=True)
#    def getLearn(self):
#        return learn.word
    def toDictionary(self):
        out = {
               "id" : self.key().id(),
               "vote" : self.vote
               
        }
        return out
    
    def forJSON(self, cross):
        if not cross:
            learn = self.word1
            native = self.word2
            learnLang = self.word1Lang
            nativeLang = self.word2Lang
            lspec = self.special1
            ldesc = self.word1.desc
            lpronouc = self.word1.pronouc
            nspec = self.special2
            ndesc = self.word2.desc
            npronouc = self.word2.pronouc
            #output.append({"learn" : w.word1.word, "native" : w.word2.word})
        else:
            learn = self.word2
            native = self.word1
            learnLang = self.word2Lang
            nativeLang = self.word1Lang
            lspec = self.special2
            ldesc = self.word2.desc
            lpronouc = self.word2.pronouc
            nspec = self.special1
            ndesc = self.word1.desc
            npronouc = self.word1.pronouc
                
        return {"learn" : learn.word,
                           "native" : native.word,
                           "learnLang" : learnLang,
                           "nativeLang" : nativeLang,
                           "id" : self.key().id(),
                           "vote" : self.vote,
                           
                           "learn_desc" : ldesc,
                           "learn_pronouc" : lpronouc,
                           "learn_spec" : lspec,
                           
                           "native_desc" : ndesc,
                           "native_pronouc" : npronouc,
                           "native_spec" : nspec,
                           
                           "vote_learn" : learn.vote,
                           "vote_native" : native.vote}
        
        #return out
        
    