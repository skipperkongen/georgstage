import pandas as pd
from georgstage.plan import Task

def get_taskstats(assignments):
    """
    return a matrix (sailor X task) with counts
    """
    df = pd.DataFrame(assignments)
    s0 = df.groupby(['gast_no', 'task']).size()
    stats = df.groupby(['gast_no', 'task']).size()
    for gast_no in gast_nos:
        for task in Task:
            stats[gast_no, task.name] = 0

    for idx, val in s0.iteritems():
        stats[idx] = s0[idx]
    return stats
