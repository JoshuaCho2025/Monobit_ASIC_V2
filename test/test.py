# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)  # Assert reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)  # De-assert reset

    # Test each state transition and output logic
    for epsilon_value in [0, 1]:  # Test for both epsilon values
        dut.ui_in.value = epsilon_value

        # Wait for a positive edge on the clock
        await RisingEdge(dut.clk)
        
        # Read outputs and validate expected behavior
        is_random_expected = 0  # Expected output, set as per your design needs
        valid_expected = 0      # Expected output, set as per your design needs
        assert dut.is_random_rsc_dat.value == is_random_expected, f"Failed: is_random expected {is_random_expected} but got {dut.is_random_rsc_dat.value}"
        assert dut.valid_rsc_dat.value == valid_expected, f"Failed: valid expected {valid_expected} but got {dut.valid_rsc_dat.value}"

        # Print output state for debugging
        dut._log.info(f"Epsilon: {epsilon_value}, Is_Random: {dut.is_random_rsc_dat.value}, Valid: {dut.valid_rsc_dat.value}")

        # Add further checks as needed for complete coverage
