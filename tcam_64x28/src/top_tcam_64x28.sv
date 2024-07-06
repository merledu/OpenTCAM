`timescale 1ns/100ps

module top_tcam_mem (
    input	logic	in_clk,
    input	logic	in_csb,
    input	logic	in_web,
    input	logic	[3:0]	in_wmask,
    input	logic	[27:0]	in_addr,
    input	logic	[31:0]	in_wdata,
    output	logic	[5:0]	out_pma
);

    // memory block selection for write logic
    wire	[3:0]	block_sel;
    assign block_sel[0] = (in_addr[9:8] == 2'd0);
    assign block_sel[1] = (in_addr[9:8] == 2'd1);
    assign block_sel[2] = (in_addr[9:8] == 2'd2);
    assign block_sel[3] = (in_addr[9:8] == 2'd3);

    // logic for write mask
    wire	[3:0]	wmask0;
    wire	[3:0]	wmask1;
    wire	[3:0]	wmask2;
    wire	[3:0]	wmask3;
    assign wmask0 = { 4{block_sel[0]} } & in_wmask;
    assign wmask1 = { 4{block_sel[1]} } & in_wmask;
    assign wmask2 = { 4{block_sel[2]} } & in_wmask;
    assign wmask3 = { 4{block_sel[3]} } & in_wmask;

    // logic for write addresses
    wire	[7:0]	aw_addr0;
    wire	[7:0]	aw_addr1;
    wire	[7:0]	aw_addr2;
    wire	[7:0]	aw_addr3;
    assign aw_addr0 = { 8{block_sel[0]} } & in_addr[7:0];
    assign aw_addr1 = { 8{block_sel[1]} } & in_addr[7:0];
    assign aw_addr2 = { 8{block_sel[2]} } & in_addr[7:0];
    assign aw_addr3 = { 8{block_sel[3]} } & in_addr[7:0];

    // address mux for all N blocks (selects between read or write addresses)
    wire	[6:0]	vtb_addr0;
    wire	[6:0]	vtb_addr1;
    wire	[6:0]	vtb_addr2;
    wire	[6:0]	vtb_addr3;
    assign vtb_addr0 = in_web ? { 1'b0, in_addr[6:0] } : aw_addr0;
    assign vtb_addr1 = in_web ? { 1'b0, in_addr[13:7] } : aw_addr1;
    assign vtb_addr2 = in_web ? { 1'b0, in_addr[20:14] } : aw_addr2;
    assign vtb_addr3 = in_web ? { 1'b0, in_addr[27:21] } : aw_addr3;

    // TCAM memory block instances
    wire	[63:0]	out_rdata0;
    wire	[63:0]	out_rdata1;
    wire	[63:0]	out_rdata2;
    wire	[63:0]	out_rdata3;

    tcam7x64 tcam7x64_dut0 (
        .in_clk      (      in_clk),
        .in_csb      (      in_csb),
        .in_web      (      in_web),
        .in_wmask    (    in_wmask),
        .in_addr     (   vtb_addr0),
        .in_wdata    (    in_wdata),
        .out_rdata   (   out_rdata0)
    );
    tcam7x64 tcam7x64_dut1 (
        .in_clk      (      in_clk),
        .in_csb      (      in_csb),
        .in_web      (      in_web),
        .in_wmask    (    in_wmask),
        .in_addr     (   vtb_addr1),
        .in_wdata    (    in_wdata),
        .out_rdata   (   out_rdata1)
    );
    tcam7x64 tcam7x64_dut2 (
        .in_clk      (      in_clk),
        .in_csb      (      in_csb),
        .in_web      (      in_web),
        .in_wmask    (    in_wmask),
        .in_addr     (   vtb_addr2),
        .in_wdata    (    in_wdata),
        .out_rdata   (   out_rdata2)
    );
    tcam7x64 tcam7x64_dut3 (
        .in_clk      (      in_clk),
        .in_csb      (      in_csb),
        .in_web      (      in_web),
        .in_wmask    (    in_wmask),
        .in_addr     (   vtb_addr3),
        .in_wdata    (    in_wdata),
        .out_rdata   (   out_rdata3)
    );

    // AND gate instantiations
    wire	[63:0]	out_andgate0;
    wire	[63:0]	out_andgate1;
    wire	[63:0]	out_andgate2;
    and_gate andgate_dut0 (.out_data (out_andgate0), in_dataA (out_rdata0), in_dataB (out_rdata1));
    and_gate andgate_dut1 (.out_data (out_andgate1), in_dataA (out_andgate0), in_dataB (out_rdata2));
    and_gate andgate_dut2 (.out_data (out_andgate2), in_dataA (out_andgate1), in_dataB (out_rdata3));

    // Priority Encoder instantiations
    priority_encoder_64x6 priority_encoder_dut0(
        .in_data  (out_andgate2),
        .out_data (out_pma)
    );
endmodule

module and_gate (
    input   logic   [63:0]  in_dataA,
    input   logic   [63:0]  in_dataB,
    output  logic   [63:0]  out_data
);

    assign out_data = in_dataA & in_dataB;
endmodule

module priority_encoder_64x6 (
    input   logic [63:0]    in_data,
    output  logic [5:0]     out_data
);    

    always @(*) begin
        if(in_data[63] == 1)        out_data=6'd63;
        else if(in_data[62] == 1)   out_data=6'd62;
        else if(in_data[61] == 1)   out_data=6'd61;
        else if(in_data[60] == 1)   out_data=6'd60;
        else if(in_data[59] == 1)   out_data=6'd59;
        else if(in_data[58] == 1)   out_data=6'd58;
        else if(in_data[57] == 1)   out_data=6'd57;
        else if(in_data[56] == 1)   out_data=6'd56;
        else if(in_data[55] == 1)   out_data=6'd55;
        else if(in_data[54] == 1)   out_data=6'd54;
        else if(in_data[53] == 1)   out_data=6'd53;
        else if(in_data[52] == 1)   out_data=6'd52;
        else if(in_data[51] == 1)   out_data=6'd51;
        else if(in_data[50] == 1)   out_data=6'd50;
        else if(in_data[49] == 1)   out_data=6'd49;
        else if(in_data[48] == 1)   out_data=6'd48;
        else if(in_data[47] == 1)   out_data=6'd47;
        else if(in_data[46] == 1)   out_data=6'd46;
        else if(in_data[45] == 1)   out_data=6'd45;
        else if(in_data[44] == 1)   out_data=6'd44;
        else if(in_data[43] == 1)   out_data=6'd43;
        else if(in_data[42] == 1)   out_data=6'd42;
        else if(in_data[41] == 1)   out_data=6'd41;
        else if(in_data[40] == 1)   out_data=6'd40;
        else if(in_data[39] == 1)   out_data=6'd39;
        else if(in_data[38] == 1)   out_data=6'd38;
        else if(in_data[37] == 1)   out_data=6'd37;
        else if(in_data[36] == 1)   out_data=6'd36;
        else if(in_data[35] == 1)   out_data=6'd35;
        else if(in_data[34] == 1)   out_data=6'd34;
        else if(in_data[33] == 1)   out_data=6'd33;
        else if(in_data[32] == 1)   out_data=6'd32;
        else if(in_data[31] == 1)   out_data=6'd31;
        else if(in_data[30] == 1)   out_data=6'd30;
        else if(in_data[29] == 1)   out_data=6'd29;
        else if(in_data[28] == 1)   out_data=6'd28;
        else if(in_data[27] == 1)   out_data=6'd27;
        else if(in_data[26] == 1)   out_data=6'd26;
        else if(in_data[25] == 1)   out_data=6'd25;
        else if(in_data[24] == 1)   out_data=6'd24;
        else if(in_data[23] == 1)   out_data=6'd23;
        else if(in_data[22] == 1)   out_data=6'd22;
        else if(in_data[21] == 1)   out_data=6'd21;
        else if(in_data[20] == 1)   out_data=6'd20;
        else if(in_data[19] == 1)   out_data=6'd19;
        else if(in_data[18] == 1)   out_data=6'd18;
        else if(in_data[17] == 1)   out_data=6'd17;
        else if(in_data[16] == 1)   out_data=6'd16;
        else if(in_data[15] == 1)   out_data=6'd15;
        else if(in_data[14] == 1)   out_data=6'd14;
        else if(in_data[13] == 1)   out_data=6'd13;
        else if(in_data[12] == 1)   out_data=6'd12;
        else if(in_data[11] == 1)   out_data=6'd11;
        else if(in_data[10] == 1)   out_data=6'd10;
        else if(in_data[9] == 1)    out_data=6'd9;
        else if(in_data[8] == 1)    out_data=6'd8;
        else if(in_data[7] == 1)    out_data=6'd7;
        else if(in_data[6] == 1)    out_data=6'd6;
        else if(in_data[5] == 1)    out_data=6'd5;
        else if(in_data[4] == 1)    out_data=6'd4;
        else if(in_data[3] == 1)    out_data=6'd3;
        else if(in_data[2] == 1)    out_data=6'd2;
        else if(in_data[1] == 1)    out_data=6'd1;
        else
            out_data=6'd0;
    end
endmodule
