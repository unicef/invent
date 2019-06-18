import requests

number_of_users = 100

# base_url = "http://test.whomaps.pulilab.com/api"
base_url = "http://192.168.99.100/api"

username_pattern = "test_user{}@example.com"
user_data = {"email": "", "password1": "123456hetNYOLC", "password2": "123456hetNYOLC"}

organisation_pattern = "Test Organisation{}"
profile_data = {"name": "Test User", "organisation": "Test Organisation", "country": "Test Country"}

project_pattern = "Test Project{}"
project_data = {
    "date": "2016-5-16T11:00:00.481197",
    "name": "",
    "organisation": "",
    "strategy": [],
    "country": 1,
    "technology_platforms": [],
    "licenses": [],
    "application": [],
    "coverage": [],
    "started": "2016-5-16T11:00:00.481197",
    "donors": [],
    "reports": [],
    "publications": [],
    "pipeline": [],
    "goals_to_scale": "Test",
    "anticipated_time": "Test",
    "pre_assessment": [0, 0, 0, 0, 0, 0]
}

# Based on actual test.whomaps.pulilab.com (2015-05-17)
countries = [
    "philippines", "sierra-leone", "kenya", "india", "bangladesh", "senegal", "malawi", "tunisia", "pakistan",
    "indonesia"
]


def generate_users():
    for x in range(1, number_of_users):
        # Register user
        user_data.update(email=username_pattern.format(x))
        response = requests.post(base_url + "/rest-auth/registration/", json=user_data)
        # print(response.status_code)

        headers = {"Authorization": "Token {}".format(response.json().get("key"))}

        # Creates profile
        profile_data.update(organisation=organisation_pattern.format(x))
        response = requests.post(base_url + "/userprofiles/", json=profile_data, headers=headers)
        # print(response.status_code)

        # Adds empty project
        # WARNING: links to countries based on simple math, there must be countries with IDs 1 to 10
        project_data.update(
            name=project_pattern.format(x), organisation=organisation_pattern.format(x), country=(x % 10) + 1)
        response = requests.post(base_url + "/projects/", json=project_data, headers=headers)
        # print(response.status_code)

        # Ugly log for copying account details from terminal
        print(username_pattern.format(x) + ", 123456, " + project_pattern.format(x) + " (" + countries[(x % 10)] + ")")


if __name__ == "__main__":
    generate_users()
