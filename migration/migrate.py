import sqlite3
import logging
import csv

conn = sqlite3.connect('./data/database.sqlite')
conn.row_factory = lambda c, r: dict(sqlite3.Row(c, r))
cur = conn.cursor()

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-7s] %(message)s')

with open('./data/students.csv', encoding='utf-8') as csvfile:
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
not_mapped = old_users_count - (total + len(not_found))
logging.info('Old database contains %s more users not in the list of students', not_mapped)

with open('data/output.csv', 'w', encoding='utf-8', newline='') as file:
	writer = csv.DictWriter(file, fieldnames=['full_name', 'email', 'points'], delimiter=',')
	writer.writeheader()
	writer.writerows(new_users)

with open('data/not_found.txt', 'w') as file:
	file.writelines(map(lambda s: s + '\n', not_found))

logging.info('Data written to file')

cur.close()
conn.close()
