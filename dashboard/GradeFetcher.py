import requests
from dashboard.models import Lo, LoGrade, Hc, HcGrade
from dashboard import db
import dateutil.parser
import concurrent.futures
import re


class GradeFetcher():
    """Parent class that fetches grades from Forum"""

    def __init__(self, session):
        self._cookie = dict(sessionid=session)
        self.api_base = "https://forum.minerva.kgi.edu/api/v1/"

    def get_url(self, url):
        """Helper Function to get Forum data"""
        r = requests.get(self.api_base + url, cookies=self._cookie)
        assert r.ok, "Forum request not successful"
        return r.json()


class HcFetcher(GradeFetcher):
    def __init__(self, session):
        super().__init__(session)

    def get_grades(self):
        """Gets all HC grades, including granular assignment and class scores"""
        # Get mean HC grades
        hc_means_raw = self.get_url("outcome-index-items?outcomeType=hc")
        # Transform into a dictionary for O(1) lookups
        hc_means = {}
        for hc in hc_means_raw:
            if "hc-item" in hc:
                hc_means[hc["hc-item"]] = hc["mean"]

        # Get HCs. There's a bit of delving into the JSON structure here because it's messy
        urls = []
        hc_tree = self.get_url("hc-trees/current?tree")
        for hc_group1 in hc_tree.get("hc-group-nodes", []):
            for hc_group2 in hc_group1.get("hc-group-nodes", []):
                for leaf_node in hc_group2.get("hc-leaf-nodes", []):
                    hc = leaf_node["hc-item"]
                    urls.append(hc["id"])
                    new_hc = Hc(hc_id=hc["id"], user_id=self._cookie["sessionid"], name=hc["name"],
                                description=hc["description"], course=hc["cornerstone-code"], mean=hc_means[hc["id"]])
                    db.session.add(new_hc)
        
        # Add the grades to the database
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
            for grades in pool.map(self.get_grade, urls):
                if grades is not None:
                    db.session.add_all(grades)

    def get_grade(self, hc_id):
        """Fetches assignment and class grades for an HC"""
        grades_data = self.get_url("outcomeindex/performance?hc-item=" + str(hc_id))
        grades = []
        for grade in grades_data:
            time = dateutil.parser.parse(grade["created-on"])
            transferred = self.is_transferred(grade["hc-item"], grade)
            grades.append(HcGrade(grade_id=grade["id"], hc_id=hc_id, user_id=self._cookie["sessionid"],
                                  score=grade["score"], weight=grade["weight"], time=time,
                                  assignment=(grade["type"] == "assignment"), transfer=transferred))
        return grades

    def is_transferred(self, hc_id, grade):
        """Checks whether or not a grade is transferred by looking at its corresponding 'focused outcomes'"""
        if grade["type"] == "assignment":
            assignment = self.get_url("assignments/{}/nested_for_detail_page".format(grade["assignment-id"]))
            # Creates a list of foregrounded HCs from the json structure
            foregrounded = [focused_hc.get("hc-item").get("id") for focused_hc in assignment.get("focused-outcomes", [])
                            if focused_hc.get("hc-item") is not None]
            return hc_id not in foregrounded
        else:
            grade_class = self.get_url("classes/{}/class_edit_page".format(
                grade["klass-id"]))
            # Creates a list of foregrounded HCs from the json structure
            foregrounded = [focused_hc.get("hc-item").get("id") for focused_hc in
                            grade_class["assessment"].get("focused-outcomes", [])
                            if focused_hc.get("hc-item") is not None]
            return hc_id not in foregrounded


class LoFetcher(GradeFetcher):
    def __init__(self, session):
        super().__init__(session)

    def get_grades(self):
        """Gets all LO grades, including granular assignment and class scores"""
        terms_list = self.get_url("terms/with-lo-trees")
        terms = [term["id"] for term in terms_list]
        urls = []
        valid_courses = re.compile('((CS|NS|B|AH|SS|CP)1)|IL181')
        for term in terms:
            # Get mean LO grades
            lo_means_raw = self.get_url("outcome-index-items?termId={}&outcomeType=lo".format(str(term)))
            # Transform into a dictionary for O(1) lookups
            lo_means = {}
            for lo in lo_means_raw:
                if "learning-outcome" in lo:
                    lo_means[lo["learning-outcome"]] = lo["mean"]
            lo_tree = self.get_url("terms/" + str(term) + "/lo-trees")
            # fetches information for every LO in the term
            for course in lo_tree:
                for co in course["course-objectives"]:
                    if valid_courses.match(course["course"]["course-code"]) is not None:
                        for lo in co["learning-outcomes"]:
                            urls.append(lo["id"])
                            new_lo = Lo(lo_id=lo["id"], user_id=self._cookie["sessionid"], name=lo["name"],
                                        description=lo["description"], term=term, co_id=co["id"],
                                        co_desc=co["description"],
                                        course=course["course"]["course-code"], mean=lo_means[lo["id"]])
                            db.session.add(new_lo)
        # Fetches individual LO grades
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
            for grades in pool.map(self.get_grade, urls):
                if grades is not None:
                    db.session.add_all(grades)

                    
    def get_grade(self, lo_id):
        """Checks whether or not a grade is transferred by looking at its corresponding 'focused outcomes'"""
        grades_data = self.get_url("outcomeindex/performance?learning-outcome=" + str(lo_id))
        grades = []
        for grade in grades_data:
            time = dateutil.parser.parse(grade["created-on"])
            grades.append(LoGrade(grade_id=grade["id"], lo_id=lo_id, user_id=self._cookie["sessionid"],
                                  score=grade["score"], weight=grade["weight"], time=time,
                                  assignment=(grade["type"] == "assignment")))
        return grades
