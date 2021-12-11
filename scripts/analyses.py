# from parse_data import *

#
#
# # Participant's average time for correct responses to math interruptions
# if p.assessment_interruption.name == "math":
#     # Average time for correct responses to math interruptions during ASSESSMENT phase
#     mathData=MathData()
#     totalTime = mathData.totalTime
#     for correctResponses in p.assessment_interruption.interruption.math_tasks:
#         # print(correctResponses.correct)
#         totalTime += float(correctResponses.timeSpent)
#         # print(totalTime)
#     totalNumberOfmathTasks = len(p.assessment_interruption.interruption.math_tasks)
#     print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
#     # print("getting attribute: ", getattr(mathData, 'average_time'))
#     mathData.average_time = totalTime/totalNumberOfmathTasks
#     averageTimeMathInterruptions = mathData.average_time
#     print("Time during correct responses to interruptions during Assessment phase", averageTimeMathInterruptions,"\n")
#
# print("BUG HEREEEEEEEEEE")
# print("p.training_interruption.name: ", p.training_interruption.name)
# # if p.training_interruption.name == "math":
# #     # Average time for correct responses to math interruptions during TRAINING phase
# #     for correctResponses in p.training_interruption.interruption.math_tasks:
# #         totalTime += float(correctResponses.timeSpent)
# #     totalNumberOfmathTasks = len(p.training_interruption.interruption.math_tasks)
# #     print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
# #     mathData.average_time = totalTime/totalNumberOfmathTasks
# #     averageTimeMathInterruptions = mathData.average_time
# #     print("Time during correct responses to interruptions during Assessment phase", averageTimeMathInterruptions,"\n")
#
# if p.testing_interruption.name == "math":
#     # Average time for correct responses to math interruptions during TESTING phase
#     for correctResponses in p.testing_interruption.interruption.math_tasks:
#         totalTime += float(correctResponses.timeSpent)
#     totalNumberOfmathTasks = len(p.testing_interruption.interruption.math_tasks)
#     print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
#     mathData.average_time = totalTime/totalNumberOfmathTasks
#     averageTimeMathInterruptions = mathData.average_time
#     print("Time during correct responses to interruptions during Assessment phase", averageTimeMathInterruptions,"\n")
#
#
#
# # Participant's average time for correct responses to stroop interruptions
#
# if p.assessment_interruption.name == "stroop":
#     # Average time for correct responses to math interruptions during ASSESSMENT phase
#     stroopData=StroopData()
#     totalTime = stroopData.totalTime
#     for correctResponses in p.assessment_interruption.interruption.stroop_tasks:
#         # print(correctResponses.correct)
#         totalTime += float(correctResponses.timeSpent)
#         # print(totalTime)
#     totalNumberOfmathTasks = len(p.assessment_interruption.interruption.stroop_tasks)
#     print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
#     # print("getting attribute: ", getattr(mathData, 'average_time'))
#     stroopData.average_time = totalTime/totalNumberOfmathTasks
#     averageTimeMathInterruptions = stroopData.average_time
#     print("Time during correct responses to interruptions during Assessment phase", averageTimeMathInterruptions,"\n")
#
# print("BUG HEREEEEEEEEEE")
# print("p.training_interruption.name: ", p.training_interruption.name)
# # ********Bug...Draw task is labelled as Hanoi task
# # if p.training_interruption.name == "stroop":
# #     # Average time for correct responses to math interruptions during TRAINING phase
# #     stroopData = StroopData()
# #     totalTime = stroopData.totalTime
# #     for correctResponses in p.training_interruption.interruption.stroop_tasks:
# #         totalTime += float(correctResponses.timeSpent)
# #     totalNumberOfmathTasks = len(p.training_interruption.interruption.stroop_tasks)
# #     print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
# #     stroopData.average_time = totalTime/totalNumberOfmathTasks
# #     averageTimeMathInterruptions = stroopData.average_time
# #     print("Time during correct responses to interruptions during Assessment phase", averageTimeMathInterruptions,"\n")
#
#
# if p.testing_interruption.name == "stroop":
#     # Average time for correct responses to math interruptions during TESTING phase
#     stroopData = StroopData()
#     totalTime = stroopData.totalTime
#     for correctResponses in p.testing_interruption.interruption.stroop_tasks:
#         totalTime += float(correctResponses.timeSpent)
#     totalNumberOfmathTasks = len(p.testing_interruption.interruption.stroop_tasks)
#     print("totalNumberOfmathTasks: ", totalNumberOfmathTasks)
#     stroopData.average_time = totalTime/totalNumberOfmathTasks
#     averageTimeMathInterruptions = stroopData.average_time
#     print("Time during correct responses to interruptions during Assessment phase", averageTimeMathInterruptions,"\n")
#
#
#
#
# # Participant's Draw task data
# # Average time, correctness, and ratio of 100% correct responses to Draw Task during ASSESSMENT phase
# # Aggregated time is save only when participant is 100% correct
#
# if p.assessment_task.name == "draw":
#     #     print("printing starting task: ", p.starting_task)
#     #     totalNumberOfDrawTasks = len(p.assessment_task.task.draw_tasks)
#     #     print("Number of draw tasks as primary task in assessment phase: ", totalNumberOfDrawTasks)
#     drawTask = DrawTask()
#     totalTimeEntirelyCorrect = drawTask.time
#     totalDrawTaskEntirelyCorrect = 0
#     fiftyPercentCorrect = 0
#     twentyFivePercentCorrect = 0
#     drawData = DrawData()
#     for correctResponses in p.assessment_task.task.draw_tasks:
#         # print("Each attempt: ", correctResponses.percentage_correct)
#         if correctResponses.percentage_correct == "100%":
#             totalDrawTaskEntirelyCorrect +=1
#             # print("After answering a SINGLE draw task 100% correct")
#             totalTimeEntirelyCorrect += float(correctResponses.time)
#         # print("aggregated time: ", totalTimeEntirelyCorrect)
#     # (17*100% + 1*50% + 2*25%)/total count * 100%
#         if correctResponses.percentage_correct == "50%":
#             fiftyPercentCorrect +=1
#             # print("After answering a SINGLE draw task 50% correct")
#         # print("aggregated fiftyPercentCorrect count: ", fiftyPercentCorrect)
#         if correctResponses.percentage_correct == "25%":
#             twentyFivePercentCorrect +=1
#             # print("After answering a SINGLE draw task 25% correct")
#         # print("aggregated twentyFivePercentCorrect count: ", twentyFivePercentCorrect)
#     totalNumberOfDrawTasks = len(p.assessment_task.task.draw_tasks)
#     weightedCorrectness = (totalDrawTaskEntirelyCorrect*1+fiftyPercentCorrect*.5+twentyFivePercentCorrect*.25)
#     drawData.average_correctness = weightedCorrectness/totalNumberOfDrawTasks
#     # print("totalDrawTaskEntirelyCorrect: ", totalDrawTaskEntirelyCorrect)
#     # print("totalNumberOfDrawTasks: ", totalNumberOfDrawTasks)
#     # print("getting attribute: ", getattr(mathData, 'average_time'))
#     drawTask.percentage_correct = totalDrawTaskEntirelyCorrect/totalNumberOfDrawTasks
#     print("Percentage of average correctness across Draw Tasks: ", drawData.average_correctness)
#     print("Percentage of Draw Task gotten 100% Correct: ", drawTask.percentage_correct)
#     drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect/totalDrawTaskEntirelyCorrect
#     averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
#     print("Time spent during 100% correct responses to draw tasks during Assessment phase", averageTimeToAnswerDrawTaskEntirelyCorrect,"\n")
#
# # Average time, correctness, and ratio of 100% correct responses to Draw Task during TRAINING phase
# # Aggregated time is save only when participant is 100% correct
# if p.training_task.name == "draw":
#     drawTask = DrawTask()
#     totalTimeEntirelyCorrect = drawTask.time
#     totalDrawTaskEntirelyCorrect = 0
#     fiftyPercentCorrect = 0
#     twentyFivePercentCorrect = 0
#     drawData = DrawData()
#     for correctResponses in p.training_task.task.draw_tasks:
#         if correctResponses.percentage_correct == "100%":
#             totalDrawTaskEntirelyCorrect +=1
#             totalTimeEntirelyCorrect += float(correctResponses.time)
#         if correctResponses.percentage_correct == "50%":
#             fiftyPercentCorrect +=1
#         if correctResponses.percentage_correct == "25%":
#             twentyFivePercentCorrect +=1
#     totalNumberOfDrawTasks = len(p.training_task.task.draw_tasks)
#     weightedCorrectness = (totalDrawTaskEntirelyCorrect*1+fiftyPercentCorrect*.5+twentyFivePercentCorrect*.25)
#     drawData.average_correctness = weightedCorrectness/totalNumberOfDrawTasks
#     drawTask.percentage_correct = totalDrawTaskEntirelyCorrect/totalNumberOfDrawTasks
#     print("Percentage of average correctness across Draw Tasks: ", drawData.average_correctness)
#     print("Percentage of Draw Task gotten 100% Correct: ", drawTask.percentage_correct)
#     drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect/totalDrawTaskEntirelyCorrect
#     averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
#     print("Time spent during 100% correct responses to draw tasks during Training phase", averageTimeToAnswerDrawTaskEntirelyCorrect,"\n")
#
#     # Average time, correctness, and ratio of 100% correct responses to Draw Task during TESTING phase
#     # Aggregated time is save only when participant is 100% correct
# if p.testing_task.name == "draw":
#     drawTask = DrawTask()
#     totalTimeEntirelyCorrect = drawTask.time
#     totalDrawTaskEntirelyCorrect = 0
#     fiftyPercentCorrect = 0
#     twentyFivePercentCorrect = 0
#     drawData = DrawData()
#     for correctResponses in p.testing_task.task.draw_tasks:
#         if correctResponses.percentage_correct == "100%":
#             totalDrawTaskEntirelyCorrect += 1
#             totalTimeEntirelyCorrect += float(correctResponses.time)
#         if correctResponses.percentage_correct == "50%":
#             fiftyPercentCorrect += 1
#         if correctResponses.percentage_correct == "25%":
#             twentyFivePercentCorrect += 1
#     totalNumberOfDrawTasks = len(p.testing_task.task.draw_tasks)
#     weightedCorrectness = (totalDrawTaskEntirelyCorrect * 1 + fiftyPercentCorrect * .5 + twentyFivePercentCorrect * .25)
#     drawData.average_correctness = weightedCorrectness / totalNumberOfDrawTasks
#     drawTask.percentage_correct = totalDrawTaskEntirelyCorrect / totalNumberOfDrawTasks
#     print("Percentage of average correctness across Draw Tasks: ", drawData.average_correctness)
#     print("Percentage of Draw Task gotten 100% Correct: ", drawTask.percentage_correct)
#     drawData.averageTimeToAnswerDrawTaskEntirelyCorrect = totalTimeEntirelyCorrect / totalDrawTaskEntirelyCorrect
#     averageTimeToAnswerDrawTaskEntirelyCorrect = drawData.averageTimeToAnswerDrawTaskEntirelyCorrect
#     print("Time spent during 100% correct responses to draw tasks during Training phase",
#           averageTimeToAnswerDrawTaskEntirelyCorrect, "\n")
#
#
# # Participant's Hanoi task data
# # Average time, correctness, and ratio of 100% correct responses to Hanoi Task during ASSESSMENT phase
# # Aggregated time is save only when participant is 100% correct
#
# if p.assessment_task.name == "hanoi":
#     iterant = 0
#     totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase = 0
#     numberOfHanoiTasksPerPhasePerParticipant = len(p.assessment_task.task.hanoi_tasks)
#     totalTime = 0
#     # print("numberOfHanoiTasksPerPhasePerParticipant: ", numberOfHanoiTasksPerPhasePerParticipant)
#     for eachHanoiTask in p.assessment_task.task.hanoi_tasks:
#         # print("number of moves incomplete and complete: ", len(p.assessment_task.task.hanoi_tasks[iterant].hanoi_move_list))
#         p.moves_to_complete = len(p.assessment_task.task.hanoi_tasks[iterant].hanoi_move_list)
#         totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
#         print("totalNumberOfMovesBeforeComplete: ", totalNumberOfMovesBeforeCompletePerTask)
#         totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase += len(p.assessment_task.task.hanoi_tasks[iterant].hanoi_move_list)
#         print("totalNumberOfMovesBeforeComplete: ", totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase)
#         # Time calculations to be implemented
#         totalTime += p.assessment_task.task.hanoi_tasks[iterant].time_to_complete
#         print("time to complete task: ", totalTime)
#         iterant+=1
#     p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase/numberOfHanoiTasksPerPhasePerParticipant
#     print("p.average_moves_to_complete: ", p.average_moves_to_complete)
#
# print("BUG HEREEEEEEEEEE")
# # Average time, correctness, and ratio of 100% correct responses to Hanoi Task during TRAINING phase
# # Aggregated time is save only when participant is 100% correct
# # ********Bug...Draw task is labelled as Hanoi task
# if p.training_task.name == "hanoi":
#     print("p.training_task.name: ", p.training_task.name)
#     iterant = 0
#     totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase = 0
#     print("HEREEEEEEEEEE")
#     print("p.training_task.name: ", p.training_task.name)
#     numberOfHanoiTasksPerPhasePerParticipant = len(p.training_task.task.hanoi_tasks)
#     totalTime = 0
#     for eachHanoiTask in p.training_task.task.hanoi_tasks:
#         p.moves_to_complete = len(p.training_task.task.hanoi_tasks[iterant].hanoi_move_list)
#         totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
#         print("totalNumberOfMovesBeforeComplete: ", totalNumberOfMovesBeforeCompletePerTask)
#         totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase += len(p.training_task.task.hanoi_tasks[iterant].hanoi_move_list)
#         print("totalNumberOfMovesBeforeComplete: ", totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase)
#         # Time calculations to be implemented
#         totalTime += p.training_task.task.hanoi_tasks[iterant].time_to_complete
#         print("time to complete task: ", totalTime)
#         iterant+=1
#     p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase/numberOfHanoiTasksPerPhasePerParticipant
#     print("p.average_moves_to_complete: ", p.average_moves_to_complete)
#
#
# # Average time, correctness, and ratio of 100% correct responses to Hanoi Task during TESTING phase
# # Aggregated time is save only when participant is 100% correct
# if p.testing_task.name == "hanoi":
#     iterant = 0
#     totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase = 0
#     numberOfHanoiTasksPerPhasePerParticipant = len(p.testing_task.task.hanoi_tasks)
#     totalTime = 0
#     for eachHanoiTask in p.testing_task.task.hanoi_tasks:
#         p.moves_to_complete = len(p.testing_task.task.hanoi_tasks[iterant].hanoi_move_list)
#         totalNumberOfMovesBeforeCompletePerTask = p.moves_to_complete
#         print("totalNumberOfMovesBeforeComplete: ", totalNumberOfMovesBeforeCompletePerTask)
#         totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase += len(p.testing_task.task.hanoi_tasks[iterant].hanoi_move_list)
#         print("totalNumberOfMovesBeforeComplete: ", totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase)
#         # Time calculations to be implemented
#         totalTime += p.testing_task.task.hanoi_tasks[iterant].time_to_complete
#         print("time to complete task: ", totalTime)
#         iterant+=1
#     p.average_moves_to_complete = totalNumberOfMovesBeforeCompleteForAllHanoiTasksPerPhase/numberOfHanoiTasksPerPhasePerParticipant
#     print("p.average_moves_to_complete: ", p.average_moves_to_complete)
#
#
#
#
#
#
#
#
# # '''
# # calculate number of moves until correct per participant per phase
# # average out number of moves for all participants per phase
# # Get primary task per phase per participant (assessment, training, and testing)
# #     For draw, get total number of tasks per participant per phase
# #         For draw, get total CORRECT responses to draw tasks per participant per phase
# #             For draw, get total CORRECT responses to draw tasks across participants per phase
# #     For hanoi, get total number of tasks per participant per phase
# #         For hanoi, get total CORRECT responses to hanoi tasks per participant per phase
# #             For hanoi, get total number of moves to complete EACH hanoi task per participant per phase
# #                 For hanoi, get average number of moves when CORRECT reponses to hanoi task per participant per phase
# #                     For hanoi, get average number of moves when CORRECT reponses to hanoi task per participant per phase
# #
# # Get interruption per phase per participant (assessment, training, and testing)
# #     For stroop, get total number of interruptions per participant per phase
# #         For stroop, get total CORRECT reponses to stroop interruptions per participant per phase
# #             For stroop, get total time to provide CORRECT reponses to stroop interruptions per participant per phase
# #                 For stroop, get average time to provide CORRECT reponses to stroop interruptions per participant per phase
# # Get interruption per phase per participant (assessment, training, and testing)
# #     For math, get total number of interruptions per participant per phase
# #         For math, get total CORRECT reponses to math interruptions per participant per phase
# #             For math, get total time to provide CORRECT reponses to math interruptions per participant per phase
# #                 For math, get average time to provide CORRECT reponses to math interruptions per participant per phase
# #
# #
# # Plot increase of decrease of average time from phase to phase per participant
# # Plot increase of decrease of average time from phase to phase across all participants
# #
# # '''