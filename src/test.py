import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.coroutine
def clock_generator(clk, period=10):
    while True:
        clk <= 0
        yield Timer(period // 2)
        clk <= 1
        yield Timer(period // 2)

@cocotb.coroutine
def reset_dut(rst_n):
    rst_n <= 0
    yield Timer(10)
    rst_n <= 1
    yield Timer(10)

@cocotb.coroutine
def run_test(dut):
    # Initialize signals
    dut.ui_in <= 0
    dut.uio_in <= 0
    dut.ena <= 0

    # Start clock
    cocotb.fork(clock_generator(dut.clk))

    # Reset DUT
    yield reset_dut(dut.rst_n)

    # Wait for initialization
    yield Timer(20)

    # Run the test
    for _ in range(10):
        dut.ui_in <= 1
        yield Timer(20)
        dut.ui_in <= 2
        yield Timer(20)
        dut.ui_in <= 3
        yield Timer(20)
        dut.ui_in <= 4
        yield Timer(20)
        dut.ui_in <= 5
        yield Timer(20)
        dut.ui_in <= 6
        yield Timer(20)
        dut.ui_in <= 7
        yield Timer(20)
        dut.ui_in <= 0
        yield Timer(0)

    yield Timer(10)
    raise cocotb.result.TestComplete
