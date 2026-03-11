import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from scheduler import (
    read_processes,
    fcfs,
    sjf_non_preemptive,
    priority_non_preemptive,
    round_robin
)

def gantt_to_string(gantt):
    parts = []
    for pid, start, end in gantt:
        parts.append(f"[{start}]--{pid}--[{end}]")
    return " ".join(parts)

def calc_averages(results):
    n = len(results)
    avg_ta = sum(r[2] for r in results) / n if n else 0.0
    avg_wt = sum(r[3] for r in results) / n if n else 0.0
    return avg_ta, avg_wt

def format_report(name, gantt, results, utilization):
    out = []
    out.append(f"--- Scheduling Algorithm: {name} ---")
    out.append("Gantt Chart:")
    out.append(gantt_to_string(gantt))
    out.append("")
    out.append("Process | Finish Time | Turnaround Time | Waiting Time")
    out.append("------------------------------------------------------")
    for pid, finish, ta, wt in results:
        out.append(f"{pid:7} | {finish:11} | {ta:15} | {wt:12}")
    avg_ta, avg_wt = calc_averages(results)
    out.append("")
    out.append(f"Average Turnaround Time: {avg_ta:.2f}")
    out.append(f"Average Waiting Time: {avg_wt:.2f}")
    out.append(f"CPU Utilization: {utilization:.2f}%")
    return "\n".join(out)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Scheduling Simulator")
        self.geometry("900x650")
        self.file_path = tk.StringVar()
        self.tq_var = tk.StringVar(value="3")
        self.build_ui()

    def build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Input file:").pack(side="left")
        ttk.Entry(top, textvariable=self.file_path, width=60).pack(side="left", padx=8)
        ttk.Button(top, text="Browse", command=self.browse_file).pack(side="left")

        ttk.Label(top, text="RR Time Quantum:").pack(side="left", padx=(20, 6))
        ttk.Entry(top, textvariable=self.tq_var, width=8).pack(side="left")

        ttk.Button(top, text="Run All", command=self.run_all).pack(side="left", padx=10)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabs = {}
        for name in ["FCFS", "SJF", "PRIORITY", "RR", "SUMMARY"]:
            frame = ttk.Frame(self.nb)
            self.nb.add(frame, text=name)
            txt = tk.Text(frame, wrap="word", font=("Consolas", 11))
            txt.pack(fill="both", expand=True)
            self.tabs[name] = txt

    def browse_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            self.file_path.set(path)

    def run_all(self):
        path = self.file_path.get().strip()
        if not path:
            messagebox.showerror("Error", "Please select processes.txt")
            return

        try:
            tq = int(self.tq_var.get())
        except ValueError:
            messagebox.showerror("Error", "Time quantum must be an integer")
            return

        try:
            processes = read_processes(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        gantt_fcfs, res_fcfs, util_fcfs = fcfs(processes)
        gantt_sjf, res_sjf, util_sjf = sjf_non_preemptive(processes)
        gantt_pr, res_pr, util_pr = priority_non_preemptive(processes)
        gantt_rr, res_rr, util_rr = round_robin(processes, tq)

        self.set_tab("FCFS", format_report("FCFS", gantt_fcfs, res_fcfs, util_fcfs))
        self.set_tab("SJF", format_report("SJF (Non-preemptive)", gantt_sjf, res_sjf, util_sjf))
        self.set_tab("PRIORITY", format_report("Priority (Non-preemptive)", gantt_pr, res_pr, util_pr))
        self.set_tab("RR", format_report(f"Round Robin (tq={tq})", gantt_rr, res_rr, util_rr))

        summary = self.make_summary([
            ("FCFS", res_fcfs, util_fcfs),
            ("SJF", res_sjf, util_sjf),
            ("PRIORITY", res_pr, util_pr),
            (f"RR (tq={tq})", res_rr, util_rr)
        ])

        self.set_tab("SUMMARY", summary)
        self.nb.select(0)

    def set_tab(self, name, content):
        txt = self.tabs[name]
        txt.delete("1.0", "end")
        txt.insert("1.0", content)

    def make_summary(self, items):
        lines = []
        lines.append("Summary Table")
        lines.append("==============================")
        lines.append("")
        lines.append(f"{'Algorithm':12} | {'Avg TA':>8} | {'Avg WT':>8} | {'CPU %':>7}")
        lines.append("-" * 45)
        for alg, results, util in items:
            avg_ta, avg_wt = calc_averages(results)
            lines.append(f"{alg:12} | {avg_ta:8.2f} | {avg_wt:8.2f} | {util:7.2f}")
        return "\n".join(lines)

if __name__ == "__main__":
    App().mainloop()
