#python
import psycopg2
import re
import requests
from tqdm import tqdm
tqdm.monitor_interval = 0




class class_list:

    def __init__(self):
        self.final_list = {}
        self.rarity_list = {}
        self.unlocks_list = {}
        self.score_list = {}
        self.class_tree = { 'CSC 402': ['CSC 401'], 'CSC 403': ['CSC 402'], 'CSC 406': ['CSC 401'],'CSC 407': [('CSC 406', 'CSC 402')],'CSC 421': [('CSC 400', 'CSC 403')],
                            'HCI 421': ['HCI 406'], 'HCI 422': ['HCI 440'], 'IS 422' : [('IS 421', 'CSC 451')],'CSC 423': ['IT 403'],'CSC 424'  : ['CSC 423'],'CSC 425': [('CSC 423', 'MAT 456')],
                            'GAM 425': ['CSC 403'], 'GAM 427': ['GAM 426'], 'SE 430' : ['CSC 403'],'HCI 430': ['IT 411', 'HCI 440', 'HCI 441'],'TDC 431': ['TDC 405'],
                            'CSC 431': ['CSC 401'],'SE 433' : ['CSC 403'], 'CSC 433': [['IT 403', 'CSC 401', 'IT 411']], 'CSC 435': [('CSC 403', 'CSC 407')], 'IS 435' : ['IS 421', 'SE 430'],
                            'GPH 436': [('CSC 393', 'MAT 150')],'CSC 436': [('CSC 435', 'CSC 447')], 'GPH 438': [['GPH 425', 'GPH 469']], 'CSC 438': ['CSC 407'],'CSC 439': ['CSC 407'],
                            'CSC 440': ['CSC 403'],'SE 441': ['CSC 403'],'HCI 441': ['CSC 403'],'GEO 442': ['GEO 441'], 'CSC 443': [('CSC 403', 'CSC 407')], 'CSC 444': [('CSC 400', 'CSC 403')],
                            'GEO 445': ['GEO 441'], 'HCI 445': [('IT 403',  ['HCI 440', 'HCI 441'])],'GEO 446': ['GEO 441'],'GEO 447': ['GEO 441'],'CSC 447': [('CSC 403', 'CSC 406')],
                            'CSC 448': ['CSC 447'],'SE 450': ['CSC 403'],'GAM 450': [('CSC 461', ['SE 456', 'SE 450'])],'HCI 450': ['IT 403'],'SE 452' : ['CSC 403'],
                            'CSC 452': [(['CSC 453', 'CSC 451', 'CSC 455'], ['CSC 401', 'IT 411'])],
                            'CSC 453': ['CSC 403'],'SE 453' : ['SE 452'],'GAM 453': [('CSC 461', ['SE 456', 'SE 450'])],'CSC 454': [['CSC 451', 'CSC 453', 'CSC 455']],
                            'HCI 454': [('HCI 406', ['HCI 440', 'HCI 441'])],'CSC 455': ['CSC 401'],
                            'SE 456' : ['CSC 403'],'IS 456' : ['IS 421'],'SE 457' : [['SE 450', 'CSC 435']],'CSC 457': ['CSC 403'],'CSC 458': ['CSC 403'],'SE 459' : ['SE 450'],
                            'TDC 460': [('TDC 405', 'TDC 413')],
                            'HCI 460': [('IT 403', ['HCI 440', 'HCI 441'])],'CSC 461': [('CSC 400', 'CSC 403', 'CSC 406')],'CSC 462': [['GAM 491', 'CSC 461']],
                            'TDC 463': [('TDC 405', 'TDC 413')],'TDC 464': ['TDC 413'],
                            'CSC 465': [('IT 403', ['CSC 40', 'IT 411'])],'IS 467' : ['IT 403', 'CSC 423'],'SE 468' : [('IT 403', ['SE 430', 'SE 450'])],'TDC 468': [(['TDC 463', 'CSC 435'], 'CSC 404')],
                            'GPH 469': [('CSC 461', ['GAM 425', 'GPH 436'])],'GAM 470': [('GAM 425', 'CSC 461')],'HCI 470': [('HCI 402', 'HCI 406')],
                            'CSC 471': [('CSC 403', 'CSC 407')],'CSC 472': [('CSC 403', 'CSC 407')],
                            'GAM 475': [('CSC 461', ['SE 456', 'SE 450'])],'CSC 475': ['CSC 407'],'SE 475' : ['CSC 403'],'GAM 476': [['CSC 461', 'SE 456', 'SE 450']],
                            'TDC 477': [['TDC 463', 'CSC 435']],'CSC 478': [('IS 467', 'CSC 401')],
                            'SE 480' : ['SE 450'],'CSC 480': ['CSC 403'],'CSC 481': ['CSC 412'],'CSC 482': ['CSC 481'],'TDC 484': ['TDC 413'],'IS 485' : [['IS 422', 'IS 430']],'GAM 486': ['CSC 471'],
                            'CSC 486': [('CSC 461', ['SE 456', 'SE 450'])],'CSC 489': [['CSC 444', 'CSC 421']],'SE 491' : ['SE 450'], 'GEO 491': ['GEO 441'], 'CSC 495': ['CSC 423'],
                            'IS 500': [['IS 430', 'SE 477']],'CSC 503': ['CSC 421'],'IS 506': ['IS 505'],'HCI 511': ['HCI 445'],'SE 511': [['SE 450', 'SE 430', 'IS 430']],
                            'TDC 511': [('TDC 411', 'TDC 460', 'TDC 463')], 'TDC 512': ['TDC 464'],'HCI 512': [('IT 403', 'HCI 470')],'HCI 513': ['IS 422', 'HCI 430'],
                            'HCI 514': [('HCI 445', 'HCI 460')],'TDC 514': [('TDC 463', 'TDC 464')],'HCI 515': [('HCI 445', 'HCI 454', 'HCI 430')],'HCI 520': [('IT 403', ['HCI 440', 'HCI 441', 'HCI 450'])],
                            'CSC 521': [(['CSC 402', 'CSC 404'], 'CSC 423')],'HCI 522': ['HCI 460'],'CSC 525': ['CSC 421'],'SE 525' : [['CSC 435', 'SE 450']],'SE 526' : ['CSC 435'],
                            'CSC 528': ['CSC 481'],'CSC 529': [('CSC 424', ['IS 467', 'ECT 584', 'CSC 578'])],'SE 529' : [('IT 403', 'SE 430')], 'HCI 530': ['HCI 454'],'CSC 531': [('CSC 421', 'SE 450')],
                            'TDC 532': ['TDC 512'],'SE 533' : ['SE 450'],'CSC 534': ['SE 450'],'IS 535' : [['SE 477', 'IS 565', 'IS 430']],'CSC 535': ['CSC 447'],'CSC 536': ['CSC 435'],
                            'GPH 536': ['GPH 469', 'GAM 470'],'CSC 538': ['CSC 528'],'CSC 540': ['CSC 471'],'TDC 542': ['TDC 512'],'CSC 543': [['CSC 453', 'CSC 455']],
                            'SE 546' : ['SE 450'],'CSC 548': ['CSC 448'],'IS 549' : [['CSC 451', 'CSC 453', 'CSC 455']],'CSC 549': ['CSC 453'],'CSC 550': ['CSC 453'],
                            'IS 550' : [['CSC 451', 'CSC 453', 'CSC 455']],'CSC 551': [('CSC 453',  ['CSC 435', 'TDC 405', 'TDC 463'])],'CSC 552': [('SE 450', 'CSC 407')],'CSC 553': ['CSC 453'],
                            'HCI 553': ['HCI 454'],'SE 554' : [['SE 450', 'SE 452']],'CSC 554': [['CSC 453', 'CSC 454']],'CSC 555': [('CSC 401',  'CSC 453')],
                            'IS 556': ['IS 430'],'SE 556': [('SE 456', 'CSC 407')],
                            'CSC 557': ['CSC 439'],'CSC 559': [('CSC 404', ['CSC 431', 'CSC 521', 'CSC 425'])],'SE 560': [['SE 450', ('CSC 301', 'SE 430')]],'TDC 560': ['TDC 460', 'TDC 463'],
                            'TDC 562': ['TDC 463'],'TDC 563': ['TDC 463'],'TDC 567': ['TDC 463'],'TDC 568': ['TDC 463'],'GPH 570': [['GPH 469', 'GAM 470']],'IS 570': ['IS 430'],
                            'IS 574': [(['SE 430', 'IS 435', 'MIS 674'], 'CSC 451')],'GAM 575': ['GAM 475'],'CSC 575': ['CSC 403'],'GPH 575': [('GPH 448', ['GPH 469', 'GAM 470'])],'GAM 576': ['GAM 575'],
                            'CSC 576': [['IS 467', 'CSC 478', 'ECT 584']],'CSC 577': [('SE 450', ['IS 467', 'CSC 478', 'ECT 584'])],
                            'TDC 577': ['TDC 477'],'CSC 578': [[('CSC 412', 'CSC 478'), ('CSC 403', 'IS 467')]],
                            'IS 579': ['IS 430'],'SE 579': ['SE 450'],'CSC 580': ['SE 450'],'HCI 580': [('HCI 445', 'HCI 454')],
                            'GPH 580': [('GPH 469', 'GAM 470')],'SE 582': [['SE 477', 'IS 430', 'SE 430', 'SE 482', 'IS 485']],
                            'CSC 583': ['CSC 480'],'CSC 587': [['CSC 403', 'HCI 460']],'CSC 588': ['CSC 461', 'SE 456', 'SE 450'],'IS 590': ['CSC 424'],'SE 591': ['SE 491'],

 }

    
    def to_list(prereq_string):
        pass

    def start(self):
        dsn = "postgres://csc394:password@35.188.8.242:5432/csc394"
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        sql = "SELECT title, subject, course_nbr, id, prereqs FROM csc394_courses ORDER BY course_nbr"
        rarity_sql = 'SELECT count(course_id), course_id, subject, catalog_nbr FROM (SELECT distinct course_id, subject, catalog_nbr, stream FROM days_offered) AS t2 GROUP BY course_id, subject, catalog_nbr ORDER BY subject, catalog_nbr;'
        self.get_rarity(rarity_sql, cur)
        self.fill_trees(cur, sql)
        self.final_calculate(self.unlocks_list, self.score_list)
        self.final_score()

    def final_score(self):
        for k, y in self.score_list.items():
            if k in self.rarity_list:
                self.final_list[k] = self.score_list[k] + self.rarity_list[k]
            else:
                self.final_list[k] = self.score_list[k]
    
    def get_rarity(self, sql, cur):
        cur.execute(sql)

        row = cur.fetchone()

        while row is not None:
            subject = row[2]
            course_number = row[3]
            rarity_score = row[0]
            course = subject + " " + str(course_number)
            self.rarity_list[course] = int(rarity_score) * 6
            row = cur.fetchone()


    def fill_trees(self, cur, sql):
        cur.execute(sql)

        row = cur.fetchone()
        
        while row is not None:
            subject = row[1]
            course_nbr = str(row[2])
            course = str(subject + " " + course_nbr)
            prereqs = row[4]
            self.insert_scores(course)
            self.get_unlocks(course)
            row = cur.fetchone()
        cur.close()

    def final_calculate(self, unlocks_list, score_list):
        for c, u in sorted(unlocks_list.items(), reverse=True):
            for i in u:
                score_list[c] = score_list[c] + score_list[i]
        


    def check_list(self, lst, item):
        if not lst:
            return False
        comp = lst[0]
        if isinstance(comp, list) or isinstance(comp, tuple):
            return self.check_list(comp, item) or self.check_list(lst[1:], item)
        elif comp == item:
            return True
        else:
            return self.check_list( lst[1:], item)
        

    def get_unlocks(self, course, score=0):
        lst = []
        for k, v in self.class_tree.items():
            if self.check_list(v, course) == True:
                lst.append(k)
        self.unlocks_list[course] = lst
                

    def get_scores2(self, course, score=0, lst=[]):
        for k,v in self.class_tree.items():
            if self.check_list(v, course) == True:
                score = score + 1
        return score

    def insert_scores(self, course):
        self.score_list[course] = self.get_scores2(course)

    def calculate_scores(self, course, unlocks_list, score_list):
        for c in unlocks_list[course]:
            score_list[course] = score_list[course] + score_list[c]








if __name__ == "__main__":
    sql = "UPDATE csc394_courses SET score = %s WHERE subject = %s AND course_nbr = %s"
    object1 = class_list()
    object1.start()
    dsn = "postgres://csc394:password@35.188.8.242:5432/csc394"
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    

    for k, y in object1.rarity_list.items():
        subject = k.split()[0]
        course_nbr = k.split()[1]
        score = y
       # print(subject + " " + str(course_nbr) + " " + str(score)+"\n")
        cur.execute(sql, (score, subject, course_nbr))
    conn.commit()
    cur.close()




