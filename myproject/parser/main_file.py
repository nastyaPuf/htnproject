import grounding as gr
import sys

def main(argv):
    #dp.parse_domain(argv[1])
    #pp.parse_problem(argv[2])
    gr.ground_everything(argv[1], argv[2])

if __name__ == '__main__':
    main(sys.argv[1:])

