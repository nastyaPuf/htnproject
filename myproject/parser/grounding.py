import problem_parser as pp
import domain_parser as dp

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


def ground(dom, prob):
    all_actions = []
    global answer
    answer = []
    problem = pp.parse_problem(prob)
    domain = dp.parse_action(dom)
    po = problem.obj
    for i in range(len(domain)):
        act_name = domain[i].name
        sep_param = dp.par_in_act(str(domain[i].param))
        print (act_name, ":")
        gen(sep_param, po, v)
        for j in range(len(answer)):
            act = GrAction(act_name, answer[j])
            all_actions.append(act)
            print(*act_name, " ", *answer[j])





ground("/Users/anastasia/Downloads/domains-totally-ordered/rover/domains/test_domain2.hddl", '/Users/anastasia/Downloads/HTN-Translation-master/examples/robot/problems/pfile_10_10.pddl')






