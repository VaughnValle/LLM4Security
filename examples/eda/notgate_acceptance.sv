// Deployment smoke test for GUIDE's VerilogEval Prob005_notgate_ref.sv.
// This checks the reference module, not a generated solution or security property.
module tb;
  reg in;
  wire out;
  RefModule dut(.in(in), .out(out));
  initial begin
    $dumpfile("waveform.vcd");
    $dumpvars(0, tb);
    in = 0; #1;
    if (out !== 1'b1) $fatal(1, "NOT(0) failed");
    in = 1; #1;
    if (out !== 1'b0) $fatal(1, "NOT(1) failed");
    $display("GUIDE_NOTGATE_PASS");
    $finish;
  end
endmodule
