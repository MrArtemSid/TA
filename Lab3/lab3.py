import sys
outs = open("out.state", "w")
def print_state(prog, state):
    print(f"s{prog}.{state}{'' if state == 0 and prog == 0 else ' -> '}", file=outs, end='')
class Calculator:
    string = ""

    def __init__(self, string):
        string = string.replace("(", " ( ")
        string = string.replace(")", " ) ")
        self.string = string.split()

    def __check(self):
        print_state(2, "0")
        try:
            print_state(2, 1)
            tmp_s = "".join(self.string) # y30
            if len(set(tmp_s) - {"0", "1", "2", "3", "4", "5", "6", "7", "8",
                                 "9", "-", "+", "*", "/", "(", ")", ".", " "}) > 0: #x18
                print_state(2, 0)
                return True # y31

            for i in range(1, len(tmp_s)): #x19
                if (tmp_s[i - 1] in {"-", "+", "*", "/", "."} and tmp_s[i] in {"-", "+", "*", "/", "."}
                        and tmp_s[i - 1] in {"-", "+", "*", "/", "."} and tmp_s[i] != "-"): #x20
                    print_state(2, 0)
                    return True # y31
            eval(tmp_s) #x21
            print_state(2, 0)
            return False #y32
        except:
            print_state(2, 0)
            return True # y31

    def __is_float(self, numstr):
        try:
            float(numstr)
            return True
        except ValueError:
            return False

    def __to_RPN(self):
        print_state(3, "0")
        priority = {"+": 2, "-": 2, "*": 3, "/": 3, "(": 1} # y4
        stack = [] # y5
        out = '' # y6
        print_state(3, 1)
        for sym in self.string: # x1
            if sym.isalpha() or sym.isnumeric() or self.__is_float(sym): # x2
                out += sym + " " # y7
            elif sym in {"+", "-", "*", "/"}: # x3
                if len(stack) == 0 or all(priority[el] < priority[sym] for el in stack): #x4
                    stack.append(sym) # y8
                else:
                    print_state(3, 2)
                    while stack and priority[stack[-1]] >= priority[sym]: # x5
                        out += stack.pop() + " " #y9
                        print_state(3, 2)
                    stack.append(sym) #y8
            elif sym == "(": #x6
                stack.append(sym) # y8
            elif sym == ")": # x7
                print_state(3, 4)
                while stack: # x8
                    tmp = stack.pop() # y12
                    print_state(3, 3)
                    if tmp == "(": # x9
                        break
                    out += tmp + " " # y13
                    print_state(3, 4)
            print_state(3, 1)
        print_state(3, 5)
        while stack: #x8
            out += stack.pop() + " " # y9
            print_state(3, 5)
        print_state(3, 0)
        return out #y14

    def calc(self):
        print_state(1, "0")
        priority = {"+": 2, "-": 2, "*": 3, "/": 3, "(": 1}  # y4
        print_state(1, 1)
        if self.__check(): #x10
            print_state(1, 0)
            return "В выражении допущена ошибка" # y15
        print_state(1, 1)
        inp = self.__to_RPN() # y16
        print_state(1, 1)
        res = 0 # y17
        stack = [] #y5
        print_state(1, 2)
        for el in inp.split(): #x11
            if el in priority: #x12
                res = stack.pop() #y18
                print_state(1, 3)
                if el == "+": #x13
                    res += stack[-1] #y19
                elif el == "-": #x14
                    res = stack[-1] - res #y20
                elif el == "*": #x15
                    res *= stack[-1] #y21
                else:
                    res = stack[-1] / res #y22
                print_state(1, 4)
                stack.pop() #y23
                stack.append(res) #y24
            else:
                tmp = float(el) #y25
                print_state(1, 5)
                if tmp < -32768 or tmp > 32767: #x16
                    print_state(1, 0)
                    return "Операнд находится за пределами" #y26
                stack.append(tmp) #y27
            print_state(1, 2)
        if res < -32768 or res > 32767: #x17
            print_state(1, 0)
            return "Переполнение" #y28
        print_state(1, 0)
        return res #y29


def main():
    print_state(0, "0")
    inp = open("input.txt").readline() #y1
    a = Calculator(inp) # y2
    print(a.calc()) # y3
    print_state(0, 0)

main()