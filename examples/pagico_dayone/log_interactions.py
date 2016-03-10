import sqlite3 as lite
from phpserialize import *
import time, os.path, re, uuid, plistlib
from datetime import datetime
from pprint import pprint as pp
import html2text, json
import CoreLocation
import sys
import arrow
import dayonelib

journal_location = '<path to dayone journal>'

dayone = dayonelib.DayOne(journal_location)


con = lite.connect('<path to pagico file>/database/main.db')

config_file_path = os.path.join(os.path.expanduser("~"), '.pagicodayone')
with open(config_file_path, 'r') as cfg_file:
    config = json.load(cfg_file)

cur_time = int(time.time())


if not config['lastrun']:
    print 'no cfg'
    print config['lastrun']
    config['lastrun'] = cur_time


with con:

    con.row_factory = lite.Row
    cur = con.cursor()
    note_query = 'SELECT * FROM mach WHERE Modified > %s AND Type="Text" AND Deleted IS NULL' % (config['lastrun'])
    cur.execute(note_query)
    config['lastrun'] = cur_time

    with open(config_file_path, 'w') as cfg_file:
        json.dump(config, cfg_file)

    rows = cur.fetchall()

    for row in rows:
        entry_date = row['Modified']

        entry = dayonelib.DayOneEntry()
        entry.time = entry_date
        entry.tags = ['pagico', 'interaction']

        # unseralize the body of the note
        row_content = loads(row['Content'])

        # entry body text
        entry_text = "%s" % (row_content['Body'])
        entry_text = html2text.html2text(entry_text)


        # entry title
        entry_title = row_content['Title']

        # All notes on a contact will have a parent. Skip anything without a parent
        if row["ParentID"] is not None:
            # Get contact info
            parent_query = 'SELECT * FROM mach WHERE UID="%s"' % (row['ParentID'])
            cur.execute(parent_query)
            parent = cur.fetchone()
            parent_content = loads(parent['content'])

            # Make sure the parent is a contact(type Profile)
            if parent['Type'] == 'Profile':
                # add contact tame as tag
                entry.add_tag(( "%s_%s" % (parent_content['firstName'], parent_content.get('lastName', ''))))

                entry.text = '# interaction: %s - %s\n\n%s' % (
                    entry_title, parent_content['Name'], entry_text)

                # @ tag syntax
                pat = re.compile(r"@(\w+)")
                inline_tags = pat.findall(entry_text)
                # pagico link syntax
                links = re.compile(r"\[(.*?)\]")
                inline_links = links.findall(entry_text)

                # add [links] in pagico as a tag in dayone
                for t in inline_links:
                    entry.add_tag(t.replace(" ", "_"))
                # add @tags in pagico to dayone
                for t in inline_tags:
                    entry.add_tag((t))

                dayone.save(entry, True)



