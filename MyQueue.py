import threading
from collections import deque

class QueueObj:
    def __init__(self, idx):
        self.q = deque()
        self.lock = threading.Lock()
        self.ident = idx


class MyQueue:
    def __init__(self, consumer_cnt):
        self.consumer_cnt = consumer_cnt
        self.qs = dict()
        for i in xrange(0, consumer_cnt):
            self.qs[i] = QueueObj(i)

    def add(self, val):
        for k in self.qs:
            q = self.qs.get(k)
            q.lock.acquire()
            try:
                q.q.append(val)
            finally:
                q.lock.release()

    def get(self, idx):
        q = self.qs.get(idx % self.consumer_cnt)
        q.lock.acquire()
        try:
            return q.q.popleft()
        finally:
            q.lock.release()
