import os
import sys
import argparse
import sqlite3
dbpath = os.path.dirname(os.path.realpath(__file__)) + '\chimpcom.db'
db = sqlite3.connect(dbpath);
cur = db.cursor()

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(description='Show items in the database.')
parser.add_argument('word', help="Word to look up.")
parser.add_argument('-p','--public',
                    dest='public',
                    action='store_const',
                    const=True,
                    default=False,
                    help="Show public memories?")
args = parser.parse_args()

data = (args.word, )

for memory in cur.execute('''SELECT content, user_id, public FROM memory_items WHERE name = ?''', data):
    print memory[0]
