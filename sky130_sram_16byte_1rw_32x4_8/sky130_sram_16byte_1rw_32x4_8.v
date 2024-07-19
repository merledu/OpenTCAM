module sky130_sram_16byte_1rw_32x4_8(
`ifdef USE_POWER_PINS
    vccd1,
    vssd1,
`endif
    clk,csb,web,wmask,addr,din,dout
  );

  parameter NUM_WMASKS = 4;
  parameter DATA_WIDTH = 32;
  parameter ADDR_WIDTH = 2;
  parameter RAM_DEPTH = 1 << ADDR_WIDTH;
  // FIXME: This delay is arbitrary.
//   parameter DELAY = 3 ;
//   parameter VERBOSE = 1 ; //Set to 0 to only display warnings
//   parameter T_HOLD = 1 ; //Delay to hold dout value after posedge. Value is arbitrary

`ifdef USE_POWER_PINS
    inout vccd1;
    inout vssd1;
`endif
  input  clk; // clock
  input  csb; // active low chip select
  input  web; // active low write control
  input [NUM_WMASKS-1:0]  wmask; // write mask
  input [ADDR_WIDTH-1:0]  addr;
  input [DATA_WIDTH-1:0]  din;
  output [DATA_WIDTH-1:0] dout;

  reg  csb_reg;
  reg  web_reg;
  reg [NUM_WMASKS-1:0]  wmask_reg;
  reg [ADDR_WIDTH-1:0]  addr_reg;
  reg [DATA_WIDTH-1:0]  din_reg;
  reg [DATA_WIDTH-1:0]  dout;

  // All inputs are registers
  always @(posedge clk)
  begin
    csb_reg <= csb;
    web_reg <= web;
    wmask_reg <= wmask;
    addr_reg <= addr;
    din_reg <= din;
    // #(T_HOLD) dout = 32'bx;
  end

reg [DATA_WIDTH-1:0]    mem [0:RAM_DEPTH-1];

  // Write Operation : When web = 0, csb = 0
  always @ (negedge clk)
  begin: MEM_WRITE
    if ( !csb_reg && !web_reg ) begin
        if (wmask_reg[0])
                mem[addr_reg][7:0] <= din_reg[7:0];
        if (wmask_reg[1])
                mem[addr_reg][15:8] <= din_reg[15:8];
        if (wmask_reg[2])
                mem[addr_reg][23:16] <= din_reg[23:16];
        if (wmask_reg[3])
                mem[addr_reg][31:24] <= din_reg[31:24];
    end
  end

  // Read Operation : When web = 1, csb = 0
  always @ (negedge clk)
  begin : MEM_READ
    if (!csb_reg && web_reg)
       dout <= mem[addr_reg];
  end
endmodule