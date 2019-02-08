## important classes

class Type:
    def __init__(self, name, val):
        self.name = name
        self.val = val

class Task:
    def __init__(self, name, param, precond, effect):
        self.name = name
        self.param = param
        self.precond = precond
        self.effect = effect

class Action:
    def __init__(self, name, param, precond, effect):
        self.name = name
        self.param = param
        self.precond = precond
        self.effect = effect

class Method:
    def __init__(self, name, precond, params, subtask, task, order):
        self.name = name
        self.task = task
        self.params = params
        self.precond = precond
        self.subtask = subtask
        self.order = order


class Predicate:
    def __init__(self, name, par):
        self.name = name
        self.par = par


class Domain:
    def __init__(selfself, name, requir, type, pred, action, task, method):
        Domain.name = name
        Domain.requir = requir
        Domain.type = type
        Domain.pred = pred
        Domain.action = action
        Domain.task = task
        Domain.method = method

class ParseError(Exception):
    pass


##function to read domain file
def read_domain(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    for i in range (len(text)):
        text[i] = text[i].strip('(')
        text[i] = text[i].strip(')')
    return text

def par_in_act(par):
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

##parsing fuctions
def parse_action(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    act = 0
    ef = 0
    brac = 0
    prec = 0
    ef_act = []
    prec_act = []
    actions = []
    act_name = ""
    par_act = ""
    for i in range(len(text)):
        if text[i].find('(') != -1:
            brac += 1
        if text[i].find(')') != -1:
            brac -= 1
        if act == 1 and brac == 0:
            Act = Action(act_name, par_act, prec_act, ef_act)
            actions.append(Act)
            act_name = ""
            par_act = ""
            ef_act = []
            prec_act = []
            act = 0
            ef = 0
            prec = 0
        if text[i].find(':action') != -1:
            text[i] = text[i].split()
            act_name = text[i][1:]
            act = 1
            brac = 1
            continue
        if text[i].find(':param') != -1 and act == 1:
            text[i] = text[i].replace("(", "")
            text[i] = text[i].replace(")", "")
            text[i] = text[i].split()
            par_act = text[i][1:]
            continue
        if ef == 1 and text[i].find('and') == -1 and act == 1:
            text[i] = text[i].replace("(", "")
            text[i] = text[i].replace(")", "")
            ef_act.append(text[i])
        if text[i].find(':effect') != -1 and act == 1:
            prec = 0
            ef = 1
        if prec == 1 and text[i].find('and') == -1 and act == 1:
            text[i] = text[i].strip('(').strip(')')
            prec_act.append(text[i])
        if text[i].find(':precond') != -1 and act == 1:
            prec = 1
    return actions


def parse_predic(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    predic = list()
    pred = 0
    brac = 100
    pr_name = ""
    for i in range(len(text)):
        if text[i].find(':predicates') != -1:
            brac = 2
            pred = 1
        if text[i].find("(") != -1:
            brac +=1
            if pred == 1 and brac == 3:
                pr_name = text[i][2:]
                brac = 1
        if text[i].find(")") != -1:
            brac -=1
            if pred == 1 and brac == 1:
                predic.append(text[i][1:-1])
        if (brac == 0):
            break
    return Predicate(pr_name, predic)

def parse_task(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    tsk = 0
    ef = 0
    brac = 0
    prec = 0
    ef_tsk = []
    prec_tsk = []
    tasks = []
    task_name = ""
    par_tsk = ""
    for i in range(len(text)):
        if text[i].find('(') != -1:
            brac += 1
        if text[i].find(')') != -1:
            brac -= 1
        if tsk == 1 and brac == 0:
            task = Task(task_name, par_tsk, prec_tsk, ef_tsk)
            tasks.append(task)
            task_name = ""
            par_tsk = ""
            ef_tsk = []
            prec_tsk = []
            tsk = 0
            ef = 0
            prec = 0
        if text[i].find(':task') != -1:
            text[i] = text[i].split()
            task_name = text[i][1:]
            tsk = 1
            brac = 1
            continue
        if text[i].find(':param') != -1 and tsk == 1:
            text[i] = text[i].replace("(", "")
            text[i] = text[i].replace(")", "")
            text[i] = text[i].split()
            par_tsk = text[i][1:]
            continue
        if ef == 1 and text[i].find('and') == -1 and tsk == 1:
            text[i] = text[i].replace("(", "")
            text[i] = text[i].replace(")", "")
            ef_tsk.append(text[i])
        if text[i].find(':effect') != -1 and tsk == 1:
            prec = 0
            ef = 1
        if prec == 1 and text[i].find('and') == -1 and tsk == 1:
            text[i] = text[i].strip('(').strip(')')
            prec_tsk.append(text[i])
        if text[i].find(':precond') != -1 and tsk == 1:
            prec = 1
    return tasks


def parse_types(Dom):
    type = dict()
    with open(Dom) as file:
        text = [row.strip() for row in file]
    for i in range(len(text)):
        if text[i].find(":types") != -1:
            for j in range(i + 1, len(text)):
                if text[j].find(')') == -1:
                    s = text[j].find('-')
                    if (s == -1):
                        type[text[j]] = ""
                    else:
                        type[text[j][:s]] = text[j][s + 1:]
                else:
                    break
    return type


def parse_requirement(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    for i in range(len(text)):
        if (text[i].find(":requirements") != -1):
            text[i] = text[i].strip('(').strip(')')
            text[i] = text[i].split()
            return text[i][1:]


def parse_method(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    meth_name = ""
    meth_prec = []
    meth_task = []
    meth_subtask = Task
    meth_param = []
    meth_order = []
    methods = []
    mth = 0
    br = 0
    prec = 0
    for i in range(len(text)):
        if text[i].find(":method") != -1:
            text[i] = text[i].strip(')').strip('(')
            text[i] = text[i].split()
            meth_name = text[i][1:]
            mth = 1
            br = 1
            continue
        if (text[i].find(')') != -1 and mth == 0 and br == 1):
            m = Method(meth_name, meth_prec, meth_param, meth_subtask, meth_task, meth_order)
            methods.append(m)
            meth_name = ""
            meth_prec = []
            meth_task = Task
            meth_subtask = Task
            meth_param = ""
            meth_order = []
            methods = []
            mth = 0
            br = 0
        if (text[i].find(':task') != -1 and mth == 1):
            text[i].strip(')').strip('(')
            text[i].split()
            meth_task = text[i][1:]
        if (text[i].find(':param') != -1 and mth == 1):
            text[i].strip(')').strip('(')
            text[i].split()
            meth_param = text[i][1:]
        if (text[i].find(':precondition') != -1 and mth == 1):
            prec = 1
        if prec == 1 and text[i].find('and') == -1 and mth == 1:
            text[i] = text[i].strip('(').strip(')')
            meth_prec.append(text[i])
        if (text[i].find(':subtask') != -1 and mth == 1):
            prec = 0
        ##на стадии разработки





#parse domain file and answer
def domain_parser(Dom):
    x = 5
    y = 5
    with open(Dom) as file:
        text = [row.strip() for row in file]
    text[0] = text[0].strip(')').strip('(')
    text[0] = text[0].split()
    D = Domain(text[0][2:], parse_requirement(Dom), parse_types(Dom), parse_predic(Dom), parse_action(Dom), parse_task(Dom), y)
    print("domain name - ", D.name)
    print("___________________________________")
    print("requirements - ", parse_requirement(Dom))
    print("___________________________________")
    print("types:")
    for key in sorted(D.type.keys()):
        print(key + ":" + D.type[key])
    print("___________________________________")
    print("predicates:")
    for i in D.pred.par:
        print(i)
    print("___________________________________")
    print("actions: ")
    for act in D.action:
        print("name - ", act.name)
        print("parametres - ", act.param)
        print("preconditions - ", act.precond)
        print("effects - ", act.effect)
        print ("*******")
    print()
    print("tasks: ")
    for tsk in D.task:
        print("name - ", tsk.name)
        print("parametres - ", tsk.param)
        print("preconditions - ", tsk.precond)
        print("effects - ", tsk.effect)
        print("++++++")
    print()
    print()
    print("methods: ")





