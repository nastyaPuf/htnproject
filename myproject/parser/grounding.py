import problem_parser as pp
import domain_parser as dp


class GrAction:
    def __init__(self, name, param, precond, effect):
        self.name = name
        self.param = param
        self.precond = precond
        self.effect = effect

class GrTask:
    def __init__(self, name, param, precond, subtask):
        self.name = name
        self.param = param
        self.precond = precond
        self.subtask = subtask




class Grounder:
    dompars = dp.Parser()
    v = list()
    p = pp.Parser()
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

    def prec(self, param, par_from_action):
        count = 0
        s = dict()
        for x in param:
            if x.find('?') != -1:
                count += 1;
                s[x] = par_from_action[count - 1]
        return s

    def precondition(self, diction, prec):
        for x in prec:
            for i in range(len(x)):
                for d in diction:
                    if x[i] == d:
                        x[i] = diction[d]

    def effect(self, diction, eff):
        for x in eff:
            for i in range(len(x)):
                for d in diction:
                    if x[i] == d:
                        x[i] = diction[d]

    def subtask(self, diction, sub):
        all_subtasks = []
        for x in sub:
            x = self.dompars.subt_sep(x)
            par = x.param
            for i in range(len(par)):
                for d in diction:
                    if par[i] == d:
                        par[i] = diction[d]
            x.param = par
            all_subtasks.append(x)
        return all_subtasks


    def action(self, dom, problem):
        all_actions = []
        global answer
        answer = []
        domain = self.dompars.action(dom)
        po = problem.obj
        for i in range(len(domain)):
            act_name = domain[i].name
            sep_param = self.dompars.par_in_act(str(domain[i].param))
            self.gen(sep_param, po)
            for j in range(len(answer)):
                domain[i].effect = self.dompars.action(dom)[i].effect
                domain[i].precond = self.dompars.action(dom)[i].precond
                x = self.prec(domain[i].param, answer[j])
                self.precondition(x, domain[i].precond)
                self.effect(x, domain[i].effect)
                act = GrAction(act_name, answer[j], domain[i].precond, domain[i].effect)
                all_actions.append(act)
                print(*act_name, " ", *answer[j])
                print(*domain[i].precond)
                print(*domain[i].effect)
            answer = []
        return all_actions

    def task(self, dom, problem):
        all_tasks = []
        global answer
        answer = []
        d = dp.Parser()
        domain = d.method(dom)
        po = problem.obj
        for i in range(len(domain)):
            tsk_name = domain[i].task
            sep_param = self.par_in_task(str(domain[i].params))
            self.gen(sep_param, po)
            for j in range(len(answer)):
                domain[i].prec = d.method(dom)[i].prec
                x = self.prec(domain[i].params, answer[j])
                self.precondition(x, domain[i].prec)
                all_subtasks = self.subtask(x, domain[i].subtask)
                act = GrTask(tsk_name, answer[j], domain[i].prec, all_subtasks)
                all_tasks.append(act)
                print(*tsk_name, " ", *answer[j])
                print(*domain[i].prec)
                for x in all_subtasks:
                    print(x.name, x.param)
            answer = []
        return all_tasks

    def everything(self, dom, prob):
        problem = self.p.problem(prob)
        t = self.task(dom, problem)
        a = self.action(dom, problem)
        return a, t
