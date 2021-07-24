import Scripts.Assignments as Assignments
AssignmentsList = Assignments.AssignmentsListClass()

#Imports 
from . import Test1

#Append assignment Test1 into Assignments List
AssignmentsList.append(Test1.Test1, "t")
