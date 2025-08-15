`timescale 1ns/1ps
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
