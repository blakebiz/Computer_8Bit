from computer import Computer
from perms import get_permutations


def get_answer(a, b, op):
    if op:
        result = (a + b) % 256
    else:
        result = ((a - b) + 256) % 256
    return '{:0>{w}}'.format(bin(result)[2:], w=8)


def full_test():
    program = []

    def callback(data, correct_answer):
        if data != correct_answer:
            print(f'data: {data}\ncorrect answer: {correct_answer}')
            input('Error occurred! Press enter to continue')

    for sub in range(0, 2):
        for data_b in get_permutations(8):
            program.append(['00000100', data_b])
            for data_a in get_permutations(8):
                program.append([f'0000001{sub}', data_a])
                program.append([f'0000100{sub}', lambda x: callback(x, get_answer(data_a, data_b, sub))])

    computer = Computer()
    computer.store_program(program)
    computer.run()
