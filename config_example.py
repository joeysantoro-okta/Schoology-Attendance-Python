KEY='KEY HERE'
SECRET='SECRET HERE'

SCHOOL_ID='SCHOOL ID HERE'

SCHOOLOGY_URL='https://api.schoology.com/v1/'
USERS_URL=SCHOOLOGY_URL + 'users/'
SCHOOLS_URL = SCHOOLOGY_URL + 'schools/' + SCHOOL_ID
COURSES_URL = SCHOOLOGY_URL + 'courses/'
SECTION_LIST_URL = COURSES_URL + '{}/sections/'
SECTION_VIEW_URL = SCHOOLOGY_URL + '/sections/'
USER_SECTIONS_URL = USERS_URL + '{}/sections/'
ATTENDANCE_URL= SECTION_VIEW_URL + '{}/attendance'