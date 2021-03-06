import requests, json, time, os.path
from subprocess import call
import dayonelib

journal_location = '<path to dayone journal>'

dayone = dayonelib.DayOne(journal_location)

config_file_path = os.path.join(os.path.expanduser("~"), '.todoistdayone')
with open(config_file_path, 'r') as cfg_file:
    config = json.load(cfg_file)

url = "https://todoist.com/API/v6/get_all_completed_items"

cur_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

if not config['lastrun']:
    config['lastrun'] = cur_time

post_data = {"token": config['token'],
             "annotate_notes": "true", "since": "2016-03-08T20:06:00"}

r = requests.post(url, post_data)

data = json.loads(r.text)

config['lastrun'] = cur_time

with open(config_file_path, 'w') as cfg_file:
    json.dump(config, cfg_file)

for task in data['items']:
    entry = dayonelib.DayOneEntry()

    project_id = task['project_id']
    api_time = time.strptime(task['completed_date'],
                    "%a %d %b %Y %H:%M:%S +0000")
    task_time = time.localtime(time.mktime(api_time) - time.altzone)

    notes = ""
    if task['notes']:
        notes = "\n## Notes:\n"
        for note in task['notes']:
            notes += "\n### %s\n    %s\n" % (note['posted'], note['content'])
    text = "%s @%s_project @done @todoist%s" % (task['content'],
            data['projects'][str(task['project_id'])]['name'].replace(' ', '_'), notes)

    entry.text = text
    entry.time = api_time
    entry.tz = "UTC"
    dayone.save(entry)
