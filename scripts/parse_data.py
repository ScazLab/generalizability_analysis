#!/usr/bin/env python3
import os
import copy

# starting task
START_TASK_DRAW = 1
START_TASK_HANOI = 2

# interruption task
START_INTERRUPTION_STROOP = 1
START_INTERRUPTION_MATH = 2

# condition
CONDITION_SWITCH_TASK = 1
CONDITION_SWITCH_INTERRUPTION = 2


class DemographicData():
    def __init__(self):
        self.age = -1
        self.gender = ""
        self.education = ""

    def parse(self, pieces):
        self.age = pieces[3]
        self.gender = pieces[4]
        self.education = pieces[5]


class DiagnosisData():
    def __init__(self):
        self.asd = False
        self.color_blind = False
        self.hearing_impaired = False
        self.adhd = False
        self.prefer_not_to_say = False
        self.none = False

    def parse(self, pieces):
        self.asd = pieces[3]
        self.color_blind = pieces[4]
        self.hearing_impaired = pieces[5]
        self.adhd = pieces[6]
        self.prefer_not_to_say = pieces[7]
        self.none = pieces[8]


class EffortData():
    def __init__(self):
        self.task = ""
        self.effort = 0
        self.confidence = 0

    def parse(self, pieces):
        self.task = pieces[2]
        self.effort = pieces[3]
        self.confidence = pieces[4]


class SurveyData():
    def __init__(self):
        self.demographics = None
        self.diagnosis = None
        self.effort = []


class HanoiMove():
    def __init__(self):
        # ~ self.p1 = ""
        # ~ self.p2 = ""
        # ~ self.p3 = ""
        self.pegs = ""
        self.status = "incomplete"
        self.time = 0
        self.after_interruption = 0

    def parse(self, pieces):
        self.pegs = pieces[3]
        self.status = pieces[5]
        self.time = pieces[8]


class HanoiTask():
    def __init__(self):
        self.hanoi_move_list = []
        self.time_to_complete = 0
        self.moves_to_complete = 0
        self.completed = False


class HanoiData():
    def __init__(self):
        self.hanoi_tasks = []
        self.average_time_move_piece = 0
        self.average_time_move_after_interruption = 0
        self.average_time_move_not_after_interruption = 0
        self.average_moves_to_complete = 0
        self.average_time_to_complete = 0


class DrawTask():
    def __init__(self):
        self.answer = ""
        self.correct_answer = ""
        self.percentage_correct = 0
        self.time = 0
        self.after_interruption = 0

    def parse(self, pieces):
        self.answer = pieces[3]
        self.correct_answer = pieces[4]
        self.percentage_correct = pieces[5]
        self.time = pieces[7]


class DrawData():
    def __init__(self):
        self.draw_tasks = []
        self.average_time_to_answer = 0
        self.average_time_to_answer_after_interruption = 0
        self.average_time_to_answer_after_no_interruption = 0
        self.average_correctness = 0
        self.average_correctness_after_interruption = 0
        self.average_correctness_after_no_interruption = 0


class StroopTask():
    def __init__(self):
        self.correct = False
        self.time = 0

    def parse(self, pieces):
        if (pieces[5] == "CORRECT"):
            self.correct = True
        else:
            self.correct = False
        self.time = pieces[8]


class StroopData():
    def __init__(self):
        self.stroop_tasks = []
        self.average_time = 0
        self.average_correctness = 0


class MathTask():
    def __init__(self):
        self.correct = False
        self.time = 0

    def parse(self, pieces):
        if (pieces[5] == "CORRECT"):
            self.correct = True
        else:
            self.correct = False
        self.time = pieces[8]


class MathData():
    def __init__(self):
        self.math_tasks = []
        self.average_time = 0
        self.average_correctness = 0


class Task():
    def __init__(self, name):
        self.name = name
        self.task = None


class Interruption():
    def __init__(self, name):
        self.name = name
        self.interruption = None


class Participant():
    def __init__(self, p_id):
        self.p_id = p_id

        self.starting_task = 0
        self.starting_interruption = 0
        self.condition = 0
        self.survey = None

        self.tutorial_hanoi = None
        self.tutorial_draw = None
        self.tutorial_stroop = None
        self.tutorial_math = None

        self.assessment_task = None
        self.assessment_interruption = None
        self.training_task = None
        self.training_interruption = None
        self.testing_task = None
        self.testing_interruption = None

    def print_participant(self):
        pass

    # ~ print (vars(self.starting_task ))
    # ~ print (vars(self.starting_interruption))
    # ~ print (vars(self.condition ))
    # ~ print (vars(self.survey))

    # ~ print (vars(self.tutorial_hanoi))
    # ~ print (vars(self.tutorial_draw ))
    # ~ print (vars(self.tutorial_stroop))
    # ~ print (vars(self.tutorial_math ))

    # ~ print (vars(self.assessment_task.task.hanoi_tasks[0].hanoi_move_list[0]))
    # ~ print ((self.assessment_task.task))
    # ~ print (vars(self.assessment_interruption.interruption))
    # ~ print (vars(self.training_task.task.draw_tasks[15] ))
    # ~ print (vars(self.training_interruption.interruption.math_tasks[0]))
    # ~ print (vars(self.testing_task.task ))
    # ~ print (vars(self.testing_interruption.interruption))

    def parse_condition(self, pieces):
        int_task = int(pieces[1])
        main_task = int(pieces[2])
        condition = int(pieces[3])

        # ~ print (int_task)
        # ~ print (main_task)
        # ~ print (condition)
        if (int_task == START_INTERRUPTION_MATH):
            self.starting_interruption = START_INTERRUPTION_MATH
        if (int_task == START_INTERRUPTION_STROOP):
            self.starting_interruption = START_INTERRUPTION_STROOP
        if (main_task == START_TASK_DRAW):
            self.starting_task = START_TASK_DRAW
        if (main_task == START_TASK_HANOI):
            self.starting_task = START_TASK_HANOI
        if (condition == CONDITION_SWITCH_INTERRUPTION):
            self.condition = CONDITION_SWITCH_INTERRUPTION
        if (condition == CONDITION_SWITCH_TASK):
            self.condition = CONDITION_SWITCH_TASK


###############################################################################

# f = open("/home/nicole/coding/generalizability_analysis/pilot_data/265411-861179.txt", "r")
filepath = "../generalizability_analysis/pilot_data/265411-861179.txt"
filename = os.path.basename(filepath)
p_id = os.path.splitext(filename)[0]
f = open(filepath, "r")

# f = open("../generalizability_analysis/pilot_data/265411-861179.txt", "r")

p = Participant(p_id)
# print(p.p_id)
sv = SurveyData()

ht = HanoiTask()

h = HanoiData()
d = DrawData()
s = StroopData()
m = MathData()

SCENE_SURVEYS = 1
SCENE_TUTORIAL = 2
SCENE_ASSESSEMENT = 3
SCENE_TRAINING = 4
SCENE_TESTING = 5

scene = SCENE_SURVEYS

line_n = 0
for line in f:
    pieces = line.split(',')
    line_n += 1
    if (line_n == 2):  # the second line has the information about the condition
        p.parse_condition(pieces)

    if (pieces[0]) == "SURVEYS":
        if (pieces[1] == "SURVEY"):
            if (pieces[2] == "DEMOGRAPHICS"):
                dd = DemographicData()
                dd.parse(pieces)
                sv.demographics = dd
            if (pieces[2] == "DIAGNOSIS"):
                diag = DiagnosisData()
                diag.parse(pieces)
                sv.diagnosis = diag

    if (pieces[0] == "TUTORIAL"):
        if (scene != SCENE_TUTORIAL):
            scene = SCENE_TUTORIAL
        if (pieces[1] == "INTERRUPTION"):
            if (pieces[2] == "stroop"):
                st = StroopTask()
                st.parse(pieces)
                s.stroop_tasks.append(st)
            if (pieces[2] == "area"):
                ma = MathTask()
                ma.parse(pieces)
                m.math_tasks.append(ma)
        if (pieces[1] == "PRIMARY"):
            if (pieces[2] == "HANOI"):
                han = HanoiMove()
                han.parse(pieces)
                ht.hanoi_move_list.append(han)
                if (han.status == "complete"):
                    # ~ print ("complete")
                    h.hanoi_tasks.append(ht)
                    ht = HanoiTask()
            if (pieces[2] == "path"):
                dr = DrawTask()
                dr.parse(pieces)
                d.draw_tasks.append(dr)

    if (pieces[0]) == "ASSESSMENT":
        if (scene != SCENE_ASSESSEMENT):
            scene = SCENE_ASSESSEMENT
            p.tutorial_hanoi = copy.deepcopy(h)
            p.tutorial_draw = copy.deepcopy(d)
            p.tutorial_stroop = copy.deepcopy(s)
            p.tutorial_math = copy.deepcopy(m)

            h = HanoiData()
            d = DrawData()
            s = StroopData()
            m = MathData()

        if (pieces[1] == "INTERRUPTION"):
            if (pieces[2] == "stroop"):
                st = StroopTask()
                st.parse(pieces)
                s.stroop_tasks.append(st)
            if (pieces[2] == "area"):
                ma = MathTask()
                ma.parse(pieces)
                m.math_tasks.append(ma)
        if (pieces[1] == "PRIMARY"):
            if (pieces[2] == "HANOI"):
                han = HanoiMove()
                han.parse(pieces)
                ht.hanoi_move_list.append(han)
                if (han.status == "complete"):
                    h.hanoi_tasks.append(ht)
                    ht = HanoiTask()
            if (pieces[2] == "path"):
                dr = DrawTask()
                dr.parse(pieces)
                d.draw_tasks.append(dr)
                # p = PathTask()
                # p.parse(pieces)
                # d.draw_tasks.append(dr)
        if (pieces[1] == "SURVEY"):
            ef = EffortData()
            ef.parse(pieces)
            sv.effort.append(ef)

    if (pieces[0] == "TRAINING"):
        if (scene != SCENE_TRAINING):
            scene = SCENE_TRAINING
            if (p.starting_task == START_TASK_DRAW):
                t = Task("draw")
                t.task = copy.deepcopy(d)
                p.assessment_task = t
            if (p.starting_task == START_TASK_HANOI):
                t = Task("hanoi")
                t.task = copy.deepcopy(h)
                p.assessment_task = t
            if (p.starting_interruption == START_INTERRUPTION_MATH):
                i = Interruption("math")
                i.interruption = copy.deepcopy(m)
                p.assessment_interruption = i
            if (p.starting_interruption == START_INTERRUPTION_STROOP):
                i = Interruption("stroop")
                i.interruption = copy.deepcopy(s)
                p.assessment_interruption = i

            h = HanoiData()
            d = DrawData()
            s = StroopData()
            m = MathData()

        if (pieces[1] == "INTERRUPTION"):
            if (pieces[2] == "stroop"):
                st = StroopTask()
                st.parse(pieces)
                s.stroop_tasks.append(st)
            if (pieces[2] == "area"):
                ma = MathTask()
                ma.parse(pieces)
                m.math_tasks.append(ma)
        if (pieces[1] == "PRIMARY"):
            if (pieces[2] == "HANOI"):
                han = HanoiMove()
                han.parse(pieces)
                ht.hanoi_move_list.append(han)
                if (han.status == "complete"):
                    h.hanoi_tasks.append(ht)
                    ht = HanoiTask()
            if (pieces[2] == "path"):
                dr = DrawTask()
                dr.parse(pieces)
                d.draw_tasks.append(dr)
        if (pieces[1] == "SURVEY"):
            ef = EffortData()
            ef.parse(pieces)
            sv.effort.append(ef)

    if (pieces[0]) == "TESTING":
        if (scene != SCENE_TESTING):
            scene = SCENE_TESTING
            if (p.starting_task == START_TASK_DRAW and p.condition == CONDITION_SWITCH_TASK):
                t = Task("draw")
                t.task = copy.deepcopy(h)
                p.training_task = t
            if (p.starting_task == START_TASK_HANOI and p.condition == CONDITION_SWITCH_TASK):
                t = Task("hanoi")
                t.task = copy.deepcopy(d)
                p.training_task = t
            if (p.starting_task == START_TASK_DRAW and p.condition == CONDITION_SWITCH_INTERRUPTION):
                t = Task("draw")
                t.task = copy.deepcopy(d)
                p.training_task = t
            if (p.starting_task == START_TASK_HANOI and p.condition == CONDITION_SWITCH_INTERRUPTION):
                t = Task("hanoi")
                t.task = copy.deepcopy(h)
                p.training_task = t

            if (p.starting_interruption == START_INTERRUPTION_MATH and p.condition == CONDITION_SWITCH_TASK):
                i = Interruption("math")
                i.interruption = copy.deepcopy(m)
                p.training_interruption = i
                print("math tasks count?: ", len(i.interruption.math_tasks))
                print("math total time?: ", i.interruption.average_time)

                mt = MathTask()
                mt.parse(pieces)                                       
                corrects = mt.parse(pieces) == "CORRECT"
                print("correctness of maths in iteration?: ", corrects)

            if (p.starting_interruption == START_INTERRUPTION_STROOP and p.condition == CONDITION_SWITCH_TASK):
                i = Interruption("stroop")
                i.interruption = copy.deepcopy(s)
                p.training_interruption = i
            if (p.starting_interruption == START_INTERRUPTION_STROOP and p.condition == CONDITION_SWITCH_INTERRUPTION):
                i = Interruption("stroop")
                i.interruption = copy.deepcopy(s)
                p.training_interruption = i
            if (p.starting_interruption == START_INTERRUPTION_MATH and p.condition == CONDITION_SWITCH_INTERRUPTION):
                i = Interruption("math")
                i.interruption = copy.deepcopy(m)
                p.training_interruption = i

            h = HanoiData()
            d = DrawData()
            s = StroopData()
            m = MathData()

        if (pieces[1] == "INTERRUPTION"):
            if (pieces[2] == "stroop"):
                st = StroopTask()
                st.parse(pieces)
                s.stroop_tasks.append(st)
            if (pieces[2] == "area"):
                ma = MathTask()
                ma.parse(pieces)
                m.math_tasks.append(ma)
        if (pieces[1] == "PRIMARY"):
            if (pieces[2] == "HANOI"):
                han = HanoiMove()
                han.parse(pieces)
                ht.hanoi_move_list.append(han)
                if (han.status == "complete"):
                    h.hanoi_tasks.append(ht)
                    ht = HanoiTask()
            if (pieces[2] == "path"):
                dr = DrawTask()
                dr.parse(pieces)
                d.draw_tasks.append(dr)
        if (pieces[1] == "SURVEY"):
            ef = EffortData()
            ef.parse(pieces)
            sv.effort.append(ef)

if (p.starting_task == START_TASK_DRAW):
    t = Task("draw")
    t.task = copy.deepcopy(d)
    p.testing_task = t
    print("number of draw tasks", len(p.testing_task.task.draw_tasks))
if (p.starting_task == START_TASK_HANOI):
    t = Task("hanoi")
    t.task = copy.deepcopy(h)
    p.testing_task = t
    print("number of hanoi tasks", len(t.task.hanoi_tasks))
if (p.starting_interruption == START_INTERRUPTION_MATH):
    i = Interruption("math")
    i.interruption = copy.deepcopy(m)
    p.testing_interruption = i
    print("number of math interruptions", len(p.testing_interruption.interruption.math_tasks))
if (p.starting_interruption == START_INTERRUPTION_STROOP):
    i = Interruption("stroop")
    i.interruption = copy.deepcopy(s)
    p.testing_interruption = i
    print("number of stroop interruptions", len(p.testing_interruption.interruption.stroop_tasks))
p.survey = sv

##########################################

# ~ print (vars(p.survey))
# ~ print(vars(p))
# ~ p.print_participant()
