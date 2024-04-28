import psutil

class TaskView():
    def __init__(self) -> None:
        self.processes = []
    
    def getAllProcesses(self) -> list:
        for process in psutil.process_iter(["pid", "name"]):
            processName = process.info["name"]
            if processName in self.processes:
                continue
            if ".exe" not in processName:
                continue
            self.processes.append(process.info)
        return self.processes
    
    def findProcess(self, processName) -> dict:
        self.processes = self.getAllProcesses()
        
        for process in self.processes:
            if processName in process["name"]:
                return process
        return None

print(TaskView().findProcess("brave.exe"))

# There are no comments because it's still a work in progress
