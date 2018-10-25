#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Human():
    def __init__(self, name, gender):
        self.name   = name
        self.gender = gender


name_ = raw_input("Please enter the name: ")
gndr_ = raw_input("Please enter the gender: ")
#print type(name_)
#print gndr_
akshay = Human(name_, gndr_)

#print akshay
print ("Human's name is: %s" % akshay.name)
print ("Human's gender is: %s" % akshay.gender)
