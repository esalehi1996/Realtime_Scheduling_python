from tasks import Periodic_Task
from tasks import APeriodic_Task


def polling_server(task_list, job_list, server_period, server_capacity, clock_number):

    schedule = []
    online_tasks = []
    job_queue = []
    server_budget = 0
    server_active = False

    for job in job_list:
        job_queue.append(APeriodic_Task(job.name, job.arrival, job.compute, job.deadline, job.precedence))
    job_queue.sort(key=lambda x: x.arrival, reverse=False)

    for i in range(clock_number):
        for task in task_list:
            if (i % task.period) == task.phase:
                online_tasks.append(Periodic_Task(task.name, task.phase, task.compute, task.period, task.deadline))

        online_tasks.sort(key=lambda x: x.period, reverse=False)

        if i % server_period == 0:
            server_budget = server_capacity
            server_active = True
            if len(job_queue) == 0 or job_queue[0].arrival > i:
                server_active = False
                server_budget = 0
            if len(online_tasks) > 0 and online_tasks[0].period <= server_period:
                online_tasks[0].dec_compute_time()
                schedule.append(online_tasks[0].name)
                if online_tasks[0].compute == 0:
                    del online_tasks[0]
            else:
                if server_active:
                    job_queue[0].dec_compute_time()
                    server_budget = server_budget - 1
                    schedule.append(job_queue[0].name)
                    if server_budget == 0:
                        server_active = False
                    if job_queue[0].compute == 0:
                        del job_queue[0]
                else:
                    schedule.append("idle")
                    continue
        else:
            if len(job_queue) == 0 or job_queue[0].arrival > i:
                server_active = False
                server_budget = 0
            if server_active:
                if len(online_tasks) > 0 and online_tasks[0].period <= server_period:
                    online_tasks[0].dec_compute_time()
                    schedule.append(online_tasks[0].name)
                    if online_tasks[0].compute == 0:
                        del online_tasks[0]
                else:
                    job_queue[0].dec_compute_time()
                    server_budget = server_budget - 1
                    schedule.append(job_queue[0].name)
                    if server_budget == 0:
                        server_active = False
                    if job_queue[0].compute == 0:
                        del job_queue[0]
            else:
                if len(online_tasks) == 0:
                    schedule.append("idle")
                    continue
                else:
                    online_tasks[0].dec_compute_time()
                    schedule.append(online_tasks[0].name)
                    if online_tasks[0].compute == 0:
                        del online_tasks[0]

    return schedule


def background_scheduling(task_list, job_list, clock_number):

    schedule = []
    online_tasks = []
    job_queue = []

    for job in job_list:
        job_queue.append(APeriodic_Task(job.name, job.arrival, job.compute, job.deadline, job.precedence))
    job_queue.sort(key=lambda x: x.arrival, reverse=False)

    for i in range(clock_number):
        for task in task_list:
            if (i % task.period) == task.phase:
                online_tasks.append(Periodic_Task(task.name, task.phase, task.compute, task.period, task.deadline))

        online_tasks.sort(key=lambda x: x.period, reverse=False)
        if len(online_tasks) == 0:
            if len(job_queue) == 0 or job_queue[0].arrival > i:
                schedule.append("idle")
                continue
            else:
                job_queue[0].dec_compute_time()
                schedule.append(job_queue[0].name)
                if job_queue[0].compute == 0:
                    del job_queue[0]
        else:
            online_tasks[0].dec_compute_time()
            schedule.append(online_tasks[0].name)
            if online_tasks[0].compute == 0:
                del online_tasks[0]

    return schedule


