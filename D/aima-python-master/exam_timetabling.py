from csp import CSP, backtracking_search, mac, mrv, forward_checking, min_conflicts
import pandas as pd

class ExamTimetablingCSP(CSP):
    def __init__(self, courses, timeslots, constraints, course_info):

        neighbors = {course: [other for other in courses if other != course] for course in courses}

        domains = {course: timeslots[:] for course in courses}
        super().__init__(courses, domains, neighbors, self.constraint)

        self.course_info = course_info
        self.no_overlap = constraints['no_overlap']
        self.difficult = constraints['difficult']
        self.same_semester = constraints['same_semester']

    def constraint(self, A, a, B, b):
        """Custom constraints for exam timetabling."""
        if a == b:
            # kanena mathima den prepei na einai sthn idia wra 
            return False

        day_a, time_a = a.split()
        day_b, time_b = b.split()

        # If these courses must not overlap (e.g., both labs)
        if (A, B) in self.no_overlap or (B, A) in self.no_overlap:
            if day_a == day_b:
                return False

        # duskola mathimata, diafora 2 hmerwn 
        if (A, B) in self.difficult or (B, A) in self.difficult:
            if abs(int(day_a.replace('Day', '')) - int(day_b.replace('Day', ''))) < 2:
                return False

        # idios kathigitis, allh hmera Same professor courses on different days
        if self.course_info[A]['professor'] == self.course_info[B]['professor']:
            if day_a == day_b:
                return False

        # idio eksamhno, allh hmera Same semester courses on different days
        if (A, B) in self.same_semester or (B, A) in self.same_semester:
            if day_a == day_b:
                return False

        return True

def validate_solution(solution, course_info, constraints): # func to check on my result
    time_slot_usage = {}
    valid = True

    print("Validating solution...\n")

    for course, time_slot in solution.items():
        # constraint 1
        if time_slot in time_slot_usage:
            print(f"Conflict: Multiple exams scheduled in {time_slot} (e.g., {course} and {time_slot_usage[time_slot]})")
            valid = False
        else:
            time_slot_usage[time_slot] = course

    
    for course1, time_slot1 in solution.items():
        for course2, time_slot2 in solution.items():
            if course1 < course2: # constraint 2
                day1, _ = time_slot1.split()
                day2, _ = time_slot2.split()

                # idios kathigitis allh hmera
                if course_info[course1]['professor'] == course_info[course2]['professor']:
                    if day1 == day2:
                        print(f"Conflict: {course1} and {course2} (same professor) on {day1}")
                        valid = False

                # duskola mathimata prepei na exoun diafora 2 toul hmerwn
                if (course1, course2) in constraints['difficult'] or (course2, course1) in constraints['difficult']:
                    d1 = int(day1.replace("Day", ""))
                    d2 = int(day2.replace("Day", ""))
                    if abs(d1 - d2) < 2:
                        print(f"Conflict: Difficult courses {course1} and {course2} are too close in time (Days {d1} and {d2})")
                        valid = False

                # idio eksamino allh imera
                if (course1, course2) in constraints['same_semester'] or (course2, course1) in constraints['same_semester']:
                    if day1 == day2:
                        print(f"Conflict: Same semester courses {course1} and {course2} on the same day ({day1})")
                        valid = False

    if valid:
        print("Solution is valid.")
    else:
        print("Solution has conflicts.")

if __name__ == "__main__":
    file_path = "h3-data.csv"
    course_data = pd.read_csv(file_path)

    # Convert TRUE/FALSE to bool
    course_data['Δύσκολο (TRUE/FALSE)'] = course_data['Δύσκολο (TRUE/FALSE)'].apply(lambda x: True if str(x).strip().upper() == 'TRUE' else False)
    course_data['Εργαστήριο (TRUE/FALSE)'] = course_data['Εργαστήριο (TRUE/FALSE)'].apply(lambda x: True if str(x).strip().upper() == 'TRUE' else False)

    courses = course_data['Μάθημα'].tolist()
    course_info = {
        row['Μάθημα']: {
            'professor': row['Καθηγητής'],
            'difficult': row['Δύσκολο (TRUE/FALSE)'],
            'laboratory': row['Εργαστήριο (TRUE/FALSE)']
        }
        for _, row in course_data.iterrows()
    }

    # Timeslots: 21 days × 3 slots per day
    timeslots = [f"Day{day} {hour}" for day in range(1, 22) for hour in ['9-12', '12-3', '3-6']]

    # Semester constraints
    same_semester_constraints = []
    semester_groups = course_data.groupby('Εξάμηνο')['Μάθημα'].apply(list)
    for _, courses_in_semester in semester_groups.items():
        for i, course1 in enumerate(courses_in_semester):
            for course2 in courses_in_semester[i+1:]:
                same_semester_constraints.append((course1, course2))

    no_overlap_constraints = []
    difficult_constraints = []
    for course1, info1 in course_info.items():
        for course2, info2 in course_info.items():
            if course1 < course2:
                # Both labs => no_overlap
                if info1['laboratory'] and info2['laboratory']:
                    no_overlap_constraints.append((course1, course2))
                # Both difficult => difficult constraints
                if info1['difficult'] and info2['difficult']:
                    difficult_constraints.append((course1, course2))

    constraints = {
        'no_overlap': no_overlap_constraints,
        'difficult': difficult_constraints,
        'same_semester': same_semester_constraints
    }


    exam_csp = ExamTimetablingCSP(courses, timeslots, constraints, course_info) # csp init

    print("Solving using MRV + Forward Checking...") # FC solution
    result_mrv_fc = backtracking_search(
        exam_csp,
        select_unassigned_variable=mrv,
        inference=forward_checking
    )

    if result_mrv_fc:
        print("\nResult (FC):")
        for course, time in result_mrv_fc.items():
            print(f"{course}: {time}")
        print("\nValidating the solution (FC):\n")
        validate_solution(result_mrv_fc, course_info, constraints)
    else:
        print("No solution found with FC.")

    exam_csp = ExamTimetablingCSP(courses, timeslots, constraints, course_info) # csp reset
    print("\nSolving using MRV + MAC...") # mac solution
    result_mrv_mac = backtracking_search(
        exam_csp,
        select_unassigned_variable=mrv,
        inference=mac
    )

    if result_mrv_mac:
        print("\nResult (MAC):")
        for course, time in result_mrv_mac.items():
            print(f"{course}: {time}")
        print("\nValidating the solution (MAC):\n")
        validate_solution(result_mrv_mac, course_info, constraints)
    else:
        print("No solution found with MAC.")

   
    exam_csp = ExamTimetablingCSP(courses, timeslots, constraints, course_info) # csp reset
    print("\nSolving using Min-Conflicts...") # min conflict solution
    result_min_conflicts = min_conflicts(exam_csp, max_steps=1000) # can use values otherthan 1o00

    if result_min_conflicts:
        print("\nResult (Min-Conflicts):")
        for course, time in result_min_conflicts.items():
            print(f"{course}: {time}")
        print("\nValidating the solution (Min-Conflicts):\n")
        validate_solution(result_min_conflicts, course_info, constraints)
    else:
        print("No solution found with Min-Conflicts.")
