from config import *
from pprint import pprint
from requests_oauthlib import OAuth1Session
import json

all_limit = 200 

def main():
	get(SCHOOLS_URL)

def get(url, parameters={}, start=None, limit=None):
	if start is not None:
		parameters['start'] = start
	if limit is not None:
		parameters['limit'] = limit
	client = getClient()
	r = client.get(url, params=parameters)
	if r.status_code != 200:
		return 'Unexpected error, {}'.format(r.status_code)
	return r.json()

def getClient():
	return OAuth1Session(KEY, SECRET, None, None)

## 493 courses
def fetchCourses(start=0):
	return get(COURSES_URL, start=start, limit=all_limit)

def fetchAllCourses():
	resp = fetchCourses()
	courses = resp['course']
	links = resp['links']
	i = all_limit
	while 'next' in links:
		resp = fetchCourses(i)
		courses += resp['course']
		links = resp['links']
		i+=all_limit
	return courses

def fetchUsers(start=0):
	return get(USERS_URL, start=start, limit=all_limit)

def fetchCourseSections(course_id):
	# , parameters={'include_past': '1'}
	return get(SECTION_LIST_URL.format(course_id), start=0)

## TODO: make sure links has no 'next'
def fetchAllSections():
	ret = []
	courses = fetchAllCourses()
	course_ids = [c['id'] for c in courses]
	for course in course_ids:
		sections = fetchCourseSections(course)
		if sections['total'] > 0:
			ret += sections['section']
	return ret

## caching
## cat active_courses.json | jq 'map(.title + ":" + ((.sections | length)  | tostring))'
## cat active_courses.json | jq 'keys'
## cat active_courses.json | jq 'map(.sections | map(.id)) | flatten'
## visualize statuses
## cat all_attendance.json | jq 'map(.totals.total | map(.status)) | flatten | unique'
## count all occurences of status
## cat all_attendance.json | jq 'map(.totals.total ) | flatten | map(select(.status==4)) | map(.count) | add'

def refreshActiveCourses():
	data = {} ## key is course id
	## value is {title, code, sections[]}
	### section design {id, title, code}
	sections = fetchAllSections()
	for sect in sections:
		cid = sect['course_id']
		if cid not in data:
			data[cid] = {
				'title' : sect['course_title'],
				'code' : sect['course_code'],
				'sections' : []
			}
		section_data = {
			'id' : sect['id'],
			'title' : sect['section_title'],
			'code' : sect['section_code']
		}
		data[cid]['sections'].append(section_data)

	with open('active_courses.json', 'w') as f:
		f.write(json.dumps(data))
	return 'Done'

def fetchSection(section_id):
	return get(SECTION_VIEW_URL + str(section_id))

def fetchUserSections(user_id):
	return get(USER_SECTIONS_URL.format(user_id))

def fetchAttendance(course_id):
	return get(ATTENDANCE_URL.format(course_id))

def getAllSectionIds():
	with open('active_courses.json') as f:
		data = json.loads(f.read())

	sections = []
	for i in data:
		sections += data[i]['sections']
	return [sect['id'] for sect in sections]

def fetchAllAttendance():
	ret = []
	section_ids = getAllSectionIds()
	for i in section_ids:
		attendance = fetchAttendance(i)
		pprint(attendance)
		ret.append(attendance)
		break
	return ret