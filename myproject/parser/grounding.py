import problem_parser as pp
import domain_parser as dp
import copy


class GrAction:
    def __init__(self, name, param):
        self.name = name
        self.param = param

class GrTask:
    def __init__(self, name, param):
        self.name = name
        self.param = param


class Grounder:
    v = list()
    def param_for_ground(self, par):
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

    def par_in_task(self, par):
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

    def gen(self, a, dict):
        global answer
        j = len(self.v)
        if (j == len(a)):
            answer.append(self.v[:])
        else:
            for val in dict[a[j]].split():
                self.v.append(val)
                self.gen(a, dict)
                self.v.pop()

    def action(self, dom, problem):
        all_actions = []
        par = []
        global answer
        answer = []
        d = dp.Parser()
        domain = d.action(dom)
        po = problem.obj
        for i in range(len(domain)):
            act_name = domain[i].name
            sep_param = d.par_in_act(str(domain[i].param))
            self.gen(sep_param, po)
            for j in range(len(answer)):
                par.append(answer[j])
                print(*act_name, " ", *answer[j])
            answer = []
            act = GrAction(act_name, copy.deepcopy(par))
            all_actions.append(act)
        return all_actions

    def task(self, dom, problem):
        all_tasks = []
        par = []
        global answer
        answer = []
        d = dp.Parser()
        domain = d.task(dom)
        po = problem.obj
        for i in range(len(domain)):
            tsk_name = domain[i].name
            sep_param = self.par_in_task(str(domain[i].param))
            self.gen(sep_param, po)
            for j in range(len(answer)):
                par.append(answer[j])
                print(*tsk_name, " ", *answer[j])
            answer = []
            tsk = GrTask(tsk_name, copy.deepcopy(par))
            par = []
            all_tasks.append(tsk)
        return all_tasks

    def everything(self, dom, prob):
        p = pp.Parser()
        problem = p.problem(prob)
        t = self.task(dom, problem)
        a = self.action(dom, problem)

#gr = Grounder()
#gr.everything('/Users/anastasia/Downloads/htnproject-master/myproject/parser/domain_robot.pddl', '/Users/anastasia/Downloads/htnproject-master/myproject/parser/problem_robot.pddl')

