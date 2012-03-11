'''
Created on 16.1.2012

@author: m1uan
'''
# http://simplejson.googlecode.com/svn/tags/simplejson-2.0.9/docs/index.html

import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template

from wordcore.word import *
from wordcore import core
from django.utils import simplejson as json
from google.appengine.api import memcache

class WordCtrl(webapp.RequestHandler):

    def generateCodeForLastUpdateCache(self, learnCode, nativeCode, object=False):
        nc, lc, o1, o2 = core.WordCore().ResortLearnAndNativeCode(learnCode, nativeCode, "", "")
        
        code = "LUC_" + nc + "_" + lc
        
        if not object:
            code += learnCode + nativeCode
        
        return code
        
    def writeToLastUpdateCacheHuman(self, data, learnCode, nativeCode):
        cachecode = self.generateCodeForLastUpdateCache(learnCode, nativeCode)
        nc, lc, o1, o2 = core.WordCore().ResortLearnAndNativeCode(learnCode, nativeCode, "", "")
        
        if nc == learnCode:
            json = self.createJSONFromWords(data)
        else:
            json = self.createJSONFromWords(data, True)
        
        if not memcache.add(cachecode, json):
            memcache.set(cachecode, json)
            
    def writeToLastUpdateCache(self, key, learnCode, nativeCode):
        CACHEMAX = 35
        cachecode = self.generateCodeForLastUpdateCache(learnCode, nativeCode, True)
        
        data = memcache.get(cachecode)
        if data is None:
            data = []
        
        position = 0
        found = False
        for w in data:
            tid = key.id()
            mid = w["id"]
            if mid == tid:
                found = True
                break;
            position += 1
    
        if found:
            del data[position]
        
        word = core.WordCore().getWord(key)
        
        if word is not None:
            # todo store text wersion
            data.insert(0, word.forJSON(False))
            
            
        # only cachemax items
        while len(data) > CACHEMAX:
            data.pop()
            
        self.writeToLastUpdateCacheHuman(data, learnCode, nativeCode)
        self.writeToLastUpdateCacheHuman(data, nativeCode, learnCode)
            
        if memcache.add(cachecode, data) is False:
            memcache.set(cachecode, data)    
    
    # get parameters: 
    # l - [TEXT] learn word
    # n - [TEXT] native word
    # lc - [CODE] learn code
    # nc - [CODE] native code
    # lp - [TEXT] learn pronouciation
    # np - [TEXT] native pronouciation
    # ld - [TEXT] learn description
    # nd - [TEXT] native description
    # ls - [TEXT] learn special/additional info
    # ns - [TEXT] native special/additional info
    # nocache [INT] 1 -- no cache :-)      
    def methodAddWord(self):
        strl = cgi.escape(self.request.get('l'))
        strlc = cgi.escape(self.request.get('lc'))
        strn = cgi.escape(self.request.get('n'))
        strnc = cgi.escape(self.request.get('nc'))
        strlp = cgi.escape(self.request.get('lp'))
        strld = cgi.escape(self.request.get('ld'))
        strls = cgi.escape(self.request.get('ls'))
        strnp = cgi.escape(self.request.get('np'))
        strnd = cgi.escape(self.request.get('nd'))
        strns = cgi.escape(self.request.get('ns'))
        nocache = cgi.escape(self.request.get('nocache'))
        
        if len(nocache) < 1:
            nocache = 0
        else:
            nocache = int(nocache)
    
        
        if len(strl) > 0 and len(strn) > 0:
            wc = core.WordCore()
            result, key, errorcode = wc.addWord(strl, strn, strlc, strnc, strlp, strld, strls, strnp, strnd, strns)
            
            if result:
                if nocache != 1:
                    self.writeToLastUpdateCache(key, strlc, strnc)                    
                self.showResult("word", str(key))  
            elif isinstance(key, str) and isinstance(errorcode, int):
                  self.showErrorResult(errorcode, key)
            else:
                self.showErrorResult(1, "word is not stored or updated")
#            self.response.headers['Access-Control-Allow-Origin'] = '*'
#            self.response.out.write("Add word learn: " + strl)
#            self.response.out.write(" native: " + strn)
#            self.response.out.write("(lc/nc " + self.request.get('lc'))
#            self.response.out.write("/" + self.request.get('nc') + ")")
        return 

    def methodTrans(self):
        str = cgi.escape(self.request.get('s'))
        codeFrom = cgi.escape(self.request.get('f'))
        codeTo = cgi.escape(self.request.get('t'))
        
        if len(str) > 0 and len(codeFrom) > 0 and len(codeTo) > 0:
            wc = core.WordCore()
            words = wc.getTranslation(str, codeFrom, codeTo)
            
            if len(words) > 0:
                self.response.out.write("<div > TRANSLATE</div>")
                for w in words:
                    self.response.out.write("<br>" + w) 
            
        return


    def methodGetLastUpdatedWords(self, learnCode, nativeCode, type):
        #json = self.methodGetWordsFromDB(learnCode, nativeCode, type, 0, True)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/xml'
        
        key = self.generateCodeForLastUpdateCache(learnCode, nativeCode)
        
        data = memcache.get(key)
        if not data:
            self.response.out.write("{len: 0}")
        else:
            self.response.out.write(data)
    # get parameters    
    # lc - [TEXT] learn langugage [CS, EN, .. ]
    # nc - [TEXT] native langugage [CS, EN, .. ]
    # t - [TEXT] type [json, html]
    # p - [INT] page [0, ... ]
    def methodGetWords(self):
        
        learnCode = self.request.get('lc')
        nativeCode = self.request.get('nc')
        type = self.request.get('t')
        page = self.request.get('p')
        lastUpdated = False
        
        if len(page) < 1:
            pageI = 0
        else:
            pageI = int(page)
        
        if pageI < 0:
            self.methodGetLastUpdatedWords(learnCode, nativeCode, type)
            return
        
        key = "K_" + learnCode + nativeCode + "_" + type + "_" + str(pageI)
        data = memcache.get(key)
        if data is not None:
            json = data
        else:
            json = self.methodGetWordsFromDB(learnCode, nativeCode, type, pageI, lastUpdated)
            if not memcache.add(key, json, 12*3600):
                self.response.out.write("ja nevim")
        
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
        self.response.headers['Content-Type'] = 'application/xml'
        self.response.out.write(json)


    def createJSONFromWords(self, words, cross=False):
        output = {}
        nativeIds = "natives"
        nativeIdNum = "num_natives"
        
        if not cross:
            name_learn = "learn"
            name_native = "native"
            name_native_desc = "native_desc"
            name_learn_spec = "learn_spec"
            name_learn_pronouc = "learn_pronouc" 
        else:
            name_learn = "native"
            name_native = "learn"
            name_native_desc = "learn_desc"
            name_learn_spec = "native_spec"
            name_learn_pronouc = "native_pronouc" 
            
            
        for word in words:
            id = word[name_learn]
            native = word[name_native]
            
            details = {
                    "native" : native,
                    "id" : word["id"],
                    "vote" : word["vote"],
                    "desc" : word[name_native_desc]
                    }
            
            if output.has_key(id):
                data = output[id]
                data[nativeIds].append(details)
                data[nativeIdNum] = data[nativeIdNum] + 1
            else:
                data = { 
                    nativeIds : [ details ],
                    nativeIdNum : 1,
                    "spec" : word[name_learn_spec],
                    "learn" : id,
                    "pronouc": word[name_learn_pronouc]
                    }
                #data[nativeIds].append(details)
                output[id] = data
        
        jsonrespons = []
        for word in output:
            n = output[word]
            jsonrespons.append({"word" : n})
            
       
        return json.dumps({"len" : len(jsonrespons), "data" : jsonrespons})

    def methodGetWordsFromDB(self, learnCode, nativeCode, type, page, lastUpdated):         
        wc = core.WordCore()
        words = wc.getWords(learnCode, nativeCode, page, lastUpdated)
        
#        if type == 'json':
#            self.response.out.write(json.dumps(words))
#            return
        
        return self.createJSONFromWords(words)
        
        row = """
        <div class="word" id="word_%(index)i">
            <div class="word_row" onClick="javascript:showDetail('%(index)i');">
            <span id="word_row_learn_%(index)i">%(learn)s</span>
            <span class="word_row_native" id="word_row_native_%(index)i">- %(native)s</span>
            </div>
            <div class="word_details_area" id="detail_area_%(index)i">
                %(detail)s
            </div>
        </div>
        """
#        row ='<div class="row">%(learn)s - %(native)s</div>'
#        row += '<div class="detail" id="#detail_%(index)i">'
#        row += "%(detail)s"
#        row += '</div>'
        
        detailRow = """
        <div>
            <a href="javascript:" class="word_detail" id="word_detail_%(learn)s" onClick="javascript:wordVote('%(id)s');">%(learn)s - %(native)s</a>
            <a href="javascript:" onClick="javascript:wordDelete('%(id)s');">(X)</a>
            <a href="javascript:" onClick="javascript:wordEdit('%(learn)s', '%(native)s');">(E)</a>
        </div>
        """
        
        strout = ""
        index = 1
        for o in output.keys():
            index += 1
            native = ""
            detail = ""
            for n in output[o]:
                native += n["native"] + ", "
                detail += detailRow % {"learn" : o, "native" : n["native"], "id" : n["id"]}
            native = native[:-2]
            
            strout += row % {"learn": o, "native" : native, "index" : index, "detail" : detail}
#        output = { "len" : len(words), "words" : words }
#        self.response.out.write("<br> len: " + str(len(words)))
#        self.response.out.write("<script> showWords('#words', ")
        #self.response.out.write(json.dumps(output))

        self.response.out.write("<br>" + strout)
#        self.response.out.write(");</script>")
        #for w in words:
        #    self.response.out.write("<br>" + w["learn"] + " - " +str( w["native"]))
            #self.response.out.write(" - " + w.word1Code.code + "/" + w.word2Code.code)
        self.response.out.write(cgi.escape(self.request.get('content')))
        return
    
    def methodGetLangs(self):
        langs = LangId.all()
        self.showErrorResult(1, "deprecated")
    
    def methodWordWote(self):
        
        id = self.request.get('id')
        idi = int(id)
        loaded_word = Word.get_by_id([idi])
        
        if len(loaded_word) < 1 or loaded_word[0] is None:
            self.showErrorResult(1, "the id (" + id + ") is wrong")
            return
        
        word = loaded_word[0]
        word.vote = word.vote + 1
        word.save()
        
        dic = word.toDictionary()
        self.showResult("word", dic)
        
        
    def showResultEx(self, data_name, data, error, error_message):
        show = { "error" : error, "error_message" : error_message }
        
        if data_name != None and data != None:
            show[data_name] = data
        
        self.response.headers['Access-Control-Allow-Origin'] = '*'       
        self.response.out.write(json.dumps(show))

    def showErrorResult(self, error, error_message):
        self.showResultEx(None, None, error, error_message)
    
    def showResult(self, data_name, data):
        self.showResultEx(data_name, data, "0", "ok")
    
    def methodWordRemove(self):
        id = self.request.get('id')
        word = Word.get_by_id(id)
        word.vote = word.vote - 1
        word.save()
        #todo :remove if vote 1



    def getLangIds(self):
        lang = LangId()
        a = lang.all()
        results = a.fetch(10)
        
        
        for i in results:
            i.code
            self.response.out.write(' ' + i.code + "key:")
    
    def get(self):
        
       
        
        method = cgi.escape(self.request.get('m'))
        
        if method == 'add':
            self.methodAddWord()
        elif method == 'trans':
            self.methodTrans()
        elif method == 'show':
            self.methodGetWords()
        elif method == 'vote':
            self.methodWordWote()
        elif method == 'getlangs':
            self.methodGetLangs()
        elif len(method) < 1:
            self.response.out.write('method not set')
        else:
            self.response.out.write('uknown method \"' + method + '\"')
            
        
        
        #lang.save()
        
    def post(self):
         self.methodGetWords()
         