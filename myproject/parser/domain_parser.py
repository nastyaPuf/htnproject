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

class Subtask:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks

class Action:
    def __init__(self, name, param, precond, effect):
        self.name = name
        self.param = param
        self.precond = precond
        self.effect = effect

class Method:
    def __init__(self, name, params, prec, subtask, task, order):
        self.name = name
        self.task = task
        self.params = params
        self.subtask = subtask
        self.order = order
        self.prec = prec


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


def parse_types(Dom):
    s = ""
    with open(Dom) as file:
        text = [row.strip() for row in file]
    for i in range(len(text)):
        if text[i].find(":types") != -1:
            text[i] = text[i].strip(')').strip('(')
            text[i] = text[i].split()
            s = text[i][1:]
    return s

def parse_requirement(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    for i in range(len(text)):
        if (text[i].find(":requirements") != -1):
            text[i] = text[i].strip('(').strip(')')
            text[i] = text[i].split()
            return text[i][1:]


def parse_task(Dom):
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
        if (text[i].find('method') != -1):
            return actions
        if text[i].find('(') != -1:
            brac += 1
        if text[i].find(')') != -1:
            brac -= 1
        if act == 1 and brac == 0:
            task = Task(act_name, par_act, prec_act, ef_act)
            actions.append(task)
            act_name = ""
            par_act = ""
            ef_act = []
            prec_act = []
            act = 0
            ef = 0
            prec = 0
        if text[i].find(':task') != -1:
            text[i] = text[i].replace("(", "")
            text[i] = text[i].replace(")", "")
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

def parse_method(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    meth_name = ""
    meth_task = []
    meth_subtask = []
    meth_param = []
    meth_order = []
    methods = []
    prec_mth = ""
    mth = 0
    subt = 0
    order = 0
    prec = 0
    for i in range(len(text)):
        if (text[i].find('action') != -1):
            return methods
        if text[i].find(":method") != -1:
            text[i] = text[i].strip(')').strip('(')
            text[i] = text[i].split()
            meth_name = text[i][1:]
            mth = 1
        elif (text[i] == '))'):
            m = Method(meth_name, meth_param, prec_mth, meth_subtask, meth_task, meth_order)
            methods.append(m)
            meth_name = ""
            meth_task = ""
            meth_subtask = []
            meth_param = ""
            meth_order = []
            prec_mth = ""
            mth = 0
            order = 0
        elif text[i].find(':param') != -1 and mth == 1:
                text[i] = text[i].replace("(", "")
                text[i] = text[i].replace(")", "")
                text[i] = text[i].split()
                meth_param = text[i][1:]
        elif text[i].find(':precond') != -1 and mth == 1:
            text[i] = text[i].split()
            prec_mth = text[i][2:]
        elif (text[i].find(':task') != -1 and mth == 1):
            text[i] = text[i] = text[i].strip(')').strip('(')
            text[i] = text[i].replace("(", "")
            text[i] = text[i].split()
            meth_task = text[i][1:]
        elif (text[i].find(':subtask') != -1 and mth == 1):
            subt = 1
        elif (text[i].find(':ordering') != -1):
            order = 1
            subt = 0
        elif (subt == 1 and mth == 1 and order == 0):
            sub = text[i]
            meth_subtask.append(sub)
        elif (order == 1):
            text[i].strip(')').strip('(')
            meth_order.append(text[i])

def subt_sep(sub):
    new_sub = sub
    firpar = sub.find('(')
    secpar = sub.find('(', firpar + 1)
    name = sub[firpar:secpar - 1]
    name = str(name)
    name = name.strip('(').strip(')')
    tasks = sub[secpar + 1:]
    tasks = str(tasks)
    tasks = tasks.replace("(", "")
    tasks = tasks.replace(")", "")
    s = Subtask(name, tasks)
    return s

#parse domain file and answer
def domain_parser(Dom):
    x = 5
    y = 5
    with open(Dom) as file:
        text = [row.strip() for row in file]
    text[0] = text[0].strip(')').strip('(')
    text[0] = text[0].split()
    D = Domain(text[0][2:], parse_requirement(Dom), parse_types(Dom), parse_predic(Dom), parse_action(Dom), parse_task(Dom), parse_method(Dom))
    print("domain name - ", D.name)
    print("___________________________________")
    print("requirements - ", parse_requirement(Dom))
    print("___________________________________")
    print("types - ", parse_types(Dom))
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
    for mth in D.method:
        print("name - ", mth.name)
        print("task - ", mth.task)
        print("preconditions - ", mth.prec)
        print("parametres - ", mth.params)
        print("subtask:")
        for sub in mth.subtask:
            s = subt_sep(sub)
            print(s.name, "-", s.tasks)
        if (mth.order != []):
            print("ordering:")
            print(*mth.order)
        print('++++++')
        print()

##парсит Домен, не печатая его
def parse_domain(Dom):
    with open(Dom) as file:
        text = [row.strip() for row in file]
    text[0] = text[0].strip(')').strip('(')
    text[0] = text[0].split()
    D = Domain(text[0][2:], parse_requirement(Dom), parse_types(Dom), parse_predic(Dom), parse_action(Dom), parse_task(Dom), parse_method(Dom))
    return D



#domain_parser('/Users/anastasia/Downloads/domain_robot.pddl')