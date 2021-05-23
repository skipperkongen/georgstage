from enum import Enum
from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas as pd
import pulp as P

def print_sol(task_counts, X):
    TIDSPUNKTER = ['08 - 12', '12 - 16', '16 - 20', '20 - 24', '24 - 04', '04 - 08']
    n_gasts, n_tasks = task_counts.shape
    n_shifts = 6

    for k in range(6):
        print(f'Vagt {TIDSPUNKTER[k]}')
        for j in range(len(Activity)):
            for i in range(n_gasts):
                x = X[i][j][k]
                if x.varValue == 1:
                    task_name = Task(j)
                    count = task_counts[i][j]
                    print(f'- Gast {i} er {task_name} ({count} før)')

def team_minmax(team, size=20):
    return team*size, team*size+size



def get_instance(task_counts, vagthavende, pejlegast_b=None, sick=[], hu=[], assigned={}, n_shifts=6, pejl_shift=2, kabys_shifts=[0,1,2], team_order=[0,1,2]):
    """
    TODO: handle vagthavende samme morgen og aften
    TODO: håndter allerede udfyldte vagter
    """
    n_gasts, n_tasks = task_counts.shape
    n_teams = len(team_order)
    assert(len(vagthavende) == n_teams)

    # x_ijk, gast i, task j, shift k
    X = P.LpVariable.dicts('x', (range(n_gasts), range(n_tasks), range(n_shifts)), 0, 1, P.LpBinary)

    V = P.LpVariable.dicts('v', (range(n_gasts), range(n_teams)), 0, 1, P.LpBinary)

    prob = P.LpProblem('Schedule', P.LpMinimize)

    # objective function
    prob += P.lpSum([
        task_counts[i][j] * X[i][j][k]
        for i in range(n_gasts)
        for j in range(n_tasks)
        for k in range(n_shifts)
    ])

    # same vagthavende gast morning and evening constraint
    # - Couldn't solve elegantly yet, so controlled via parameter for now
    # - probably not possible with a linear constraint on X; could introduce special variable
    j_vhe = Task.VAGTHAVENDE_ELEV.value
    for k1, team in enumerate(team_order):
        k2 = k1 + 3
        min_gast, max_gast = team_minmax(team)
        matches = list(filter(lambda i: min_gast <= i < max_gast, vagthavende))
        # check that exactly one gast from each team has vhe duty
        assert(len(matches) == 1)
        i = matches[0]
        prob += X[i][j_vhe][k1] == 1
        prob += X[i][j_vhe][k2] == 1


    # pre-assigned duties constraints
    for k,value in assigned.items():
        for i,task in value.items():
            j = task.value
            prob += X[i][j][k] == 1


    # pejlegast constraints
    j_a = Task.PEJLEGAST_A.value
    j_b = Task.PEJLEGAST_B.value
    for k in range(n_shifts):
        if k == pejl_shift:
            if pejlegast_b is not None:
                # assert that pejlegast_b is from right team
                active_team = team_order[k % 3]
                min_gast, max_gast = team_minmax(active_team)
                assert(min_gast <= pejlegast_b < max_gast)
                prob += X[pejlegast_b][j_b][k] == 1
            else:
                prob += P.lpSum([X[i][j_b][k] for i in range(n_gasts)]) == 1
            prob += P.lpSum([X[i][j_a][k] for i in range(n_gasts)]) == 1
        else:
            prob += P.lpSum([X[i][j_a][k] for i in range(n_gasts)]) == 0
            prob += P.lpSum([X[i][j_b][k] for i in range(n_gasts)]) == 0

    # kabys constraint
    j = Task.DÆKSELEV_I_KABYS.value
    for k in range(n_shifts):
        if k in kabys_shifts:
            prob += P.lpSum([X[i][j][k] for i in range(n_gasts)]) == 1
        else:
            prob += P.lpSum([X[i][j][k] for i in range(n_gasts)]) == 0

    # 0 or 1 task per gast, depending on shift constraint
    for k in range(n_shifts):
        active_team = team_order[k % 3]
        min_gast, max_gast = team_minmax(active_team)
        for i in range(n_gasts):
            i_works = int(min_gast <= i < max_gast)
            prob += P.lpSum([X[i][j][k] for j in range(n_tasks)]) <= i_works

    # exactly 1 gast per task per shift, but ignore vagthavende, pejlegast and kabys
    ignored = [
        Task.VAGTHAVENDE_ELEV.value,
        Task.PEJLEGAST_A.value,
        Task.PEJLEGAST_B.value,
        Task.DÆKSELEV_I_KABYS.value,
    ]
    other_tasks = [j for j in range(n_tasks) if j not in ignored]
    for k in range(n_shifts):
        for j in other_tasks:
            #print(f'[DEBUG] shift {k}, task {j}')
            prob += P.lpSum([
                X[i][j][k]
                for i in range(n_gasts)
            ]) == 1

    # no tasks for left-out gasts (i.e. sick and hu)
    for i in sick + hu:
        prob += P.lpSum([
            X[i][j][k]
            for j in range(n_tasks)
            for k in range(n_shifts)
        ]) == 0

    return prob, X
