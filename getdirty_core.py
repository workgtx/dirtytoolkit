import requests
from re import split
from json_to_csv import JsonToCsv


class GrabData:
    def __init__(self, act, method, index, page, per_page):
        self.act = str(act)
        self.method = str(method)
        self.index = str(index)
        self.page = int(page)
        self.per_page = int(per_page)
        self.firstpage = True

    def url_gen_f(self):
        __b = {1: {1: 'https://d3.ru/api', 2: 'domains',
                   3: 'posts', 4: 'votes', 5: 'comments', 6: 'users'},
               2: {1: 'per_page', 2: 'page', 3: 'sorting'},
               3: {1: 'hotness', 2: 'rating',
                   3: 'date_created', 4: 'date_changed'},
               4: {1: '/', 2: '?', 3: '&', 4: '='}}
        __url = {'domains': '%s%s%s%s%s%s%d%s%s%s%d'
                 % (__b[1][1], '/', __b[1][2], '?', __b[2][2], '=',
                    self.page, '&', __b[2][1], '=', self.per_page),
                 'posts': '%s%s%s%s%s%s%s%s%s%s%d%s%s%s%d%s%s%s%s'
                 % (__b[1][1], '/', __b[1][2], '/', self.index, '/',
                    __b[1][3], '?', __b[2][2], '=', self.page, '&',
                    __b[2][1], '=', self.per_page, '&',
                    __b[2][3], '=', __b[3][3]),
                 'p_votes': '%s%s%s%s%s%s%s%s%s%s%d%s%s%s%d'
                 % (__b[1][1], '/', __b[1][3], '/', self.index, '/',
                    __b[1][4], '?', __b[2][2], '=', self.page, '&',
                    __b[2][1], '=', self.per_page),
                 'comments': '%s%s%s%s%s%s%s%s%s%s%d%s%s%s%d'
                 % (__b[1][1], '/', __b[1][3], '/', self.index, '/',
                    __b[1][5], '?', __b[2][2], '=', self.page, '&',
                    __b[2][1], '=', self.per_page),
                 'c_votes': '%s%s%s%s%s%s%s%s'
                 % (__b[1][1], '/', __b[1][5], '/', self.index, '/',
                    __b[1][4], '/'),
                 'users': '%s%s%s%s%s%s%s%s%s%s%s'
                 % (__b[1][1], '/', __b[1][6], '/', self.index, '/',
                    __b[1][3], '?', __b[2][1], '=', self.per_page),
                 'u_votes': '%s%s%s%s%s%s%s%s'
                 % (__b[1][1], '/', __b[1][6], '/', self.index, '/',
                    __b[1][4], '/')}[self.act]

        self.url = __url
        return(self.url)

    def get_data_f(self):
        __headers = {'X-Futuware-UID': '',
                     'X-Futuware-SID': ''}
        self.response = ''
        if self.method == 'upvoters' or 'downvoters':
            self.response = (requests.get(self.url, headers=__headers)).content
        else:
            self.response = (requests.get(self.url)).content
        return(self.response)

    def get_page_item_f(self):
        self.methods = ['pgc', 'upvoters', 'downvoters']
        self.method = self.methods[0]
        GrabData.prepare_f(self)
        GrabData.separator_f(self)
        self.numofpages = int(self.separated[0])
        self.numofitems = int(self.separated[1])
        return (self.numofpages, self.numofitems)

    def up_down_voters_f(self):
        n = 0
        self.upvoters = ''
        self.downvoters = ''
        self.page = 1
        while self.page <= self.numofpages:
            GrabData.up_down_cycle_f(self, 1)
            GrabData.up_down_cycle_f(self, 2)
            self.page += 1
            GrabData.url_gen_f(self)
            GrabData.get_data_f(self)
            n += 1
        self.parsed = self.upvoters
        if len(self.parsed) > 0:
            GrabData.separator_f(self)
            self.upvoters = self.separated
        else:
            self.upvoters = []
        self.parsed = self.downvoters
        if len(self.parsed) > 0:
            GrabData.separator_f(self)
            self.downvoters = self.separated
        else:
            self.downvoters = []
        return (self.upvoters, self.downvoters)

    def up_down_cycle_f(self, i):
        if i == 1:
            try:
                self.method = self.methods[i]
                GrabData.prepare_f(self)
                if self.page == 1:
                    self.upvoters = self.parsed
                else:
                    self.upvoters = '%ssephereslinesephere%s'\
                            % (self.upvoters, self.parsed)
            except Exception:
                return('')
            return (self.upvoters)
        else:
            try:
                self.method = self.methods[i]
                GrabData.prepare_f(self)
                if self.page == 1:
                    self.downvoters = self.parsed
                else:
                    self.downvoters = '%ssephereslinesephere%s'\
                            % (self.downvoters, self.parsed)
            except Exception:
                return('')
            return (self.downvoters)

    def prepare_f(self):
        __struct = {'pgc': '''"page_count","item_count"''',
                    'posts': '''+"posts"[."domain"["id"],."user"["id", "login"],"id","rating",\
                             ."data"["title","text",."link"[."embed"["title","description"],\
                              "url"]], "comments_count","tags", "golden",\
                              "can_delete","can_unpublish","can_edit",\
                              "can_moderate","created"]''',
                    'upvoters': '''+"upvotes"["vote",."user"["id","login"],"changed",\
                             ."user"["gender","rank","karma","is_golden",
                              "active","deleted"]]''',
                    'downvoters': '''+"downvotes"["vote",."user"["id","login"],"changed",\
                             ."user"["gender","rank","karma","is_golden",\
                              "active","deleted"]]''',
                    'domains': '''+"domains"["id","readers_count","prefix",\
                              "name","title","description","is_elections_enabled",\
                              "is_readable_for_everyone",."owner"["login"],\
                             ."president"["login"]]''',
                    'comments': '''+"comments"["id","parent_id","tree_level","rating",\
                             ."user"["id","login"],"body","can_delete",\
                              "can_remove_comment_threads","can_edit",\
                              "can_moderate","created"]'''}
        __pg_mask = JsonToCsv(__struct[self.method],
                              nullValue='null', debug=False)
        __pg_extr = __pg_mask.extractData(self.response)
        __pg_pars = __pg_mask.dataToStr(__pg_extr, separator='sephere',
                                        lineSeparator='sephereslinesephere')
        self.parsed = __pg_pars
        return (self.parsed)

    def cleaner_f(self):
        self.parsed = self.parsed.replace('\"', '').replace('\r\n', '\t')\
                      .replace('\t', '    ').replace('[', '').replace(']', '')\
                      .replace('{', '').replace('}', '',)
        return (self.parsed)

    def separator_f(self):
        if self.method == 'pgc':
            self.separated = split('sephere', self.parsed)
        else:
            __dlim = 'seplinehere'
            __separated = split('sephere', self.parsed)
            self.separated = [[]]
            for i in __separated:
                if i == __dlim:
                    self.separated.append([])
                else:
                    self.separated[-1].append(i)
        return(self.separated)
