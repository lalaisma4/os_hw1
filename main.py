import csv
import sys
import os

CONTEXT_SWITCH_TIME = 0.001
TIME_QUANTUM = 4

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0
        self.start_time = -1

def read_processes(filename):
    processes = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            priority_map = {'high': 1, 'normal': 2, 'low': 3}
            p = Process(
                row['Process_ID'],
                int(row['Arrival_Time']),
                int(row['CPU_Burst_Time']),
                priority_map[row['Priority']]
            )
            processes.append(p)
    return processes

def fcfs(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    procs.sort(key=lambda x: x.arrival)
    
    timeline = []
    time = 0
    context_switches = 0
    
    for p in procs:
        if time < p.arrival:
            if time > 0:
                context_switches += 1
            timeline.append(('IDLE', time, p.arrival))
            time = p.arrival
        
        if timeline and timeline[-1][0] != 'IDLE':
            context_switches += 1
            
        p.start_time = time
        p.completion = time + p.burst
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst
        
        timeline.append((p.pid, time, p.completion))
        time = p.completion
    
    return procs, timeline, context_switches

def preemptive_sjf(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    timeline = []
    time = 0
    completed = []
    context_switches = 0
    last_pid = None
    
    while len(completed) < len(procs):
        ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
        
        if not ready:
            next_arrival = min([p.arrival for p in procs if p.remaining > 0])
            if last_pid:
                context_switches += 1
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            last_pid = None
            continue
        
        current = min(ready, key=lambda x: (x.remaining, x.arrival))
        
        if last_pid and last_pid != current.pid:
            context_switches += 1
        
        if current.start_time == -1:
            current.start_time = time
        
        next_event = time + 1
        for p in procs:
            if p.arrival > time and p.arrival < next_event:
                next_event = p.arrival
        
        if current.remaining < next_event - time:
            next_event = time + current.remaining
        
        duration = next_event - time
        timeline.append((current.pid, time, next_event))
        current.remaining -= duration
        time = next_event
        last_pid = current.pid
        
        if current.remaining == 0:
            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst
            completed.append(current)
    
    return procs, timeline, context_switches

def non_preemptive_sjf(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    timeline = []
    time = 0
    completed = []
    context_switches = 0
    
    while len(completed) < len(procs):
        ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
        
        if not ready:
            next_arrival = min([p.arrival for p in procs if p.remaining > 0])
            if time > 0:
                context_switches += 1
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            continue
        
        current = min(ready, key=lambda x: (x.burst, x.arrival))
        
        if timeline and timeline[-1][0] != 'IDLE':
            context_switches += 1
            
        current.start_time = time
        current.completion = time + current.burst
        current.turnaround = current.completion - current.arrival
        current.waiting = current.turnaround - current.burst
        current.remaining = 0
        
        timeline.append((current.pid, time, current.completion))
        time = current.completion
        completed.append(current)
    
    return procs, timeline, context_switches

def round_robin(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    timeline = []
    time = 0
    queue = []
    context_switches = 0
    last_pid = None
    completed = []
    
    procs.sort(key=lambda x: x.arrival)
    idx = 0
    
    while len(completed) < len(procs):
        while idx < len(procs) and procs[idx].arrival <= time:
            queue.append(procs[idx])
            idx += 1
        
        if not queue:
            next_arrival = procs[idx].arrival
            if last_pid:
                context_switches += 1
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            last_pid = None
            continue
        
        current = queue.pop(0)
        
        if last_pid and last_pid != current.pid:
            context_switches += 1
        
        if current.start_time == -1:
            current.start_time = time
        
        exec_time = min(TIME_QUANTUM, current.remaining)
        current.remaining -= exec_time
        
        timeline.append((current.pid, time, time + exec_time))
        time += exec_time
        last_pid = current.pid
        
        while idx < len(procs) and procs[idx].arrival <= time:
            queue.append(procs[idx])
            idx += 1
        
        if current.remaining > 0:
            queue.append(current)
        else:
            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst
            completed.append(current)
    
    return procs, timeline, context_switches

def preemptive_priority(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    timeline = []
    time = 0
    completed = []
    context_switches = 0
    last_pid = None
    
    while len(completed) < len(procs):
        ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
        
        if not ready:
            next_arrival = min([p.arrival for p in procs if p.remaining > 0])
            if last_pid:
                context_switches += 1
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            last_pid = None
            continue
        
        current = min(ready, key=lambda x: (x.priority, x.arrival))
        
        if last_pid and last_pid != current.pid:
            context_switches += 1
        
        if current.start_time == -1:
            current.start_time = time
        
        next_event = time + 1
        for p in procs:
            if p.arrival > time and p.arrival < next_event:
                next_event = p.arrival
        
        if current.remaining < next_event - time:
            next_event = time + current.remaining
        
        duration = next_event - time
        timeline.append((current.pid, time, next_event))
        current.remaining -= duration
        time = next_event
        last_pid = current.pid
        
        if current.remaining == 0:
            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst
            completed.append(current)
    
    return procs, timeline, context_switches

def non_preemptive_priority(processes):
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    timeline = []
    time = 0
    completed = []
    context_switches = 0
    
    while len(completed) < len(procs):
        ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
        
        if not ready:
            next_arrival = min([p.arrival for p in procs if p.remaining > 0])
            if time > 0:
                context_switches += 1
            timeline.append(('IDLE', time, next_arrival))
            time = next_arrival
            continue
        
        current = min(ready, key=lambda x: (x.priority, x.arrival))
        
        if timeline and timeline[-1][0] != 'IDLE':
            context_switches += 1
            
        current.start_time = time
        current.completion = time + current.burst
        current.turnaround = current.completion - current.arrival
        current.waiting = current.turnaround - current.burst
        current.remaining = 0
        
        timeline.append((current.pid, time, current.completion))
        time = current.completion
        completed.append(current)
    
    return procs, timeline, context_switches

def merge_timeline(timeline):
    if not timeline:
        return []
    
    merged = []
    current_pid, start, end = timeline[0]
    
    for i in range(1, len(timeline)):
        pid, s, e = timeline[i]
        if pid == current_pid and s == end:
            end = e
        else:
            merged.append((current_pid, start, end))
            current_pid, start, end = pid, s, e
    
    merged.append((current_pid, start, end))
    return merged

def calculate_metrics(processes, timeline, context_switches):
    completion_times = {p.pid: p.completion for p in processes}
    
    waiting_times = [p.waiting for p in processes]
    turnaround_times = [p.turnaround for p in processes]
    
    max_wait = max(waiting_times)
    avg_wait = sum(waiting_times) / len(waiting_times)
    max_turnaround = max(turnaround_times)
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    
    throughput = {}
    for t in [50, 100, 150, 200]:
        count = sum(1 for p in processes if p.completion <= t)
        throughput[t] = count
    
    total_time = max(p.completion for p in processes)
    idle_time = sum(e - s for pid, s, e in timeline if pid == 'IDLE')
    cpu_busy_time = total_time - idle_time
    context_switch_overhead = context_switches * CONTEXT_SWITCH_TIME
    cpu_efficiency = ((cpu_busy_time - context_switch_overhead) / total_time) * 100
    
    return {
        'max_wait': max_wait,
        'avg_wait': avg_wait,
        'max_turnaround': max_turnaround,
        'avg_turnaround': avg_turnaround,
        'throughput': throughput,
        'cpu_efficiency': cpu_efficiency,
        'context_switches': context_switches
    }

def write_results(algo_name, processes, timeline, metrics, output_dir):
    merged = merge_timeline(timeline)
    
    filename = os.path.join(output_dir, f"{algo_name}.txt")
    with open(filename, 'w') as f:
        f.write(f"=== {algo_name.upper().replace('_', ' ')} ===\n\n")
        
        f.write("Zaman Tablosu:\n")
        for pid, start, end in merged:
            f.write(f"[{start:4}] - - {pid:8s} - - [{end:4}]\n")
        
        f.write(f"\nMaksimum Bekleme Süresi: {metrics['max_wait']}\n")
        f.write(f"Ortalama Bekleme Süresi: {metrics['avg_wait']:.2f}\n")
        
        f.write(f"\nMaksimum Tamamlanma Süresi: {metrics['max_turnaround']}\n")
        f.write(f"Ortalama Tamamlanma Süresi: {metrics['avg_turnaround']:.2f}\n")
        
        f.write(f"\nİş Tamamlama Sayısı (Throughput):\n")
        for t in [50, 100, 150, 200]:
            f.write(f"  T={t}: {metrics['throughput'][t]} işlem\n")
        
        f.write(f"\nOrtalama CPU Verimliliği: {metrics['cpu_efficiency']:.2f}%\n")
        f.write(f"Toplam Bağlam Değiştirme Sayısı: {metrics['context_switches']}\n")

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python main.py <input.csv>")
        return
    
    input_file = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = f"results_{base_name}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    processes = read_processes(input_file)
    
    algorithms = [
        ("fcfs", fcfs),
        ("preemptive_sjf", preemptive_sjf),
        ("non_preemptive_sjf", non_preemptive_sjf),
        ("round_robin", round_robin),
        ("preemptive_priority", preemptive_priority),
        ("non_preemptive_priority", non_preemptive_priority)
    ]
    
    for name, algo in algorithms:
        procs, timeline, cs = algo(processes)
        metrics = calculate_metrics(procs, timeline, cs)
        write_results(name, procs, timeline, metrics, output_dir)
        print(f"{name} tamamlandı")
    
    print(f"\nSonuçlar '{output_dir}' klasörüne kaydedildi")

if __name__ == "__main__":
    main()
