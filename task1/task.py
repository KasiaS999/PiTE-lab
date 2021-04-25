# Class diary
#
# Create program for handling lesson scores.
# Use python to handle student (highscool) class scores, and attendance.
# Make it possible to:
# - Get students total average score (average across classes)
# - get students average score in class
# - hold students name and surname
# - Count total attendance of student
#
# Please, use your imagination and create more functionalities.
# Your project should be able to handle entire school(s?).
# If you have enough courage and time, try storing (reading/writing)
# data in text files (YAML, JSON).
# If you have even more courage, try implementing user interface (might be text-like).
#
#Try to expand your implementation as best as you can. 
#Think of as many features as you can, and try implementing them.
#Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
#Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
#The goal of this task is for you to SHOW YOUR BEST python programming skills.
#Impress everyone with your skills, show off with your code.
#
#Your program must be runnable with command "python task.py".
#Show some usecases of your library in the code (print some things)
#
#When you are done upload this code to your github repository. 
#
#Delete these comments before commit!
#Good luck.
# Class diary
#
import json
import statistics


def average(fun, list1):
    average_list = list(map(fun, list1))
    return statistics.mean(average_list)

def student_average(student):
    return average(statistics.mean,student["grades"].values() )

def class_average(class1):
    return average(student_average,class1["students"] )

def school_average(school):
    return average(class_average, school["classes"])

def schools_average(schools):
    return average(school_average, schools)

def find_student_class(class_name, schools):
    for school in schools:
        for class1 in school["classes"]:
            if class1["class_name"]==class_name:
                return class1

def get_student_average(class_name, name, surname, schools):
    class1 = find_student_class(class_name, schools)
    for student in class1["students"]:
          if student["name"]==name:
              if student["surname"] == surname:
                  return student_average(student) 


def get_student_attendance(student):
    return 100*statistics.mean(student["attendance"])

def get_class_attendance(class1):
    return statistics.mean(list(map(get_student_attendance, class1["students"])))

def get_school_attendance(school):
    return statistics.mean(list(map(get_class_attendance, school["classes"])))

def get_total_attendance(schools):
    return statistics.mean(list(map(get_school_attendance, schools)))

def find_student_class_and_school(name, surname, schools):
    for school in schools:
        for class1 in school["classes"]:
            for student in class1["students"]:
                if (student["name"], student["surname"]) == (name, surname):
                    return school["school_name"], class1["class_name"]


def get_student_name(student):
    return student["name"], student["surname"]


def get_students_from_class(class1):
    return list(map(get_student_name, class1["students"]))


def get_all_students_in_school(school_name, schools):
    list_of_students = []
    for school in schools:
        if school_name == school["school_name"]:
            for class1 in school["classes"]:
                list_of_students.extend(get_students_from_class(class1))
    return list_of_students


def get_class_grades(class1):
    class_grades = []
    for student in class1["students"]:
        class_grades.extend(list(student["grades"].values()))

    return class_grades


def get_all_grades_in_school(school):
    grades = []
    grades.extend(list(map(get_class_grades, school["classes"])))
    return grades


if __name__ == "__main__":
    with open("data.json", 'r') as json_file:
        schools_dict =json.load(json_file)
        schools = schools_dict["schools"]

school1 = schools[0]
school2 = schools[1]

class1 = school1["classes"][0]
class2 = school1["classes"][1]
class3 = school2["classes"][0]
student = class1["students"][0]

print("Wioletta Mazur, IIc,  average: {}".format(round(get_student_average("IIc", "Wioletta","Mazur", schools), 2)))
print("Andrzej Zielinski, IIb,  average: {}".format(round(get_student_average("IIb", "Andrzej","Zielinski", schools), 2)))
print("{} average is {}".format(class1["class_name"], round(class_average(class1), 2)))
print("{} average is {}".format(school2["school_name"], round(school_average(school1), 2)))
print("Average attendance in {} is {}%".format(school1["school_name"], get_school_attendance(school1)))
print("Average attendance in {} is {}%".format(class2["class_name"], get_class_attendance(class2)))
print("{} {} average attendance is {}%".format(student["name"], student["surname"], get_student_attendance(student)))
school_and_class = find_student_class_and_school("Agata", "Dubiel", schools)
print("Agata Dubiel is a {} student, class {}".format(school_and_class[0],school_and_class[1] ))
school_and_class = find_student_class_and_school("Konrad", "Filip", schools)
print("Konrad Filip is a {} student, class {}".format(school_and_class[0],school_and_class[1] ))
print("All students in IILO: \n {}".format(get_all_students_in_school("IILO", schools)))
print("All grades in {}: \n {}".format(school1["school_name"], get_all_grades_in_school(school1)))
