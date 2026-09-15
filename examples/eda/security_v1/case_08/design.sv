module dut(input clk, reset, load, input [7:0] din, output reg [7:0] value);
always @(posedge clk) begin
 if(load) value <= din;
 else if(reset) value <= 0;
end
endmodule
