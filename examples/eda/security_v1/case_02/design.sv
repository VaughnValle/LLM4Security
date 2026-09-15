module dut(input request, privileged, bypass, output grant);
assign grant = request & (privileged | bypass);
endmodule
