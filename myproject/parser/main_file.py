import grounding as gr
import sys

def main(argv):
    #dp.parse_domain(argv[0])
    #pp.parse_problem(argv[1])
    g = gr.Grounder()
    g.everything(argv[0], argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])
