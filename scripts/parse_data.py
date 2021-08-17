#!/usr/bin/env python3
import os
import copy
import fnmatch
import inspect
import statistics
import pandas as pd
import numpy as np


#starting task
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
        self.timeSpent = 0

    def parse(self, pieces, interruption_just_happened):
        self.pegs = pieces[3]
        self.status = pieces[5]
        self.time = pieces[8]
        self.after_interruption = interruption_just_happened
        self.timeSpent = pieces[6]



class HanoiTask():
    def __init__(self):
        self.hanoi_move_list = []
        self.time_to_complete = 0
        self.moves_to_complete = 0
        self.completed = False
        self.interrupted_during_task = False


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
        self.timeSpent = 0
        self.after_interruption = 0
        self.draw_response_list = []
        self.draw_tasks_responses = []
        self.interrupted_during_task = False

    def parse(self, pieces, interruption_just_happened):
        self.answer = pieces[3]
        self.correct_answer = pieces[4]
        self.percentage_correct = pieces[5]
        self.time = pieces[6]
        self.timeSpent = pieces[6]
        self.after_interruption = interruption_just_happened


class DrawData():
    def __init__(self):
        self.draw_tasks = []
        self.average_time_to_answer = 0
        self.average_time_to_answer_after_interruption = 0
        self.average_time_to_answer_after_no_interruption = 0
        self.average_correctness = 0
        self.average_correctness_after_interruption = 0
        self.average_correctness_after_no_interruption = 0
        self.averageTimeToAnswerDrawTaskEntirelyCorrect = 0


class StroopTask():
    def __init__(self):
        self.correct = False
        self.time = 0
        self.timeSpent = 0

    def parse(self, pieces):
        if (pieces[5] == "CORRECT"):
            self.correct = True
        else:
            self.correct = False
        self.time = pieces[8]
        self.timeSpent = pieces[6]


class StroopData():
    def __init__(self):
        self.stroop_tasks = []
        self.totalTime = 0
        self.average_time = 0
        self.average_correctness = 0


class MathTask():
    def __init__(self):
        self.correct = False
        self.time = 0
        self.timeSpent = 0

    def parse(self, pieces):
        if (pieces[5] == "CORRECT"):
            self.correct = True
        else:
            self.correct = False
        self.time = pieces[8]
        self.timeSpent = pieces[6]


class MathData():
    def __init__(self):
        self.math_tasks = []
        self.totalTime = 0
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

def lineNumber():
    # Returns the current line number
    return inspect.currentframe().f_back.f_lineno


###############################################################################

# f = open("/home/nicole/coding/generalizability_analysis/pilot_data/265411-861179.txt", "r")

directory = "../pilot_data/"
Matches = []
pid = []


averageTimeMathInterruptionsListAssess = []
stanDevAverageTimeMathInterruptionsListAssess = []
averageTimeMathInterruptionsListTrain = []
stanDevAverageTimeMathInterruptionsListTrain = []
averageTimeMathInterruptionsListTest = []
stanDevAverageTimeMathInterruptionsListTest = []

averageTimeStroopInterruptionsListAssess = []
stanDevAverageTimeStroopInterruptionsListAssess = []
averageTimeStroopInterruptionsListTrain = []
stanDevAverageTimeStroopInterruptionsListTrain = []
averageTimeStroopInterruptionsListTest = []
stanDevAverageTimeStroopInterruptionsListTest = []

averageTimeToAnswerDrawTaskEntirelyCorrectListAssess = []
averageTimeToAnswerDrawTaskEntirelyCorrectListTrain = []
averageTimeToAnswerDrawTaskEntirelyCorrectListTest = []

averageNumberOfMovesBeforeCompleteForAllHanoiTasksListAssess = []
averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain = []
averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTest = []

avgTimesToCompletionForAllHanoiTasksListAssessment = []
avgTimesToCompletionForAllHanoiTasksListTraining = []
avgTimesToCompletionForAllHanoiTasksListTesting = []

averageTimeRespondAfterInterruptionListAssessment =[]
averageTimeRespondAfterInterruptionListTraining =[]
averageTimeRespondAfterInterruptionListTesting =[]

averageTimeMoveAfterInterruptionListAssessment =[]
averageTimeMoveAfterInterruptionListTraining =[]
averageTimeMoveAfterInterruptionListTesting =[]

all_participants = []
pattern = '*.txt'
files = os.listdir(directory)
Matches = fnmatch.filter(files, pattern)
for filenames in Matches:
    f = open(directory+filenames, "r")
    filename = os.path.basename(filenames)
    p_id = os.path.splitext(filename)[0]
    p = Participant(p_id)
    pid.append(p.p_id)

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
    
    interruption_just_happened = 0
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
                    han.parse(pieces, 0)
                    ht.hanoi_move_list.append(han)
                    if (han.status == "complete"):
                        # ~ print ("complete")
                        h.hanoi_tasks.append(ht)
                        ht = HanoiTask()
                if (pieces[2] == "path"):
                    dr = DrawTask()
                    dr.parse(pieces, 0)
                    dr.draw_response_list.append(dr)
                    if (dr.percentage_correct == "25%" or "50%" or "100%"):
                        dr.draw_tasks_responses.append(dr)


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
                interruption_just_happened = 1
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
                    han.parse(pieces, interruption_just_happened)
                    ht.hanoi_move_list.append(han)
                    if (interruption_just_happened == 1):
                        ht.interrupted_during_task = True
                    if (han.status == "complete"):
                        h.hanoi_tasks.append(ht)
                        ht = HanoiTask()
                if (pieces[2] == "path"):
                    dr = DrawTask()
                    dr.parse(pieces, interruption_just_happened)
                    d.draw_tasks.append(dr)
                    dr.draw_response_list.append(dr)
                    if (interruption_just_happened == 1):
                        dr.interrupted_during_task = True
                    if (dr.percentage_correct == "25%" or "50%" or "100%"):
                        dr.draw_tasks_responses.append(dr)

                interruption_just_happened = 0
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
                interruption_just_happened = 1
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
                    han.parse(pieces, interruption_just_happened)
                    ht.hanoi_move_list.append(han)
                    if (interruption_just_happened == 1):
                        ht.interrupted_during_task = True
                    if (han.status == "complete"):
                        h.hanoi_tasks.append(ht)
                        ht = HanoiTask()
                if (pieces[2] == "path"):
                    dr = DrawTask()
                    dr.parse(pieces, interruption_just_happened)
                    d.draw_tasks.append(dr)
                    dr.draw_response_list.append(dr)
                    if (interruption_just_happened == 1):
                        dr.interrupted_during_task = True
                    if (dr.percentage_correct == "25%" or "50%" or "100%"):
                        dr.draw_tasks_responses.append(dr)
            if (pieces[1] == "SURVEY"):
                ef = EffortData()
                ef.parse(pieces)
                sv.effort.append(ef)

        if (pieces[0]) == "TESTING":
            if (scene != SCENE_TESTING):
                scene = SCENE_TESTING
                if (p.starting_task == START_TASK_DRAW and p.condition == CONDITION_SWITCH_TASK):
                    t = Task("hanoi")
                    t.task = copy.deepcopy(h)
                    p.training_task = t
                if (p.starting_task == START_TASK_HANOI and p.condition == CONDITION_SWITCH_TASK):
                    t = Task("draw")
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
                    # ~ print ("math")
                    # ~ print (m)
                    i.interruption = copy.deepcopy(m)
                    p.training_interruption = i
                if (p.starting_interruption == START_INTERRUPTION_STROOP and p.condition == CONDITION_SWITCH_TASK):
                    i = Interruption("stroop")
                    i.interruption = copy.deepcopy(s)
                    p.training_interruption = i
                if (p.starting_interruption == START_INTERRUPTION_STROOP and p.condition == CONDITION_SWITCH_INTERRUPTION):
                    i = Interruption("math")
                    i.interruption = copy.deepcopy(m)
                    p.training_interruption = i
                if (p.starting_interruption == START_INTERRUPTION_MATH and p.condition == CONDITION_SWITCH_INTERRUPTION):
                    i = Interruption("stroop")
                    i.interruption = copy.deepcopy(s)
                    p.training_interruption = i

                h = HanoiData()
                d = DrawData()
                s = StroopData()
                m = MathData()

            if (pieces[1] == "INTERRUPTION"):
                interruption_just_happened = 1
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
                    han.parse(pieces, interruption_just_happened)
                    ht.hanoi_move_list.append(han)
                    if (interruption_just_happened == 1):
                        ht.interrupted_during_task = True
                    if (han.status == "complete"):
                        h.hanoi_tasks.append(ht)
                        ht = HanoiTask()
                if (pieces[2] == "path"):
                    dr = DrawTask()
                    dr.parse(pieces, interruption_just_happened)
                    d.draw_tasks.append(dr)
                    dr.draw_response_list.append(dr)
                    if (interruption_just_happened == 1):
                        dr.interrupted_during_task = True
                    if (dr.percentage_correct == "25%" or "50%" or "100%"):
                        dr.draw_tasks_responses.append(dr)
            if (pieces[1] == "SURVEY"):
                ef = EffortData()
                ef.parse(pieces)
                sv.effort.append(ef)

    if (p.starting_task == START_TASK_DRAW):
        t = Task("draw")
        t.task = copy.deepcopy(d)
        p.testing_task = t
    if (p.starting_task == START_TASK_HANOI):
        t = Task("hanoi")
        t.task = copy.deepcopy(h)
        p.testing_task = t
    if (p.starting_interruption == START_INTERRUPTION_MATH):
        i = Interruption("math")
        i.interruption = copy.deepcopy(m)
        p.testing_interruption = i
    if (p.starting_interruption == START_INTERRUPTION_STROOP):
        i = Interruption("stroop")
        i.interruption = copy.deepcopy(s)
        p.testing_interruption = i
    p.survey = sv
    all_participants.append(p)
    
   

##############################################################################################

# PARTICIPANT DETAILS
id_arr = []
conditions_arr = []
starting_task_arr = []
starting_interruption_arr = []

# ASSESSMENT (a) VARIABLES
a_i_name = []     # interruption (i) name
a_i_count = []    # total number of interruptions given
a_i_percentage = [] # percentage of average correctness across interruptions
a_i_time = []     # time during correct responses to interruptions
a_i_times = []    # aggregated time of average times for interruptions

a_p_name = []                 # primary (p) task name
a_p_count = []                # total number of tasks given
a_p_correctness = []          # weighted correctness across all tasks
a_p_time = []                 # time during correct responses to tasks
a_p_times = []                # average times to complete tasks
a_p_percentage = []           # percentage of average correctness across tasks (draw only)
a_p_percentage100 = []        # percentages of 100% correct responses to tasks (draw only)
a_p_resumption = []           # time to resume after interruption (hanoi only ??)
a_p_resumptions = []          # times to resume after interruptions (hanoi only ??)
a_p_interruptions = []        # total number of consective batch of interruptions during task (hanoi only)
a_p_movestotal = []           # total number of moves to complete all tasks (hanoi only)
a_p_movetasktime = []         # average time after a move (hanoi only)
a_p_moveinterruptedtime = []  # average time to move after interruption (hanoi only ??)

# TRAINING (tr) VARIABLES
tr_i_name = []         # interruption name
tr_i_count = []        # total number of interruptions given
tr_i_percentage = []   # percentage of correct reposnses
tr_i_time = []         # time during correct responses to interruptions
tr_i_times = []        # aggregated time of average times for interruptions

tr_p_name = []                 # primary (p) task name
tr_p_count = []                # total number of tasks given
tr_p_correctness = []          # weighted correctness across all tasks
tr_p_time = []                 # time during correct responses to tasks
tr_p_times = []                # average times to complete tasks
tr_p_percentage = []           # percentage of average correctness across tasks (draw only)
tr_p_percentage100 = []        # percentages of 100% correct responses to tasks (draw only)
tr_p_resumption = []           # time to resume after interruption (hanoi only ??)
tr_p_resumptions = []          # times to resume after interruptions (hanoi only ??)
tr_p_interruptions = []        # total number of consective batch of interruptions during task (hanoi only)
tr_p_movestotal = []           # total number of moves to complete all tasks (hanoi only)
tr_p_movetasktime = []         # average time after a move (hanoi only)
tr_p_moveinterruptedtime = []  # average time to move after interruption (hanoi only ??)

# TESTING (te) VARIABLES
te_i_name = []         # interruption name
te_i_count = []        # total number of interruptions given
te_i_percentage = []   # percentage of correct reposnses
te_i_time = []         # time during correct responses to interruptions
te_i_times = []        # aggregated time of average times for interruptions

te_p_name = []                 # primary (p) task name
te_p_count = []                # total number of tasks given
te_p_correctness = []          # correctness across all tasks
te_p_time = []                 # time during correct responses to tasks
te_p_times = []                # average times to complete tasks
te_p_percentage = []           # percentage of average correctness across tasks (draw only)
te_p_percentage100 = []        # percentages of 100% correct responses to tasks (draw only)
te_p_resumption = []           # time to resume after interruption (hanoi only ??)
te_p_resumptions = []          # times to resume after interruptions (hanoi only ??)
te_p_interruptions = []        # total number of consective batch of interruptions during task (hanoi only)
te_p_movestotal = []           # total number of moves to complete all tasks (hanoi only)
te_p_movetasktime = []         # average time after a move (hanoi only)
te_p_moveinterruptedtime = []  # average time to move after interruption (hanoi only ??)

for p in all_participants:
    print("\n")
    print("*********************** Data for Participant ID: "+p.p_id+ " starts here  ***********************","\n")
    print("The condition is:" + str(p.condition))
    print("The starting task is:" + str(p.starting_task))
    print("The starting interruption is:" + str(p.starting_interruption))

    id_arr.append(p.p_id)
    conditions_arr.append(p.condition)
    starting_task_arr.append(p.starting_task)
    starting_interruption_arr.append(p.starting_interruption)

    # Analyses
    # Participant's average time for correct responses to math interruptions
    # Average time for correct responses to math interruptions during ASSESSMENT phase
    if p.assessment_interruption.name == "math":
        print("v--------------------------Assessment Phase--------------------------v")
        print("Interruptive Task: ", p.assessment_interruption.name)
        mathData=MathData()
        totalTime = mathData.totalTime
        correctResponseCount = 0
        for correctResponses in p.assessment_interruption.interruption.math_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
                # print("correct checks: ", correctResponses.correct)
            totalTime += float(correctResponses.timeSpent)
            # print(totalTime)
            # correctResponseCount+=1
        # print("count of correct responses: ", correctResponseCount)
        totalNumberOfmathTasks = len(p.assessment_interruption.interruption.math_tasks)
        print("totalNumberOfmathTasks_Assessment for: "+p.p_id+ "is: ", totalNumberOfmathTasks)
        # print("getting attribute: ", getattr(mathData, 'average_time'))
        mathData.average_time = totalTime/totalNumberOfmathTasks
        averageTimeMathInterruptions = mathData.average_time
        percentCorrect = correctResponseCount/totalNumberOfmathTasks
        print("Time during correct responses to math interruptions during assessment phase for "+p.p_id+ " is: ", averageTimeMathInterruptions,"seconds")
        print("Percentage correct responses to interruptions math during assessment phase for "+p.p_id+ " is: "+str(percentCorrect*100)+"%","\n")
        averageTimeMathInterruptionsListAssess.append(mathData.average_time)
        print("averageTimeMathInterruptionsAggregated_ListAssess: ", averageTimeMathInterruptionsListAssess)
        print("^--------------------------End of Assessment Phase--------------------------^")

        a_i_name.append(p.assessment_interruption.name)
        a_i_count.append(totalNumberOfmathTasks)
        a_i_percentage.append(percentCorrect)
        a_i_time.append(averageTimeMathInterruptions)
        a_i_times.append(averageTimeMathInterruptionsListAssess)

    # Average time for correct responses to math interruptions during TRAINING phase
    if p.training_interruption.name == "math":
        print("v--------------------------Training Phase--------------------------v")
        print("Interruptive Task: ", p.training_interruption.name)
        mathData = MathData()
        # ~ print("p.training_interruption.name: ", p.training_interruption.name)
        # ~ print('BUG HEREEEEEEEEEE at line {}'.format(lineNumber()), "\n")
        correctResponseCount = 0
        totalTime = mathData.totalTime
        # ~ print (p.training_interruption.interruption)
        for correctResponses in p.training_interruption.interruption.math_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        # ~ print("count of correct responses: ", correctResponseCount)
        totalNumberOfmathTasks = len(p.training_interruption.interruption.math_tasks)
        print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
        mathData.average_time = totalTime/totalNumberOfmathTasks
        averageTimeMathInterruptions = mathData.average_time
        percentCorrect = correctResponseCount / totalNumberOfmathTasks
        print("Time during correct responses to math interruptions during Training phase for "+p.p_id+ " is: ",averageTimeMathInterruptions, "seconds")
        print("Percentage correct responses to interruptions math during Training phase for "+p.p_id+ " is: "+str(percentCorrect * 100)+"%","\n")
        averageTimeMathInterruptionsListTrain.append(mathData.average_time)
        print("averageTimeMathInterruptionsListTrain: ", averageTimeMathInterruptionsListTrain)
        print("^--------------------------End of Training Phase--------------------------^")

        tr_i_name.append(p.training_interruption.name)
        tr_i_count.append(len(p.training_interruption.interruption.math_tasks))
        tr_i_percentage.append(percentCorrect)
        tr_i_time.append(averageTimeMathInterruptions)
        tr_i_times.append(averageTimeMathInterruptionsListTrain)

    # Average time for correct responses to math interruptions during TESTING phase
    if p.testing_interruption.name == "math":
        print("v--------------------------Testing Phase--------------------------v")
        print("Interruptive Task: ", p.testing_interruption.name)
        mathData = MathData()
        correctResponseCount = 0
        totalTime = mathData.totalTime
        for correctResponses in p.testing_interruption.interruption.math_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        totalNumberOfmathTasks = len(p.testing_interruption.interruption.math_tasks)
        mathData.average_time = totalTime/totalNumberOfmathTasks
        averageTimeMathInterruptions = mathData.average_time
        percentCorrect = correctResponseCount / totalNumberOfmathTasks
        print("Time during correct responses to math interruptions during Testing phase for "+p.p_id+ " is: ",
              averageTimeMathInterruptions, "seconds")
        print("Percentage correct responses to interruptions math during Testing phase for "+p.p_id+ " is: "+str(percentCorrect * 100)+"%",
              "\n")
        averageTimeMathInterruptionsListTest.append(mathData.average_time)
        print("averageTimeMathInterruptionsListTest: ", averageTimeMathInterruptionsListTest)
        print("^--------------------------End of Testing Phase--------------------------^")

        te_i_name.append(p.testing_interruption.name)
        te_i_count.append(len(p.testing_interruption.interruption.math_tasks))
        te_i_percentage.append(percentCorrect)
        te_i_time.append(averageTimeMathInterruptions)
        te_i_times.append(averageTimeMathInterruptionsListTest)

    # Participant's average time for correct responses to stroop interruptions Assessment phase
    if p.assessment_interruption.name == "stroop":
        print("v--------------------------Assessment Phase--------------------------v")
        print("Interruptive Task: ", p.assessment_interruption.name)
        stroopData=StroopData()
        totalTime = stroopData.totalTime
        correctResponseCount = 0
        for correctResponses in p.assessment_interruption.interruption.stroop_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            # print(correctResponses.correct)
            totalTime += float(correctResponses.timeSpent)
            # print(totalTime)
        # print("count of correct responses: ", correctResponseCount)
        totalNumberOfStroopTasks = len(p.assessment_interruption.interruption.stroop_tasks)
        # print("totalNumberOfmathTasks: ", totalNumberOfStroopTasks)
        # print("getting attribute: ", getattr(mathData, 'average_time'))
        stroopData.average_time = totalTime/totalNumberOfStroopTasks
        averageTimeStroopInterruptions = stroopData.average_time
        percentCorrect = correctResponseCount / totalNumberOfStroopTasks
        print("Time during correct responses to stroop interruptions during Assessment phase for "+p.p_id+ " is: ",
              averageTimeStroopInterruptions, "seconds")
        print("Percentage correct responses to interruptions stroop during Assessment phase for "+p.p_id+ " is: "+str(percentCorrect * 100)+"%",
              "\n")
        averageTimeStroopInterruptionsListAssess.append(stroopData.average_time)
        # print("averageTimeStroopInterruptionsListAssess: ", averageTimeStroopInterruptionsListAssess)
        print("^--------------------------End of Assessment Phase--------------------------^")

        a_i_name.append(p.assessment_interruption.name)
        a_i_count.append(totalNumberOfStroopTasks)
        a_i_percentage.append(percentCorrect)
        a_i_time.append(averageTimeStroopInterruptions)
        a_i_times.append(averageTimeStroopInterruptionsListAssess)

    # Participant's average time for correct responses to stroop interruptions in Training phase
    if p.training_interruption.name == "stroop":
        print("v--------------------------Training Phase--------------------------v")
        print("Interruptive Task: ", p.training_interruption.name)
        # ~ print('BUG HEREEEEEEEEEE at line {}'.format(lineNumber()), "\n")
        stroopData = StroopData()
        totalTime = stroopData.totalTime
        # ~ print (p.training_interruption.interruption)
        correctResponseCount = 0
        for correctResponses in p.training_interruption.interruption.stroop_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        # print("count of correct responses: ", correctResponseCount)
        totalNumberOfStroopTasks = len(p.training_interruption.interruption.stroop_tasks)
        # print("totalNumberOfmathTasks: ", totalNumberOfStroopTasks)
        stroopData.average_time = totalTime/totalNumberOfStroopTasks
        averageTimeStroopInterruptions = stroopData.average_time
        percentCorrect = correctResponseCount / totalNumberOfStroopTasks
        print("Time during correct responses to stroop interruptions during Training phase for "+p.p_id+ " is: ",
              averageTimeStroopInterruptions, "seconds")
        print("Percentage correct responses to interruptions stroop during Training phase for "+p.p_id+ " is: "+str(percentCorrect * 100)+ "%",
              "\n")
        averageTimeStroopInterruptionsListTrain.append(stroopData.average_time)
        # ~ print("averageTimeStroopInterruptionsListTaining: ", averageTimeStroopInterruptionsListTrain)
        print("^--------------------------End of Training Phase--------------------------^")

        tr_i_name.append(p.training_interruption.name)
        tr_i_count.append(totalNumberOfStroopTasks)
        tr_i_percentage.append(percentCorrect)
        tr_i_time.append(averageTimeStroopInterruptions)
        tr_i_times.append(averageTimeStroopInterruptionsListTrain)

    # Average time for correct responses to stroop interruptions during TESTING phase
    if p.testing_interruption.name == "stroop":
        print("v--------------------------Testing Phase--------------------------v")
        # print("Primary Task: ", p.testing_interruption.name)
        print("Interruptive Task: ", p.testing_interruption.name)
        stroopData = StroopData()
        totalTime = stroopData.totalTime
        correctResponseCount = 0
        for correctResponses in p.testing_interruption.interruption.stroop_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        # print("count of correct responses: ", correctResponseCount)
        totalNumberOfStroopTasks = len(p.testing_interruption.interruption.stroop_tasks)
        # print("totalNumberOfmathTasks: ", totalNumberOfStroopTasks)
        stroopData.average_time = totalTime/totalNumberOfStroopTasks
        averageTimeStroopInterruptions = stroopData.average_time
        percentCorrect = correctResponseCount / totalNumberOfStroopTasks
        print("Time during correct responses to stroop interruptions during Testing phase for "+p.p_id+ " is: ",
              averageTimeStroopInterruptions, "seconds")
        print("Percentage correct responses to interruptions stroop during Testing phase for "+p.p_id+ " is: "+ str(percentCorrect * 100)+ "%",
              "\n")
        averageTimeStroopInterruptionsListTest.append(stroopData.average_time)
        # print("averageTimeStroopInterruptionsListTest: ", averageTimeStroopInterruptionsListTest)
        print("^--------------------------End of Testing Phase--------------------------^")

        te_i_name.append(p.testing_interruption.name)
        te_i_count.append(totalNumberOfStroopTasks)
        te_i_percentage.append(percentCorrect)
        te_i_time.append(averageTimeStroopInterruptions)
        te_i_times.append(averageTimeStroopInterruptionsListTest)

    # Participant's Draw task data
    # Average time, correctness, and ratio of 100% correct responses to Draw Task during ASSESSMENT phase
    # Aggregated time is save only when participant is 100% correct
    if p.assessment_task.name == "draw":
        print("v--------------------------Assessment Phase--------------------------v")
        print("Primary Task: ", p.assessment_task.name)
        print("Interruptive Task: ", p.assessment_interruption.name)
        #     totalNumberOfDrawTasks = len(p.assessment_task.task.draw_tasks)
        #     print("Number of draw tasks as primary task in assessment phase: ", totalNumberOfDrawTasks)
        drawTask = DrawTask()
        totalTimeEntirelyCorrect = drawTask.time
        totalDrawTaskEntirelyCorrect = 0
        fiftyPercentCorrect = 0
        twentyFivePercentCorrect = 0
        drawData = DrawData()
        for correctResponses in p.assessment_task.task.draw_tasks:
            # print("Each attempt: ", correctResponses.percentage_correct)
            if correctResponses.percentage_correct == "100%":
                totalDrawTaskEntirelyCorrect +=1
                # print("After answering a SINGLE draw task 100% correct")
                totalTimeEntirelyCorrect += float(correctResponses.time)
            # print("aggregated time: ", totalTimeEntirelyCorrect)
            if correctResponses.percentage_correct == "50%":
                fiftyPercentCorrect +=1
                # print("After answering a SINGLE draw task 50% correct")
            # print("aggregated fiftyPercentCorrect count: ", fiftyPercentCorrect)
            if correctResponses.percentage_correct == "25%":
                twentyFivePercentCorrect +=1
                # print("After answering a SINGLE draw task 25% correct")
            # print("aggregated twentyFivePercentCorrect count: ", twentyFivePercentCorrect)
        totalNumberOfDrawTasks = len(p.assessment_task.task.draw_tasks)
        # (17*100% + 1*50% + 2*25%)/total count * 100%
        weightedCorrectness = (totalDrawTaskEntirelyCorrect*1+fiftyPercentCorrect*.5+twentyFivePercentCorrect*.25)
        drawData.average_correctness = weightedCorrectness/totalNumberOfDrawTasks
        # print("totalDrawTaskEntirelyCorrect for "+p.p_id+ "during ASSESSMENT phase is: ", totalDrawTaskEntirelyCorrect)
        # print("totalNumberOfDrawTasks for "+p.p_id+ "during ASSESSMENT phase is: ", totalNumberOfDrawTasks)
        # print("getting attribute: ", getattr(mathData, 'average_time'))
        drawTask.percentage_correct = totalDrawTaskEntirelyCorrect/totalNumberOfDrawTasks
        print("Percentage of average correctness across Draw Tasks for", p.p_id,
              "during ASSESSMENT phase is " + str(drawData.average_correctness * 100) + "%")
        print("Percentage of Draw Task gotten 100% Correct for", p.p_id,
              "during ASSESSMENT phase is " + str(drawTask.percentage_correct * 100) + "%")
        # print("Percentage of average correctness across Draw Tasks: ", drawData.average_correctness)
        # print("Percentage of Draw Task gotten 100% Correct: ", drawTask.percentage_correct)
        drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect/totalDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
        print("Time spent during 100% correct responses to draw tasks by",p.p_id, "during ASSESSMENT phase is: ", averageTimeToAnswerDrawTaskEntirelyCorrect,"\n")
        averageTimeToAnswerDrawTaskEntirelyCorrectListAssess.append(drawData.average_correctness)
        print("averageTimeToAnswerDrawTaskEntirelyCorrectListAssess: ", averageTimeToAnswerDrawTaskEntirelyCorrectListAssess)

        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant = 0
        numberOfDrawTasksPerPhasePerParticipant = len(p.assessment_task.task.draw_tasks)
        print("numberOfDrawTasksPerPhasePerParticipant: ", numberOfDrawTasksPerPhasePerParticipant)
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachDrawTask in p.assessment_task.task.draw_tasks:
            print(eachDrawTask.interrupted_during_task)
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    print("eachMove.timeSpent: ", eachMove.timeSpent)
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask += 1
                        print("Time to resume task after interruption: ", eachMove.timeSpent)
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        print("List of resumption times after interruption in phase: ", durationB4resumptionList)
                        p.average_time_to_answer_after_interruption = sum(durationB4resumptionList) / len(
                            durationB4resumptionList)
            totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant += len(
                p.assessment_task.task.draw_tasks[iterant].draw_response_list)
            iterant += 1
        print("Total Number of consecutive batch of interruptions During Primary Task: ",
              numberOfInterruptionsDuringTask)
        print("Total Number of Moves taken to Complete All Draw Tasks per Phase per Participant: ",
              totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant)
        print("Time to complete task: " + str(totalTime) + " seconds")
        averageTimeRespondAfterInterruptionListAssessment.append(p.average_time_to_answer_after_interruption)
        print("averageTimeMoveAfterInterruptionList: ", averageTimeRespondAfterInterruptionListAssessment)
        print("^--------------------------End of Assessment Phase--------------------------^")

        a_p_name.append(p.assessment_task.name)
        a_p_count.append(len(p.assessment_task.task.draw_tasks))
        a_p_correctness.append(weightedCorrectness)
        a_p_time.append(averageTimeToAnswerDrawTaskEntirelyCorrect)
        a_p_times.append(averageTimeToAnswerDrawTaskEntirelyCorrectListAssess)
        a_p_percentage.append(drawData.average_correctness)
        a_p_percentage100.append(drawTask.percentage_correct)
        a_p_resumption.append(p.average_time_to_answer_after_interruption)             # what's the resumption lag for draw?
        a_p_resumptions.append(durationB4resumptionList)            # what are the resumption lags for draw?
        a_p_interruptions.append("NA")         # consecutive batch of interruptions is not relevant to draw
        a_p_movestotal.append("uncollected")             # how many clicks on average to complete a draw task?
        a_p_movetasktime.append(averageTimeRespondAfterInterruptionListAssessment)           # what is the average time after a click?
        a_p_moveinterruptedtime.append(p.average_time_to_answer_after_interruption)    # how much time until a click after an interruption?

    # Average time, correctness, and ratio of 100% correct responses to Draw Task during TRAINING phase
    # Aggregated time is save only when participant is 100% correct
    if p.training_task.name == "draw":
        print("v--------------------------Training Phase--------------------------v")
        print("Primary Task: ", p.training_task.name)
        print("Interruptive Task: ", p.training_interruption.name)
        drawTask = DrawTask()
        totalTimeEntirelyCorrect = drawTask.time
        totalDrawTaskEntirelyCorrect = 0
        fiftyPercentCorrect = 0
        twentyFivePercentCorrect = 0
        drawData = DrawData()
        for correctResponses in p.training_task.task.draw_tasks:
            if correctResponses.percentage_correct == "100%":
                totalDrawTaskEntirelyCorrect +=1
                totalTimeEntirelyCorrect += float(correctResponses.time)
            if correctResponses.percentage_correct == "50%":
                fiftyPercentCorrect +=1
            if correctResponses.percentage_correct == "25%":
                twentyFivePercentCorrect +=1
        totalNumberOfDrawTasks = len(p.training_task.task.draw_tasks)
        weightedCorrectness = (totalDrawTaskEntirelyCorrect*1+fiftyPercentCorrect*.5+twentyFivePercentCorrect*.25)
        drawData.average_correctness = weightedCorrectness/totalNumberOfDrawTasks
        drawTask.percentage_correct = totalDrawTaskEntirelyCorrect/totalNumberOfDrawTasks
        print("Percentage of average correctness across Draw Tasks for", p.p_id,
              "during TRAINING phase is " + str(drawData.average_correctness * 100) + "%")
        print("Percentage of Draw Task gotten 100% Correct for", p.p_id,
              "during TRAINING phase is " + str(drawTask.percentage_correct * 100) + "%")
        drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect/totalDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
        print("Time spent during 100% correct responses to draw tasks by",p.p_id, "during TRAINING phase is: ", averageTimeToAnswerDrawTaskEntirelyCorrect,"\n")
        averageTimeToAnswerDrawTaskEntirelyCorrectListTrain.append(drawData.average_correctness)
        print("averageTimeToAnswerDrawTaskEntirelyCorrectListTrain: ", averageTimeToAnswerDrawTaskEntirelyCorrectListTrain)

        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant = 0
        numberOfDrawTasksPerPhasePerParticipant = len(p.training_task.task.draw_tasks)
        print("numberOfDrawTasksPerPhasePerParticipant: ", numberOfDrawTasksPerPhasePerParticipant)
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachDrawTask in p.training_task.task.draw_tasks:
            print (eachDrawTask.interrupted_during_task)
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    print("eachMove.timeSpent: ", eachMove.timeSpent)
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask += 1
                        print("Time to resume task after interruption: ", eachMove.timeSpent)
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        print("List of resumption times after interruption in phase: ", durationB4resumptionList)
                        p.average_time_to_answer_after_interruption = sum(durationB4resumptionList) / len(
                            durationB4resumptionList)
            totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant += len(
                p.training_task.task.draw_tasks[iterant].draw_response_list)
            iterant += 1
        print("Total Number of consecutive batch of interruptions During Primary Task: ",
              numberOfInterruptionsDuringTask)
        print("Total Number of Moves taken to Complete All Draw Tasks per Phase per Participant: ",
              totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant)
        print("Time to complete task: " + str(totalTime) + " seconds")
        averageTimeRespondAfterInterruptionListTraining.append(p.average_time_to_answer_after_interruption)
        print("averageTimeMoveAfterInterruptionList: ", averageTimeRespondAfterInterruptionListTraining)
        print("^--------------------------End of Training Phase--------------------------^")

        tr_p_name.append(p.training_task.name)
        tr_p_count.append(totalNumberOfDrawTasks)
        tr_p_correctness.append(weightedCorrectness)
        tr_p_time.append(averageTimeToAnswerDrawTaskEntirelyCorrect)
        tr_p_times.append(averageTimeToAnswerDrawTaskEntirelyCorrectListTrain)
        tr_p_percentage.append(drawData.average_correctness)
        tr_p_percentage100.append(drawTask.percentage_correct)
        tr_p_resumption.append(p.average_time_to_answer_after_interruption)             # what's the resumption lag for draw?
        tr_p_resumptions.append(durationB4resumptionList)            # what are the resumption lags for draw?
        tr_p_interruptions.append("NA")         # consecutive batch of interruptions is not relevant to draw
        tr_p_movestotal.append("uncollected")             # how many clicks on average to complete a draw task?
        tr_p_movetasktime.append(averageTimeRespondAfterInterruptionListTraining)          # what is the average time after a click?
        tr_p_moveinterruptedtime.append(p.average_time_to_answer_after_interruption)    # how much time until a click after an interruption?

    # Average time, correctness, and ratio of 100% correct responses to Draw Task during TESTING phase
    # Aggregated time is save only when participant is 100% correct
    if p.testing_task.name == "draw":
        print("v--------------------------Testing Phase--------------------------v")
        print("Primary Task: ", p.testing_task.name)
        print("Interruptive Task: ", p.testing_interruption.name)
        drawTask = DrawTask()
        totalTimeEntirelyCorrect = drawTask.time
        totalDrawTaskEntirelyCorrect = 0
        fiftyPercentCorrect = 0
        twentyFivePercentCorrect = 0
        drawData = DrawData()
        for correctResponses in p.testing_task.task.draw_tasks:
            if correctResponses.percentage_correct == "100%":
                totalDrawTaskEntirelyCorrect += 1
                totalTimeEntirelyCorrect += float(correctResponses.time)
            if correctResponses.percentage_correct == "50%":
                fiftyPercentCorrect += 1
            if correctResponses.percentage_correct == "25%":
                twentyFivePercentCorrect += 1
        totalNumberOfDrawTasks = len(p.testing_task.task.draw_tasks)
        weightedCorrectness = (totalDrawTaskEntirelyCorrect * 1 + fiftyPercentCorrect * .5 + twentyFivePercentCorrect * .25)
        drawData.average_correctness = weightedCorrectness / totalNumberOfDrawTasks
        drawTask.percentage_correct = totalDrawTaskEntirelyCorrect / totalNumberOfDrawTasks
        print("Percentage of average correctness across Draw Tasks for",p.p_id, "during TESTING phase is "+str(drawData.average_correctness*100)+"%")
        print("Percentage of Draw Task gotten 100% Correct for",p.p_id, "during TESTING phase is "+str(drawTask.percentage_correct*100)+"%")
        drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect / totalDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
        print("Time spent during 100% correct responses to draw tasks by",p.p_id, "during TESTING phase is: ",
              averageTimeToAnswerDrawTaskEntirelyCorrect, "\n")
        averageTimeToAnswerDrawTaskEntirelyCorrectListTest.append(drawData.average_correctness)
        print("averageTimeToAnswerDrawTaskEntirelyCorrectListTest: ", averageTimeToAnswerDrawTaskEntirelyCorrectListTest)

        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant = 0
        numberOfDrawTasksPerPhasePerParticipant = len(p.testing_task.task.draw_tasks)
        print("numberOfDrawTasksPerPhasePerParticipant: ", numberOfDrawTasksPerPhasePerParticipant)
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachDrawTask in p.testing_task.task.draw_tasks:
            print(eachDrawTask.interrupted_during_task)
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    print("eachMove.timeSpent: ", eachMove.timeSpent)
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask += 1
                        print("Time to resume task after interruption: ", eachMove.timeSpent)
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        print("List of resumption times after interruption in phase: ", durationB4resumptionList)
                        p.average_time_to_answer_after_interruption = sum(durationB4resumptionList) / len(
                            durationB4resumptionList)
            totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant += len(
                p.testing_task.task.draw_tasks[iterant].draw_response_list)
            iterant += 1
        print("Total Number of consecutive batch of interruptions During Primary Task: ",
              numberOfInterruptionsDuringTask)
        print("Total Number of Moves taken to Complete All Draw Tasks per Phase per Participant: ",
              totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant)
        print("Time to complete task: " + str(totalTime) + " seconds")
        averageTimeRespondAfterInterruptionListTesting.append(p.average_time_to_answer_after_interruption)
        print("averageTimeMoveAfterInterruptionList: ", averageTimeRespondAfterInterruptionListTesting)
        print("^--------------------------End of Testing Phase--------------------------^")

        te_p_name.append(p.testing_task.name)
        te_p_count.append(totalNumberOfDrawTasks)
        te_p_correctness.append(weightedCorrectness)
        te_p_time.append(averageTimeToAnswerDrawTaskEntirelyCorrect)
        te_p_times.append(averageTimeToAnswerDrawTaskEntirelyCorrectListTest)
        te_p_percentage.append(drawData.average_correctness)
        te_p_percentage100.append(drawTask.percentage_correct)
        te_p_resumption.append(p.average_time_to_answer_after_interruption)             # what's the resumption lag for draw?
        te_p_resumptions.append(durationB4resumptionList)            # what are the resumption lags for draw?
        te_p_interruptions.append("NA")         # consecutive batch of interruptions is not relevant to draw
        te_p_movestotal.append("uncollected")             # how many clicks on average to complete a draw task?
        te_p_movetasktime.append(averageTimeRespondAfterInterruptionListTesting)          # what is the average time after a click?
        te_p_moveinterruptedtime.append(p.average_time_to_answer_after_interruption)    # how much time until a click after an interruption?

    # Participant's Hanoi task data
    # Hanoi Task during ASSESSMENT phase
    if p.assessment_task.name == "hanoi":
        print("v--------------------------Assessment Phase--------------------------v")
        print("Primary Task: "+ p.assessment_task.name)
        print("Interruptive Task: ", p.assessment_interruption.name)
        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant = 0
        numberOfHanoiTasksPerPhasePerParticipant = len(p.assessment_task.task.hanoi_tasks)
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachHanoiTask in p.assessment_task.task.hanoi_tasks:
            if eachHanoiTask.interrupted_during_task == True:
                for eachMove in eachHanoiTask.hanoi_move_list:
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask +=1
                        print("Time to resume task after interruption: ", eachMove.timeSpent)
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        print("List of resumption times after interruption: ", durationB4resumptionList)
            p.moves_to_complete = len(p.assessment_task.task.hanoi_tasks[iterant].hanoi_move_list)
            totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
            totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.assessment_task.task.hanoi_tasks[iterant].hanoi_move_list)
            iterant+=1
        print("Total Number of consecutive batch of interruptions During Primary Task: ", numberOfInterruptionsDuringTask)
        print("Total Number of Moves taken to Complete All Hanoi Tasks per Phase per Participant: ",
              totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant)
        print("Time to complete task: "+ str(totalTime)+ " seconds")
        p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_to_complete = totalTime/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_move_after_interruption = sum(durationB4resumptionList)/len(durationB4resumptionList)
        print("p.average_time_move_after_interruption: ", p.average_time_move_after_interruption)
        print("Average Number of Moves Before Completion of " +p.assessment_task.name+" tasks in Assessment phase by "+p.p_id+ " is", p.average_moves_to_complete)
        avgTimesToCompletionForAllHanoiTasksListAssessment.append(p.average_time_to_complete)
        print("avgTimesToCompletionForAllHanoiTasksListAssessment", avgTimesToCompletionForAllHanoiTasksListAssessment)
        averageTimeMoveAfterInterruptionListAssessment.append(p.average_time_move_after_interruption)
        print("averageTimeMoveAfterInterruptionList: ", averageTimeMoveAfterInterruptionListAssessment)
        averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain.append(p.average_moves_to_complete)
        print("^--------------------------End of Assessement Phase--------------------------^")

        a_p_name.append(p.assessment_task.name)
        a_p_count.append(len(p.assessment_task.task.hanoi_tasks))
        a_p_correctness.append("N/A") # hanoi doesn't have a correctness
        a_p_time.append(totalTime) # total time on phase
        a_p_times.append(p.average_time_to_complete) # time per hanoi question
        a_p_percentage.append("N/A") # hanoi doesn't have a correctness
        a_p_percentage100.append("N/A") # hanoi doesn't have a correctness
        a_p_resumption.append(p.average_time_move_after_interruption) # what is the average resumption time?
        a_p_resumptions.append(durationB4resumptionList)
        a_p_interruptions.append(numberOfInterruptionsDuringTask)
        a_p_movestotal.append(p.average_moves_to_complete)
        a_p_movetasktime.append(averageTimeMoveAfterInterruptionListAssessment)
        a_p_moveinterruptedtime.append(p.average_time_move_after_interruption)

    # Hanoi Task during TRAINING phase
    if p.training_task.name == "hanoi":
        print("v--------------------------Training Phase--------------------------v")
        print("Primary Task: "+ p.training_task.name)
        print("Interruptive Task: ", p.training_interruption.name)
        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant = 0
        numberOfHanoiTasksPerPhasePerParticipant = len(p.training_task.task.hanoi_tasks)
        # print("numberOfHanoiTasksPerPhasePerParticipant: ", numberOfHanoiTasksPerPhasePerParticipant)
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachHanoiTask in p.training_task.task.hanoi_tasks:
            #####################
            # print ("Was there an interruption during the task?")
            # print (eachHanoiTask.interrupted_during_task)
            if eachHanoiTask.interrupted_during_task == True:
                for eachMove in eachHanoiTask.hanoi_move_list:
                    # print ("interruption just happened:")
                    # print ("eachMove.after_interruption: ", eachMove.after_interruption)
                    # print("eachMove.timeSpent: ", eachMove.timeSpent)
                    totalTime += float(eachMove.timeSpent)
                    # print("Total time till this point in task: ", totalTime)
                    if eachMove.after_interruption == 1:
                        # print("Here's an interruption: ", eachMove.after_interruption)
                        numberOfInterruptionsDuringTask +=1
                        print("Time to resume task after interruption: ", eachMove.timeSpent)
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        print("List of resumption times after interruption: ", durationB4resumptionList)
                        # print("Number of Interruptions During Current Task: ", numberOfInterruptionsDuringTask)
            # print("Total Number of Interruptions During Primary Task so far: ", numberOfInterruptionsDuringTask)
            #####################
            p.moves_to_complete = len(p.training_task.task.hanoi_tasks[iterant].hanoi_move_list)
            totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
            # print("totalNumberOfMovesBeforeCompletePerTask by "+p.p_id+ " is: ", totalNumberOfMovesBeforeCompletePerTask)
            totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.training_task.task.hanoi_tasks[iterant].hanoi_move_list)
            # print("totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase: ", totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant)
            iterant+=1
        print("Total Number of consecutive batch of interruptions During Primary Task: ", numberOfInterruptionsDuringTask)
        print("Total Number of Moves taken to Complete All Hanoi Tasks per Phase per Participant: ",
              totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant)
        print("Time to complete task: "+ str(totalTime)+ " seconds")
        p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_to_complete = totalTime/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_move_after_interruption = sum(durationB4resumptionList)/len(durationB4resumptionList)
        print("p.average_time_move_after_interruption: ", p.average_time_move_after_interruption)
        print("Average Number of Moves Before Completion of " +p.training_task.name+" tasks in Training phase by "+p.p_id+ " is", p.average_moves_to_complete)
        avgTimesToCompletionForAllHanoiTasksListTraining.append(p.average_time_to_complete) #p.average_time_to_complete.append(totalTime)
        print("avgTimesToCompletionForAllHanoiTasksListTraining", avgTimesToCompletionForAllHanoiTasksListTraining)
        averageTimeMoveAfterInterruptionListTraining.append(p.average_time_move_after_interruption)
        print("averageTimeMoveAfterInterruptionList: ", averageTimeMoveAfterInterruptionListTraining)
        averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain.append(p.average_moves_to_complete)
        print("^--------------------------End of Training Phase--------------------------^")

        tr_p_name.append(p.training_task.name)
        tr_p_count.append(len(p.training_task.task.hanoi_tasks))
        tr_p_correctness.append("N/A") # hanoi doesn't have a correctness
        tr_p_time.append(totalTime) # total time on phase
        tr_p_times.append(p.average_time_to_complete) # time per hanoi question
        tr_p_percentage.append("N/A") # hanoi doesn't have a correctness
        tr_p_percentage100.append("N/A") # hanoi doesn't have a correctness
        tr_p_resumption.append(p.average_time_move_after_interruption) # what is the average resumption time?
        tr_p_resumptions.append(durationB4resumptionList)
        tr_p_interruptions.append(numberOfInterruptionsDuringTask)
        tr_p_movestotal.append(p.average_moves_to_complete)
        tr_p_movetasktime.append(averageTimeMoveAfterInterruptionListTraining)
        tr_p_moveinterruptedtime.append(p.average_time_move_after_interruption)

    # Hanoi Task during TESTING phase
    if p.testing_task.name == "hanoi":
        print("v--------------------------Testing Phase--------------------------v")
        print("Primary Task: "+ p.testing_task.name)
        print("Interruptive Task: ", p.testing_interruption.name)
        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant = 0
        numberOfHanoiTasksPerPhasePerParticipant = len(p.testing_task.task.hanoi_tasks)
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachHanoiTask in p.testing_task.task.hanoi_tasks:
            if eachHanoiTask.interrupted_during_task == True:
                for eachMove in eachHanoiTask.hanoi_move_list:
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask +=1
                        print("Time to resume task after interruption: ", eachMove.timeSpent)
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        print("List of resumption times after interruption: ", durationB4resumptionList)
            p.moves_to_complete = len(p.testing_task.task.hanoi_tasks[iterant].hanoi_move_list)
            totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
            totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.testing_task.task.hanoi_tasks[iterant].hanoi_move_list)
            iterant+=1
        print("Total Number of consecutive batch of interruptions During Primary Task: ", numberOfInterruptionsDuringTask)
        print("Total Number of Moves taken to Complete All Hanoi Tasks per Phase per Participant: ",
              totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant)
        print("Time to complete task: "+ str(totalTime)+ " seconds")
        p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_to_complete = totalTime/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_move_after_interruption = sum(durationB4resumptionList)/len(durationB4resumptionList)
        print("p.average_time_move_after_interruption: ", p.average_time_move_after_interruption)
        print("Average Number of Moves Before Completion of " +p.testing_task.name+" tasks in Testing phase by "+p.p_id+ " is", p.average_moves_to_complete)
        avgTimesToCompletionForAllHanoiTasksListTesting.append(p.average_time_to_complete)
        print("avgTimesToCompletionForAllHanoiTasksListTesting", avgTimesToCompletionForAllHanoiTasksListTesting)
        averageTimeMoveAfterInterruptionListTesting.append(p.average_time_move_after_interruption)
        print("averageTimeMoveAfterInterruptionList: ", averageTimeMoveAfterInterruptionListTesting)
        averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTest.append(p.average_moves_to_complete)
        print("^--------------------------End of Testing Phase--------------------------^")

        te_p_name.append(p.testing_task.name)
        te_p_count.append(len(p.testing_task.task.hanoi_tasks))
        te_p_correctness.append("N/A") # hanoi doesn't have a correctness
        te_p_time.append(totalTime) # total time on phase
        te_p_times.append(p.average_time_to_complete) # time per hanoi question
        te_p_percentage.append("N/A") # hanoi doesn't have a correctness
        te_p_percentage100.append("N/A") # hanoi doesn't have a correctness
        te_p_resumption.append(p.average_time_move_after_interruption) # what is the average resumption time?
        te_p_resumptions.append(durationB4resumptionList)
        te_p_interruptions.append(numberOfInterruptionsDuringTask)
        te_p_movestotal.append(p.average_moves_to_complete)
        te_p_movetasktime.append(averageTimeMoveAfterInterruptionListTesting)
        te_p_moveinterruptedtime.append(p.average_time_move_after_interruption)

print("\n")
print("Some Summaries of Stats")
print("-------------phase results demarcation-------------")
print("averageNumberOfMovesBeforeCompleteForAllHanoiTasksAssessList: ",
              averageNumberOfMovesBeforeCompleteForAllHanoiTasksListAssess)
print("avgTimesToCompletionForAllHanoiTasksList: ", avgTimesToCompletionForAllHanoiTasksListAssessment)
print("averageTimeMoveAfterInterruptionList: ", averageTimeMoveAfterInterruptionListAssessment)
# print("Standard Dev averageNumberOfMovesBeforeCompleteForAllHanoiTasksListAssess: ",
#           str(statistics.stdev(averageNumberOfMovesBeforeCompleteForAllHanoiTasksListAssess))+ " seconds")
print("Standard Dev avgTimesToCompletionForAllHanoiTasksList: ",
          str(statistics.stdev(avgTimesToCompletionForAllHanoiTasksListAssessment))+ " seconds")
print("Standard Dev averageTimeMoveAfterInterruptionList: ",
          str(statistics.stdev(averageTimeMoveAfterInterruptionListAssessment))+ " seconds")

print("-------------phase results demarcation-------------")
print("averageNumberOfMovesBeforeCompleteForAllHanoiTasksTrainginList: ",
              averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain)
print("avgTimesToCompletionForAllHanoiTasksList: ", avgTimesToCompletionForAllHanoiTasksListTraining)
print("averageTimeMoveAfterInterruptionList: ", averageTimeMoveAfterInterruptionListTraining)
print("Standard Dev averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain: ",
          str(statistics.stdev(averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain))+ " seconds")
print("Standard Dev avgTimesToCompletionForAllHanoiTasksList: ",
          str(statistics.stdev(avgTimesToCompletionForAllHanoiTasksListTraining))+ " seconds")
print("Standard Dev averageTimeMoveAfterInterruptionList: ",
          str(statistics.stdev(averageTimeMoveAfterInterruptionListTraining))+ " seconds")

print("-------------phase results demarcation-------------")
print("averageNumberOfMovesBeforeCompleteForAllHanoiTasksTestingList: ",
              averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTest)
print("avgTimesToCompletionForAllHanoiTasksList: ", avgTimesToCompletionForAllHanoiTasksListTesting)
print("averageTimeMoveAfterInterruptionList: ", averageTimeMoveAfterInterruptionListTesting)
print("Standard Dev averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTest: ",
          str(statistics.stdev(averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTest))+ " seconds")
print("Standard Dev avgTimesToCompletionForAllHanoiTasksList: ",
          str(statistics.stdev(avgTimesToCompletionForAllHanoiTasksListTesting))+ " seconds")
print("Standard Dev averageTimeMoveAfterInterruptionList: ",
          str(statistics.stdev(averageTimeMoveAfterInterruptionListTesting))+ " seconds")


# EXPORT METRICS TO CSV

# print(
#     "PID", len(id_arr), "\n", 
#     "Condition", len(conditions_arr), "\n",
#     "Starting Task", len(starting_task_arr), "\n",
#     "Starting Interruption", len(starting_interruption_arr), "\n",
#     "a_i_name", len(a_i_name), "\n",
#     "a_i_count", len(a_i_count), "\n",
#     "a_i_percentage", len(a_i_percentage), "\n",
#     "a_i_time", len(a_i_time), "\n",
#     "a_i_times", len(a_i_times), "\n",
#     "a_p_name", len(a_i_name), "\n",
#     "a_p_count", len(a_p_count), "\n",
#     "a_p_correctness", len(a_p_correctness), "\n",
#     "a_p_time", len(a_p_time), "\n",
#     "a_p_times", len(a_p_times), "\n",
#     "a_p_percentage", len(a_p_percentage), "\n",
#     "a_p_percentage100", len(a_p_percentage100), "\n",
#     "a_p_resumption", len(a_p_resumption), "\n",
#     "a_p_resumptions", len(a_p_resumptions), "\n",
#     "a_p_interruptions", len(a_p_interruptions), "\n",
#     "a_p_movestotal", len(a_p_movestotal), "\n",
#     "a_p_moveinterruptedtime", len(a_p_moveinterruptedtime), "\n",
#     "tr_i_name", len(tr_i_name), "\n",
#     "tr_i_count", len(tr_i_count),"\n",
#     "tr_i_percentage", len(tr_i_percentage), "\n",
#     "tr_i_time", len(tr_i_time), "\n",
#     "tr_i_times", len(tr_i_times), "\n",
#     "tr_p_name", len(tr_i_name), "\n",
#     "tr_p_count", len(tr_p_count), "\n",
#     "tr_p_correctness", len(tr_p_correctness), "\n",
#     "tr_p_time", len(tr_p_time), "\n",
#     "tr_p_times", len(tr_p_times), "\n",
#     "tr_p_percentage", len(tr_p_percentage), "\n",
#     "tr_p_percentage100", len(tr_p_percentage100), "\n",
#     "tr_p_resumption", len(tr_p_resumption), "\n",
#     "tr_p_resumptions", len(tr_p_resumptions), "\n",
#     "tr_p_interruptions", len(tr_p_interruptions), "\n",
#     "tr_p_movestotal", len(tr_p_movestotal), "\n",
#     "tr_p_moveinterruptedtime", len(tr_p_moveinterruptedtime), "\n", 
#     "te_i_name", len(te_i_name), "\n",
#     "te_i_count", len(te_i_count), "\n",
#     "te_i_percentage", len(te_i_percentage), "\n",
#     "te_i_time", len(te_i_time), "\n",
#     "te_i_times", len(te_i_times), "\n",
#     "te_p_name", len(te_i_name), "\n",
#     "te_p_count", len(te_p_count), "\n",
#     "te_p_correctness", len(te_p_correctness), "\n",
#     "te_p_time", len(te_p_time), "\n",
#     "te_p_times", len(te_p_times), "\n",
#     "te_p_percentage", len(te_p_percentage), "\n",
#     "te_p_percentage100", len(te_p_percentage100), "\n",
#     "te_p_resumption", len(te_p_resumption), "\n",
#     "te_p_resumptions", len(te_p_resumptions), "\n",
#     "te_p_interruptions", len(te_p_interruptions), "\n",
#     "te_p_movestotal", len(te_p_movestotal), "\n",
#     "te_p_moveinterruptedtime", len(tr_p_moveinterruptedtime), "\n"
#     )

columnTitles = {
    "PID": id_arr, 
    "Condition": conditions_arr, 
    "Starting Task": starting_task_arr, 
    "Starting Interruption": starting_interruption_arr, 
    
    "a_i_name": a_i_name, 
    "a_i_count": a_i_count,
    "a_i_percentage": a_i_percentage,
    "a_i_time": a_i_time,
    "a_i_times": a_i_times,
    
    "a_p_name": a_i_name,
    "a_p_count": a_p_count,
    "a_p_correctness": a_p_correctness,
    "a_p_time": a_p_time,
    "a_p_times": a_p_times,
    "a_p_percentage": a_p_percentage,
    "a_p_percentage100": a_p_percentage100,
    "a_p_resumption": a_p_resumption, 
    "a_p_resumptions": a_p_resumptions,
    "a_p_interruptions": a_p_interruptions, 
    "a_p_movestotal": a_p_movestotal,
    "a_p_moveinterruptedtime": a_p_moveinterruptedtime,

    "tr_i_name": tr_i_name, 
    "tr_i_count": tr_i_count,
    "tr_i_percentage": tr_i_percentage,
    "tr_i_time": tr_i_time,
    "tr_i_times": tr_i_times,
    
    "tr_p_name": tr_i_name,
    "tr_p_count": tr_p_count,
    "tr_p_correctness": tr_p_correctness,
    "tr_p_time": tr_p_time,
    "tr_p_times": tr_p_times,
    "tr_p_percentage": tr_p_percentage,
    "tr_p_percentage100": tr_p_percentage100,
    "tr_p_resumption": tr_p_resumption, 
    "tr_p_resumptions": tr_p_resumptions,
    "tr_p_interruptions": tr_p_interruptions, 
    "tr_p_movestotal": tr_p_movestotal,
    "tr_p_moveinterruptedtime": tr_p_moveinterruptedtime, 

    "te_i_name": te_i_name, 
    "te_i_count": te_i_count,
    "te_i_percentage": te_i_percentage,
    "te_i_time": te_i_time,
    "te_i_times": te_i_times,
    
    "te_p_name": te_i_name,
    "te_p_count": te_p_count,
    "te_p_correctness": te_p_correctness,
    "te_p_time": te_p_time,
    "te_p_times": te_p_times,
    "te_p_percentage": te_p_percentage,
    "te_p_percentage100": te_p_percentage100,
    "te_p_resumption": te_p_resumption, 
    "te_p_resumptions": te_p_resumptions,
    "te_p_interruptions": te_p_interruptions, 
    "te_p_movestotal": te_p_movestotal,
    "te_p_moveinterruptedtime": tr_p_moveinterruptedtime   
    }

dataframe = pd.DataFrame(columnTitles)
dataframe.to_csv('../DataResults/results.csv')
print("METRICS EXPORTED SUCCESSFULLY")