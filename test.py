from tasks import  Periodic_Task,APeriodic_Task
from periodic_algorithms import *
from aperiodic_algorithms import *
from fixed_priority_servers import polling_server,background_scheduling
'''

task0 = Periodic_Task(name = "t0", phase = 0, compute = 2, deadline = 5, period= 5)
task1 = Periodic_Task(name = "t1", phase = 0, compute = 4, deadline = 7, period= 7)
t_list = []
t_list.append(task0)
t_list.append(task1)

print("edf periodic")
sched = earliest_deadline_first_periodic(t_list, 35)
print(sched)

job0 = APeriodic_Task("j0", 0, 1, 2, "")
job1 = APeriodic_Task("j1", 0, 2, 5, "")
job2 = APeriodic_Task("j2", 2, 2, 4, "")
job3 = APeriodic_Task("j3", 3, 2, 10, "")
job4 = APeriodic_Task("j4", 6, 2, 9, "")
j_list = []
j_list.append(job0)
j_list.append(job1)
j_list.append(job2)
j_list.append(job3)
j_list.append(job4)

print("jackson")
sched = horn(j_list, 12)
print(sched)

task2 = Periodic_Task("t2", 0, 1, 4, 4)
task3 = Periodic_Task("t3", 0, 2, 6, 6)
job5 = APeriodic_Task("j5", 2, 2, 100, "")
job6 = APeriodic_Task("j6", 8, 1, 100, "")
job7 = APeriodic_Task("j7", 12, 2, 100, "")
job8 = APeriodic_Task("j8", 19, 1, 100, "")
t_list.clear()
t_list.append(task2)
t_list.append(task3)
j_list.clear()
j_list.append(job5)
j_list.append(job6)
j_list.append(job7)
j_list.append(job8)

print("polling server")
sched = polling_server(t_list, j_list, 5, 2, 40)
print(sched)


tasklist = []
t1 = APeriodic_Task(name = 't1', arrival=  0, compute= 1, deadline= 100, precedence= [])
t2 = APeriodic_Task(name = 't2', arrival=  0, compute= 2, deadline= 100, precedence= ['t1'])
t3 = APeriodic_Task(name = 't3', arrival=  0, compute= 3, deadline= 100, precedence= ['t1'])
t4 = APeriodic_Task(name = 't4', arrival=  0, compute= 4, deadline= 100, precedence= ['t2'])
t5 = APeriodic_Task(name = 't5', arrival=  0, compute= 5, deadline= 100, precedence= ['t2'])
t6 = APeriodic_Task(name = 't6', arrival=  0, compute= 6, deadline= 100, precedence= ['t3'])
tasklist.append(t1)
tasklist.append(t2)
tasklist.append(t3)
tasklist.append(t4)
tasklist.append(t5)
tasklist.append(t6)

'''


tasklist = []
t1 = APeriodic_Task(name = 't1', arrival=  0, compute= 1, deadline= 100, precedence= [])
t2 = APeriodic_Task(name = 't2', arrival=  0, compute= 2, deadline= 100, precedence= ['t1'])
t3 = APeriodic_Task(name = 't3', arrival=  0, compute= 3, deadline= 100, precedence= ['t1'])
t4 = APeriodic_Task(name = 't4', arrival=  0, compute= 4, deadline= 100, precedence= ['t2'])
t5 = APeriodic_Task(name = 't5', arrival=  0, compute= 5, deadline= 100, precedence= ['t2'])
t6 = APeriodic_Task(name = 't6', arrival=  0, compute= 6, deadline= 100, precedence= ['t3'])
tasklist.append(t1)
tasklist.append(t2)
tasklist.append(t3)
tasklist.append(t4)
tasklist.append(t5)
tasklist.append(t6)
new_task_list = EDFstar(tasklist)
for t in new_task_list:
    print(t.name , t.arrival , t.compute , t.deadline )
sched = horn(new_task_list,100)
print(sched)
