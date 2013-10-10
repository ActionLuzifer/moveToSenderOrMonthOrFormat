#!/usr/bin/python3
# encoding: utf-8
'''
mtsomofa -- moves video files

mtsomofa is a description

It defines classes_and_methods

@author:     ActionLuzifer
        
@copyright:  2013. All rights reserved.
        
@license:    GPL v3

@contact:    actionluzi@yahoo.de
@deffield    updated: Updated
'''

import sys
import os
import source

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2013-06-01'
__updated__ = '2013-06-01'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by ActionLuzifer on %s.
  Copyright 2013. All rights reserved.
  
  Licensed under the GPL v3
  http://www.gnu.org/licenses/gpl-3.0.en.html
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))
        
    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-s", "--sender", dest="sender", help="sortieren nach Sender [default: %(default)s]")
        parser.add_argument("-t", "--time",   dest="time",   help="sortieren nach Zeit [default: %(default)s]")
        parser.add_argument("-f", "--format", dest="format", help="sortieren nach Format [default: %(default)s]")
        parser.add_argument("-st", "--sender", dest="sender", help="sortieren nach Sender und Zeit [default: %(default)s]")
        parser.add_argument("-sf", "--sender", dest="sender", help="sortieren nach Sender und Format [default: %(default)s]")
        parser.add_argument("-ts", "--time",   dest="time",   help="sortieren nach Zeit und Sender [default: %(default)s]")
        parser.add_argument("-tf", "--time",   dest="time",   help="sortieren nach Zeit und Format [default: %(default)s]")
        parser.add_argument("-fs", "--format", dest="format", help="sortieren nach Format und Sender [default: %(default)s]")
        parser.add_argument("-ft", "--format", dest="format", help="sortieren nach Format und Zeit [default: %(default)s]")
        parser.add_argument("-stf", "--sender", dest="sender", help="sortieren nach Sender, Zeit und Format [default: %(default)s]")
        parser.add_argument("-sft", "--sender", dest="sender", help="sortieren nach Sender, Format und Zeit [default: %(default)s]")
        parser.add_argument("-tsf", "--time",   dest="time",   help="sortieren nach Zeit, Sender und Format [default: %(default)s]")
        parser.add_argument("-tfs", "--time",   dest="time",   help="sortieren nach Zeit, Format und Sender [default: %(default)s]")
        parser.add_argument("-fst", "--format", dest="format", help="sortieren nach Format, Sender und Zeit [default: %(default)s]")
        parser.add_argument("-fts", "--format", dest="format", help="sortieren nach Format, Zeit und Sender [default: %(default)s]")
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')
        
        print("argv:")
        print(argv)
        print()
        # Process arguments
        args = parser.parse_args()
        print("args:")
        print(args)
        print()
        
        paths = args.paths
        verbose = args.verbose
        recurse = args.recurse
        inpat = args.include
        expat = args.exclude
        
        print()
        print()
        if type(args.include) is not None:
            print('args.include: "'+args.include+'"')
        else:
            print('args.include: ""')
        print()
        print()
        if type(args.exclude) is not None:
            print('args.exclude: "'+str(args.exclude)+'"')
        else:
            print('args.exclude: ""')
        
        if verbose > 0:
            print("Verbose mode on")
            if recurse:
                print("Recursive mode on")
            else:
                print("Recursive mode off")
        
        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")
        for inpath in paths:
            ### do something with inpath ###
            print(inpath)
            #mtsomof = source.mtsomofC()
            #mtsomof.run(inpath)
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'mtsomofa_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())