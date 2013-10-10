'''
Created on 2013-06-01

@author: actionluzifer
'''

import os
import sys
from source import mtsam
from source import motvf
from source.mtsam import isAnOTVFile


class mtsomofC(object):


    def run(self, path):
        self.path = path
        print("path: "+path)
        files = os.listdir(path)
        print(files)
        filesList = []
        movies = {}
        mediaInfo = motvf.MediaInfo()
        descriptionDict = self.loadDescription()
        self.logPrintDescription(descriptionDict)
        for file in files:
            if "descript.ion" not in file:
                print()
                fullfilename = os.path.normpath(path+"/"+file)
                if os.path.isfile(fullfilename):
                    year, month, sender, isAnOTVFile = mtsam.getData(fullfilename)
                    
                    info = mediaInfo.getInfo(fullfilename)
                    dar, par = mediaInfo.getDPInfo(info)
                    self.logprintInfos(file, year, month, sender, dar, par, isAnOTVFile)
                    if dar and par:
                        self.appendMovieToDict(file, movies, dar, par, self.getDescription(file, descriptionDict))
                    else:
                        filesList.append(file)
                else:
                    print("nofile: "+file)
        
        self.logprint(movies, filesList)
        filesList = self.doSortUnsorted(movies, filesList, descriptionDict)
        self.doRename(movies, filesList, descriptionDict)
        self.logprint(movies, filesList)


    def appendMovieToDict(self, file, movies, dar, par, description):
        print("moviefile")
        if dar in movies:
            dardict = movies[dar]
        else:
            dardict = {}
            movies[dar] = dardict
        
        if par in dardict:
            pardict = dardict[par]
        else:
            pardict = {}
            dardict[par] = pardict
        
        filelist = []
        filelist.append((file, description))
        pardict[file] = filelist


    def doSortUnsorted(self, movies, files, descriptionDict):
        print("laenge der unsortierten: "+str(len(files)))
        newfiles = []
        for unsortedFile in files:
            filename = None
            wasCompatible = False
            for dars in movies:
                for pars in movies[dars]:
                    for filename in movies[dars][pars]:
                        print("scanne: "+unsortedFile)
                        isOK = self.isCompatible(filename, unsortedFile)
                        if isOK:
                            movies[dars][pars][filename].append((unsortedFile, self.getDescription(unsortedFile, descriptionDict)))
                            wasCompatible = True
                            break
            
            if not wasCompatible:
                if filename is not None:
                    print("fehlgeschlagen: #1="+filename+" #2="+unsortedFile)
                else:
                    print("fehlgeschlagen: #1="+" #2="+unsortedFile)
                newfiles.append((unsortedFile, self.getDescription(unsortedFile, descriptionDict)))

        return newfiles


    def isCompatible(self, file, unsortedFile):
        fileShort = ""
        laenge = 0
        for aChar in unsortedFile:
            fileShort = fileShort+aChar
            head,sep,tail = file.partition(fileShort)
            laenge = len(fileShort)
            if head is None:
                if tail is None:
                    break
            else:
                if len(head)>0:
                    break

        if laenge*2 > len(file):
            return True
        else:
            return False


    def logprint(self, movies, filesList):
        print()
        print()
        print("sortiert")
        print(movies)
        for dars in movies:
            print("dars: "+dars)
            for pars in movies[dars]:
                print("  pars: "+pars)
                for files in movies[dars][pars]:
                    print("    point: "+files)
                    for file in movies[dars][pars][files]:
                        if type(file) is tuple:
                            print('      file: '+file[0]+'  -> "'+file[1]+'"')
                        else:
                            print("      file: "+file)
        print()
        print()
        print("unsortiert:")
        for file in filesList:
            if type(file) is tuple:
                print('           '+file[0]+'  -> "'+file[1]+'"')
            else:
                print("           "+file)


    def logprintInfos(self, file, year, month, sender, dar, par, isAnOTVFile):
        print("file: "+file)
        print("      year:        "+year)
        print("      month:       "+month)
        print("      sender:      "+sender)
        if isAnOTVFile:
            print("      isAnOTVFile: true")
        else:
            print("      isAnOTVFile: false")
        print("      dar:         "+str(dar))
        print("      par:         "+str(par))


    def logPrintDescription(self, descriptionDict):
        print()
        print()
        print("descript.ion: ")
        print(descriptionDict)
        print()
        print()


    def loadDescription(self):
        return mtsam.loadDescription(self.path)


    def writeDescription(self, _path, _filename, _description):
        mtsam.writeDescription(_path, _filename, _description)


    def getDescription(self, unsortedFile, descriptionDict):
        description = ""
        if unsortedFile in descriptionDict:
            description = descriptionDict[unsortedFile]
            print("                    #"+str(unsortedFile)+"#")
            print("                   ->"+description)
        else:
            print("###nicht gefunden: "+unsortedFile)
        return description

    def doRename(self, movies, filesList, descriptionDict):
        pass
        #self.writeDescription(filename, description)


    def getDirZeit(self, filename, mediaInfo, args):
        year, month, sender, isAnOTVFile = mtsam.getData(filename)
        path = os.path.normpath(year+"-"+month)
        if len(args) > 0:
            if args[0] == "s":
                path = os.path.normpath(path+"/"+self.getDirSender(filename, mediaInfo, args[1:]))
            elif args[0] == "f":
                path = os.path.normpath(path+"/"+self.getDirFormat(filename, mediaInfo, args[1:]))    
        return path
    
    
    def getDirSender(self, filename, mediaInfo, args):
        year, month, sender, isAnOTVFile = mtsam.getData(filename)
        path = sender
        if len(args) > 0:
            if args[0] == "t":
                path = os.path.normpath(path+"/"+self.getDirZeit(filename, mediaInfo, args[1:]))
            elif args[0] == "f":
                path = os.path.normpath(path+"/"+self.getDirFormat(filename, mediaInfo, args[1:]))
        return path
    
    
    def getDirFormat(self, filename, mediaInfo, args):
        #year, month, sender, isAnOTVFile = mtsam.getData(filename)
        info = mediaInfo.getInfo(args)
        dar, par = mediaInfo.getDPInfo(info) 
        path = os.path.normpath(dar+'/'+par)
        if len(args) > 0:
            if args[0] == "s":
                path = os.path.normpath(path+'/'+self.getDirSender(filename, mediaInfo, args[1:]))
            elif args[0] == "t":
                path = os.path.normpath(path+'/'+self.getDirZeit(filename, mediaInfo, args[1:]))
        return path

