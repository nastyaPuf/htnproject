import grounding as gr
import domain_parser as dp
import problem_parser as pp
import random

Dom = '/Users/anastasia/Downloads/domain_robot.pddl'

Prob = '/Users/anastasia/Downloads/problem_robot.pddl'

##state --  лист строк, отображающих текущее состояние
##


init_state = pp.parse_problem(Prob).init
tsk = dp.parse_task(Dom)
act = dp.parse_action(Dom)
T = pp.parse_problem(Prob).goal
method = dp.parse_method(Dom)

def prec_to_normal(prec): ##приводит precondition/initial state к массиву из строк, в каждой строке 1 состояние/предпосылка
    brac = 0
    s = ""
    for p in prec:
        s += p
    precond = []
    fir = 0
    sec = 0
    for i in range(len(s)):
        if s[i] == '(':
            fir = i
            brac += 1
        elif s[i] == ')':
            sec = i
            brac -= 1
        if brac == 0:
            precond.append(s[fir + 1:sec])
    return precond


def applic(action, state):
    par = action.prec
    for p in par:
        if str(state).find(p) == -1:  ##пока может работать только pre+
            return 0
    return 1

def state_update(state, action): ##пока может работать только с ef+
    eff = action.effect
    state.append(eff)
    return state

##ac должно быть ground actions, то есть O тоже

def Htn_planner(s_0, T, O, M):
    if len(T) == 0:
        return 0
    t1 = T[0][0]
    tsktype = 0
    for x in O:           ##t1 - primitive compound?
        if(x.name == t1):
            tsktype = 1
    ##print(tsktype)
    if tsktype == 1:        ##t1 primitive
        accomplaction = []
        A = []
        for x in O:
            if x.name == t1:
                accomplaction.append(x)
        applicable = []
        for ac in accomplaction:
            if applic(ac, s_0) == 1:
                A.append(ac)
        ##выберем элемент a недерменированно из A
        a = random.choice(A)
        if len(A) == 0:
            return -1
        s_0 = state_update(s_0, a)
        T.pop([0])
        P = Htn_planner(s_0, T, O, M)
        if (P == -1):
            return -1
        ans = {P, a}
        return ans


    else:                   ##t1 compound
        accomplaction = []
        D = []
        t1 = t1.split()
        for x in M:
            if x.task == t1:
                accomplaction.append(x)
        print(prec_to_normal(accomplaction[0].prec))
        applicable = []
        for ac in accomplaction:
            if applic(ac, s_0) == 1:
                D.append(ac)
        if len(D) == 0:
            return -1
        d = random.choice(D)
        task = T.pop([0])
        for x in D:
            T.append(x.subtask)
        P = Htn_planner(s_0, T, O, M)

#T - то, что определяет цель
s = Htn_planner(init_state, T, act, method)