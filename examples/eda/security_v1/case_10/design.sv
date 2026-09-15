module dut(input enabled, input [7:0] secret, output [7:0] data);
assign data = enabled ? secret : {7'b0,secret[0]};
endmodule
