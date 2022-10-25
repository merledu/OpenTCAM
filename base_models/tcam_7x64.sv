
module tcam7x64 (
    input logic         clk_i,
    input logic         csb_i,
    input logic         web_i,
    input logic  [3:0]  wmask_i,
    input logic  [7:0]  addr_i,
    input logic  [31:0] wdata_i,
    output logic [63:0] rdata_o
);

    //////////////////////
    //  Write address   //
    //////////////////////

    logic [7:0] aw_addr;

    assign aw_addr = {8{~web_i}} & addr_i;

    ////////////////////////////
    //  Read/Search address   //
    ////////////////////////////

    logic [7:0] ar_addr1;
    logic [7:0] ar_addr2;

    assign ar_addr1 = {1'b0, addr_i[6:0]}; // always read/search lower 128 rows
    assign ar_addr2 = {1'b1, addr_i[6:0]} & {8{web_i}}; // always read/search upper 128 rows

    /////////
    // PMA //
    /////////

    logic [31:0] rdata_lower;
    logic [31:0] rdata_upper;
    logic [63:0] rdata;

    assign rdata = {rdata_upper , rdata_lower};
    assign rdata_o = rdata;

    sky130_sram_1kbyte_1rw1r_32x256_8 u_vtb(

        // Port 0: RW
        .clk0	(clk_i),
        .csb0	(csb_i),
        .web0	(web_i),
        .wmask0	(wmask_i),
        .addr0	((web_i ? ar_addr1: aw_addr)),
        .din0	(wdata_i),
        .dout0	(rdata_lower),
        // Port 1: R
        .clk1	(clk_i),
        .csb1	(csb_i),
        .addr1	(ar_addr2),
        .dout1	(rdata_upper)
    );

endmodule