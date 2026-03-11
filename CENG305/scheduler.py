import sys
class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = int(arrival)
        self.burst = int(burst)
        self.priority = int(priority)


def read_processes(filename):
    processes = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pid, arr, burst, pr = [x.strip() for x in line.split(",")]
            processes.append(Process(pid, arr, burst, pr))
    return processes


def fcfs(processes):
    time = 0
    gantt = []
    results = []
    idle = 0

    for p in processes:
        if time < p.arrival:
            idle += p.arrival - time
            time = p.arrival

        start = time
        time += p.burst
        finish = time

        gantt.append((p.pid, start, finish))
        turnaround = finish - p.arrival
        waiting = turnaround - p.burst

        results.append((p.pid, finish, turnaround, waiting))

    total_time = gantt[-1][2]
    utilization = ((total_time - idle) / total_time) * 100

    return gantt, results, utilization

def sjf(processes):

    time = 0
    gantt = []
    results = []
    idle = 0
    completed = []

    while len(completed) < len(processes):
        available = [p for p in processes if p.arrival <= time and p not in completed]

        if not available:
            next_arrival = min(p.arrival for p in processes if p not in completed)
            idle += next_arrival - time
            time = next_arrival
            continue

        available.sort(key=lambda p: (p.burst, p.arrival))
        p = available[0]

        start = time
        time += p.burst
        finish = time

        gantt.append((p.pid, start, finish))

        turnaround = finish - p.arrival
        waiting = turnaround - p.burst
        results.append((p.pid, finish, turnaround, waiting))

        completed.append(p)
       
        total_time = gantt[-1][2]
    utilization = ((total_time - idle) / total_time) * 100

    return gantt, results, utilization

def priority_scheduling(processes):
    time = 0
    gantt = []
    results = []
    idle = 0
    completed = []

    while len(completed) < len(processes):
        available = [p for p in processes if p.arrival <= time and p not in completed]

        if not available:
            next_arrival = min(p.arrival for p in processes if p not in completed)
            idle += next_arrival - time
            time = next_arrival
            continue

        available.sort(key=lambda p: (p.priority, p.arrival))
        p = available[0]

        start = time
        time += p.burst
        finish = time

        gantt.append((p.pid, start, finish))

        turnaround = finish - p.arrival
        waiting = turnaround - p.burst
        results.append((p.pid, finish, turnaround, waiting))

        completed.append(p)

    total_time = gantt[-1][2]
    utilization = ((total_time - idle) / total_time) * 100

    return gantt, results, utilization

    total_time = gantt[-1][2]
    utilization = ((total_time - idle) / total_time) * 100

    return gantt, results, utilization

def round_robin(processes, tq):
    time = 0
    gantt = []
    idle = 0

    remaining = {p.pid: p.burst for p in processes}
    finish_time = {}

    ready = []
    processes_sorted = sorted(processes, key=lambda p: p.arrival)
    i = 0
    n = len(processes)

    if processes_sorted:
        time = processes_sorted[0].arrival

    while len(finish_time) < n:
        while i < n and processes_sorted[i].arrival <= time:
            ready.append(processes_sorted[i])
            i += 1

        if not ready:
            next_arrival = processes_sorted[i].arrival
            gantt.append(("IDLE", time, next_arrival))
            idle += next_arrival - time
            time = next_arrival
            continue

        p = ready.pop(0)
        run = min(tq, remaining[p.pid])

        start = time
        time += run
        remaining[p.pid] -= run
        gantt.append((p.pid, start, time))

        while i < n and processes_sorted[i].arrival <= time:
            ready.append(processes_sorted[i])
            i += 1

        if remaining[p.pid] == 0:
            finish_time[p.pid] = time
        else:
            ready.append(p)

    results = []

    for p in processes:
        finish = finish_time[p.pid]
        turnaround = finish - p.arrival
        waiting = turnaround - p.burst
        results.append((p.pid, finish, turnaround, waiting))

    total_time = gantt[-1][2]
    utilization = ((total_time - idle) / total_time) * 100

    return gantt, results, utilization

def print_output(name, gantt, results, utilization):
    print(f"\n--- Scheduling Algorithm: {name} ---")
    print("Gantt Chart:")
    for pid, start, end in gantt:
        print(f"[{start}]--{pid}--[{end}] ", end="")
    print("\n")

    print("Process | Finish | Turnaround | Waiting")
    print("---------------------------------------")
    for r in results:
        print(f"{r[0]:7} | {r[1]:6} | {r[2]:10} | {r[3]:7}")

    avg_ta = sum(r[2] for r in results) / len(results)
    avg_wt = sum(r[3] for r in results) / len(results)

    print(f"\nAverage Turnaround Time: {avg_ta:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"CPU Utilization: {utilization:.2f}%\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scheduler.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    processes = read_processes(input_file)

    print("Processes read from file:")
    for p in processes:
        print(p.pid, p.arrival, p.burst, p.priority)

    processes_fcfs = sorted(processes, key=lambda x: x.arrival)

    gantt_fcfs, res_fcfs, util_fcfs = fcfs(processes_fcfs)
    print_output("FCFS", gantt_fcfs, res_fcfs, util_fcfs)

    gantt_sjf, res_sjf, util_sjf = sjf(processes)
    print_output("SJF (Non-preemptive)", gantt_sjf, res_sjf, util_sjf)
    
    gantt_pr, results_pr, util_pr = priority_scheduling(processes)
    print_output("Priority (Non-preemptive)", gantt_pr, results_pr, util_pr)

    tq = 3
    gantt_rr, results_rr, util_rr = round_robin(processes, tq)
    print_output(f"Round Robin (tq={tq})", gantt_rr, results_rr, util_rr)

def sjf_non_preemptive(processes):
    return sjf(processes)


def priority_non_preemptive(processes):
    return priority_scheduling(processes)
