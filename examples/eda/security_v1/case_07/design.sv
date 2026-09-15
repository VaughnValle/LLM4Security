module dut(input clk, reset, load, input [7:0] din, output reg [7:0] value);
always @(posedge clk) begin
 if(reset) value <= 0;
 else if(load) value <= din;
end
endmodule
