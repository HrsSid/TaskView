import psutil
import os


class TaskManager:
    def __init__(self) -> None:
        self.processes = []
    
    def getAllProcesses(self) -> list:
        """Create and return a list of all processes currently running.

        Process filtering rules:
            1: process can not exist twice in the returning list.
            2: process has to be an executable, end with the `.exe` extension.

        Returns:
            list: `{"name": name, "pid": pid}`, this is an item example.
        """
        for process in psutil.process_iter(["pid", "name"]): # getting every process in currently running
            processName = process.info["name"] # getting the process name in a separate variable
            if processName in self.processes: # making sure that the process is not already in the list already
                continue
            if ".exe" not in processName: # making sure the process is an executable (so system processes are not contained)
                continue
            self.processes.append(process.info) # appending the process to the list
        return self.processes # item example: {"name": name, "pid": pid}
    
    def findProcess(self, processName: str) -> dict:
        """Find a process by its name, the search algorithm is case-insensitive.

        Args:
            processName (str): The name of the process to find.

        Returns:
            dict: `{"name": name, "pid": pid}`.
        """
        self.processes = self.getAllProcesses() # making sure that the list is up-to-date and not empty
        for process in self.processes: # getting all the processes one at a time
            if processName in process["name"]: # checking to see if the process name given matches any currently running process
                return process # if the name matches, return the process in this syntax -> {"name": name, "pid": pid}
        return None # otherwise return None
    
    def terminateProcess(self, processName):
        for process in psutil.process_iter():
            if process.name().lower() == processName.lower():
                process.kill()
    
    def startProcess(self, processName):
        os.system("start " + processName)
