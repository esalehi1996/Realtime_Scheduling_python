class Periodic_Task:

    def __init__(self, name, phase, compute, period, deadline):
        self.name = name
        self.phase = phase
        self.compute = compute
        self.period = period
        self.deadline = deadline

    def dec_compute_time(self):
        self.compute = self.compute - 1





class APeriodic_Task:

    def __init__(self,name , arrival , compute , deadline , precedence):
        self.name = name
        self.arrival = arrival
        self.compute = compute
        self.deadline = deadline
        self.precedence = precedence

    def dec_compute_time(self):
        self.compute = self.compute - 1




