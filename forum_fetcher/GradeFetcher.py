import requests
import redis
class GradeFetcher():
    def __init__(self, session):
        self._cookie = dict(sessionid=session)
        self.api_base = "https://forum.minerva.kgi.edu/api/v1/"
    def get_url(self, url):
        return requests.get(self.api_base + url, cookies=self._cookie).json()

class HcFetcher(GradeFetcher):
    def __init__(self, session):
        super().__init__(session)

    def get_grades(self):
        hcs = {}
        hc_tree = self.get_url("hc-trees/current?tree")
        for hc_group1 in hc_tree["hc-group-nodes"]:
            if "hc-group-nodes" in hc_group1:
                for hc_group2 in hc_group1["hc-group-nodes"]:
                    for leaf_node in hc_group2["hc-leaf-nodes"]:
                        hc = leaf_node["hc-item"]
                        mean = self.get_url("outcome-index-items?outcomeType=hc?hc-item=" + str(hc["id"])).get("mean", None)
                        hcs[hc["id"]] = {"name": hc["name"], "description": hc["description"],
                                         "cornerstone": hc["cornerstone-code"], "mean": mean}
                        self.get_grade(hc["hc-item"])
    def get_grade(self, id):
        grades_data = self.get_url("outcomeindex/performance?hc-item=" + str(id))
        hc_grades = []
        for grade in grades_data:
            grade_id = grade["id"]
            score = grade["score"]
            assignment = grade["type"] == "assignment"
            date = grade["created-on"]
            weight = grade["weight"]
            hc_grades.append({"id": grade_id, "lo_id": id, "score": score})
        return hc_grades


class LoFetcher(GradeFetcher):
    def __init__(self, session):
        super().__init__(session)
    def get_grades(self):
        endpoint = "terms/with-lo-trees"
        terms_list = self.get_url(endpoint)
        terms = [term["id"] for term in terms_list]
        los = {}
        grades = {}
        for term in terms:
            lo_tree = self.get_url("terms/" + str(term) + "/lo-trees")
            for course in lo_tree:
                course_name = course["course"]["course-code"]
                for co in course["course-objectives"]:
                    co_id = co["id"]
                    co_desc = co["description"]
                    for lo in co["learning-outcomes"]:
                        lo_id = lo["id"]
                        lo_name = lo["name"]
                        lo_desc = lo["description"]
                        mean = self.get_url("outcome-index-item?learning-outcome=" + str(lo_id))["mean"]
                        los[lo["id"]] = {"name": lo_name, "description": lo_desc,
                                "course": course_name, "co_id": co_id, "co_desc": co_desc, "mean": mean}
                        grades[lo["id"]] = self.get_grade(lo["id"])

        return los, grades

    def get_grade(self, id):
        grades_data = self.get_url("outcomeindex/performance?learning-outcome=" + str(id))
        lo_grades = []
        for grade in grades_data:
            grade_id = grade["id"]
            score = grade["score"]
            assignment = grade["type"] == "assignment"
            date = grade["created-on"]
            weight = grade["weight"]
            lo_grades.append({"id": grade_id, "lo_id": id, "score": score})
        return lo_grades
