from tasks import APeriodic_Task
import numpy as np
import pandas as pd


def jackson(task_list, clock_number):

    schedule = []
    online_tasks = []

    for task in task_list:
        online_tasks.append(APeriodic_Task(task.name, task.arrival, task.compute, task.deadline, task.precedence))

    online_tasks.sort(key=lambda x: x.deadline, reverse=False)

    for i in range(clock_number):
        if len(online_tasks) == 0:
            schedule.append("idle")
            continue
        schedule.append(online_tasks[0].name)
        online_tasks[0].dec_compute_time()
        if online_tasks[0].compute == 0:
            del online_tasks[0]

    return schedule


def horn(task_list, clock_number):

    schedule = []
    online_tasks = []

    for i in range(clock_number):
        for task in task_list:
            if i == task.arrival:
                online_tasks.append(APeriodic_Task(task.name, task.arrival, task.compute, task.deadline, task.precedence))

        online_tasks.sort(key=lambda x: x.deadline, reverse=False)
        if len(online_tasks) == 0:
            schedule.append("idle")
            continue
        schedule.append(online_tasks[0].name)
        online_tasks[0].dec_compute_time()
        if online_tasks[0].compute == 0:
            del online_tasks[0]

    return schedule


def feasibility_check(task_list , start_time):

    feasiblity = False
    for task in task_list:
        st = max(start_time, task.arrival)
        if task.compute + st > task.deadline:
            return False
    if len(task_list) == 1:
        return True
    for i in range(len(task_list)):
        new_task_list = task_list.copy()
        tcom = new_task_list[i].compute
        st = max(new_task_list[i].arrival, start_time)
        del new_task_list[i]
        feasiblity = feasiblity | feasibility_check(task_list = new_task_list, start_time = st + tcom)
    return feasiblity


def bratley(task_list):
    return feasibility_check(task_list, 0)


def LDF(tasklist):
    graphmatrix = np.zeros([len(tasklist) , len(tasklist)])
    namelist = []
    sched = []
    for i,t in enumerate(tasklist):
        namelist.append(t.name)
        for p in t.precedence:
            graphmatrix[i,indexfinder(tasklist,p)] = 1
    graphmatrix = graphmatrix.T
    gmat = pd.DataFrame(graphmatrix, columns= namelist, index= namelist)

    while not gmat.empty:
        df = gmat[(gmat.T == 0).all()]
        name_ls = df.index.values
        tmd = maxdeadlinefinder(tasklist,name_ls)
        sched.append(tmd)
        gmat = gmat.drop(tmd.name, axis=0)
        gmat = gmat.drop(tmd.name , axis = 1)
    schedule = []
    sched = reversed(sched)
    for t in sched:
        for n in range(t.compute):
            schedule.append(t.name)
    return schedule


def indexfinder(tasklist,p):
    for i,t in enumerate(tasklist):
        if(t.name == p):
            return i

def maxdeadlinefinder(tasklist,namelist):
    maxdeadline = -1
    for name in namelist:
        for t in tasklist:
            if t.name == name:
                break
        if t.deadline > maxdeadline:
            maxdeadline = t.deadline
            task_with_max_deadline = t
    return task_with_max_deadline

def EDFstar(tasklist):
    graphmatrix = np.zeros([len(tasklist), len(tasklist)])
    namelist = []
    sched = []
    for i, t in enumerate(tasklist):
        namelist.append(t.name)
        for p in t.precedence:
            graphmatrix[i, indexfinder(tasklist, p)] = 1
    df = pd.DataFrame(graphmatrix, columns=namelist, index=namelist)
    dfT = pd.DataFrame(graphmatrix.T, columns=namelist, index=namelist)
    rdf = pd.DataFrame(columns= [] , index= namelist)
    ddf = pd.DataFrame(columns= [] , index= namelist)
    #rdf.loc['t1',0] = 1
    while not df.empty:
        tdf = df[(df.T == 0).all()]
        name_ls = tdf.index.values
        for name in name_ls:
            rel = release_finder(name,tasklist,rdf)
            rdf.loc[name,0] = rel
            df = df.drop(name, axis=0)
            df = df.drop(name, axis=1)
    dfTaux = pd.DataFrame(graphmatrix.T, columns=namelist, index=namelist)
    while not dfT.empty:
        tdf = dfT[(dfT.T == 0).all()]
        name_ls = tdf.index.values
        for name in name_ls:
            prec_ls = []
            for n in list(dfTaux):
                if(dfTaux.loc[name,n]== 1):
                    for tsk in tasklist:
                        if(tsk.name == n):
                            prec_ls.append(tsk)
                            break
            deadline = deadline_finder(name,tasklist,ddf,prec_ls)
            ddf.loc[name,0] = deadline
            dfT = dfT.drop(name, axis=0)
            dfT = dfT.drop(name, axis=1)
    new_tasklist = []
    for t in tasklist:
        new_tasklist.append(APeriodic_Task(name = t.name, arrival=  rdf.loc[t.name,0], compute= t.compute, deadline= ddf.loc[t.name,0], precedence= []))
    return new_tasklist




def release_finder(name , tasklist , rdf):
    for t in tasklist:
        if(t.name == name):
            task = t
            break
    release = task.arrival
    pred_ls = []
    for pred in task.precedence:
        for t in tasklist:
            if(t.name == pred):
                pred_ls.append(t)
                break
    for t in pred_ls:
        if(rdf.loc[t.name,0] + t.compute > release):
            release = rdf.loc[t.name,0] + t.compute
    return release


def deadline_finder(name,tasklist,ddf,prec_ls):
    for t in tasklist:
        if(t.name == name):
            task = t
            break
    deadline = task.deadline
    for t in prec_ls:
        if(ddf.loc[t.name,0] - t.compute < deadline):
            deadline = ddf.loc[t.name,0] - t.compute
    return deadline









