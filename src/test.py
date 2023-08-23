import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


""" 
La idea es aprovechar los 8 bits y concatenar las salidas de los 4 motores, con el estado siguiente,
es decir, si el estado actual es 0 en forma decimal (00000000 -> ui_in) significa que la entrada de los sensores 000, 
por lo tanto los motores estan los 4 en 0, y dado que estamos en el estado stanby nos moveremos a goforward,
de esta forma la salida en 8 bits sera 00010101 -> uo_out, los primeros 00 no los ocupamos, el 01 significa 
el estado que estamos (goforward) y los ultimos 0101 son los estados de los motores, en este caso 1010, para
cuando estamos en la derecha, en otras palabras la salida uo_out en decimal es igual a 21, y asi sucesivamente
"""

""" 
parameter Standby = 2'b00;
parameter goforward = 2'b01;
parameter goright = 2'b10;
parameter goleft = 2'b11;

wire f_sensor, l_sensor, r_sensor;

            Standby : begin
                motorB_i = 0;
                motorB_d = 0;
                motorA_i = 0;
                motorA_d = 0;
            end
            goforward: begin
                motorB_i = 0;
                motorB_d = 1;
                motorA_i = 0;
                motorA_d = 1;
            end
            goright: begin
                motorB_i = 1;
                motorB_d = 0;
                motorA_i = 0;
                motorA_d = 1;
            end
            goleft: begin
                motorB_i = 0;
                motorB_d = 1;
                motorA_i = 1;
                motorA_d = 0;
            end

            
ui_in     uo_out(st_next) out decimal  nombre del estado salida
00000000    00010101        21          goforward
00000001    00110110        54          goleft
00000010    00101001        41          goright
00000011    00010101        21          goforward 
00000100    00101001        41          goright
00000101    00110110        54          goleft   
00000110    00101001        41          goright
00000111    00101001        41          goright

falta considerar cualquier otro caso que debiera ser Stanby?*

"""

#salidas esperadas para entrada en el orden de 0,1,2,3,4,5,6,7 en forma decimal
estado_siguiente_esperado = [ 21, 54, 41, 21, 41, 54, 41, 41]

@cocotb.test()
async def test(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0

    # check all segments and roll over
    for i in range(8):
        dut._log.info("revisando salida esperada para entrada {}".format(i))
        dut.ui_in.value = i
        await ClockCycles(dut.clk, 10)
        assert int(dut.uo_out.value) == estado_siguiente_esperado[i]
