#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:38:21 2017

@author: tugg
"""
import pandas as pa
from pyDatalog import pyDatalog

# ---------------------------------------------------------------------------
# Social graph analysis:
# work through this code from top to bottom (in the way you would use a R or Jupyter notebook as well...) and write datalog clauses and python code in order to solve the respective tasks. Overall, there are 7 tasks.
# ---------------------------------------------------------------------------
calls = pa.read_csv('calls.csv', sep='\t', encoding='utf-8')
texts = pa.read_csv('texts.csv', sep='\t', encoding='utf-8')

suspect = 'Quandt Katarina'
company_Board = ['Soltau Kristine', 'Eder Eva', 'Michael Jill']

pyDatalog.create_terms('knows','has_link','many_more_needed', 'X', 'Y', 'Z', 'P', 'P2', 'paths', 'path_with_cost', 'C', 'C2')
pyDatalog.clear()

# First treat calls simply as social links (denoted knows), which have no date
for i in range(0,50):
    +knows(calls.iloc[i,1], calls.iloc[i,2])

# Task 1: Knowing someone is a bi-directional relationship -> define the predicate accordingly
knows(X,Y) <= knows(Y,X)

# Task 2: Define the predicate has_link in a way that it is true if there exists some connection (path of people knowing the next link) in the social graph
# Hints:
#   check if your predictate works: at least 1 of the following asserts should be true (2 if you read in all 150 communcation records)
#   assert (has_link('Quandt Katarina', company_Board[0]))
#   assert (has_link('Quandt Katarina', company_Board[1]))
#   assert (has_link('Quandt Katarina', company_Board[2]))
has_link(X,Y) <= knows(X,Y)
has_link(X,Y) <= has_link(X,Z) & knows(Z,Y) & (X!=Y)

#print(has_link(suspect, company_Board[1]))

# Task 3: You already know that a connection exists; now give the concrete paths between the board members and the suspect
# Hints:
#   if a knows b, there is a path between a and b
#   (X._not_in(P2)) is used to check wether x is not in path P2
#   (P==P2+[Z]) declares P as a new path containing P2 and Z
paths(X,Y,P) <= paths(X,Z,P2) & knows(Y ,Z) & (X != Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z])
paths(X,Y,P) <= knows(X,Y) & (P==[])

#print(paths(suspect, company_Board[1], P))

# Task 4: There are so many path, therefore we are only interested in short paths.
# find all the paths between the suspect and the company board, which contain five people or less
path_with_cost(X,Y,P,C) <= path_with_cost(X,Z,P2,C2) & knows(Z,Y) & (X!=Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z]) & (C==C2+1) & (C <= 5)
path_with_cost(X,Y,P,C) <= knows(X,Y) & (P==[]) & (C==0)

# ---------------------------------------------------------------------------
# Call-Data analysis:
# Now we use the text and the calls data together their corresponding dates
# ---------------------------------------------------------------------------
date_board_decision = '12.2.2017'
date_shares_bought = '23.2.2017'
pyDatalog.create_terms('called,texted,date_has_link_called,date_has_link_texted,D,D2,path_final,contacted')
pyDatalog.clear()

for i in range(0,50): # calls
    +called(calls.iloc[i,1], calls.iloc[i,2],calls.iloc[i,3])

for i in range(0,50): # texts
    +texted(texts.iloc[i,1], texts.iloc[i,2],texts.iloc[i,3])

called(X,Y,Z) <= called(Y,X,Z) # calls are bi-directional


# Task 5: we are again interested in links, but this time a connection is only valid if the links are descending in date
# find out who could have actually sent an information, when imposing this new restriction
# Hints:
#   You are allowed to naively compare the dates lexicographically using ">" and "<"; it works in this example of concrete dates (but is of course evil in general)
date_has_link_called(X,Y,D) <= called(X,Y,D)
date_has_link_called(X,Y,D) <= date_has_link_called(X,Z,D2) & called(Z,Y,D) & (X!=Y) & (D <= D2)

date_has_link_texted(X,Y,D) <= texted(X,Y,D)
date_has_link_texted(X,Y,D) <= date_has_link_texted(X,Z,D2) & texted(Z,Y,D) & (X!=Y) & (D <= D2)

contacted(X,Y,D) <= called(X,Y,D)
contacted(X,Y,D) <= texted(X,Y,D)

print(contacted(suspect,Y,D))

# Task 6: at last find all the communication paths which lead to the suspect, again with the restriction that the dates have to be ordered correctly
#path_called(X,Y,P,D) <= path_called(X,Z,P2,D2) & called(Y,Z,D) & (X!=Y) & (Y._not_in(P2)) & (P==P2+[Y]) & (D <= D2)
path_final(X,Y,P,D) <= path_final(X,Z,P2,D2) & contacted(Y ,Z, D) & (X != Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z]) & (D <= D2)
path_final(X,Y,P,D) <= contacted(X,Y,D) & (P==[])

print(path_final(suspect,company_Board[1],P,D))
# Final task: after seeing this information, who, if anybody, do you think has given a tipp to the suspect?

# Eder Eva

# General hint (only use on last resort!):
#   if nothing else helped, have a look at https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py