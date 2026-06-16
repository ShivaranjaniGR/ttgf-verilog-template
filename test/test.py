import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

@cocotb.test()
async def test_pwm_generator_behavior(dut):
    """Test the PWM generator inputs, safety constraints, and output toggles"""
    
    # 1. Initialize a 50 MHz clock (20ns period)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock)

    # 2. Assert Reset System-wide
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    
    # Verify outputs stay low during a reset condition
    assert dut.uo_out.value == 0, "Outputs leaked logic high during reset!"
    
    # Release Reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # 3. Apply Basic Operational Inputs
    # ui_in bit mapping: bit 0 = enable, bits 4-1 = raw_period, bit 5 = invert
    enable = 1
    raw_period = 8    # Set period to 8 clock cycles
    invert = 0
    ui_val = (invert << 5) | (raw_period << 1) | enable
    
    # uio_in bit mapping: bits 3-0 = raw_duty
    raw_duty = 4      # Set duty cycle to 4 clock cycles (50% duty)
    uio_val = raw_duty

    # Apply values to the simulation on the falling clock edge
    await FallingEdge(dut.clk)
    dut.ui_in.value = ui_val
    dut.uio_in.value = uio_val

    # Let the simulation run for 20 clock cycles to watch the waves generate
    await ClockCycles(dut.clk, 20)

    # 4. Test the Safety Clamps (Force period low to see if it clamps to 3)
    await FallingEdge(dut.clk)
    unsafe_period = 1 # Should automatically clamp to 3 internally
    ui_val_clamp = (invert << 5) | (unsafe_period << 1) | enable
    dut.ui_in.value = ui_val_clamp
    
    await ClockCycles(dut.clk, 10)
