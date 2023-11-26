import html_parser
import sys
import warnings


sys.setrecursionlimit(2147483647)
warnings.simplefilter("always")

states = []
input_symbols = []
stack_alphabet = []
start_state = ""
start_symbol = ""
accepting_states = set()
transitions = dict()


def check(state: str, remaining_input: list, stack_contents: list) -> bool:    
    if not remaining_input and (state in accepting_states or not stack_contents):
        return True
    
    if remaining_input:
        # If the transition is not spontaneous.
        popped_input_symbol = remaining_input.pop()
        if state in transitions and stack_contents[-1] in transitions[state] and popped_input_symbol in transitions[state][stack_contents[-1]]:
            popped_stack_element = stack_contents.pop()
            for possibility in transitions[state][popped_stack_element][popped_input_symbol]:
                p, l = possibility
                replaced_symbols = [] if l[0] == 'e' else l

                for symbol in replaced_symbols:
                    stack_contents.append(symbol)
                found = check(p, remaining_input, stack_contents)
                if found:
                    return True
                
                for symbol in replaced_symbols:
                    stack_contents.pop()
                    
            stack_contents.append(popped_stack_element)
        
        remaining_input.append(popped_input_symbol)

    # If the transition is spontaneous.
    if state in transitions and stack_contents[-1] in transitions[state] and 'e' in transitions[state][stack_contents[-1]]:
        popped_stack_element = stack_contents.pop()
        for possibility in transitions[state][popped_stack_element]['e']:
            p, l = possibility
            replaced_symbols = [] if l[0] == 'e' else l
            
            for symbol in replaced_symbols:
                stack_contents.append(symbol)
            
            found = check(p, remaining_input, stack_contents)
            if found:
                return True
            
            for symbol in replaced_symbols:
                stack_contents.pop()
                
        stack_contents.append(popped_stack_element)
    return False
            

def read_pda(pda_location: str):
    global states, input_symbols, stack_alphabet, start_state, start_symbol, accepting_states, transitions
    with open(pda_location) as file:
        line = file.readline()
        line = line.strip()
        states = line.split(' ')

        line = file.readline()
        line = line.strip()
        input_symbols = line.split(' ')

        line = file.readline()
        line = line.strip()
        stack_alphabet = line.split(' ')

        line = file.readline()
        line = line.strip()
        start_state = line

        line = file.readline()
        line = line.strip()
        start_symbol = line

        line = file.readline()
        line = line.strip()
        accepting_states = set(line.split(' '))

        transitions_list = []

        for line in file:
            line = line.strip().split(' ')
            q, a, X, p = line[:4]
            l = line[4:]
            l.reverse()

            transitions_list.append([q, X, a, p, l])
            transitions[q] = dict()

        for transition in transitions_list:
            q, X, a, p, l = transition
            transitions[q][X] = dict()
        
        for transition in transitions_list:
            q, X, a, p, l = transition
            transitions[q][X][a] = []
        
        for transition in transitions_list:
            q, X, a, p, l = transition
            transitions[q][X][a].append((p, l))


def read_pda_ignore_comments_and_newline(pda_location: str):
    global states, input_symbols, stack_alphabet, start_state, start_symbol, accepting_states, transitions
    with open(pda_location) as file:
        line = file.readline()
        line = line.strip()
        states = line.split(' ')

        line = file.readline()
        line = line.strip()
        input_symbols = line.split(' ')

        line = file.readline()
        line = line.strip()
        stack_alphabet = line.split(' ')

        line = file.readline()
        line = line.strip()
        start_state = line

        line = file.readline()
        line = line.strip()
        start_symbol = line

        line = file.readline()
        line = line.strip()
        accepting_states = set(line.split(' '))

        transitions_list = []

        for line in file:
            # line = line.strip().split(' ')
            line = line.strip()
            if not line or line[0] == '#':
                continue
            line = line.split(' ')

            q, a, X, p = line[:4]
            l = line[4:]
            l.reverse()

            transitions_list.append([q, X, a, p, l])
            transitions[q] = dict()

        for transition in transitions_list:
            q, X, a, p, l = transition
            transitions[q][X] = dict()
        
        for transition in transitions_list:
            q, X, a, p, l = transition
            transitions[q][X][a] = []
        
        for transition in transitions_list:
            q, X, a, p, l = transition
            transitions[q][X][a].append((p, l))

if __name__ == "__main__":
    pda_location = sys.argv[1]
    read_pda_ignore_comments_and_newline(pda_location)

    file_location = sys.argv[2]
    tokens = html_parser.parse_no_attributes(file_location)
    tokens.reverse()

    result = check(start_state, tokens, [start_symbol])
    if result:
        print("Accepted")
    else:
        print("Not accepted")



# def test_pda():
#     pda_location = sys.argv[1]
#     read_pda(pda_location)
#     print("PDA loaded!")

#     # print("States", states)
#     # print("Input symbols", input_symbols)
#     # print("Stack alphabet", stack_alphabet)
#     # print("Start state", start_state)
#     # print("Start symbol", start_symbol)
#     # print("Accepting states", accepting_states)
#     # import pprint
#     # print("Transitions", end=' ')
#     # pprint.pprint(transitions)


#     file_location = sys.argv[2]
#     with open(file_location) as file:
#         inputs = file.readlines()
    
#     # get_token asumsi 1 huruf 1 token
#     inputs = [list(x.strip()) for x in inputs]
#     for i in range(len(inputs)):
#         inputs[i].reverse()
    
#     for string in inputs:
#         result = check(start_state, string.copy(), [start_symbol])

#         string = ''.join(string)
#         string = string[::-1]
#         if result:
#             print(f"\"{string}\" is accepted.")
#         else:
#             print(f"\"{string}\" is not accepted.")