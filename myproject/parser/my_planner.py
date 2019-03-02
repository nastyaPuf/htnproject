import grounding as gr
import domain_parser as dp
import problem_parser as pp
import random


Dom = '../domain_robot.pddl'

Prob = '../problem_robot.pddl'


par_prob = pp.Parser()
init_state = par_prob.problem(Prob).init
T = par_prob.problem(Prob).goal
par_domain = dp.Parser()
tsk = par_domain.task(Dom)
method = par_domain.method(Dom)
g = gr.Grounder()
gr_action, gr_task = g.everything(Dom, Prob)

def precond_to_pos_neg(prec):
    pos = []
    neg = []
    for x in prec:
        if x[0] == 'not':
            del x[0]
            neg.append(x)
        else:
            pos.append(x)
    return pos, neg


def effect_to_pos_neg(eff):
    pos = []
    neg = []
    for x in eff:
        if x[0] == 'not':
            del x[0]
            neg.append(x)
        else:
            pos.append(x)
    return pos, neg

def state_to_pos_neg(state):
    pos = []
    neg = []
    for x in state:
        if x[0] == 'not':
            t = x.remove(x[0])
            neg.append(t)
        else:
            pos.append(x)
    return pos, neg


def applic(pos_prec, neg_prec, pos_state, neg_state):
    ap_pos = dict()
    ap_neg = dict()
    pos_pr = []
    neg_pr = []
    for pp in pos_prec:
        pp1 = ' '.join(pp)
        pos_pr.append(pp1)

    for np in neg_prec:
        np1 = ' '.join(np)
        neg_pr.append(np1)

    for pp in pos_pr:
        ap_pos[pp] = 0

    for np in neg_pr:
        ap_neg[np] = 0

    for pp in pos_prec:
        for ps in pos_state:
            if pp == ps:
                pp1 = ' '.join(pp)
                ap_pos[pp1] = 1

    for np in neg_prec:
        for ns in neg_state:
            if np == ns:
                np1 = ' '.join(np)
                ap_neg[np1] = 1

    for pp in pos_pr:
        if ap_pos[pp] == 0:
            return 0

    for np in neg_pr:
        if ap_neg[np] == 0:
            return 0
    return 1


def state_update(pos_state, neg_state, pos_eff, neg_eff):
    count = 0
    for pe in pos_eff:
        for ps in pos_state:
            if pe == ps:
                count = 1
        if count == 0:
            pos_state.append(pe)

    count = 0
    for ne in neg_eff:
        for ps in neg_state:
            if ne == ps:
                count = 1
        if count == 0:
            neg_state.append(ne)

    for pe in pos_eff:
        for ns in neg_state:
            if pe == ns:
                neg_state.remove(ns)

    for ne in neg_eff:
        for ps in pos_state:
            if ne == ps:
                pos_state.remove(ne)

coun = 0
ans = list()
def Htn_planner(pos_state, neg_state, T, O, M, coun):
    global ans
    if len(T) == 0:
        return []
    name = T[0].name
    param = T[0].param
    print(name, param)
    tsktype = 0
    for x in O:           ##t1 - primitive compound?
        if x.name[0] == name:
            tsktype = 1
    if tsktype == 1:      ##t1 primitive
        accomplaction = []
        for x in O:
            if x.name[0] == name and x.param == param:
                accomplaction.append(x)
        applicable = []
        for ac in accomplaction:
            pos_pr, neg_pr = precond_to_pos_neg(ac.precond)
            #print(pos_pr)
            #print(neg_pr)
            #print(pos_state)
            #print(neg_state)
            if applic(pos_pr, neg_pr, pos_state, neg_state) == 1:
                applicable.append(ac)
        if len(applicable) == 0:
            return -1
        ##выберем элемент a недерменированно из A
        a = random.choice(applicable)
        pos_ef, neg_ef = effect_to_pos_neg(a.effect)
        state_update(pos_state, neg_state, pos_ef, neg_ef)
        del T[0]
        p = Htn_planner(pos_state, neg_state, T, O, M, coun)
        if p == -1:
            return -1
        ans.append(a)
        return ans


    else:                                     ##t1 compound
        accomplaction = []
        name = name.split()
        for x in M:
            if x.name == name and x.param == param:
                accomplaction.append(x)
        if len(accomplaction) == 0:
            print(1)
            return -1
        new_tasks = []
        for ac in accomplaction:
            new_tasks.append(ac.subtask)
        del T[0]
        T1 = []
        for x in new_tasks:
            for sub in x:
                T1.append(sub)
                if (htn.get(coun) == None):
                    htn[coun] = sub.name + ' ' + ' '.join(sub.param)
                else:
                    htn[coun] += ' ' + sub.name + ' ' + ' '.join(sub.param)
        for x in T:
            T1.append(x)
        T = T1
        return Htn_planner(pos_state, neg_state, T, O, M, coun + 1)

pos_state, neg_state = state_to_pos_neg(init_state)
htn = dict()
s = Htn_planner(pos_state, neg_state, T, gr_action, gr_task, 0)
print("-----------------")
if s != -1:
    s.reverse()
    for actions in s:
        print(*actions.name, *actions.param)
else:
    print("No solutions")
#print(htn)
