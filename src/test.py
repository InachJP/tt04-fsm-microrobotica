import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_controlador_microbots(dut):
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.fork(clock.start())

    # Reset the module
    dut.rst_n <= 0
    await RisingEdge(dut.clk)
    dut.rst_n <= 1
    await RisingEdge(dut.clk)

    # Define states and transitions for the test
    states = {
        "Standby": 0,
        "goforward": 1,
        "goright": 2,
        "goleft": 3
    }

    transitions = [
        ("Standby", "goforward"),
        ("goforward", "goforward"),
        ("goforward", "Standby"),
        ("Standby", "goright"),
        ("goright", "goright"),
        ("goright", "Standby"),
        ("Standby", "goleft"),
        ("goleft", "goleft"),
        ("goleft", "Standby")
    ]

    # Run the test
    state = "Standby"
    for transition in transitions:
        from_state, to_state = transition
        # Set input sensors based on current state
        if from_state == "Standby":
            dut.f_sensor <= 0
            dut.l_sensor <= 0
            dut.r_sensor <= 0
        elif from_state == "goforward":
            dut.f_sensor <= 0
            dut.l_sensor <= 1
            dut.r_sensor <= 1
        elif from_state == "goright":
            dut.f_sensor <= 1
            dut.l_sensor <= 1
            dut.r_sensor <= 0
        elif from_state == "goleft":
            dut.f_sensor <= 1
            dut.l_sensor <= 0
            dut.r_sensor <= 1
        
        await ClockCycles(dut.clk, 1)
        
        assert states[state] == int(dut.state)

        state = to_state
        await Timer(1, units="ns")

    cocotb.log.info("Test completed successfully")
