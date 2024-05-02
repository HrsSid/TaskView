import sys
import psutil


class TaskView:
    def __init__(self) -> None:
        self.processes = []  # list of all processes

    def getAllProcesses(self) -> list:
        """Create and return a list of all processes currently running.

        Process filtering rules:
            1: process can not exist twice in the returning list.
            2: process has to be an executable, end with the `.exe` extension.

        Returns:
            list: `{"name": name, "pid": pid}`, this is an item example.
        """
        # Appending the processes to the self.processes list (list syntax -> [{"name": name, "pid": pid}])
        for process in psutil.process_iter(["pid", "name"]):
            processName = process.info["name"]  # saving the name of the process
            if (
                processName in self.processes
            ):  # making sure that the process is not already in the list
                continue
            if (
                ".exe" not in processName
            ):  # making sure the process is an executable (so it does not overlap with any system processes)
                continue
            self.processes.append(process.info)  # appending the process to the list
        return self.processes  # returning the filtered processes

    def findProcess(self, processName: str) -> dict:
        """Find a process by its name, the search algorithm is case-insensitive.

        Args:
            processName (str): The name of the process to find.

        Returns:
            dict: `{"name": name, "pid": pid}`.
        """
        self.processes = (
            self.getAllProcesses()
        )  # making sure that the list is up-to-date and also is not empty
        for process in self.processes:
            if (
                processName in process["name"]
            ):  # checking if the process name matches the name of the process given
                return process  # if the name matches, return the process in this syntax -> {"name": name, "pid": pid}
        return None  # otherwise return none

    def listAllProcesses(self) -> list:
        """Create a more user friendly list of all processes currently running. (Does not include pid and items are strings instead of dictionaries).

        Returns:
            list: Return a list containing all of the process names currently running.
        """
        self.processes = (
            self.getAllProcesses()
        )  # making sure that the list is up-to-date and also is not empty
        returnList = (
            []
        )  # defining a temporary list to store the names of the processes before returning it
        for process in self.processes:
            if (
                process.get("name") not in returnList
            ):  # checking to see if the process name is already in the list
                returnList.append(
                    process.get("name")
                )  # if the name is not in the list, append it to the list. This is to prevent double entries
        return returnList  # returning the list

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
# !!! The comments are describing the code as I understand it it may not be completely correct !!!
