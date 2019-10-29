import problem_parser as pp
import domain_parser as dp
import copy


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
        if j == len(a):
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

    def param_in_prec(self, param, po):
        d = dict()

        for i in range(len(param)):
            for x in po:
                if po[x].find(param[i]) != -1:
                    d[param[i]] = po[x]
        return d

    def par_for_prec(self, param, ans):
        d = dict()
        for i in range(len(param)):
            d[param[i]] = ans[i]
        return d


    def effect_for_prec(self, eff, dict):
        for e in eff:
            for i in range(len(e)):
                if dict.get(e[i]) != None:
                    e[i] = dict[e[i]]

    def precendent(self, prec, po):
        all_prec = []
        global answer
        answer = []
        domain = self.dompars.precendents(prec)
        for i in range(len(domain)):
            prec_name = domain[i].name
            param = self.param_in_prec(domain[i].param, po)
            self.gen(domain[i].param, param)
            for j in range(len(answer)):
                dict_for_param = self.par_for_prec(domain[i].param, answer[j])
                domain[i].effect = self.dompars.precendents(prec)[i].effect
                domain[i].precond = self.dompars.precendents(prec)[i].precond
                self.effect_for_prec(domain[i].effect, dict_for_param)
                self.effect_for_prec(domain[i].precond, dict_for_param)
                precen = GrAction(prec_name, answer[j], domain[i].precond, domain[i].effect)
                all_prec.append(precen)
                #print(*prec_name, " ", *answer[j])
                #print(*domain[i].precond)
                #print(*domain[i].effect)
            answer = []
        return all_prec


    def action(self, dom, po):
        all_actions = []
        global answer
        answer = []
        domain = self.dompars.action(dom)
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
                #print(*act_name, " ", *answer[j])
                #print(*domain[i].precond)
                #print(*domain[i].effect)
            answer = []
        return all_actions

    def task(self, dom, po):
        all_tasks = []
        global answer
        answer = []
        d = dp.Parser()
        domain = d.method(dom)
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
                #print(*tsk_name, " ", *answer[j])
                #print(*domain[i].prec)
                #for x in all_subtasks:
                 #   print(x.name, x.param)
            answer = []
        return all_tasks

    def everything(self, dom, prob, prec):
        problem = self.p.problem(prob)
        po = problem.obj
        t = self.task(dom, po)
        a = self.action(dom, po)
        p = self.precendent(prec, po)
        for pr in p:
            a.append(pr)
        return a, t

    def check(self, prob, prec):
        problem = self.p.problem(prob)
        return self.precendent(prec, problem)
