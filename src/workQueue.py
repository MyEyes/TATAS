from queue import Queue, Empty
import threading
import logging
from .workitem_result import WorkItemResult

class WorkQueue:
    def __init__(self, workers):
        self.workers = workers
        self.worker_0 = self.workers[0]
        self.submissionQueue = Queue()
        self.workerThreads = []
        self.running = True
        self.logger = logging.getLogger('TATAS.WorkQueue')
        for w in self.workers:
            wt = threading.Thread(target=self.__workerThread,args=[w])
            self.workerThreads.append(wt)
            wt.start()

    def create_workfile(self, workinfo, path):
        return self.worker_0.create_workfile(workinfo, path)

    def submitWork(self, workfile):
        self.submissionQueue.put(workfile)

    def process_workfile_sync(self, workfile) -> WorkItemResult:
        self.submitWork(workfile)
        workfile.waitForCompletion()
        return workfile.result

    def __workerThread(self, worker):
        while self.running:
            try:
                workfile = self.submissionQueue.get(block=True, timeout=0.1)
                if workfile:
                    worker.process_workfile_sync(workfile)
            except Empty:
                pass

    def terminate(self):
        self.running = False
        self.logger.info("Waiting for threads to terminate")
        for w in self.workerThreads:
            w.join()
        self.logger.info("Terminating worker processes")
        for w in self.workers:
            w.terminate()

