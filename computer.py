import time

from machine import Pin


def pad(program):
    for index in enumerate(program):
        if len(program[index]) == 1:
            program[index].append('0' * 8)


class Computer:
    def __init__(self,
                 clock_pin=28,
                 clock_interval=500,
                 instruction_pins=(*range(16, 23), 26),
                 data_pins=range(8),
                 input_pins=range(8, 16)):
        self.clock_pin = Pin(clock_pin, Pin.OUT)
        self.clock_interval = clock_interval
        self.instruction_pins = [Pin(i, Pin.OUT) for i in instruction_pins]
        self.data_pins = [Pin(i, Pin.OUT) for i in data_pins]
        self.input_pins = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in input_pins]
        self.program = []

    def execute(self, instruction):
        start = time.ticks_ms()
        # if input pin is true
        if instruction[0][4] == '1' and not isinstance(instruction[1], int):
            map(lambda x: x.value(0), self.data_pins)
            for opcode, i_pin in zip(instruction[0], self.instruction_pins):
                i_pin.value(opcode)
            instruction[1](''.join(map(lambda x: str(x.value()), self.input_pins)))
        else:
            for index, (opcode, data) in enumerate(instruction):
                self.instruction_pins[index].value(int(opcode))
                self.data_pins[index].value(int(data))
        self.tick(start)

    def tick(self, start=None):
        start = start or time.ticks_ms()
        self.clock_pin.value(1)
        time.sleep_ms(self.clock_interval - time.ticks_diff(time.ticks_ms(), start))
        self.clock_pin.value(0)

    def store_program(self, program):
        self.program = program

    def run(self):
        for instruction in self.program:
            self.execute(instruction)
