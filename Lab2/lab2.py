errors = ["нет ошибок", "неверный код операции", "неверный формат данных",
          "неверная длина операндов", "деление на 0", "переполнение"]
out = open("output.state", "w")
def print_state(state, op, a, b, err):
    print(f"s({bin(state)[2:].zfill(3)})", f"{op:02}",
          bin(a)[2:].zfill(8), bin(b)[2:].zfill(8),
          f"{bin(err)[2:].zfill(3)} ({errors[err]})", "", sep="\n", file=out)
def main():
    print_state(0, 0, 0, 0, 0) #s0
    err = 0 #y1
    inp = open("input.txt") #y2
    splitted_line = inp.readline().split() #y3
    print_state(1, 0, 0, 0, 0) #s1

    if splitted_line[0] not in {"10", "01"}: #x0
        err = 1 #y4
    elif len(splitted_line) != 3 or any(set(el) not in [{"0", "1"}, {"1"}, {"0"}] for el in splitted_line): #x1
        err = 2 #y5
    elif len(splitted_line[0]) != 2 or len(splitted_line[1]) != 8 or len(splitted_line[2]) != 8: #x2
        err = 3 #y6
    print_state(2, 0, 0, 0, err)  # s2
    if err: #x3
        print("error:", bin(err)[2:].zfill(3), f"({errors[err]})") #y7
        return
    op, a, b = splitted_line #y8

    a = int(a, 2) #y9
    b = int(b, 2) #y10
    print_state(3, op, a, b, err)  # s3
    if op == "10": #x4
        if b != 0: #x5
            a //= b #y11
        else:
            err = 4 #y12
    elif op == "01": #x6
        ans = a * b #y13
        print_state(5, op, a, b, err)  # s5
        if ans > (2 ** 8) - 1: #x7
            err = 5 #y14
        else:
            a = ans #y15
    print_state(4, op, a, b, err) #s4
    if not err: #x8
        print("res:", bin(a)[2:].zfill(8)) #y16
    else:
        print("error:", bin(err)[2:].zfill(3), f"({errors[err]})") #y17
        return
    print() #y18

    print_state(0, op, a, b, err) #s0
main()