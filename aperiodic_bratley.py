from tasks import APeriodic_Task
import numpy as np
import pandas as pd

def bratley(tasklist):
    return feasibility_check(tasklist,0)




def feasibility_check(tasklist , starttime):
    feasiblity = False
    for t in tasklist:
        st = max(starttime,t.arrival)
        if(t.compute + st > t.deadline):
            return False
    if(len(tasklist)==1):
        return True
    for i in range(len(tasklist)):
        newtasklist = tasklist.copy()
        tcom = newtasklist[i].compute
        st = max(newtasklist[i].arrival,starttime)
        del newtasklist[i]
        feasiblity = feasiblity | feasibility_check(tasklist = newtasklist , starttime = st + tcom)
    return feasiblity


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









'''
tasklist = []
t1 = APeriodic_Task(name = '', arrival=  4, compute= 7, deadline= 11, precedence= [])
t2 = APeriodic_Task(name = '', arrival=  1, compute= 1, deadline= 5, precedence= [])
t3 = APeriodic_Task(name = '', arrival=  1, compute= 2, deadline= 6, precedence= [])
t4 = APeriodic_Task(name = '', arrival=  0, compute= 2, deadline= 4, precedence= [])


print(bratley(tasklist))

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
#sched = LDF(tasklist)
#print(sched)
new_tasklist = EDFstar(tasklist)

for t in new_tasklist:
    print(t.name,t.arrival,t.compute,t.deadline)