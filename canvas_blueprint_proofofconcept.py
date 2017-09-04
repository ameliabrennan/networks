# Proof of concept for automating Canvas Blueprint associations
# August 25th 2017
# Sarah, Marcus, David, with help from Sam with tokens
# Able to send API request to Canvas to associate a template course with multiple associated courses
# Proof of concept that the associations do not need to be manual and with the GUI, when scaling up 

import requests

# Sarah's token generated August 25th
canvas_token = '9595~sq973vfs23ahbdOUoLPObzFHAmSYxEMRKC0PVYRBHT7OH9q1RByxwBXsJbGkAndM'


#### EXAMPLE 1: a hard-coded request for one template course, one association
request_string_example = "https://rmit.instructure.com:443/api/v1/courses/20438/blueprint_templates/default/update_associations?course_ids_to_add=27977"
authentication_string = "&access_token=" + canvas_token
request_string = request_string_example + authentication_string

print("\nTrying single example")
print("Attempting API request: ")
print(request_string)
result = requests.put(request_string)
print(result)

if (result.status_code == 200):
    result_String = str(result.content)
    print(result_String)
    print("Success!")
else:
    print("Booh!")


##### EXAMPLE 2: looping through multiple association courses with a single template course

# Components of the generic request string
request_string_part1 = "https://rmit.instructure.com:443/api/v1/courses/"
request_string_part2 = "/blueprint_templates/default/update_associations?course_ids_to_add="
authentication_string = "&access_token=" + canvas_token

# the template course
template_course = '20438'

# list of courses to associate with this template course
association_courses = ['27976', '27977', '27978']

print("\nLooping through template course associations for: ", template_course)

success_count = 0
for association_course in association_courses:
    print(association_course)
    print("Attempting API request:")
    request_string = request_string_part1 + template_course + request_string_part2 + association_course + authentication_string
    print(request_string)
    # ACTIONS ARE COMMENTED OUT NOW DURING TESTING
    result = requests.put(request_string)
    print(result)
    if (result.status_code == 200):
       success_count += 1
       result_String = str(result.content)
       print(result_String)
    else:
       print("Booh!")

print("\nSuccess count: %s" %success_count)