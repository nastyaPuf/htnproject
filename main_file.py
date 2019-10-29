import grounding as gr
import my_planner as mp
import sys

def main(argv):
    #dp.parse_domain(argv[1])
    #pp.parse_problem(argv[2])
    #g = gr.Grounder()
    #g.everything(argv[0], argv[1])
    planner = mp.Planner()
    planner.HTN(argv[0], argv[1], argv[2])


if __name__ == '__main__':
    main(sys.argv[1:])

