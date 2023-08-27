"""Consume courses api."""

import requests

username = "tester"
password = "tester"
base_url = 'http://127.0.0.1:8000/api/'

# Retrieve all courses
retrieve = requests.get(f'{base_url}courses/', timeout=4)
courses = retrieve.json()
available_courses = ', '.join(
    [course['title'] for course in courses]
)
print(f"Available courses: {available_courses}")

for course in courses:
    course_id = course['id']
    course_title = course['title']
    res = requests.post(
        f"{base_url}courses/{course_id}/enroll/",
        auth=(username, password),
        timeout=4
    )

    if res.status_code == 200:
        # Successful enrollment
        print(f"Successfully enrolled in {course_title}")
    print("Wrong username or password")
