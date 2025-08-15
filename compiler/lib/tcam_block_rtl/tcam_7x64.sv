`timescale 1ns/1ps
module tcam7x64 (
    input   logic           in_clk,
    input   logic           in_csb,
    input   logic           in_web,
    input   logic   [3:0]   in_wmask,
    input   logic   [7:0]   in_addr,
    input   logic   [31:0]  in_wdata,
    output  logic   [63:0]  out_rdata
);

    // * ------------------------------ Write address
    logic [7:0] aw_addr;

    assign aw_addr = {8{~in_web}} & in_addr;

    // * ------------------------------ Read/Search address
    logic [7:0] ar_addr1;
    logic [7:0] ar_addr2;

    // always read/search lower 128 rows
    assign ar_addr1 = {1'b0, in_addr[6:0]};
    // always read/search upper 128 rows
    assign ar_addr2 = {1'b1, in_addr[6:0]} & {8{in_web}};

    // * ------------------------------ PMA
    logic [31:0] rdata_lower;
    logic [31:0] rdata_upper;
    logic [63:0] rdata;

    assign rdata = {rdata_upper, rdata_lower};
    assign out_rdata = rdata;

    sky130_sram_1kbyte_1rw1r_32x256_8 dut_vtb(
        // Port 0: RW
        .clk0       (in_clk),
        .csb0       (in_csb),
        .web0       (in_web),
        .wmask0     (in_wmask),
        .addr0      ((in_web ? ar_addr1: aw_addr)),
        .din0       (in_wdata),
        .dout0      (rdata_lower),
        // Port 1: R
        .clk1       (in_clk),
        .csb1       (in_csb),
        .addr1      (ar_addr2),
        .dout1      (rdata_upper)
    );

endmodule
