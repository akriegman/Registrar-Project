# let's see what happens
import itertools
import sys

#class declarations
class Student:
    def __init__(self, id, prefs):
        self.id = id
        self.prefs = prefs
        self.coursesAssigned = []

    def __str__(self):
        return str(self.id)# + " " + str(self.prefs[0]) + " " + str(self.prefs[1]) + " " + str(self.prefs[2]) + " " + str(self.prefs[3])

    def __repr__(self):
        return str(self)

class Room:
    """These objects represent each room. It's field is the capacity of the room"""

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

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
        #start time field
        #end time field

    def __str__(self):
        return str(self.id) + "\t" + str(self.room) + "\t" + str(self.teacher) + "\t" + str(self.period) #+ "\t" + str(self.students)

    def __repr__(self):
        return str(self)

    #does overlap method
    # def doesOverlap(self, otherCourse)

class Period:
    """A period is a list of the classes in that period."""

    def __init__(self, id):
        self.id = id
        self.courses = []

    def __str__(self):
        return str(self.id) + " " + str(self.courses)

    def __repr__(self):
        return str(self)


def calculateScore(students):
    score = 0
    maxScore = 0
    for student in students:
        maxScore += len(student.prefs)
        for course in student.coursesAssigned:
            if course.id in student.prefs:
                score += 1
    return score, maxScore




if __name__=='__main__':

    try:
        constraintsPath    = sys.argv[1]
        prefsPath          = sys.argv[2]
        scheduleOutputPath = sys.argv[3]

    except IndexError:
        print('\nERROR: Argument missmatch\n'
              '\nCorrect usage is:'
              '\n"python3 registrarGroupProject.py <constraintsPath> <prefsPath> <scheduleOutputPath>"\n')
        exit(1)


    # numStudents, numPeriods, numRooms, numCourses, numTeachers = 0,0,0,0,0


    rooms = []
    courses = []

    constraintsFile = open(constraintsPath,"r+")
    numPeriods = int(((constraintsFile.readline()).split())[2])      #This should take the numPeriods from the constraintsFile
    numRooms = int(((constraintsFile.readline()).split())[1])        #This should take the numRooms from the

    # Rooms Parsing
    for i in range(0,numRooms):
        ourLine = constraintsFile.readline()
        listOfOurLine = ourLine.split()
        rooms.append(Room(int(listOfOurLine[0]),int(listOfOurLine[1])))
        # print("Thing we just added: ", rooms[i])

    roomLookup = {r.id:r for r in rooms}

    numCourses = int(((constraintsFile.readline()).split())[1])
    numTeachers = int(((constraintsFile.readline()).split())[1])


    # Courses Parsing
    for i in range(0,numCourses):
        ourLine = constraintsFile.readline()
        listOfOurLine = ourLine.split()
        courses.append(Course(int(listOfOurLine[0]),int(listOfOurLine[1])))       #adds the course with id and teacher

    courseLookup = {c.id:c for c in courses}

    # Students Parsing
    prefsFile = open(prefsPath,"r+")
    numStudents = int(((prefsFile.readline()).split())[1])      #This should take the numStudents from the prefsFile

    #
    students = []

    for i in range(0,numStudents):
        ourLine = prefsFile.readline()
        listOfOurLine = ourLine.split()
        students.append(Student(int(listOfOurLine[0]), list(map(int, listOfOurLine[1:5]))))

    # Create periods
    periods = [Period(i) for i in range(1, numPeriods + 1)]

    # Preprocessing: create conflict matrix
    conflicts = {}
    # Keys are comma separated, no parenthesis pairs
    # Main diagonal is popularity of each class
    for pair in itertools.product(range(1, numCourses + 1), repeat = 2):
        conflicts[pair] = 0

    for s in students:
        for pair in itertools.product(s.prefs, repeat = 2):
            conflicts[pair] += 1


    # Preprocessing: sort list of classes by popularity score
    courses.sort(key = lambda c: -conflicts[c.id, c.id])

    # Preprocessing: sort Rooms in order of decreasing capacity
    rooms.sort(key = lambda r: -r.capacity)


    ######## Assign each class in classes to a time slot ########


    def teacherInPeriod(teacher, period):
        ### Checks whether the given teacher is already teaching a course in the ###
        ### given period ###
        return teacher in [c.teacher for c in period.courses]

    for course in courses:
          # Make a dictionary of conflict costs of assigning course to each period
          cost = {}
          for period in periods:
              cost[period.id] = sum([conflicts[course.id, c.id] for c in period.courses])

          periods.sort(key = lambda p: cost[p.id])

          for p in periods:
              # Add the course to the first period p if its teacher isn't already
              # teaching during p and there's still at least one room available
              if (not teacherInPeriod(course.teacher, p)) and (len(p.courses) < len(rooms)):
                  course.period = p.id
                  p.courses += [course]
                  break


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
    for student in students:
        busyPeriods = []
        for course in map(lambda p: courseLookup[p], student.prefs):
            if course.period == 0:
                continue
            room = roomLookup[course.room] # room of c
            period = course.period # period of c
            # print("line 186!!!!")
            if ((len(course.students) < room.capacity) and (not (period in busyPeriods))):
                # print("in the if line 190!!!")
                course.students.append(student)         # for Course object
                student.coursesAssigned.append(course)  # for Student object
                busyPeriods.append(course.period)

    # for s in students:
    # for c in courses:
    #     print(c.students)

    #That could be all!
    # What do we write to the output file?


    # print("####")
    score, maxScore = calculateScore(students)
    print("Score is: {}/{} = {}%\n".format(score, maxScore, "%.1f" % (score/maxScore * 100)))
    # print("####")


    with open(scheduleOutputPath, 'w') as outputFile:
        outputFile.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for course in courses:
            outputFile.write(str(course) + "\t")
            outputFile.write(' '.join(map(lambda s: str(s.id), course.students)) + "\n")
            # for studentID in course.students:
            #     outputFile.write(studentID + " ")
