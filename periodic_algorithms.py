from tasks import Periodic_Task


def rate_monotonic(task_list, clock_number):

    schedule = []
    online_tasks = []

    for i in range(clock_number):
        for task in task_list:
            if (i % task.period) == task.phase:
                online_tasks.append(
                    Periodic_Task(task.name, task.phase, task.compute, task.period, task.deadline))
        online_tasks.sort(key=lambda x: x.period, reverse=False)
        if len(online_tasks) == 0:
            schedule.append("idle")
            continue
        schedule.append(online_tasks[0].name)
        online_tasks[0].dec_compute_time()
        if online_tasks[0].compute == 0:
            del online_tasks[0]

    return schedule


def earliest_deadline_first_periodic(task_list, clock_number):

    schedule = []
    online_tasks = []

    for i in range(clock_number):
        for task in task_list:
            if (i % task.period) == task.phase:
                online_tasks.append(
                    Periodic_Task(task.name, task.phase, task.compute, task.period, task.deadline + i))
        online_tasks.sort(key=lambda x: x.deadline, reverse=False)
        if len(online_tasks) == 0:
            schedule.append("idle")
            continue
        schedule.append(online_tasks[0].name)
        online_tasks[0].dec_compute_time()
        if online_tasks[0].compute == 0:
            del online_tasks[0]

    return schedule


def deadline_monotonic(task_list, clock_number):

    schedule = []
    online_tasks = []

    for i in range(clock_number):
        for task in task_list:
            if (i % task.period) == task.phase:
                online_tasks.append(
                    Periodic_Task(task.name, task.phase, task.compute, task.period, task.deadline))
        online_tasks.sort(key=lambda x: x.deadline, reverse=False)
        if len(online_tasks) == 0:
            schedule.append("idle")
            continue
        schedule.append(online_tasks[0].name)
        online_tasks[0].dec_compute_time()
        if online_tasks[0].compute == 0:
            del online_tasks[0]

    return schedule
