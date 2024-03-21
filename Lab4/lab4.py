outs = open("out.state", "w")
variables = dict()
num_line = 0
space_cnt = 0


def print_state(prog, state):
    print(f"s{state}{'' if state == 0 and prog == 0 else ' -> '}", file=outs, end='')


def is_float(numstr):
    try:
        float(numstr)
        return True
    except ValueError:
        return False


def replace_var_by_value(string):
    for i in range(len(string)):
        if string[i] in variables:
            string[i] = variables[string[i]]
        elif string[i] not in {"-", "+", "*", "/", "(", ")", ".", " ", ">", "<", "==", "<=", ">=", "&", "|",
                               "!"} and not is_float(string[i]):
            raise ValueError(f"Переменная <{string[i]}> не инициализирована")


class Calculator:
    string = ""

    def __init__(self, string):
        string = string.replace("(", " ( ")
        string = string.replace(")", " ) ")
        self.string = string.split()
        replace_var_by_value(self.string)

    def __check(self):
        try:
            tmp_s = "".join([str(el) for el in self.string])
            if len(set(tmp_s) - {"0", "1", "2", "3", "4", "5", "6", "7", "8",
                                 "9", "-", "+", "*", "/", "(", ")", ".", " "}) > 0:
                return True

            for i in range(1, len(tmp_s)):
                if (tmp_s[i - 1] in {"-", "+", "*", "/", "."} and tmp_s[i] in {"-", "+", "*", "/", "."}
                        and tmp_s[i - 1] in {"-", "+", "*", "/", "."} and tmp_s[i] != "-"):
                    return True
            eval(tmp_s)
            return False
        except:
            return True

    def __to_RPN(self):
        priority = {"+": 2, "-": 2, "*": 3, "/": 3, "(": 1}
        stack = []
        out = ''
        for sym in self.string:
            sym = str(sym)
            if sym.isalpha() or sym.isnumeric() or is_float(sym):
                out += sym + " "
            elif sym in {"+", "-", "*", "/"}:
                if len(stack) == 0 or all(priority[el] < priority[sym] for el in stack):
                    stack.append(sym)
                else:
                    while stack and priority[stack[-1]] >= priority[sym]:
                        out += stack.pop() + " "
                    stack.append(sym)
            elif sym == "(":
                stack.append(sym)
            elif sym == ")":
                while stack:
                    tmp = stack.pop()
                    if tmp == "(":
                        break
                    out += tmp + " "
        while stack:
            out += stack.pop() + " "
        return out

    def calc(self):
        priority = {"+": 2, "-": 2, "*": 3, "/": 3, "(": 1}
        if self.__check():
            raise ValueError("В выражении допущена ошибка")
        inp = self.__to_RPN()
        res = 0
        stack = []
        for el in inp.split():
            if el in priority:
                res = stack.pop()
                if el == "+":
                    res += stack[-1]
                elif el == "-":
                    res = stack[-1] - res
                elif el == "*":
                    res *= stack[-1]
                else:
                    res = stack[-1] / res
                stack.pop()
                stack.append(res)
            else:
                tmp = float(el)
                if tmp < -32768 or tmp > 32767:
                    raise ValueError("Операнд находится за пределами")
                stack.append(tmp)
        if res < -32768 or res > 32767:
            raise ValueError("Переполнение")
        if res == 0 and len(stack) == 1:
            res = str(stack[0])
        return res


def get_var(line):
    return line[line.index("(") + 1:line.rindex(")")]


def get_value(line):
    var_name = get_var(line)
    if '"' in var_name:
        return var_name.replace('"', "")
    if var_name in variables:
        return variables[get_var(line)]
    else:
        try:
            tmp = Calculator(var_name)
            ans = tmp.calc()
        except Exception as e:
            raise ValueError(e)
        return ans


def err(e):
    print(f"Строка {num_line}: {e}")
    print_state(0, 0)
    exit(1)


def try_boolean(if_cond):
    if_cond = if_cond.replace("(", " ( ").replace(")", " ) ").split()
    replace_var_by_value(if_cond)
    if len({">", "<", "==", ">=", "<=", "!="} & set(if_cond)) == 0:
        raise ValueError("Ошибка в условии")
    if_cond = [str(el) for el in if_cond]
    res = eval("".join(if_cond))
    return res


def main():
    print_state(0, "0")
    global num_line
    inp = open("input.txt") # y1
    open_brackets = [] # y2
    print_state(0, 1)
    for line in inp: # x1
        num_line += 1 # y3
        line = line.strip().rstrip() # y4
        print_state(0, 2)
        if "} else {" in line: # x2
            open_brackets.append(1 - open_brackets.pop()) # y5
            continue
        elif "}" in line: # x3
            open_brackets.pop() # y6
            continue
        elif line.startswith("if "): # x4
            try: # x5
                if_cond = get_var(line) # y7
                res = try_boolean(if_cond) # y8
                open_brackets.append(int(res)) # y9
            except Exception as e:
                err(e) # y10
        elif len(line) == 0 or len(open_brackets) > 0 and not open_brackets[-1]: # x6
            continue
        elif " = " in line: # x7
            splitted_line = line.split(" = ") # y11
            print_state(0, 3)
            if len(splitted_line) == 2 and splitted_line[0][0].isalpha(): # x8
                if "input()" in splitted_line[1]: # x9
                    variables[splitted_line[0]] = input() # y12
                    continue
                elif '"' in splitted_line[1]: # x10
                    variables[splitted_line[0]] = splitted_line[1].replace('"', "") # y13
                    continue
                e = -1 # y14
                print_state(0, 4)
                try: # x5
                    tmp = Calculator(splitted_line[1]) # y15
                    res = tmp.calc() # y16
                except Exception as er:
                    e = er # y17
                print_state(0, 5)
                if e != -1: # x11
                    try: #x5
                        res = try_boolean(splitted_line[1]) # y18
                        print_state(0, 6)
                    except:
                        err(e) # y10

                variables[splitted_line[0]] = float(res) # y19

            else:
                err("Ошибка") # y20
        elif line.startswith("print("): # x12
            try: #x5
                print(get_value(line)) # y21
            except Exception as e:
                err(e) # y10
        else:
            err("Неизвестная команда") # y22
        print_state(0, 1)
    print_state(0, 0)


main()
