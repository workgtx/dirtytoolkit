#!/usr/bin/python
import getdirty_core


class Extractor:
    def __init__(self, index=0, page=1, per_page=42):
        self.x = {1: 'domains', 2: 'posts', 3: 'comments', 4: 'p_votes',
                  5: 'c_votes', 6: 'votes', 7: 'u_votes', 8: 'users'}
        self.index = str(index)
        self.page = int(page)
        self.per_page = int(per_page)

    def domains_f(self):
        domains = getdirty_core.GrabData(
                self.x[1], self.x[1], self.index,
                self.page, self.per_page)
        domains.url_gen_f()
        domains.get_data_f()
        domains.get_page_item_f()
        domains.method = self.x[1]
        domains.get_data_f()
        domains.prepare_f()
        domains.cleaner_f()
        domains.separator_f()
        self.domains = domains.separated
        self.numofpages = domains.numofpages
        self.numofitems = domains.numofitems
        return (self.domains,
                self.numofpages,
                self.numofitems)

    def posts_f(self):
        posts = getdirty_core.GrabData(
                self.x[2], self.x[2], self.index,
                self.page, self.per_page)
        posts.url_gen_f()
        posts.get_data_f()
        posts.prepare_f()
        posts.cleaner_f()
        posts.separator_f()
        self.posts = posts.separated
        return (self.posts)

    def comments_f(self):
        comments = getdirty_core.GrabData(
                   self.x[3], self.x[3], self.index,
                   self.page, self.per_page)
        comments.url_gen_f()
        comments.get_data_f()
        comments.prepare_f()
        comments.cleaner_f()
        comments.separator_f()
        self.comments = comments.separated
        return (self.comments)

    def postvoters_f(self):
        self.per_page = 210
        postvoters = getdirty_core.GrabData(
                     self.x[4], self.x[6], self.index,
                     self.page, self.per_page)
        postvoters.url_gen_f()
        postvoters.get_data_f()
        postvoters.get_page_item_f()
        postvoters.up_down_voters_f()
        self.postupvoters = postvoters.upvoters
        self.postdownvoters = postvoters.downvoters
        return (self.postupvoters,
                self.postdownvoters)

    def commentvoters_f(self):
        self.per_page = 210
        commentvoters = getdirty_core.GrabData(
                        self.x[5], self.x[6], self.index,
                        self.page, self.per_page)
        commentvoters.url_gen_f()
        commentvoters.get_data_f()
        commentvoters.get_page_item_f()
        commentvoters.up_down_voters_f()
        self.commentupvoters = commentvoters.upvoters
        self.commentdownvoters = commentvoters.downvoters
        return (self.commentupvoters,
                self.commentdownvoters)

    def users_f(self):
        self.per_page = 210
        uservoters = getdirty_core.GrabData(
                     self.x[7], self.x[6], self.index,
                     self.page, self.per_page)
        uservoters.url_gen_f()
        uservoters.get_data_f()
        uservoters.get_page_item_f()
        uservoters.up_down_voters_f()
        self.userupvoters = uservoters.upvoters
        self.userdownvoters = uservoters.downvoters
        return (self.userupvoters,
                self.userdownvoters)

    def userposts_f(self):
        self.per_page = 42
        userposts = getdirty_core.GrabData(
                    self.x[8], self.x[8], self.index,
                    self.page, self.per_page)
        userposts.url_gen_f()
        userposts.get_data_f()
        userposts.get_page_item_f()
        userposts.prepare_f()
        userposts.separator_f()
        return (userposts.numofitems,
                userposts.numofpages,
                userposts.separated)
