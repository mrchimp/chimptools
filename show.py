#!/usr/bin/env python

import os
import sys
import argparse
import sqlite3

# Set up database connection
dbpath = os.path.dirname(os.path.realpath(__file__)) + '\chimpcom.db'
db = sqlite3.connect(dbpath);
c = db.cursor()

# On errors show help and exit
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# Set up some arguments
parser = MyParser(description='show items stored using the SAVE command')
mutual_args = parser.add_mutually_exclusive_group()
mutual_args.add_argument('-w','--words',
                        dest='words',
                        action='store_const',
                        const=True,
                        default=False,
                        help="show a list of saved words.")
mutual_args.add_argument('word', nargs="?", help="Word to look up.")

parser.add_argument('filter', nargs="?", help="Filter word[s].")

pubpriv = parser.add_mutually_exclusive_group()
pubpriv.add_argument('-u','--public',
                        dest='public',
                        action='store_const',
                        const=True,
                        default=False,
                        help="show public memories")
pubpriv.add_argument('-r','--private',
                        dest='private',
                        action='store_const',
                        const=True,
                        default=False,
                        help="show private memories")
parser.add_argument('-m','--mine',
                        dest='mine',
                        action='store_const',
                        const=True,
                        default=False,
                        help="show only memories saved by you - public or private")
parser.add_argument('-d','--distinct',
                        dest='distinct',
                        action='store_const',
                        const=True,
                        default=False,
                        help="show one memory per word")
args = parser.parse_args()



# -w Show list of words
if args.words:
    for row in c.execute('''SELECT DISTINCT name FROM memory_items'''):
        print row[0]
    sys.exit()


if args.public:
    public_items = 'public'
elif args.private:
    public_items = 'private'
elif args.mine:
    public_items = 'hide'
else:
    public_items = 'both'


# Get memories
sql = '''SELECT  memory_items.id      as id, 
                 memory_items.name    as name, 
                 memory_items.content as content,
                 memory_items.public  as public,
                 users.id             as user_id,
                 users.username       as username
         FROM    memory_items,
                 users
         WHERE   memory_items.user_id = users.id '''

showall = False
if args.word and args.word != '*' and args.word != 'all':
    showall = True
    sql += '\nAND memory_items.name = :name '

if public_items == 'public':
    sql += '\nAND memory_items.public = 1 '
elif public_items == 'private':
    sql += '''\nAND memory_items.user_id = :user_id
              AND memory_items.public = 0 '''
elif public_items == 'mine':
    sql += '\nAND memory_items.user_id = :user_id '
else:
    sql += '''\nAND ( memory_items.user_id = :user_id
              OR    memory_items.public  = 1 ) ''';

if args.filter:
    args.filter = '%' + args.filter + '%'
    sql += '\nAND memory_items.content LIKE :search_str '

sql += '\nORDER BY memory_items.name, memory_items.id ';

if args.distinct:
    sql += '\nGROUP BY memory_items.name '

# Construct data for db query
data = {"name": args.word,
        "search_str": args.filter,
        "user_id": 1}

last_word = ''


c.execute(sql, data)
memories = c.fetchall()

if not memories:
    print 'No memories found.'
else:
    for memory in memories:
        try:
            if last_word != memory[1]:
                print '\n\n=== ' + memory[1] + ' ==='
            print memory[2]
            last_word = memory[1]
        except UnicodeEncodeError:
            print "unicode error"
