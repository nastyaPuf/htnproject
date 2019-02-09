import problem_parser as pp
import domain_parser as dp
import copy

v = list()

def param_for_ground(par):
    s = dict()
    par = par.replace(',', "")
    par = par.replace(" ", "")
    par = par.replace("'", "")
    left = par.find('?')
    while (1):
        s1 = par.find('-', left)
        right = par.find('?', s1)
        if right == -1:
            right = len(par) - 1
        if s.get(par[s1 + 1: right]) == None:
            s[par[s1 + 1: right]] = [par[left + 1:s1]]
        else:
            s[par[s1 + 1: right]].append(par[left + 1:s1])
        if right == len(par) - 1:
            break
        left = right
    return s

def par_in_task(par):
    s = []
    par = par.replace(',', "")
    par = par.replace(" ", "")
    par = par.replace("'", "")
    left = par.find('?')
    while (1):
        s1 = par.find('-', left)
        right = par.find('?', s1)
        if right == -1:
            right = len(par) - 1
        s.append(par[s1 + 1: right])
        if right == len(par) - 1:
            break
        left = right
    return s

def gen(a, dict, v = list()):
    global answer
    j = len(v)
    if (j == len(a)):
        answer.append(v[:])
    else:
        for val in dict[a[j]].split():
            v.append(val)
            gen(a, dict)
            v.pop()

class GrAction:
    def __init__(self, name, param):
        self.name = name
        self.param = param

class GrTask:
    def __init__(self, name, param):
        self.name = name
        self.param = param

def ground_action(dom, prob):
    all_actions = []
    par = []
    global answer
    answer = []
    problem = pp.parse_problem(prob)
    domain = dp.parse_action(dom)
    po = problem.obj
    for i in range(len(domain)):
        act_name = domain[i].name
        sep_param = dp.par_in_act(str(domain[i].param))
        gen(sep_param, po, v)
        for j in range(len(answer)):
            par.append(answer[j])
            print(*act_name, " ", *answer[j])
        answer = []
        act = GrAction(act_name, copy.deepcopy(par))
        all_actions.append(act)

def ground_task(dom, prob):
    all_tasks = []
    par = []
    global answer
    answer = []
    problem = pp.parse_problem(prob)
    domain = dp.parse_task(dom)
    po = problem.obj
    for i in range(len(domain)):
        tsk_name = domain[i].name
        sep_param = par_in_task(str(domain[i].param))
        gen(sep_param, po, v)
        for j in range(len(answer)):
            par.append(answer[j])
            print(*tsk_name, " ", *answer[j])
        answer = []
        tsk = GrTask(tsk_name, copy.deepcopy(par))
        par = []
        all_tasks.append(tsk)


ground_task()