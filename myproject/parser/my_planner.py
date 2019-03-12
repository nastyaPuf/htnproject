import grounding as gr
import domain_parser as dp
import problem_parser as pp
import copy


class Planner:
    def precond_to_pos_neg(self, prec):
        pos = []
        neg = []
        prec1 = copy.deepcopy(prec)
        for x in prec1:
            if x[0] == 'not':
                del(x[0])
                neg.append(x)
            else:
                pos.append(x)
        return pos, neg


    def effect_to_pos_neg(self, eff):
        pos = []
        neg = []
        eff1 = copy.deepcopy(eff)
        for x in eff1:
            if x[0] == 'not':
                del x[0]
                neg.append(x)
            else:
                pos.append(x)
        return pos, neg

    def state_to_pos_neg(self, state):
        state1 = copy.deepcopy(state)
        pos = []
        neg = []
        for x in state1:
            if x[0] == 'not':
                x.remove(x[0])
                neg.append(x)
            else:
                pos.append(x)
        return pos, neg


    def applic(self, pos_prec, neg_prec, pos_state, neg_state):
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


    def state_update(self, pos_state, neg_state, pos_eff, neg_eff):
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


    ans = list()


    def Htn_planner(self, pos_state, neg_state, T, O, M):
        global ans
        if len(T) == 0:
            return
        name = T[0].name
        param = T[0].param
        #print(name, param)
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
                pos_pr, neg_pr = self.precond_to_pos_neg(ac.precond)
                #print(pos_pr)
                #print(neg_pr)
                #print(pos_state)
                #print(neg_state)
                if self.applic(pos_pr, neg_pr, pos_state, neg_state) == 1:
                    applicable.append(ac)
            if len(applicable) == 0:
                return -1
            for a in applicable:
                pos_ef, neg_ef = self.effect_to_pos_neg(a.effect)
                self.state_update(pos_state, neg_state, pos_ef, neg_ef)
                del T[0]
                p = self.Htn_planner(pos_state, neg_state, T, O, M)
                if p == -1:
                    return -1
                self.ans.append(a)
                return self.ans


        else:                                     ##t1 compound
            accomplaction = []
            coun = 0
            name = name.split()
            for x in M:
                if x.name == name and x.param == param:
                    accomplaction.append(x)
            if len(accomplaction) == 0:
                return -1
            del T[0]
            for i in range(len(accomplaction)):
                new_tasks = []
                new_tasks.append(accomplaction[i].subtask)
                T1 = []
                for x in new_tasks:
                    for sub in x:
                        T1.append(sub)
                        coun += 1
                for x in T:
                    T1.append(x)
                T = T1
                htn = self.Htn_planner(pos_state, neg_state, T, O, M)
                if htn == -1 and i == len(accomplaction) - 1:
                    return -1
                elif htn != -1:
                    return htn
                else:
                    size = copy.deepcopy(len(T))
                    T.reverse()
                    for j in range(size):
                        T.pop(len(T) - 1)
                        coun -= 1
                        if coun == 0:
                            break
                    T.reverse()

    def Write_precendents(self, Goal, pos_last_state, neg_last_state, pos_new_state, neg_new_state, s):
        with open("precendents.pddl", "a+") as file:
            file.write("name:\n")
            for g in Goal:
                file.write(g.name + " " + ' '.join(g.param) + "\n")
            file.write("\r" + "initial state:\n")
            for p in pos_last_state:
                file.write(' '.join(p) + "\n")
            for n in neg_last_state:
                if n != None:
                    file.write("not " + ' '.join(n) + "\n")
            file.write("\r")
            file.write("effects:\n")
            for p in pos_new_state:
                file.write(' '.join(p) + "\n")
            for n in neg_new_state:
                if n != None:
                    file.write("not " + ' '.join(n) + "\n")
            file.write("\ntasks:\n")
            for act in s:
                file.write(' '.join(act.name) + " " + ' '.join(act.param) + "\n")
            file.write("\r\r\r\r")

    def HTN(self, Dom, Prob):
        par_prob = pp.Parser()
        init_state = par_prob.problem(Prob).init
        goal = par_prob.problem(Prob).goal
        g = gr.Grounder()
        gr_action, gr_task = g.everything(Dom, Prob)
        pos_state, neg_state = self.state_to_pos_neg(init_state)
        pos_last_state = copy.deepcopy(pos_state)
        neg_last_state = copy.deepcopy(neg_state)
        Goal = copy.deepcopy(goal)
        s = self.Htn_planner(pos_state, neg_state, goal, gr_action, gr_task)
        if s != -1:
            s.reverse()
            self.Write_precendents(Goal, pos_last_state, neg_last_state, pos_state, neg_state, s)
        if s != -1:
            for actions in s:
                print(*actions.name, *actions.param)
        else:
            print("No solutions")
