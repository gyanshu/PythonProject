import time
import threading
import heapq
from typing import Optional
from queue import PriorityQueue

# Base class for scheduled tasks
class ScheduledTask:
    def __init__(self, arrival_time: float, context):
        self.arrival_time = arrival_time
        self.context = context

    def execute(self):
        self.context.execute()

    def is_recurring(self) -> bool:
        raise NotImplementedError

    def next_scheduled_task(self) -> Optional["ScheduledTask"]:
        raise NotImplementedError

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

# One-time task
class OneTimeTask(ScheduledTask):
    def __init__(self, arrival_time: float, context):
        super().__init__(arrival_time, context)

    def is_recurring(self) -> bool:
        return False

    def next_scheduled_task(self) -> Optional["ScheduledTask"]:
        return None

# Recurring task
class RecurringTask(ScheduledTask):
    def __init__(self, arrival_time: float, interval: float, context):
        super().__init__(arrival_time, context)
        self.interval = interval

    def is_recurring(self) -> bool:
        return True

    def next_scheduled_task(self) -> Optional["ScheduledTask"]:
        return RecurringTask(self.arrival_time + self.interval, self.interval, self.context)

# Execution context
class ExecutionContext:
    def __init__(self, task_name: str):
        self.task_name = task_name

    def execute(self):
        print(f"Executing task: {self.task_name} at {time.time()}")

# Task Store with a priority queue
class TaskStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.queue = []

    def add(self, task: ScheduledTask):
        with self.lock:
            heapq.heappush(self.queue, task)

    def poll(self) -> Optional[ScheduledTask]:
        with self.lock:
            return heapq.heappop(self.queue) if self.queue else None

    def peek(self) -> Optional[ScheduledTask]:
        with self.lock:
            return self.queue[0] if self.queue else None

    def is_empty(self) -> bool:
        with self.lock:
            return len(self.queue) == 0

# Worker thread for executing tasks
class TaskRunner(threading.Thread):
    def __init__(self, task_store: TaskStore):
        super().__init__()
        self.task_store = task_store
        self.running = True

    def run(self):
        while self.running:
            task = self.task_store.poll()
            if task:
                now = time.time()
                delay = task.arrival_time - now
                if delay > 0:
                    time.sleep(delay)

                task.execute()
                if task.is_recurring():
                    self.task_store.add(task.next_scheduled_task())

            else:
                time.sleep(1)  # No tasks, sleep briefly to reduce CPU usage

    def stop(self):
        self.running = False

# Task Scheduler
class TaskScheduler:
    def __init__(self, num_threads: int):
        self.task_store = TaskStore()
        self.threads = [TaskRunner(self.task_store) for _ in range(num_threads)]

    def start(self):
        for thread in self.threads:
            thread.start()

    def schedule_task(self, task: ScheduledTask):
        self.task_store.add(task)

    def stop(self):
        for thread in self.threads:
            thread.stop()
        for thread in self.threads:
            thread.join()

# Example usage
if __name__ == "__main__":
    scheduler = TaskScheduler(num_threads=2)
    scheduler.start()

    scheduler.schedule_task(OneTimeTask(time.time() + 5, ExecutionContext("One-time Task 1")))
    scheduler.schedule_task(RecurringTask(time.time() + 2, 3, ExecutionContext("Recurring Task")))

    time.sleep(10)  # Let tasks run for a while
    scheduler.stop()
