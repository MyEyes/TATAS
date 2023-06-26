from .workitem import WorkItem

class WorkItemResult:
    def __init__(self, workitem):
        self.workitem = workitem
        self.data = {}