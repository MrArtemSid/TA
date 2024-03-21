import sys
outs = open("out.state", "w")

class TmpClass:
    tab_cnt = 0
    var = ''
    length = ''

    def __init__(self, tab_cnt, var, length):
        self.tab_cnt = tab_cnt
        self.var = var
        self.length = length

is_first_time = 1
def print_state(state):
    print(f"s{state}{' -> ' if state != 0 else ''}", file=outs, end='')


def main():
    print_state('0')
    inp = open("in.pas") #y1
    out = open("out.pas", "w") #y2

    sys.stdout = out #y3
    stack = [] #y4
    stack1 = [] #y5
    print_state(1)  # s1
    for line in inp: #x0
        line = line.rstrip() #y6 s1
        split_line = line.split() #y7 s1
        is_for_prev = 0 #y8 s1
        print_state(2) #s2
        if "for" in split_line: #x1
            stack1.append("for") #y9
        elif any(el in {"while", "else", "if"} for el in split_line): #x2
            stack1.append(0) #y10
        elif len(stack1) > 0: #x3
            markers = {"begin", 'end;'} & set(split_line) #y11
            print_state(4) #s4
            if len(markers) > 0: #x4
                if stack1[-1] == "for": #x5
                    is_for_prev = 1 #y12
                print_state(5) #s5
                if "end;" in markers: #x6
                    stack1.pop() #y13
        print_state(3) #s3
        if "for" in split_line: #x1
            to_ind = split_line.index("to") #y14
            do_ind = split_line.index("do") #y15

            tab_cnt = line.find("for ") #y16
            start = split_line[split_line.index("for") + 1:to_ind] #y17

            print(f"{' ' * tab_cnt}{' '.join(start)};") #y18
            print(' ' * tab_cnt + "repeat", *split_line[do_ind + 1:]) #y19

            stack.append(TmpClass(tab_cnt, start[0].split(":=")[0], split_line[do_ind - 1])) #y20
        elif "begin" in split_line and len(stack) and is_for_prev: #x7
            continue #y21
        elif "end;" in split_line and len(stack) and is_for_prev: #x8
            tmp = stack[-1] #y22
            print(f"{' ' * tmp.tab_cnt}\t{tmp.var} := {tmp.var} + 1;") #y23
            print(f"{' ' * tmp.tab_cnt}until {tmp.var} > {tmp.length};") #y24
            stack.pop() #y25
        else:
            print(line) #y26
        print_state(1)  # s1

    out.close() #y27
    print_state(0)
main()
