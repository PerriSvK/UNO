class Scheduler:
    def __init__(self):
        self._task_list = []

    def add_task(self, task, time):
        self._task_list.append([task, time])

    def tick(self):
        i = 0
        while i < len(self._task_list):
            a = self._task_list[i]
            if a[1] == 0:
                a[0].run()
                self._task_list.pop(i)
            else:
                a[1] -= 1
                i += 1
