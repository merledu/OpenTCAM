`timescale 1ns/1ps
module and_gate (
    input   logic   [63:0]  in_dataA,
    input   logic   [63:0]  in_dataB,
    output  logic   [63:0]  out_data
);

    assign out_data = in_dataA & in_dataB;

endmodule
