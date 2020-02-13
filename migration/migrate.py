import argparse
import sqlite3
import logging
import json
import csv
import os

import psycopg2, psycopg2.extras


parser = argparse.ArgumentParser(description='Match accounts from the old database to current student emails')
parser.add_argument('--sqlite_db', default='./data/database.sqlite', help='Path to the SQLite db file')
parser.add_argument('--students', default='./data/students.csv', help='Path to the csv file with students info')
parser.add_argument('--outfolder', default='./data/', help='Path to the folder where output files will be placed')
parser.add_argument('db_url', nargs='?', default=None, help='Connection URL to the target Postgres DB')

args = parser.parse_args()

conn = sqlite3.connect(args.sqlite_db)
conn.row_factory = lambda c, r: dict(sqlite3.Row(c, r))
cur = conn.cursor()

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-7s] %(message)s')

os.makedirs(args.outfolder, exist_ok=True)
with open(args.students, encoding='utf-8') as csvfile:
	reader = csv.DictReader(csvfile)
	students = list(reader)
	logging.info('Loaded database of current students (count: %s)', len(students))

cur.execute('SELECT COUNT(*) AS count FROM User')
old_users_count = cur.fetchone()['count']
logging.info('Old database has %s users', old_users_count)

new_users = []
not_found = []
total = 0
for student in students:
	username, extension = student['email'].split('@', 1)
	cur.execute('SELECT first_name, last_name, points FROM User WHERE email LIKE ?', (f'{username}@innopolis.%',))
	result = cur.fetchone()

	if result == None:
		logging.warning('Cannot find an account for "%s" (%s)', student['full_name'], student['email'])
		not_found.append(student['email'])
		continue
	logging.debug('Found user "%s" (%s) with %s points', student['full_name'], student['email'], result['points'])
	total += 1

	# Don't bother if has no points
	if result['points'] == 0:
		continue

	new_users.append({
		'email': student['email'],
		'full_name': result['first_name'] + ' ' + result['last_name'],
		'points': result['points'],
	})

logging.info('Account mapping completed.')
logging.info('Mapped %s accounts. Ignored %s accounts with no points. Did not find old accounts for %s students.',
				len(new_users), total - len(new_users), len(not_found))
not_mapped = old_users_count - total
logging.info('Old database contains %s more users not in the list of students', not_mapped)

with open(os.path.join(args.outfolder, 'accounts.csv'), 'w', encoding='utf-8', newline='') as file:
	writer = csv.DictWriter(file, fieldnames=['full_name', 'email', 'points'], delimiter=',')
	writer.writeheader()
	writer.writerows(new_users)

if len(not_found) > 0:
	with open(os.path.join(args.outfolder, 'not_found_emails.txt'), 'w') as file:
		file.writelines(map(lambda s: s + '\n', not_found))

logging.info('Data written to file(s)')

cur.close()
conn.close()

if args.db_url is not None:
	logging.info('Writing to target database')
	conn = psycopg2.connect(args.db_url)
	cur = conn.cursor()
	default_notification_settings = json.dumps({
		'innostore': 'off',
		'volunteering': 'off',
		'project_creation': 'off',
		'administration': 'off',
		'service': 'email',
	})
	psycopg2.extras.execute_values(
			cur, 
			'INSERT INTO accounts (full_name, email, is_admin, notification_settings) VALUES %s',
			new_users,
			template=f"(%(full_name)s, %(email)s, false, '{default_notification_settings}')",
	)
	logging.debug('Accounts created')
	psycopg2.extras.execute_values(
			cur, 
			'INSERT INTO transactions (account_email, change) VALUES %s',
			new_users,
			template=f"(%(email)s, %(points)s)",
	)
	logging.debug('Transactions created')
	conn.commit()
	cur.close()
	conn.close()
	logging.info('Points added successfully')
