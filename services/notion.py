import requests

from constants import NOTION_API_KEY


class Notion:
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
    }
    filters = {}

    @staticmethod
    def _add_activities_to_courses(courses: dict, raw_activities: dict):
        for course in courses:
            for activity in course["activities"]:
                block_activity = {}
                for i in raw_activities["results"]:
                    if i["id"] == activity["id"]:
                        block_activity = i
                activity.update(
                    {
                        "id": block_activity["id"],
                        "name": block_activity["properties"]["Name"]["title"][0][
                            "text"
                        ]["content"],
                        "status": block_activity["properties"]["Status"]["status"]["name"]
                    }
                )

    def get_courses(self):
        self.filters = {"and": [{"property": "term", "contains": "16-01-2024"}]}
        res = self.post("databases", "25df7cda-23dc-4da5-a494-8ef1f6384a05")
        # print(res["results"])
        courses = [
            {
                "name": course["properties"]["Name"]["title"][0]["text"]["content"],
                "activities": course["properties"]["Activities"]["relation"],
            }
            for course in res["results"]
            if course["properties"]["term"]["rich_text"][0]["text"]["content"]
            == "16-01-2024"
        ]
        raw_activities = self.post("databases", "6bcbf3fd-8130-48e6-b302-37c6ce8b3ff2")

        self._add_activities_to_courses(courses, raw_activities)
        
        return courses

    def post(self, type, id):
        url = f"https://api.notion.com/v1/{type}/{id}/query"
        kwargs = {}
        if self.filters != {}:
            kwargs["data"] = self.filters

        return requests.post(url=url, headers=self.headers, **kwargs).json()
