# let's see what happens
import itertools
import sys
import random
import argparse

#class declarations
class Student:
    def __init__(self, id, prefs):
        self.id = id
        self.prefs = prefs
        self.coursesAssigned = []
        # For Extension 3:
        self.prefsRank = []
        self.busyPeriods = []
        # For Extension 4:
        self.classYear = random.randint(1,4)

    def __str__(self):
        return str(self.id) + ' year:{}\n'.format(self.classYear)
        # + " " + str(self.prefs[0]) + " " + str(self.prefs[1]) + " " + str(self.prefs[2]) + " " + str(self.prefs[3])

    def __repr__(self):
        return str(self)

    # For Extension 3
    def prefsRank(self):
        classNums = len(self.prefsRank)
        self.classRank = random.sample(range(1,classNums + 1), classNums) # 1-4 list corresponding to prefs.



class Room:
    """These objects represent each room. Its field is the capacity of the room"""

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.department = 0

    def __str__(self):
        return str(self.id) + " " + str(self.capacity)
        # return "Room id: " + self.id + " , capacity: " + self.capacity

    def __repr__(self):
        return str(self)

class Course:
    def __init__(self, id, teacher):
        self.id = id
        self.teacher = teacher
        self.students = []
        self.period = 0
        self.room = 0
        self.department = 0

    def __str__(self):
        return str(self.id) + "\t" + str(self.room) + "\t" + str(self.teacher) + "\t" + str(self.period) #+ "\t" + str(self.students)

    def __repr__(self):
        return str(self)

class Period:
    """A period is a list of the classes in that period."""

    def __init__(self, id, startTime, endTime, days):
        self.id = id
        self.courses = []
        self.startTime = startTime          #float from 0 to 24
        self.endTime = endTime             #float from 0 to 24
        self.overlaps = []  # overlapping periods
        self.days = days            #example: (False, True, False, True, False)

    def __str__(self):
        return str(self.id) + ' s:{}'.format(self.startTime) + ' e:{}'.format(self.endTime) + ' C:{}'.format(str(self.courses)) + "\n"

    def __repr__(self):
        return str(self)

    def overlaps_with(self, other):
        """ Returns true if self overlaps with other, false otherwise """
        time_overlap =  not (self.endTime <= other.startTime or self.startTime >= other.endTime)
        day_overlap = True in map(lambda a,b: a and b, self.days, other.days)
        return (time_overlap and day_overlap)


def calculateScore(students):
    scoresByYear = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0
    }
    maxScoresByYear = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0
    }

    for student in students:
        maxScoresByYear[student.classYear] += len(student.prefs)
        for course in student.coursesAssigned:
            if course.id in student.prefs:
                scoresByYear[student.classYear] += 1

    score = sum(scoresByYear.values())
    maxScore = sum(maxScoresByYear.values())

    return score, maxScore, scoresByYear, maxScoresByYear




if __name__=='__main__':
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument("constraintsPath")
    # parser.add_argument("prefsPath")
    # parser.add_argument("scheduleOutputPath")
    # parser.add_argument

    try:
        constraintsPath    = sys.argv[1]
        prefsPath          = sys.argv[2]
        scheduleOutputPath = sys.argv[3]
        try:
            extension      = int(sys.argv[4])
        except IndexError:
            extension      = 0
        try:
            extArg1 = float(sys.argv[5])
        except IndexError:
            extArg1 = 0
        try:
            extArg2 = float(sys.argv[6])
        except IndexError:
            extArg2 = 0

    except IndexError:
        print('\nERROR: Argument missmatch\n'
              '\nCorrect usage is:'
              '\n"python3 registrarGroupProject.py <constraintsPath> <prefsPath> <scheduleOutputPath>"\n')
        exit(1)



    rooms = []
    courses = []
    periods = []

    constraintsFile = open(constraintsPath,"r+")
    numPeriods = int(((constraintsFile.readline()).split())[2])      #This should take the numPeriods from the constraintsFile

    numDays = 5

    badStringsToDays = {
    "M": (True, False, False, False, False),
    "F": (False, False, False, False, True),
    "TTH" : (False, True, False, True, False),
    "MWF" : (True, False, True, False, True),
    "MW" : (True, False, True, False, False),
    "M-F" : (True, True, True, True, True),
    "W" : (False, False, True, False, False),
    "T" : (False, True, False, False, False),
    "TTH" : (False, False, False, True, False),
    "MTTH" : (True, True, False, True, False),
    "TH" : (False, False, False, True, False),
    "WF" : (False, False, True, False, True)}

    dayToIndex = {
    "M" : 0,
    "T" : 1,
    "W" : 2,
    "H" : 3,
    "F" : 4
    }

    # daysToBadStrings = {v:k for k,v in badStringsToDays.items()}

    #parsing periods
    #Here's where we read in start time and end time of each period and which days it's on
    lastLineRead = ""
    done = False
    periodID = 0
    while not done:
        lastLineRead = constraintsFile.readline()
        splitUpLine = lastLineRead.split()
        if splitUpLine[0] == "Rooms":
            done = True
        else:
            startTime = float((splitUpLine[1]).split(":")[0]) + (float((splitUpLine[1]).split(":")[1])*(1/60))
            if splitUpLine[2] == "PM":
                 startTime += 12.0
            endTime = float((splitUpLine[3].split(":"))[0]) + (float((splitUpLine[3]).split(":")[1])*(1/60))
            if splitUpLine[4] == "PM":
                 endTime += 12.0
            # periodDays = badStringsToDays[splitUpLine[5]]
            periodDays = [False for i in range(5)]
            for day in splitUpLine[5:]:
                periodDays[dayToIndex[day]] = True

            periods.append(Period(periodID, startTime, endTime, periodDays))
        periodID += 1

    periodLookup = {p.id:p for p in periods}

    numRooms = int(splitUpLine[1])        #This should take the numRooms from the constraints file


    # Rooms Parsing
    for i in range(0,numRooms):
        ourLine = constraintsFile.readline()
        listOfOurLine = ourLine.split()
        rooms.append(Room(listOfOurLine[0],int(listOfOurLine[1])))
        # print("Thing we just added: ", rooms[i])

    roomLookup = {r.id:r for r in rooms}

    numCourses = int(((constraintsFile.readline()).split())[1])
    numTeachers = int(((constraintsFile.readline()).split())[1])


    # Courses Parsing
    newTeacherIndex = -1             #only negative numbers. these teachers need to be hired
    for i in range(0,numCourses):
        ourLine = constraintsFile.readline()
        listOfOurLine = ourLine.split()

        if len(listOfOurLine) == 1:
            #this class has no specified teacher
            teacherNumber = newTeacherIndex
            newTeacherIndex -= 1
        else:
            teacherNumber = int(listOfOurLine[1])

        courses.append(Course(int(listOfOurLine[0]),teacherNumber))       #adds the course with id and teacher

    courseLookup = {c.id:c for c in courses}
    teachers = list({c.teacher for c in courses})


    # Students Parsing
    prefsFile = open(prefsPath,"r+")
    numStudents = int(((prefsFile.readline()).split())[1])      #This should take the numStudents from the prefsFile
    students = []
    for i in range(numStudents):
        ourLine = prefsFile.readline()
        listOfOurLine = ourLine.split()
        desiredCourses = list(map(int, listOfOurLine[1:len(listOfOurLine)-1]))
        desiredCourses = [c for c in desiredCourses if c in courseLookup]
        students.append(Student(int(listOfOurLine[0]), desiredCourses))

    # if extension == 4:
    # for i in range(numStudents):
    #     if float(i) / numStudents < 1/4:
    #         students[i].classYear = 1
    #     elif 1/4 <= float(i) / numStudents < 1/2:
    #         students[i].classYear = 2
    #     elif 1/2 <= float(i) / numStudents < 3/4:
    #         students[i].classYear = 3
    #     else:
    #         students[i].classYear = 4

    # Preprocessing: create conflict matrix
    conflicts = {}
    # Keys are comma separated, no parenthesis pairs
    # Main diagonal is popularity of each class
    for pair in itertools.product(list(courseLookup), repeat = 2):
        conflicts[pair] = 0

    for s in students:
        for pair in itertools.product(s.prefs, repeat = 2):
            conflicts[pair] += 1


    # Preprocessing: sort list of classes by popularity score
    courses.sort(key = lambda c: -conflicts[c.id, c.id])

    # Preprocessing: sort Rooms in order of decreasing capacity
    rooms.sort(key = lambda r: -r.capacity)


    # print("\n")
    # print("Num courses: %i" % len(courses))
    # print("Num rooms: %i" % len(rooms))
    # print("Num students: %i" % len(students))
    # print("\n")


    ######## Extensions processing ########

    ## Deadzone extension ##
    if extension == 1:
        # print("\n\nDeadzone\n\n")
        dz_start = extArg1
        dz_end   = extArg2
        days = (1,1,1,1,1)

        deadzone = Period(-1, dz_start, dz_end, days) # def __init__(self, id, startTime, endTime, days):

        # print("Periods before removing deadzone conflicts:", len(periods))
        newPeriods = periods.copy()
        for p in periods:
            if p.overlaps_with(deadzone):
                newPeriods.remove(p)
                del periodLookup[p.id]
        periods = newPeriods
        print("Periods after removing deadzone conflicts:", len(periods))
        print("#############################\n\n")


    if extension == 2:
        # print("\n#### Office Hour Extension: ####")

        length = extArg1
        numDays = extArg2
        print(length*numDays)
        sep = lambda x: (x,x+length)
        tfList = [True if i < numDays else False for i in range(5)]
        officeHours = {t:Period(-t, *sep(random.randint(8, 10)), random.sample(tfList, k=5)) for t in teachers}

    if extension == 5:
        numDepartments = 20
        for course in courses:
            course.department = random.randint(1, numDepartments)
        for room in rooms:
            room.department = random.randint(1, numDepartments)


    ######## Assign each class in classes to a time slot ########

    def teacherInPeriod(teacher, period):
        ### Checks whether the given teacher is already teaching a course in the ###
        ### given period ###
        return teacher in [c.teacher for c in period.courses]

    #TODO: fill out each periods list of overlapping periods
    for p1 in periods:
        for p2 in periods:
            if p1.overlaps_with(p2):
                p1.overlaps.append(p2.id)

    for course in courses:
          # Make a dictionary of conflict costs of assigning course to each period
          cost = {}
          for period in periods:
              conflictsInOverlappingPeriods = [sum([conflicts[course.id, c.id] for c in periodLookup[p].courses]) for p in period.overlaps]
              cost[period.id] = sum(conflictsInOverlappingPeriods)

          periods.sort(key = lambda p: cost[p.id])

          for p in periods:
              # Add the course to the first period p if its teacher isn't already
              # teaching during p and there's still at least one room available
              if extension == 2:
                  if p.overlaps_with(officeHours[course.teacher]):
                      continue
              teachersInConflictingPeriods = [c.teacher for per in p.overlaps for c in periodLookup[per].courses]
              if (not course.teacher in teachersInConflictingPeriods) and (len(p.courses) < len(rooms)):
                  course.period = p.id
                  p.courses += [course]
                  break

    if extension == 5:
        buildings = {i:[] for i in range(1, numDepartments + 1)}
        for room in rooms:
            buildings[room.department].append(room)
        for period in periods:
            overflow = []
            bigC = period.courses
            remainingRooms = rooms.copy()
            indices = {i:0 for i in range(1, numDepartments + 1)}
            for i in range(len(bigC)):
                try:
                    bigC[i].room = buildings[bigC[i].department][indices[bigC[i].department]].id
                    remainingRooms.remove(buildings[bigC[i].department][indices[bigC[i].department]])
                    indices[bigC[i].department] += 1
                except IndexError:
                    overflow.append(bigC[i])
            for i in range(len(overflow)):
                room = remainingRooms[i].id
                course = overflow[i]
                course.room = room
    else:
        for period in periods:
            bigC = period.courses       #The list of classes in the period
            for i in range(len(bigC)):
                room = rooms[i].id
                course = courseLookup[bigC[i].id]
                course.room = room

    # print(periods)


    # For each student s in S:
    #     For each course c in s's course list:
    #         Let r and t be the room and time to which c is assigned
    #         If the number of students assigned to c is less than r capacity and s is not already assigned to another course in t:
    #             Assign s to c (both ways)
    # print(students)

    ###### EXTENSIONS 3 & 4 #####
    '''
    ### Student Prefs Rank
    if extension == 3:
        print("\n\n#### Priority by Student Preferences Rank Extension: ####")
        # Sorts student.prefs by student.prefsRank
        for student in students:
            zip_prefs_prefsRank = zip(student.prefsRank, student.prefs)
            zip_prefs_prefsRank.sort()
            student.prefs = [prefs for prefsRank, prefs in zip_prefs_prefsRank]

        # Now assign only the first student.prefs, pop prefs from list and move to next student.
        for i in range(1,8): # 7 is the max number of selected courses
            for student in students:
                try:
                    course = map(i, student.prefs):
                    if course.period == 0:
                        continue
                    room = roomLookup[course.room] # room of c
                    period = course.period # period of c
                    if ((len(course.students) < room.capacity) and (not (period in busyPeriods))):
                        course.students.append(student)         # for Course object
                        student.coursesAssigned.append(course)  # for Student object
                        student.busyPeriods.append(course.period)
                except:
                    continue
    # '''

    ### Student Assignment by Class Year
    if extension == 4:
        print("\n#### Priority by Seniority Extension: ####")
        # Reorder students by self.classYear
        students = sorted(students, key = lambda stud: stud.classYear, reverse=True)
        # print(students)
    # else:
    #     random.shuffle(students)

    for student in students:
        busyPeriods = []
        for course in map(lambda p: courseLookup[p], student.prefs):
            if course.period == 0:
                continue
            room = roomLookup[course.room] # room of c
            period = course.period # period of c
            if ((len(course.students) < room.capacity) and (not (period in busyPeriods))):
                course.students.append(student)         # for Course object
                student.coursesAssigned.append(course)  # for Student object
                busyPeriods.append(course.period)

    # for s in students:
    # for c in courses:
    #     print(c.students)
    if extension == 4:
        print("####")
        score, maxScore, scoresByYear, maxScoresByYear = calculateScore(students)
        print("Senior score is:    {}/{} = {}%".format(scoresByYear[4], maxScoresByYear[4], "%.1f" % (scoresByYear[4]/maxScoresByYear[4] * 100)))
        print("Junior score is:    {}/{} = {}%".format(scoresByYear[3], maxScoresByYear[3], "%.1f" % (scoresByYear[3]/maxScoresByYear[3] * 100)))
        print("Sophomore score is: {}/{} = {}%".format(scoresByYear[2], maxScoresByYear[2], "%.1f" % (scoresByYear[2]/maxScoresByYear[2] * 100)))
        print("Freshman score is:  {}/{} = {}%".format(scoresByYear[1], maxScoresByYear[1], "%.1f" % (scoresByYear[1]/maxScoresByYear[1] * 100)))
        print('')
        print("TOTAL score is:     {}/{} = {}%".format(score, maxScore, "%.1f" % (score/maxScore * 100)))
        print("####")

    #That could be all!
    # What do we write to the output file?
    with open(scheduleOutputPath, 'w') as outputFile:
        outputFile.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for course in courses:
            outputFile.write(str(course) + "\t")
            outputFile.write(' '.join(map(lambda s: str(s.id), course.students)) + "\n")
            # for studentID in course.students:
            #     outputFile.write(studentID + " ")
