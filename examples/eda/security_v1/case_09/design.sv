module dut(input enabled, input [7:0] secret, output [7:0] data);
assign data = enabled ? secret : 8'h00;
endmodule
