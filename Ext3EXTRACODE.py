# Line 400ish

    ### Student Prefs Rank
    if extension == 3:
        print("\n\n#### Priority by Student Preferences Rank Extension: ####")
        # Sorts student.prefs by student.prefsRank
        for student in students:
            # student.prefsRank(student)
            # zip_prefs_prefsRank = zip(student.prefsRank, student.prefs)
            # zip_prefs_prefsRank.sort()
            # student.prefs = [prefs for prefsRank, prefs in zip_prefs_prefsRank]

            # print("\n")
            # print(student.prefs)
            # print(student.prefsRank)
            student.prefs = [prefs for prefsRank, prefs in sorted(zip(student.prefsRank,student.prefs))]
            # print(student.prefs)


        # Now assign only the first student.prefs, (DO NOT pop prefs from list) and move to next student.
        for i in range(1,8): # 7 is the max number of selected courses
            for student in students:
                try:
                    course = map(i - 1, student.prefs)
                    if course.period == 0:
                        continue
                    room = roomLookup[course.room] # room of c
                    period = course.period # period of c
                    if ((len(course.students) < room.capacity) and (not (period in busyPeriods))):
                        course.students.append(student)         # for Course object
                        student.coursesAssigned.append(course)  # for Student object
                        student.busyPeriods.append(course.period)

                except:     # if out of range
                    continue


    '''
    # For Extension 3
    def prefsRank(self):
        classNums = len(self.prefs)
        self.prefsRank = random.sample(range(1,classNums + 1), classNums) # 1-4 list corresponding to prefs.
    # '''
