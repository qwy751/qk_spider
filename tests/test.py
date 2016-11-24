

def accumulate():
    tally = 0
    while 1:
        next = yield
        if next is None:
            return tally
        tally += next


def gather_tallied(tallies):
    while 1:
        tally = yield from accumulate()
        tallies.append(tally)

tallies = []

acc = gather_tallied(tallies)
next(acc)
for i in range(4):
    acc.send(i)

acc.send(None)
for i in range(5):
    acc.send(i)

acc.send(None)

tallies