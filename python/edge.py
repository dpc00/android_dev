import time
import pickle

dep = set()


class Edge():
    def __init__(self, di, si):
        self.di = di
        self.si = si
        self.cdt = time.time()
        self.udt = self.cdt - 10
        self.rcdt = time.time()
        self.rudt = self.rcdt


    def __hash__(self):
        from bhash import bhash
        return bhash((self.di, self.si))

    def __eq__(self, other):
        return (self.di, self.si) == (other.di, other.si)

    def bctck(self):
        return self.cdt > self.udt

    def rbctck(self):
        return self.rcdt > self.rudt

    def clr(self):
        if self.udt != self.cdt:
            print('-clr', self.di, self.si)
            self.udt = self.cdt
            saveedges()

    def rclr(self):
        if self.rudt != self.rcdt:
            print('-rclr', self.di, self.si)
            self.rudt = self.rcdt
            saveedges()

    def rtset(self, mt=None):
        if mt is None:
            self.cdt = time.time()
        else:
            self.cdt = mt
        saveedges()

    def rrtset(self, mt=None):
        if mt is None:
            self.rcdt = time.time()
        else:
            self.rcdt = mt
        saveedges()

    def __repr__(self):
        return repr(
            (self.di, self.si, self.cdt, self.udt, self.rcdt, self.rudt))


# change detected time

edges = {}


def findEdge(di, si):
    if len(edges) != len(dep):
        for e in dep:
            edges[e.di, e.si] = e
    return edges[di, si]


def loadedges():
    from config import paths, pre
    edgepf = pre('FLAGS') / 'edges.pp'
    global dep
    try:
        dep = set()
        with open(edgepf, "rb") as fh:
            dep = pickle.load(fh)
    except:
        dep = set()


def saveedges():
    from config import pre
    edgepf = pre('FLAGS') / 'edges.pp'
    global dep
    with open(edgepf, "wb") as fh:
        pickle.dump(dep, fh)


def lrtset(di, si):
    e = findEdge(di, si)
    e.rtset()


loadedges()

if __name__ == '__main__':
    lrtset('git', 'pyth')
