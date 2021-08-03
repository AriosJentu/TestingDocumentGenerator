import Scripts.Assignments as Assignments
AssignmentsInformation = Assignments.AssignmentsInformationClass()

#Imports 
from . import Test1
from . import Test2

#Append assignments into Assignments Information List
AssignmentsInformation.append(Test1.Test1, "t")
AssignmentsInformation.append(Test2.Test2, "t")
