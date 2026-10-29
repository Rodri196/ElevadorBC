# SPDX-License-Identifier: Apache-2.0
# Test exhaustivo de los 64 pares (piso actual, piso objetivo).
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer, ClockCycles


async def tick(dut, destination):
    # Se cambian los bits en el flanco de bajada para evitar carreras.
    await FallingEdge(dut.clk)
    dut.ui_in.value = destination
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")


def check_leds(dut, floor, context):
    expected = 1 << floor
    observed = int(dut.uo_out.value)
    assert observed == expected, (
        f"{context}: piso esperado {floor}, LEDs esperado "
        f"0x{expected:02x}, observado 0x{observed:02x}"
    )
    assert int(dut.uio_oe.value) == 0
    assert int(dut.uio_out.value) == 0


@cocotb.test()
async def test_todos_los_estados_y_destinos(dut):
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    for current in range(8):
        for target in range(8):
            # Cada par Q,T se comprueba partiendo de un reset limpio.
            await FallingEdge(dut.clk)
            dut.rst_n.value = 0
            dut.ui_in.value = current
            await ClockCycles(dut.clk, 2)
            await Timer(1, unit="ns")
            check_leds(dut, 0, f"reset Q={current} T={target}")
            await FallingEdge(dut.clk)
            dut.rst_n.value = 1
            for f in range(1, current + 1):
                await RisingEdge(dut.clk)
                await Timer(1, unit="ns")
                check_leds(dut, f, f"preparando Q={current}, T={target}")
                await FallingEdge(dut.clk)
            # En el caso current=0 esperamos un flanco de bajada para configurar T.
            # En los otros casos ya estamos en flanco de bajada.
            if current == 0:
                await FallingEdge(dut.clk)
            check_leds(dut, current, f"estado inicial Q={current}")
            dut.ui_in.value = target
            await RisingEdge(dut.clk)
            await Timer(1, unit="ns")
            expected = current + (target > current) - (target < current)
            check_leds(dut, expected, f"Q={current}, T={target}")

    await FallingEdge(dut.clk)
    dut.rst_n.value = 0
    dut.ui_in.value = 7
    await ClockCycles(dut.clk, 2)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    for piso in range(1, 8):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
        check_leds(dut, piso, "subida S2 -> P5")
    await FallingEdge(dut.clk)
    dut.ui_in.value = 0
    for piso in range(6, -1, -1):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
        check_leds(dut, piso, "bajada P5 -> S2")
