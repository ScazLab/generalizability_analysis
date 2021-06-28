#!/usr/bin/env python3

#starting task
START_TASK_DRAW = 1
START_TASK_HANOI = 2

#interruption task
START_INTERRUPTION_STROOP = 1
START_INTERRUPTION_MATH = 2

#condition
CONDITION_SWITCH_TASK = 1
CONDITION_SWITCH_INTERRUPTION = 2

class DemographicData():
	def __init__(self):
		age = -1
		gender = ""
		education = ""
		
class DiagnosisData():
	def __init__(self):
		asd = False
		color_blind = False
		hearing_impaired = False
		adhd = False
		prefer_not_to_say = False
		none = False
		
class EffortData():
	def __init__(self):
		task = ""
		effort = 0
		confidence = 0		
		
class SurveyData():
	def __init__(self):
		demographics = None
		diagnosis = None
		effort = None
		
class HanoiMove():
	def __init__(self):
		p1 = ""
		p2 = ""
		p3 = ""
		status = "incomplete"
		time = 0
		after_interruption = 0
		
class HanoiTask():
	def __init__(self):
		hanoi_move_list = []
		time_to_complete = 0
		moves_to_complete = 0

			
class HanoiData():
	def __init__(self):
		hanoi_tasks = []
		average_time_move_piece = 0
		average_time_move_after_interruption = 0
		average_time_move_not_after_interruption = 0
		average_moves_to_complete = 0
		average_time_to_complete = 0

		
class DrawTask():
	def __init__(self):
		answer = ""
		correct_answer = ""
		percentage_correct = 0
		time = 0
		after_interruption = 0
		
		
class DrawData():
	def __init__(self):
		draw_tasks = []
		average_time_to_answer = 0
		average_time_to_answer_after_interruption = 0
		average_time_to_answer_after_no_interruption = 0
		average_correctness = 0
		average_correctness_after_interruption = 0
		average_correctness_after_no_interruption = 0
		
class StroopTask():
	def __init__(self):
		correct = False
		time = 0
		
class StroopData():
	def __init__(self):
		stroop_tasks = []
		average_time = 0
		average_correctness = 0
		
class MathTask():
	def __init__(self):
		correct = False
		time = 0
		
class MathData():
	def __init__(self):
		math_tasks = []
		average_time = 0
		average_correctness = 0
		
class Task():
	def __init__(self):
		name = ""
		task = None
		
class Interruption():
	def __init__(self):
		name = ""
		interruption = None

class ParsedData(object):
	def __init__(self):
		starting_task = 0
		starting_interruption = 0
		condition = 0
		survey = None
		
		assessment_task = None
		assessment_interruption = None
		training_task = None
		training_interruption = None
		test_task = None
		test_interruption = None		
		

