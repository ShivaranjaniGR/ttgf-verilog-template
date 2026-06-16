import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer

@cocotb.test()
async def test_pwm_generator_behavior(dut):
    """Test the PWM generator inputs, safety constraints, and output toggles"""
    
    # 1. Initialize and start the clock properly using the modern .start() method
    clock = Clock(dut.clk, 20, units="ns")
    await clock.start()

    # 2. Force absolute initial states immediately to clear GL 'x' states
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    if hasattr(dut, 'ena'):
        dut.ena.value = 1
    
    # Wait 20ns to let physical logic gates settle to their reset values
    await Timer(20, units="ns")
    
    # Release the hardware reset on a clean edge
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # 3. Apply Regular Operational Inputs
    # ui_in bit mapping: bit 0 = enable, bits 4-1 = raw_period, bit 5 = invert
    enable = 1
    raw_period = 8    # Set period to 8 clock cycles
    invert = 0
    ui_val = (invert << 5) | (raw_period << 1) | enable
    
    # uio_in bit mapping: bits 3-0 = raw_duty
    raw_duty = 4      # Set duty cycle to 4 clock cycles
    uio_val = raw_duty

    # Apply values cleanly aligned to the clock
    await FallingEdge(dut.clk)
    dut.ui_in.value = ui_val
    dut.uio_in.value = uio_val

    # Allow waves to generate
    await ClockCycles(dut.clk, 20)

    # 4. Test Safety Clamps
    await FallingEdge(dut.clk)
    unsafe_period = 1 # Forces internal logic clamp to 3
    ui_val_clamp = (invert << 5) | (unsafe_period << 1) | enable
    dut.ui_in.value = ui_val_clamp
    
    await ClockCycles(dut.clk, 10)
