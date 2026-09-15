`timescale 1ns/1ps
module tb;
reg request, privileged, bypass;
wire grant;
integer i;
dut d(request, privileged, bypass, grant);
initial begin
  $dumpfile("waveform.vcd"); $dumpvars(0,tb);
  for(i=0;i<8;i=i+1) begin
    {request,privileged,bypass}=i[2:0]; #1;
    $display("CHECK access request=%b privileged=%b bypass=%b grant=%b",request,privileged,bypass,grant);
    if(grant !== (request & privileged)) $fatal(1,"SECURITY_VIOLATION: authorization");
  end
  $display("SECURITY_TEST_PASS"); $finish;
end
endmodule
