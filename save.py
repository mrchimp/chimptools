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

parser = MyParser(description='Save an item to the database.')
parser.add_argument('word', help="Word to attach text to.")
parser.add_argument('content', nargs="+", help="Text to save.")
parser.add_argument('-p','--public',
                    dest='public',
                    action='store_const',
                    const=True,
                    default=False,
                    help="Is memory public?")
args = parser.parse_args()


args.content = ' '.join(args.content)

data = (str(args.word), args.content, "1", args.public, )
result = cur.execute('''INSERT INTO memory_items
            (name, content, user_id, public)
            VALUES
            (?,?,?,?)''', data)

db.commit()

if result:
    print 'Ok.'
else:
    print 'Nope.'
