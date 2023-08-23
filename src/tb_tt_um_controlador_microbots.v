module tb_tt_um_controlador_microbots;

  reg clk;
  reg rst_n;
  reg [7:0] ui_in;
  
  wire [7:0] uo_out;
  wire [7:0] uio_in;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
  wire ena;

  tt_um_controlador_microbots dut (
    .ui_in(ui_in),
    .uo_out(uo_out),
    .uio_in(uio_in),
    .uio_out(uio_out),
    .uio_oe(uio_oe),
    .ena(ena),
    .clk(clk),
    .rst_n(rst_n)
  );

  initial begin
    $dumpfile("tb_tt_um_controlador_microbots.vcd");
    $dumpvars(0, tb_tt_um_controlador_microbots);

    clk = 0;
    forever #5 clk = ~clk;
  end

  initial begin
    rst_n = 0;
    ui_in = 8'b00000000;
    #10 rst_n = 1;
    
    // Wait a few cycles for initialization
    #20;

    // Run the test
    repeat (10) begin
      ui_in = 8'b00000001;  
      #20;
      ui_in = 8'b00000010; 
      #20;
      ui_in = 8'b00000011;
      #20;
      ui_in = 8'b00000100; 
      #20;
      ui_in = 8'b00000101;  
      #20;
      ui_in = 8'b00000110;  
      #20;
      ui_in = 8'b00000111;  
      #20;
      ui_in = 8'b00000000;  // No sensors active
      #0;
    end
    
    $finish;
  end

endmodule
