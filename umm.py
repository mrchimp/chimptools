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
parser = MyParser(description='find items saved using the SAVE command')
parser.add_argument('search_term', help="Word to look for.")

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
args = parser.parse_args()



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
sql += '''\nAND ( memory_items.name LIKE :name 
            OR  memory_items.content LIKE :name )'''

if public_items == 'public':
    sql += '\nAND memory_items.public = 1 '
elif public_items == 'private':
    sql += '''\nAND memory_items.user_id = :user_id
              AND memory_items.public = 0 '''
elif public_items == 'mine':
    sql += '\nAND memory_items.user_id = :user_id '
else:
    sql += '''\n AND ( memory_items.user_id = :user_id
                  OR    memory_items.public  = 1 ) ''';

sql += '\nORDER BY memory_items.name, memory_items.id ';

# Construct data for db query
data = {"name": '%'+args.search_term+'%',
        "user_id": 1}

last_word = ''

print sql

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
