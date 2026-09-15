`timescale 1ns/1ps
module tb;
reg debug_read,authorized;
reg [7:0] secret,expected;
wire [7:0] data;
integer s,c;
dut d(debug_read,authorized,secret,data);
initial begin
 $dumpfile("waveform.vcd"); $dumpvars(0,tb);
 for(s=0;s<256;s=s+1) for(c=0;c<4;c=c+1) begin
  secret=s; {debug_read,authorized}=c[1:0]; #1;
  expected=(debug_read && authorized)?secret:0;
  $display("CHECK secret=%h read=%b authorized=%b data=%h",secret,debug_read,authorized,data);
  if(data !== expected) begin
   if(!authorized) $fatal(1,"SECURITY_VIOLATION: unauthorized debug output");
   else $fatal(1,"FUNCTIONAL_FAILURE: debug read or idle");
  end
 end
 $display("SECURITY_TEST_PASS"); $finish;
end
endmodule
