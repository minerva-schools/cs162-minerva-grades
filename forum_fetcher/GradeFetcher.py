import requests
from web.serve import db, Hc, HcGrade, Lo, LoGrade
#from datetime import datetime
import dateutil.parser

class GradeFetcher():
    def __init__(self, session):
        self._cookie = dict(sessionid=session)
        self.api_base = "https://forum.minerva.kgi.edu/api/v1/"

    def get_url(self, url):
        """Helper Function to get Forum data"""
        r = requests.get(self.api_base + url, cookies=self._cookie)
        assert r.status_code == 200, "Forum request not successful"
        return r.json()

    def db_commit(self):
        """Helper Function to commit to database and rollback if it fails, then re-raise the error"""
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

class HcFetcher(GradeFetcher):
    def __init__(self, session):
        super().__init__(session)

    def get_grades(self):
        # Get mean HC grades
        hc_means_raw = self.get_url("outcome-index-items?outcomeType=hc")
        # Transform into a dictionary for O(1) lookups
        hc_means = {}
        for hc in hc_means_raw:
            if "hc-item" in hc:
                hc_means[hc["hc-item"]] = hc["mean"]
        hc_tree = self.get_url("hc-trees/current?tree")
        for hc_group1 in hc_tree.get("hc-group-nodes", []):
            for hc_group2 in hc_group1.get("hc-group-nodes", []):
                for leaf_node in hc_group2.get("hc-leaf-nodes", []):
                    hc = leaf_node["hc-item"]
                    new_hc = Hc(hc_id=hc["id"], user_id=self._cookie["sessionid"], name=hc["name"],
                                description=hc["description"], course=hc["cornerstone-code"], mean=hc_means[hc["id"]])
                    db.session.add(new_hc)
                    self.get_grade(hc["id"])
        return self.db_commit()

    def get_grade(self, hc_id):
        grades_data = self.get_url("outcomeindex/performance?hc-item=" + str(hc_id))
        for grade in grades_data:
            time = dateutil.parser.parse(grade["created-on"])
            new_grade = HcGrade(grade_id=grade["id"],hc_id=hc_id, user_id=self._cookie["sessionid"],
                                score=grade["score"], weight=grade["weight"], time=time,
                                assignment=(grade["type"] == "assignment"), transfer=None)
            db.session.add(new_grade)
        return self.db_commit()


class LoFetcher(GradeFetcher):
    def __init__(self, session):
        super().__init__(session)

    def get_grades(self):
        endpoint = "terms/with-lo-trees"
        terms_list = self.get_url(endpoint)
        terms = [term["id"] for term in terms_list]
        grades = {}
        for term in terms:
            lo_tree = self.get_url("terms/" + str(term) + "/lo-trees")
            for course in lo_tree:
                for co in course["course-objectives"]:
                    for lo in co["learning-outcomes"]:
                        mean = self.get_url("outcome-index-item?learning-outcome=" + str(lo["id"]))["mean"]
                        new_lo = Lo(lo_id=lo["id"], user_id=self._cookie["sessionid"], name=lo["name"],
                                    description=lo["description"], term=term, co_id=co["id"], co_desc=co["description"],
                                    course=course["course"]["course-code"], mean=mean)
                        db.session.add(new_lo)
                        self.get_grade(lo["id"])
        return self.db_commit()

    def get_grade(self, lo_id):
        grades_data = self.get_url("outcomeindex/performance?learning-outcome=" + str(lo_id))
        for grade in grades_data:
            time = dateutil.parser.parse(grade["created-on"])
            new_grade = LoGrade(grade_id=grade["id"], lo_id=lo_id, user_id=self._cookie["sessionid"],
                                score=grade["score"], weight=grade["weight"], time=time,
                                assignment=(grade["type"] == "assignment"))
            db.session.add(new_grade)
        return self.db_commit()
