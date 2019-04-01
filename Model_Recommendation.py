#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:27:14 2019

@author: yorhagy
"""
import pandas as pd

def printResult(list_c, LIST):
    R = []
    for i in LIST:
        idx, score = i
        R.append([list_c[idx], score])     
    return pd.DataFrame(R, columns=['Courses', 'Score'])

class recommentation:
    def __init__(self, this_model, data_, userId=None):
        self.list_e = data_.list_email
        self.list_c = data_.list_courses
        self.data = this_model.data
        self.model = this_model.model
        self.userId = userId
        
    def recommendCourses(self, u=None):
        Id = self.list_e.index(self.userId)
        user_course = self.data.T.tocsr()
        LISTCOURSE = self.model.recommend(Id, user_course)
        return printResult(self.list_c, LISTCOURSE)
        
    def relatedItems(self, course):
        Id = self.list_c.index(course)
        RELATED = self.model.similar_items(Id)
        return printResult(self.list_c, RELATED)
    
    def relatedUser(self, Users):
        Id = Users.email.index.values[0]
        user_course = self.data.T.tocsr()
        LISTCOURSE = self.model.recommend(Id, user_course)
        return printResult(self.list_c, LISTCOURSE)
        