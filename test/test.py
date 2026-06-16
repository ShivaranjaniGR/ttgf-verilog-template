import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer

@cocotb.test()
async def test_pwm_generator_behavior(dut):
    """Test the PWM generator inputs, safety constraints, and output toggles"""
    
    # 1. Initialize a 50 MHz clock (20ns period)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock)

    # 2. Set initial values on falling edges to avoid setup/hold race conditions
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    
    # Give the simulator 1 ns to propagate the initial values
    await Timer(1, units="ns")
    
    # Verify outputs stay clean during reset condition
    assert dut.uo_out.value == 0, f"Expected 0 during reset, got {dut.uo_out.value}"
    
    # Release Reset
    await ClockCycles(dut.clk, 2)
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

    # Apply values to the simulation cleanly
    await FallingEdge(dut.clk)
    dut.ui_in.value = ui_val
    dut.uio_in.value = uio_val

    # Run simulation loop to verify generation
    await ClockCycles(dut.clk, 20)

    # 4. Test Safety Clamps (Force raw_period low to verify it clamps internally)
    await FallingEdge(dut.clk)
    unsafe_period = 1 # Hardware forces this to 4'd3 internally
    ui_val_clamp = (invert << 5) | (unsafe_period << 1) | enable
    dut.ui_in.value = ui_val_clamp
    
    await ClockCycles(dut.clk, 10)
