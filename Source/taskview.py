import sys
import psutil


class TaskView:
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

    def listAllProcesses(self):
        self.processes = self.getAllProcesses()
        returnList = []
        for process in self.processes:
            if process.get("name") not in returnList:
                returnList.append(process.get("name"))
        return returnList

    def terminateProcess(self, processName):
        for process in psutil.process_iter():
            if process.name().lower() == processName.lower():
                process.kill()


if __name__ == "__main__":
    taskView = TaskView()
    processesForProgram = taskView.getAllProcesses()
    processesForUser = taskView.listAllProcesses()
    arguments = sys.argv
    arguments.pop(0)
    if len(arguments) == 0:
        raise SyntaxError("Usage: taskview.py {process name}")
    if arguments[0] == "terminate":
        for process in arguments[1:]:
            taskView.terminateProcess(process)
    elif arguments[0] == "list":
        for process in processesForUser:
            print(process)


# In the official V1.0 commit the code will be cleaner, now I am just messing around and trying to understand how to work with processes
# There are no comments because it's still a work in progress
