def del_pr(str):
    str = str.strip(')').strip('(')
    str = str.split()
    return str

class Problem:
    def __init__(self, name, domain, obj, init, goal):
        Problem.name = name
        Problem.domain = domain
        Problem.obj = obj
        Problem.init = init
        Problem.goal = goal


def parse_problem(Prob):
    with open(Prob) as file:
        text = [row.strip() for row in file]
    pr_name = ""
    domain = ""
    obj = dict()
    ob = 0
    pr_init = []
    goal = 0
    pr_goal = []
    ini = 0
    for i in range (len(text)):
        if (text[i].find(':problem') != -1):
            text[i] = del_pr(text[i])
            pr_name = text[i][1:]
        elif (text[i].find(':domain') != -1):
            text[i] = del_pr(text[i])
            domain = text[i][1:]
        elif (text[i].find(':objects') != -1):
            ob = 1
        elif (text[i].find(':init') != -1):
            ob = 0
            ini = 1
        elif (text[i].find(':goal') != -1):
            ini = 0
            goal = 1
        elif (ob == 1 and text[i].find(')') == -1):
            text[i] = text[i].strip(')').strip('(')
            obj[text[i][:text[i].find('-')]] = [text[i][text[i].find('-') + 1:]]
        elif (ini == 1 and goal != 1):
            text[i] = del_pr(text[i])
            if (len(text[i]) != 0):
                pr_init.append(text[i])
        elif (goal == 1 and i < len(text)):
            text[i] = del_pr(text[i])
            pr_goal.append(text[i])
    pr = Problem(pr_name, domain, obj, pr_init, pr_goal)
    return pr


def print_parsing(Prob):
    problem = parse_problem(Prob)
    print("name - ", problem.name)
    print ('______________________')
    print("domain -", problem.domain)
    print('______________________')
    print("objects:")
    for objects in problem.obj:
        print(objects, "-", problem.obj[objects])
    print('______________________')
    print("initial state:")
    for state in problem.init:
        print(state)
    print('______________________')
    print("goal:")
    for goals in problem.goal:
        print(goals)

print_parsing('/Users/anastasia/Downloads/HTN-Translation-master/examples/robot/problems/pfile_10_10.pddl')





