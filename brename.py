import os
import sys
import argparse

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(description='Bulk Rename: Find and replace text in file and directory names in the current directory.')
parser.add_argument('find', help="Text to find.")
parser.add_argument('replace', help="Text to replace.")
parser.add_argument('-q', '--quiet',
                    dest='quiet',
                    action='store_const',
                    const=True,
                    default=False,
                    help="Supresses text output.")
args = parser.parse_args()
dir_list = os.listdir(os.getcwd())

for x in dir_list:
    if x.find(args.find) != -1:
        try:
            os.rename(x, x.replace(args.find, args.replace))
            if args.quiet == False:
                print "Renamed "+x+" to "+x.replace(args.find, args.replace)
        except WindowsError, err:
            if args.quiet == False:
                print 'Couldn\'t rename "'+x+'": '+str(err)
