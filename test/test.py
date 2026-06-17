import cocotb
  from cocotb.clock import Clock
  from cocotb.triggers import ClockCycles, FallingEdge, Timer

  @cocotb.test()
  async def test_pwm_generator_behavior(dut):
      """Test the PWM generator inputs, safety constraints, and output toggles"""

      dut.ui_in.value  = 0
      dut.uio_in.value = 0
      dut.rst_n.value  = 0
      dut.ena.value    = 1

      cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())

      await ClockCycles(dut.clk, 5)

      await FallingEdge(dut.clk)
      dut.rst_n.value = 1
      await ClockCycles(dut.clk, 2)

      enable     = 1
      raw_period = 8
      invert     = 0
      ui_val     = (invert << 5) | (raw_period << 1) | enable

      raw_duty = 4
      uio_val  = raw_duty

      await FallingEdge(dut.clk)
      dut.ui_in.value  = ui_val
      dut.uio_in.value = uio_val

      await ClockCycles(dut.clk, 20)

      await FallingEdge(dut.clk)
      unsafe_period = 1
      ui_val_clamp  = (invert << 5) | (unsafe_period << 1) | enable
      dut.ui_in.value = ui_val_clamp

      await ClockCycles(dut.clk, 10)
