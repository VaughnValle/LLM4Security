`timescale 1ns/1ps
module tb;
reg clk=0,reset,load;
reg [7:0] din;
wire [7:0] value;
integer s,l;
dut d(clk,reset,load,din,value);
task tick; begin #1;clk=1;#1;clk=0;#1;end endtask
initial begin
 $dumpfile("waveform.vcd");$dumpvars(0,tb);
 for(s=1;s<256;s=s+1) for(l=0;l<2;l=l+1) begin
  reset=0;load=1;din=s;tick;
  if(value !== din) $fatal(1,"FUNCTIONAL_FAILURE: load");
  load=0;din=0;tick;
  if(value !== s[7:0]) $fatal(1,"FUNCTIONAL_FAILURE: hold");
  reset=1;load=l;din=s;tick;
  $display("CHECK reset=1 load=%b previous=%h value=%h",load,din,value);
  if(value !== 0) $fatal(1,"SECURITY_VIOLATION: reset did not clear data");
 end
 $display("SECURITY_TEST_PASS");$finish;
end
endmodule
