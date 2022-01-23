#!/usr/bin/env python3
import os
import copy
import fnmatch
import inspect
import pandas as pd

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
        self.control = 0

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

directory = "../pilot_data/"
Matches = []
pid = []

averageTimeMathInterruptionsListAssess = []
averageTimeMathInterruptionsListTrain = []
averageTimeMathInterruptionsListTest = []

averageTimeStroopInterruptionsListAssess = []
averageTimeStroopInterruptionsListTrain = []
averageTimeStroopInterruptionsListTest = []

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
files = list() #os.listdir(directory)
for (dirpath, dirnames, filenames) in os.walk(directory):
    files += [os.path.join(dirpath, file) for file in filenames]
Matches = fnmatch.filter(files, pattern)
for filenames in Matches:
    f = open(directory+filenames, "r")
    filename = os.path.basename(filenames)
    p_id = os.path.splitext(filename)[0]
    p = Participant(p_id)
    if "Control" in filenames:
        p.control = 1
    elif "Experimental" in filenames:
        p.control = 0
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

prepost = 8

# PARTICIPANT DETAILS
id_arr = []
conditions_arr = []
control_arr = []
starting_task_arr = []
starting_interruption_arr = []

# DEMOGRAPHICS (d) VARIABLES
d_age = []
d_gender = []
d_education = []

d_asd = []
d_colorblind = []
d_hearingimpaired = []
d_adhd = []
d_prefernottosay = []
d_none = []

# ASSESSMENT (a) VARIABLES
a_i_name = []     # interruption (i) name
a_i_pre_percentage = [] # percentage of average correctness across interruptions
a_i_pre_time = []     # time during correct responses to interruptions
a_i_post_percentage = [] # percentage of average correctness across interruptions
a_i_post_time = []     # time during correct responses to interruptions

a_p_name = []                 # primary (p) task name
a_p_pre_correctness = []          # weighted correctness across all tasks
a_p_pre_time = []                 # time during correct responses to tasks
a_p_pre_resumption = []           # time to resume after interruption (hanoi only ??)
a_p_pre_movestotal = []           # total number of moves to complete all tasks (hanoi only)
a_p_post_correctness = []          # weighted correctness across all tasks
a_p_post_time = []                 # time during correct responses to tasks
a_p_post_resumption = []           # time to resume after interruption (hanoi only ??)
a_p_post_movestotal = []           # total number of moves to complete all tasks (hanoi only)

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

for p in all_participants:
    print(p.p_id)

    # study information
    control_arr.append(p.control)
    id_arr.append(p.p_id)
    conditions_arr.append(p.condition)
    starting_task_arr.append(p.starting_task)
    starting_interruption_arr.append(p.starting_interruption)

    # demographics
    d_age.append(p.survey.demographics.age)
    d_gender.append(p.survey.demographics.gender)
    d_education.append(p.survey.demographics.education)

    # diagnosis
    d_asd.append(p.survey.diagnosis.asd)
    d_colorblind.append(p.survey.diagnosis.color_blind)
    d_hearingimpaired.append(p.survey.diagnosis.hearing_impaired)
    d_adhd.append(p.survey.diagnosis.adhd)
    d_prefernottosay.append(p.survey.diagnosis.prefer_not_to_say)
    d_none.append(p.survey.diagnosis.none)

    if p.assessment_interruption.name == "math":
        mathData=MathData()
        
        # pre
        pre_totalTime = 0 #mathData.totalTime
        pre_correctResponseCount = 0
        for correctResponses in p.assessment_interruption.interruption.math_tasks[:prepost]:
            if correctResponses.correct == True:
                pre_correctResponseCount += 1
            pre_totalTime += float(correctResponses.timeSpent)
        pre_averageTimeMathInterruptions = pre_totalTime/prepost
        pre_percentCorrect = pre_correctResponseCount/prepost
        print('PRE: count = %d, percentage = %2.2f, time = %f' % (prepost, pre_percentCorrect, pre_averageTimeMathInterruptions))

        # post
        post_totalTime = 0 #mathData.totalTime
        post_correctResponseCount = 0
        for correctResponses in p.assessment_interruption.interruption.math_tasks[
            len(p.assessment_interruption.interruption.math_tasks)-prepost:
        ]:
            if correctResponses.correct == True:
                post_correctResponseCount += 1
            post_totalTime += float(correctResponses.timeSpent)
        post_averageTimeMathInterruptions = post_totalTime/prepost
        post_percentCorrect = post_correctResponseCount/prepost
        print('POST: count = %d, percentage = %2.2f, time = %f' % (prepost, post_percentCorrect, post_averageTimeMathInterruptions))

        
        # record data
        a_i_name.append(p.assessment_interruption.name)
        a_i_pre_percentage.append(pre_percentCorrect)
        a_i_pre_time.append(pre_averageTimeMathInterruptions)
        a_i_post_percentage.append(post_percentCorrect)
        a_i_post_time.append(post_averageTimeMathInterruptions)
        
    if p.training_interruption.name == "math":
        mathData = MathData()

        # determine the total time spent and number of correct answers in this phase
        correctResponseCount = 0
        totalTime = mathData.totalTime
        for correctResponses in p.training_interruption.interruption.math_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        totalNumberOfmathTasks = len(p.training_interruption.interruption.math_tasks)
        
        # calculate average time per given task
        mathData.average_time = totalTime/totalNumberOfmathTasks
        averageTimeMathInterruptions = mathData.average_time
        averageTimeMathInterruptionsListTrain.append(mathData.average_time)

        # calculate the percentage of tasks answered correctly
        percentCorrect = correctResponseCount / totalNumberOfmathTasks

        # record data
        tr_i_name.append(p.training_interruption.name)
        tr_i_count.append(len(p.training_interruption.interruption.math_tasks))
        tr_i_percentage.append(percentCorrect)
        tr_i_time.append(averageTimeMathInterruptions)
        tr_i_times.append(averageTimeMathInterruptionsListTrain)

    if p.testing_interruption.name == "math":
        mathData = MathData()

        # determine the total time spent and number of correct tasks in this phase
        correctResponseCount = 0
        totalTime = mathData.totalTime
        for correctResponses in p.testing_interruption.interruption.math_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        totalNumberOfmathTasks = len(p.testing_interruption.interruption.math_tasks)
        
        # calculate the time spent per given task
        mathData.average_time = totalTime/totalNumberOfmathTasks
        averageTimeMathInterruptions = mathData.average_time
        averageTimeMathInterruptionsListTest.append(mathData.average_time)
        
        # calculate the percentage of tasks answered correctly
        percentCorrect = correctResponseCount / totalNumberOfmathTasks
        
        # record data
        te_i_name.append(p.testing_interruption.name)
        te_i_count.append(len(p.testing_interruption.interruption.math_tasks))
        te_i_percentage.append(percentCorrect)
        te_i_time.append(averageTimeMathInterruptions)
        te_i_times.append(averageTimeMathInterruptionsListTest)

    if p.assessment_interruption.name == "stroop":
        stroopData=StroopData()
        
        # pre
        pre_totalTime = 0 #mathData.totalTime
        pre_correctResponseCount = 0
        for correctResponses in p.assessment_interruption.interruption.stroop_tasks[:prepost]:
            if correctResponses.correct == True:
                pre_correctResponseCount += 1
            pre_totalTime += float(correctResponses.timeSpent)
        pre_averageTimeStroopInterruptions = pre_totalTime/prepost
        pre_percentCorrect = pre_correctResponseCount/prepost
        print('PRE: count = %d, percentage = %2.2f, time = %f' % (prepost, pre_percentCorrect, pre_averageTimeStroopInterruptions))

        # post
        post_totalTime = 0 #mathData.totalTime
        post_correctResponseCount = 0
        for correctResponses in p.assessment_interruption.interruption.stroop_tasks[
            len(p.assessment_interruption.interruption.stroop_tasks)-prepost:
        ]:
            if correctResponses.correct == True:
                post_correctResponseCount += 1
            post_totalTime += float(correctResponses.timeSpent)
        post_averageTimeStroopInterruptions = post_totalTime/prepost
        post_percentCorrect = post_correctResponseCount/prepost
        print('POST: count = %d, percentage = %2.2f, time = %f' % (prepost, post_percentCorrect, post_averageTimeStroopInterruptions))

        # record data
        a_i_name.append(p.assessment_interruption.name)
        a_i_pre_percentage.append(pre_percentCorrect)
        a_i_pre_time.append(pre_averageTimeStroopInterruptions)
        a_i_post_percentage.append(post_percentCorrect)
        a_i_post_time.append(post_averageTimeStroopInterruptions)

    if p.training_interruption.name == "stroop":
        stroopData = StroopData()
        
        totalTime = stroopData.totalTime
        correctResponseCount = 0
        for correctResponses in p.training_interruption.interruption.stroop_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        totalNumberOfStroopTasks = len(p.training_interruption.interruption.stroop_tasks)
        
        stroopData.average_time = totalTime/totalNumberOfStroopTasks
        averageTimeStroopInterruptions = stroopData.average_time
        averageTimeStroopInterruptionsListTrain.append(stroopData.average_time)
        
        percentCorrect = correctResponseCount / totalNumberOfStroopTasks
        
        tr_i_name.append(p.training_interruption.name)
        tr_i_count.append(totalNumberOfStroopTasks)
        tr_i_percentage.append(percentCorrect)
        tr_i_time.append(averageTimeStroopInterruptions)
        tr_i_times.append(averageTimeStroopInterruptionsListTrain)

    if p.testing_interruption.name == "stroop":
        stroopData = StroopData()

        totalTime = stroopData.totalTime
        correctResponseCount = 0
        for correctResponses in p.testing_interruption.interruption.stroop_tasks:
            if correctResponses.correct == True:
                correctResponseCount += 1
            totalTime += float(correctResponses.timeSpent)
        totalNumberOfStroopTasks = len(p.testing_interruption.interruption.stroop_tasks)
        
        stroopData.average_time = totalTime/totalNumberOfStroopTasks
        averageTimeStroopInterruptions = stroopData.average_time
        averageTimeStroopInterruptionsListTest.append(stroopData.average_time)
        
        percentCorrect = correctResponseCount / totalNumberOfStroopTasks
        
        te_i_name.append(p.testing_interruption.name)
        te_i_count.append(totalNumberOfStroopTasks)
        te_i_percentage.append(percentCorrect)
        te_i_time.append(averageTimeStroopInterruptions)
        te_i_times.append(averageTimeStroopInterruptionsListTest)

    if p.assessment_task.name == "draw":
        drawTask = DrawTask()
        drawData = DrawData()
        
        # pre
        pre_totalTimeEntirelyCorrect = 0
        pre_totalDrawTaskEntirelyCorrect = 0 # 
        pre_fiftyPercentCorrect = 0
        pre_twentyFivePercentCorrect = 0        
        for correctResponses in p.assessment_task.task.draw_tasks[:prepost]:
            if correctResponses.percentage_correct == "100%":
                pre_totalDrawTaskEntirelyCorrect +=1
                pre_totalTimeEntirelyCorrect += float(correctResponses.time)
            if correctResponses.percentage_correct == "50%":
                pre_fiftyPercentCorrect +=1
            if correctResponses.percentage_correct == "25%":
                pre_twentyFivePercentCorrect +=1
        pre_weightedCorrectness = (pre_totalDrawTaskEntirelyCorrect*1+pre_fiftyPercentCorrect*.5+pre_twentyFivePercentCorrect*.25)

        # post
        post_totalTimeEntirelyCorrect = 0
        post_totalDrawTaskEntirelyCorrect = 0 # 
        post_fiftyPercentCorrect = 0
        post_twentyFivePercentCorrect = 0        
        for correctResponses in p.assessment_task.task.draw_tasks[
            len(p.assessment_task.task.draw_tasks)-prepost:
        ]:
            if correctResponses.percentage_correct == "100%":
                post_totalDrawTaskEntirelyCorrect +=1
                post_totalTimeEntirelyCorrect += float(correctResponses.time)
            if correctResponses.percentage_correct == "50%":
                post_fiftyPercentCorrect +=1
            if correctResponses.percentage_correct == "25%":
                post_twentyFivePercentCorrect +=1
        post_weightedCorrectness = (post_totalDrawTaskEntirelyCorrect*1+post_fiftyPercentCorrect*.5+post_twentyFivePercentCorrect*.25)
        
        # time spent to answer correctly
        try:
            pre_averageTimeToAnswerDrawTaskEntirelyCorrect = pre_totalTimeEntirelyCorrect/pre_totalDrawTaskEntirelyCorrect
        except ZeroDivisionError:
            pre_averageTimeToAnswerDrawTaskEntirelyCorrect = 0
        try:
            post_averageTimeToAnswerDrawTaskEntirelyCorrect = post_totalTimeEntirelyCorrect/post_totalDrawTaskEntirelyCorrect
        except ZeroDivisionError:
            post_averageTimeToAnswerDrawTaskEntirelyCorrect = 0

        pre_durationB4resumptionList = []
        for eachDrawTask in p.assessment_task.task.draw_tasks[:prepost]:
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    if eachMove.after_interruption == 1:
                        pre_durationB4resumptionList.append(float(eachMove.timeSpent))
        post_durationB4resumptionList = []
        for eachDrawTask in p.assessment_task.task.draw_tasks[
            len(p.assessment_task.task.draw_tasks)-prepost:
        ]:
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    if eachMove.after_interruption == 1:
                        post_durationB4resumptionList.append(float(eachMove.timeSpent))

        # record data
        a_p_name.append(p.assessment_task.name)
        a_p_pre_correctness.append(pre_weightedCorrectness)
        a_p_pre_time.append(pre_averageTimeToAnswerDrawTaskEntirelyCorrect)
        a_p_pre_resumption.append(sum(pre_durationB4resumptionList) / len(pre_durationB4resumptionList))
        a_p_pre_movestotal.append("N/A")
        a_p_post_correctness.append(post_weightedCorrectness)
        a_p_post_time.append(post_averageTimeToAnswerDrawTaskEntirelyCorrect)
        a_p_post_resumption.append(sum(post_durationB4resumptionList) / len(post_durationB4resumptionList))
        a_p_post_movestotal.append("N/A") 

    if p.training_task.name == "draw":
        drawTask = DrawTask()
        drawData = DrawData()

        totalTimeEntirelyCorrect = drawTask.time
        totalDrawTaskEntirelyCorrect = 0
        fiftyPercentCorrect = 0
        twentyFivePercentCorrect = 0
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
        
        drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect/totalDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrectListTrain.append(drawData.average_correctness)
        
        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant = 0
        numberOfDrawTasksPerPhasePerParticipant = len(p.training_task.task.draw_tasks)
        
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachDrawTask in p.training_task.task.draw_tasks:
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask += 1
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        p.average_time_to_answer_after_interruption = sum(durationB4resumptionList) / len(
                            durationB4resumptionList)
            totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant += len(
                p.training_task.task.draw_tasks[iterant].draw_response_list)
            iterant += 1

        if p.control == 0:
            averageTimeRespondAfterInterruptionListTraining.append(p.average_time_to_answer_after_interruption)
            tr_p_resumption.append(p.average_time_to_answer_after_interruption)
        else:
            averageTimeRespondAfterInterruptionListTraining.append("N/A")
            tr_p_resumption.append("N/A")

        tr_p_name.append(p.training_task.name)
        tr_p_count.append(totalNumberOfDrawTasks)
        tr_p_correctness.append(weightedCorrectness)
        tr_p_time.append(averageTimeToAnswerDrawTaskEntirelyCorrect)
        tr_p_times.append(averageTimeToAnswerDrawTaskEntirelyCorrectListTrain)
        tr_p_percentage.append(drawData.average_correctness)
        tr_p_percentage100.append(drawTask.percentage_correct)
        tr_p_resumptions.append(durationB4resumptionList)
        tr_p_interruptions.append("N/A")
        tr_p_movestotal.append("N/A")
        tr_p_movetasktime.append(averageTimeRespondAfterInterruptionListTraining)
        
    if p.testing_task.name == "draw":
        drawTask = DrawTask()
        drawData = DrawData()

        totalTimeEntirelyCorrect = drawTask.time
        totalDrawTaskEntirelyCorrect = 0
        fiftyPercentCorrect = 0
        twentyFivePercentCorrect = 0
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
        
        drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = 0
        if (totalDrawTaskEntirelyCorrect != 0):
            drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect / totalDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
        averageTimeToAnswerDrawTaskEntirelyCorrectListTest.append(drawData.average_correctness)

        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant = 0
        numberOfDrawTasksPerPhasePerParticipant = len(p.testing_task.task.draw_tasks)
        
        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachDrawTask in p.testing_task.task.draw_tasks:
            if eachDrawTask.interrupted_during_task == True:
                for eachMove in eachDrawTask.draw_response_list:
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask += 1
                        durationB4resumptionList.append(float(eachMove.timeSpent))
                        p.average_time_to_answer_after_interruption = sum(durationB4resumptionList) / len(
                            durationB4resumptionList)
            totalNumberOfMovesBeforeCompleteForAllDrawTasksPerPhasePerParticipant += len(
                p.testing_task.task.draw_tasks[iterant].draw_response_list)
            iterant += 1
        averageTimeRespondAfterInterruptionListTesting.append(p.average_time_to_answer_after_interruption)

        te_p_name.append(p.testing_task.name)
        te_p_count.append(totalNumberOfDrawTasks)
        te_p_correctness.append(weightedCorrectness)
        te_p_time.append(averageTimeToAnswerDrawTaskEntirelyCorrect)
        te_p_times.append(averageTimeToAnswerDrawTaskEntirelyCorrectListTest)
        te_p_percentage.append(drawData.average_correctness)
        te_p_percentage100.append(drawTask.percentage_correct)
        te_p_resumption.append(p.average_time_to_answer_after_interruption)
        te_p_resumptions.append(durationB4resumptionList)
        te_p_interruptions.append("N/A")
        te_p_movestotal.append("N/A")
        te_p_movetasktime.append(averageTimeRespondAfterInterruptionListTesting)

    if p.assessment_task.name == "hanoi":
        # pre
        pre_iterant = 0
        pre_totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant = 0
        pre_totalTime = 0
        pre_durationB4resumptionList = []
        for eachHanoiTask in p.assessment_task.task.hanoi_tasks[:prepost]:
            if eachHanoiTask.interrupted_during_task == True:
                for eachMove in eachHanoiTask.hanoi_move_list:
                    pre_totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        pre_durationB4resumptionList.append(float(eachMove.timeSpent))
            pre_totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.assessment_task.task.hanoi_tasks[pre_iterant].hanoi_move_list)
            pre_iterant+=1
        avgTimesToCompletionForAllHanoiTasksListAssessment.append(pre_totalTime/prepost)
        averageTimeMoveAfterInterruptionListAssessment.append(sum(pre_durationB4resumptionList)/len(pre_durationB4resumptionList))
        
        # post
        post_iterant = len(p.assessment_task.task.hanoi_tasks)-prepost
        post_totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant = 0
        post_totalTime = 0
        post_durationB4resumptionList = []
        for eachHanoiTask in p.assessment_task.task.hanoi_tasks[
            len(p.assessment_task.task.hanoi_tasks)-prepost:
        ]:
            if eachHanoiTask.interrupted_during_task == True:
                for eachMove in eachHanoiTask.hanoi_move_list:
                    post_totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        post_durationB4resumptionList.append(float(eachMove.timeSpent))
            post_totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.assessment_task.task.hanoi_tasks[post_iterant].hanoi_move_list)
            post_iterant+=1
        avgTimesToCompletionForAllHanoiTasksListAssessment.append(post_totalTime/prepost)
        averageTimeMoveAfterInterruptionListAssessment.append(sum(post_durationB4resumptionList)/len(post_durationB4resumptionList))

        a_p_name.append(p.assessment_task.name)
        a_p_pre_correctness.append("N/A")
        a_p_pre_time.append(pre_totalTime/prepost)
        a_p_pre_resumption.append(sum(pre_durationB4resumptionList)/len(pre_durationB4resumptionList))
        a_p_pre_movestotal.append(pre_totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant)
        a_p_post_correctness.append("N/A")
        a_p_post_time.append(post_totalTime/prepost)
        a_p_post_resumption.append(sum(post_durationB4resumptionList)/len(post_durationB4resumptionList))
        a_p_post_movestotal.append(post_totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant)

    if p.training_task.name == "hanoi":
        iterant = 0
        totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant = 0
        numberOfHanoiTasksPerPhasePerParticipant = len(p.training_task.task.hanoi_tasks)

        totalTime = 0
        durationB4resumptionList = []
        numberOfInterruptionsDuringTask = 0
        for eachHanoiTask in p.training_task.task.hanoi_tasks:
            if eachHanoiTask.interrupted_during_task == True:
                for eachMove in eachHanoiTask.hanoi_move_list:
                    totalTime += float(eachMove.timeSpent)
                    if eachMove.after_interruption == 1:
                        numberOfInterruptionsDuringTask +=1
                        durationB4resumptionList.append(float(eachMove.timeSpent))
            p.moves_to_complete = len(p.training_task.task.hanoi_tasks[iterant].hanoi_move_list)
            totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
            totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.training_task.task.hanoi_tasks[iterant].hanoi_move_list)
            iterant+=1
        p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_to_complete = totalTime/numberOfHanoiTasksPerPhasePerParticipant
        
        avgTimesToCompletionForAllHanoiTasksListTraining.append(p.average_time_to_complete) #p.average_time_to_complete.append(totalTime)
        averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTrain.append(p.average_moves_to_complete)
        
        tr_p_name.append(p.training_task.name)
        tr_p_count.append(len(p.training_task.task.hanoi_tasks))
        tr_p_correctness.append("N/A") # hanoi doesn't have a correctness
        tr_p_time.append(totalTime) # total time on phase
        tr_p_times.append(p.average_time_to_complete) # time per hanoi question
        tr_p_percentage.append("N/A") # hanoi doesn't have a correctness
        tr_p_percentage100.append("N/A") # hanoi doesn't have a correctness
        tr_p_resumptions.append(durationB4resumptionList)
        tr_p_interruptions.append(numberOfInterruptionsDuringTask)
        tr_p_movestotal.append(p.average_moves_to_complete)
        tr_p_movetasktime.append(averageTimeMoveAfterInterruptionListTraining)

        # no interruptions are experienced during the training phase of the control
        if p.control == 0:
            p.average_time_move_after_interruption = sum(durationB4resumptionList)/len(durationB4resumptionList)
            averageTimeMoveAfterInterruptionListTraining.append(p.average_time_move_after_interruption)
            tr_p_resumption.append(p.average_time_move_after_interruption)
        else:
            averageTimeMoveAfterInterruptionListTraining.append("N/A")
            tr_p_resumption.append("N/A")

    if p.testing_task.name == "hanoi":
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
                        durationB4resumptionList.append(float(eachMove.timeSpent))
            p.moves_to_complete = len(p.testing_task.task.hanoi_tasks[iterant].hanoi_move_list)
            totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
            totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant += len(p.testing_task.task.hanoi_tasks[iterant].hanoi_move_list)
            iterant+=1
        
        p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhasePerParticipant/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_to_complete = totalTime/numberOfHanoiTasksPerPhasePerParticipant
        p.average_time_move_after_interruption = sum(durationB4resumptionList)/len(durationB4resumptionList)
        avgTimesToCompletionForAllHanoiTasksListTesting.append(p.average_time_to_complete)
        averageTimeMoveAfterInterruptionListTesting.append(p.average_time_move_after_interruption)
        averageNumberOfMovesBeforeCompleteForAllHanoiTasksListTest.append(p.average_moves_to_complete)
        
        te_p_name.append(p.testing_task.name)
        te_p_count.append(len(p.testing_task.task.hanoi_tasks))
        te_p_correctness.append("N/A") # hanoi doesn't have a correctness
        te_p_time.append(totalTime)
        te_p_times.append(p.average_time_to_complete)
        te_p_percentage.append("N/A") # hanoi doesn't have a correctness
        te_p_percentage100.append("N/A") # hanoi doesn't have a correctness
        te_p_resumption.append(p.average_time_move_after_interruption)
        te_p_resumptions.append(durationB4resumptionList)
        te_p_interruptions.append(numberOfInterruptionsDuringTask)
        te_p_movestotal.append(p.average_moves_to_complete)
        te_p_movetasktime.append(averageTimeMoveAfterInterruptionListTesting)

columnTitles = {
    "PID": id_arr, 
    "Starting Interruption": starting_interruption_arr,
    "Starting Task": starting_task_arr,
    "Condition": conditions_arr, 
    "Control": control_arr,
    
    "d_age": d_age,
    "d_gender": d_gender,
    "d_education": d_education,

    "d_asd": d_asd,
    "d_colorblind": d_colorblind,
    "d_hearingimpaired": d_hearingimpaired,
    "d_adhd": d_adhd,
    "d_prefernottosay": d_prefernottosay,
    "d_none": d_none,

    "a_i_name": a_i_name,
    "a_i_pre_percentage": a_i_pre_percentage,
    "a_i_pre_time": a_i_pre_time,
    "a_i_post_percentage": a_i_post_percentage,
    "a_i_post_time": a_i_post_time,
    
    "a_p_name": a_p_name,
    "a_p_pre_correctness": a_p_pre_correctness,
    "a_p_pre_time": a_p_pre_time,
    "a_p_pre_resumption": a_p_pre_resumption,
    "a_p_pre_movestotal": a_p_pre_movestotal,
    "a_p_post_correctness": a_p_post_correctness,
    "a_p_post_time": a_p_post_time,
    "a_p_post_resumption": a_p_post_resumption,
    "a_p_post_movestotal": a_p_post_movestotal,

    "tr_i_name": tr_i_name, 
    "tr_i_count": tr_i_count,
    "tr_i_percentage": tr_i_percentage,
    "tr_i_time": tr_i_time,
    "tr_i_times": tr_i_times,
    
    "tr_p_name": tr_p_name,
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

    "te_i_name": te_i_name, 
    "te_i_count": te_i_count,
    "te_i_percentage": te_i_percentage,
    "te_i_time": te_i_time,
    "te_i_times": te_i_times,
    
    "te_p_name": te_p_name,
    "te_p_count": te_p_count,
    "te_p_correctness": te_p_correctness,
    "te_p_time": te_p_time,
    "te_p_times": te_p_times,
    "te_p_percentage": te_p_percentage,
    "te_p_percentage100": te_p_percentage100,
    "te_p_resumption": te_p_resumption, 
    "te_p_resumptions": te_p_resumptions,
    "te_p_interruptions": te_p_interruptions, 
    "te_p_movestotal": te_p_movestotal 
    }

dataframe = pd.DataFrame(columnTitles)
dataframe.to_csv('../DataResults/phases.csv')
print("METRICS EXPORTED SUCCESSFULLY")