`timescale 1ns / 1ps

module tb;

    // Standard testbench wires driven by cocotb
    reg        clk;
    reg        rst_n;
    reg        ena;
    reg  [7:0] ui_in;
    reg  [7:0] uio_in;
    wire [7:0] uo_out;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;

    // Instantiate your exact module configuration
    tt_um_example uut (
        .ui_in   (ui_in),
        .uo_out  (uo_out),
        .uio     (uio_in), // Directly connecting the input vectors to your combined wire
        .clk     (clk),
        .rst_n   (rst_n)
    );

endmodule
