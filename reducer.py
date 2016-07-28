#!/usr/bin/env python3
import _thread
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from enums import ReduceStatus, Status
from fake_fs import FakeFS

class ReduceTask:
    def __init__(self, task_id, region, mappers, script_path):
        self.task_id = task_id
        self.region = region
        self.mappers = mappers
        self.script_path = script_path


class Reducer:
    def __init__(self, fs, name, addr, opts):
        self.fs = fs
        self.name = name
        self.addr = addr
        self.job_tracker = ServerProxy(opts["JobTracker"]["address"])
        self.tasks = {}

    # signal from JT for starting reducing
    # task_id - unique task_id
    # region for which reducer is responsible
    # mappers which contain data for current task
    # path in DFS to files
    def reduce(self, task_id, region, mappers, script_path):
        if task_id not in self.tasks:
            self.tasks = {}

        task = ReduceTask(task_id, region, mappers, script_path)
        self.tasks[task_id][region] = task
        _thread.start_new_thread(self._process_reduce_task, (task, ))
        return {'status': ReduceStatus.accepted}

    def _process_reduce_task(self, task):
        pass

    def get_status(self, task_id):
        pass

    # saves reduced result to dfs
    def save_result_to_dfs(self, task_id, result):
        pass

if __name__ == '__main__':
    name = sys.argv[1]
    port = int(sys.argv[2])
    cfg_path = sys.argv[3]
    script_path = sys.argv[4]
    rds_count = 5

    chunk = "/my_folder/chunk"
    fs = FakeFS()  # use fake fs for local development
    fs.save("aa mm adas aa bb huy what the the i don bmm", chunk)

    with open(script_path, "r") as file:
        data = file.read()
        fs.save(data, "/scripts/word_count.py")

    opts = cfg.load(cfg_path)
    print("JT address", opts["JobTracker"]["address"])

    mapper = Mapper(opts, fs, name, "http://localhost:" + str(port))
    task_id = uuid.uuid4()
    r = mapper.map(task_id, rds_count, chunk, "/scripts/word_count.py")

    while mapper.get_status(task_id, chunk)['status'] != MapStatus.finished:
        pass

    i = 1
    while i <= 4:
        print(i, "region:", mapper.read_mapped_data(task_id, i))
        i += 1