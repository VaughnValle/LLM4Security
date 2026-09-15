module dut(input clk, reset, locked, write_a, write_b, input [7:0] din, output reg [7:0] value);
always @(posedge clk) begin
 if(reset) value <= 0;
 else if((!locked && write_a) || write_b) value <= din;
end
endmodule
