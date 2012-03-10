'''
Created on 16.1.2012

@author: m1uan
'''

from word import *
from xmlrpclib import DateTime
from datetime import datetime

class WordCore():
    def addword(self, Word):
        Word.learn = ""
        Word.native = ""
        

    def entityLoadByParams(self, word, langid, desc):
        # all entity because in next step
        # will be testet the pronoucition or description
        entity = WordEntity.all(keys_only=False)
        entity.filter("word =", word)
        entity.filter("lang =", langid)
        
        if len(desc) > 0:
            entity.filter("desc =", desc)

        return entity.fetch(1)

    # str - word as text
    # langid - language id as text
    # pronouc - is pronouciation of word as text
    # desc - is description of word as text
    def createOrLoadWordEntity(self, str, langid, pronouc, desc):
        loaded = False
        
        entity = self.entityLoadByParams(str, langid, desc)
        
        # if try add new desc and the word
        # till now hadn't desc must try search
        # word without parameter desc
        testwithoutdesc = False
        if len(entity) < 1 and len(desc) > 0:
            testwithoutdesc = True
            entity = self.entityLoadByParams(str, langid, "")
        
        # no word founded
        # or - used test without desc and is expecting
        # that will be load entity without desc
        # when had load entity with the desc 
        #          - is mean we must create new entity with new desc!
        if len(entity) < 1 or (testwithoutdesc and len(entity[0].desc) > 0):
            entity = WordEntity(word=str, lang=langid, vote=100)
            entity.pronouc = pronouc
            entity.desc = desc
            
            #datenow = datetime.datetime.now()
            #entity.lastChange =datenow;
            entity.save()
            loaded = False
        else:
            entity = entity[0]
            resave = False
            # if word founded and the pronouciation isn't set
            if len(pronouc) > 0 and pronouc != entity.pronouc:
                entity.pronouc = pronouc
                resave = True
            
            if len(desc) > 0 and len != entity.desc:
                entity.desc = desc
                resave = True
            
            # if pronouc or desc changed
            if resave:
                #entity.lastChange = datetime.datetime.now()
                entity.save()
            
            loaded = True
        
        return loaded, entity


    def getLangIdFromCode(self, learnCode):
        
        lang = LangId.all(keys_only=True).filter("code =", learnCode)
        #lang.get()
        lang = lang.fetch(1)
        return lang[0]


    # switch the word1code and word2code by alphabet
    # when is switched is must also switch word1 and word2
    def ResortLearnAndNativeCode(self, word1Code, word2Code, word1, word2):
        #w1c, w2c = [word1Code, word2Code].sort()
        alist = [word1Code, word2Code]
        alist.sort();
        
        w1c = alist[0]
        w2c = alist[1]
        
        
        if w1c != word1Code:
            #switch
            w = word1
            word1 = word2
            word2 = w
        
        return str(w1c), w2c, word1, word2


    def addWord(self, word1a, word2a, word1Code, word2Code, pronouc1, desc1, spec1, pronouc2, desc2, spec2):
        
        w1c, w2c, word1, word2 = self.ResortLearnAndNativeCode(word1Code, word2Code, word1a, word2a)
        
        w1l = self.getLangIdFromCode(w1c)
        w2l = self.getLangIdFromCode(w2c)
        word1 = word1.strip()
        word2 = word2.strip()
        
        if w1c == word1Code:
            
            lpronouc = pronouc1.strip()
            ldesc = desc1.strip()
            lspec = spec1.strip()
            npronouc = pronouc2.strip()
            ndesc = desc2.strip()
            nspec = spec2.strip()
        else:
            
            lpronouc = pronouc2.strip()
            ldesc = desc2.strip()
            lspec = spec2.strip()
            npronouc = pronouc1.strip()
            ndesc = desc1.strip()
            nspec = spec1.strip()

        loadedLearn, learn_ent = self.createOrLoadWordEntity(word1, w1l, lpronouc, ldesc)
        
        #if loaded:
        #    learn_ent.lang = native_lang    
        # get or save
        loadedNative, native_ent = self.createOrLoadWordEntity(word2, w2l, npronouc, ndesc)
        
        if not loadedLearn or not loadedNative: 
            word = Word(vote=100)
            
            word.word1 = learn_ent
            word.word2 = native_ent
            
            word.word1LangId = w1l
            word.word1Lang = w1c;
            
            word.word2LangId = w2l
            word.word2Lang = w2c;
            
            word.special1 = lspec
            word.special2 = nspec
            
            word.save()
        else:
            words = Word.all();
            words.filter("word1 =", learn_ent)
            words.filter("word2 =", native_ent)
            word = words.fetch(1)
            if len(word) > 0:
                word = word[0]
                word.vote = word.vote + 1
                word.save()
            else:
                word = Word(vote=100)
                word.word1 = learn_ent
                word.word2 = native_ent
                word.word1Code = w1l
                word.word2Code = w2l
                word.save()
                
        return True, word.key()
    
    def getWord(self, key):
        
        return Word.get(key)
#        words.filter(condition1, w1c)
#        words.filter(condition2, w2c)
    
    
        
    def getWords(self, learnCode, nativeCode, startpos=0,lastUpdated=False):
        PAGESIZE = 30
        w1c, w2c, s1, s2 = self.ResortLearnAndNativeCode(learnCode, nativeCode, "", "")
        
        #l1 = self.getLangIdFromCode(w1c)
        #l2 = self.getLangIdFromCode(w2c)
        
        change = w1c != learnCode
        condition1 = "word1Lang = "
        condition2 = "word2Lang ="
#        if change:
#            condition1 = "word2Code = "
#            condition2 = "word1Code ="
#            change = True
        
        words = Word.all()
        words.filter(condition1, w1c)
        words.filter(condition2, w2c)
        if not lastUpdated:
            words.order("vote")
        else:
            words.order("lastChange")
            
        output = []
        
        o = words.fetch(limit=PAGESIZE, offset=(PAGESIZE*startpos))
        for w in o:
            learn = Word
            native = 0
            
            
#            if not change:
#                learn = w.word1
#                native = w.word2
#                learnLang = w.word1Lang
#                nativeLang = w.word2Lang
#                lspec = w.special1
#                ldesc = w.word1.desc
#                lpronouc = w.word1.pronouc
#                nspec = w.special2
#                ndesc = w.word2.desc
#                npronouc = w.word2.pronouc
#                #output.append({"learn" : w.word1.word, "native" : w.word2.word})
#            else:
#                learn = w.word2
#                native = w.word1
#                learnLang = w.word2Lang
#                nativeLang = w.word1Lang
#                lspec = w.special2
#                ldesc = w.word2.desc
#                lpronouc = w.word2.pronouc
#                nspec = w.special1
#                ndesc = w.word1.desc
#                npronouc = w.word1.pronouc
                
#            output.append({"learn" : learn.word,
#                           "native" : native.word,
#                           "learnLang" : learnLang,
#                           "nativeLang" : nativeLang,
#                           "id" : w.key().id(),
#                           "vote" : w.vote,
#                           
#                           "learn_desc" : ldesc,
#                           "learn_pronouc" : lpronouc,
#                           "learn_spec" : lspec,
#                           
#                           "native_desc" : ndesc,
#                           "native_pronouc" : npronouc,
#                           "native_spec" : nspec,
#                           
#                           "vote_learn" : learn.vote,
#                           "vote_native" : native.vote})
            output.append(w.forJSON(change))
#        worde = WordEntity.all(keys_only=True);
#        worde.filter("lang =", l1)
#        learn = worde.fetch(50);
#        cnt = len(learn)
#        #worde = WordEntity.all(keys_only=True);
#        #worde.filter("lang =", nativeLang)
#        #native = worde.fetch(5000);
#        
#        output = []
#        
#        
#        for lword in learn:
#            words = Word.all();
#            words.filter(condition1, lword)
#            #words.filter("native IN ", native)
#            words.filter(condition2, l2)
#            nativew = words.fetch(5);
#            nativestr = []
#            learnstr = ""
#            obj1 = {"learn" : "", "native" : [], "nativeCode" : "", "learnCode" : ""}
#            
#            
#            if len(nativew) > 0:
#                if change:
#                    obj1["learn"] = nativew[0].word2.word
#                else:
#                    obj1["learn"] = nativew[0].word1.word
#
#            for natw in nativew:
#                nw = ''
#                if change:
#                    nw = natw.word1.word
#                    nw += ", " + natw.word1.lang.code + " (" + natw.word1Code.code + ")"
#                else:
#                    nw = natw.word2.word
#                    nw += ", " + natw.word2.lang.code + " (" + natw.word2Code.code + ")"
#                
#                obj1["native"].append(nw)
#                
#            if len(obj1["native"]) > 0:
#                output.append(obj1)
        
        #words.filter("native.langId =", nativeLang)
        return output
        
    def getTranslation(self, txt, fromCode, toCode):
        
        w1c, w2c, s1, s2 = self.ResortLearnAndNativeCode(fromCode, toCode, txt, "")
        
        #langFrom = self.getLangIdFromCode(fromCode)
        #langTo = self.getLangIdFromCode(toCode)
        condition1 = "word1 IN"
        condition2 = "word1Code ="
        condition3 = "word2Code ="
        changed = w1c != fromCode
        
        if changed:
            condition1 = "word2 IN"
            condition2 = "word2Code ="
            condition3 = "word1Code ="
        
        codes = LangId().all()
        codes.filter("code =", fromCode)
        code = codes.fetch(4)
        
        code = code[0]
        #ws1 = words.fetch(20)
        fromW = WordEntity().all()
        fromW.filter("word =", txt.strip())
        fromW.filter("lang =", code)
        w = fromW.fetch(100)
        
        words = Word().all()
        #words.filter("learn.code = ", langFrom)
        words.filter(condition1, w)
        #words.filter(condition2, w1c)
        #words.filter(condition3, w2c)
        #words.order("-vote")
        finded = words.fetch(20)
        result = []
        
        for f in finded:
            fw = f.word2.word
            if changed:
                fw = f.word1.word
            result.append(fw)
     
        return result
