`timescale 1ns/1ps
module tb;
  reg request, privileged, bypass;
  wire grant;
  integer stimulus;
  access_gate dut(request, privileged, bypass, grant);
  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(0, tb);
    for (stimulus = 0; stimulus < 8; stimulus = stimulus + 1) begin
      {request, privileged, bypass} = stimulus[2:0];
      #1;
      if (grant !== (request & privileged))
        $fatal(1, "AUTHORIZATION_VIOLATION request=%b privileged=%b bypass=%b grant=%b",
               request, privileged, bypass, grant);
    end
    $display("AUTHORIZATION_TEST_PASS: all eight input combinations checked");
    $finish;
  end
endmodule
