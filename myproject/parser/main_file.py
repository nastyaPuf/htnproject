import grounding as gr
import domain_parser as dp
import problem_parser as pp

if __name__ == '__main__':
    ##Dom -- адрес домена
    ##Prob -- адрес проблемы
    dp.parse_domain(Dom)
    pp.parse_problem(Prob)
    dp.domain_parser(Dom)
    pp.print_parsing(Prob)
    gr.ground_action(Dom, Prob)
    gr.ground_task(Dom, Prob)
