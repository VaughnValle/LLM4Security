`timescale 1ns/1ps
module tb;
reg clk=0,reset,locked,write_a,write_b;
reg [7:0] din, expected;
wire [7:0] value;
integer l,p;
dut d(clk,reset,locked,write_a,write_b,din,value);
task tick; begin #1; clk=1; #1; clk=0; #1; end endtask
initial begin
 $dumpfile("waveform.vcd"); $dumpvars(0,tb);
 for(l=0;l<2;l=l+1) for(p=0;p<4;p=p+1) begin
  reset=1;locked=0;write_a=0;write_b=0;din=0;tick;
  if(value !== 0) $fatal(1,"FUNCTIONAL_FAILURE: reset");
  reset=0;write_a=1;din=8'h3c;tick;
  if(value !== 8'h3c) $fatal(1,"FUNCTIONAL_FAILURE: initial write");
  locked=l; {write_a,write_b}=p[1:0]; din=8'ha5; tick;
  expected=(!locked && (write_a || write_b)) ? 8'ha5 : 8'h3c;
  $display("CHECK lock=%b ports=%b%b value=%h expected=%h",locked,write_a,write_b,value,expected);
  if(value !== expected) begin
   if(locked) $fatal(1,"SECURITY_VIOLATION: locked register modified");
   else $fatal(1,"FUNCTIONAL_FAILURE: unlocked write or hold");
  end
 end
 $display("SECURITY_TEST_PASS"); $finish;
end
endmodule
