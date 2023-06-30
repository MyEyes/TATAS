import subprocess
import os
from .workitem_result import WorkItemResult
class Worker:
    def __init__(self):
        pass

    def create_workfile(self, workitem, path):
        pass

    def submit_workfile(self, workfile):
        pass

    def process_workfile_sync(self, workfile) -> WorkItemResult:
        pass

    def read_response(self):
        pass

    def terminate(self):
        pass