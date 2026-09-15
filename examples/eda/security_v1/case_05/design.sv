module dut(input debug_read, authorized, input [7:0] secret, output [7:0] data);
assign data = (debug_read && authorized) ? secret : 8'h00;
endmodule
