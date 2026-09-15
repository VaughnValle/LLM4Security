`timescale 1ns/1ps
module tb;
reg enabled;
reg [7:0] secret;
wire [7:0] data;
integer s,e;
dut d(enabled,secret,data);
initial begin
 $dumpfile("waveform.vcd");$dumpvars(0,tb);
 for(s=0;s<256;s=s+1) for(e=0;e<2;e=e+1) begin
  secret=s;enabled=e;#1;
  $display("CHECK secret=%h enabled=%b data=%h",secret,enabled,data);
  if(enabled && data !== secret) $fatal(1,"FUNCTIONAL_FAILURE: enabled output");
  if(!enabled && data !== 0) $fatal(1,"SECURITY_VIOLATION: disabled output leaks data");
 end
 $display("SECURITY_TEST_PASS");$finish;
end
endmodule
