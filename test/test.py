# SPDX-License-Identifier: Apache-2.0
# Comprobacion con reloj controlado manualmente para evitar carreras de simulacion.
import cocotb
from cocotb.triggers import Timer


async def settle(ns=100):
    await Timer(ns, unit="ns")


async def pulse(dut):
    # Poner los datos estables antes del flanco activo, incluso en gate-level.
    dut.clk.value = 0
    await settle()
    dut.clk.value = 1
    await settle()


def check_leds(dut, floor, message):
    observed = int(dut.uo_out.value)
    expected = 1 << floor
    assert observed == expected, (
        f"{message}: se esperaba piso {floor}, LEDs 0x{expected:02x}, "
        f"pero se obtuvo 0x{observed:02x}"
    )
    assert int(dut.uio_out.value) == 0
    assert int(dut.uio_oe.value) == 0


async def reset_to_s2(dut):
    dut.clk.value = 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    await settle()
    await pulse(dut)
    check_leds(dut, 0, "Durante reset")
    dut.clk.value = 0
    await settle()
    dut.rst_n.value = 1
    await settle()


@cocotb.test()
async def test_todos_los_estados_y_destinos(dut):
    dut.ena.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0
    dut.clk.value = 0
    dut.rst_n.value = 0
    await settle()

    for current in range(8):
        for target in range(8):
            await reset_to_s2(dut)

            # Colocar el elevador en el piso Q actual avanzando desde S2.
            dut.ui_in.value = current
            for floor in range(1, current + 1):
                await pulse(dut)
                check_leds(dut, floor, f"Preparando Q={current}, T={target}")
            check_leds(dut, current, f"Estado inicial Q={current}")

            # Ordenar T; cada pulso debe cambiar el piso a lo sumo en uno.
            dut.ui_in.value = target
            await pulse(dut)
            next_floor = current + (target > current) - (target < current)
            check_leds(dut, next_floor, f"Q={current}, T={target}")

    # Recorrido completo de S2 (000) a P5 (111) y de regreso.
    await reset_to_s2(dut)
    dut.ui_in.value = 7
    for floor in range(1, 8):
        await pulse(dut)
        check_leds(dut, floor, "Subiendo S2 a P5")
    dut.ui_in.value = 0
    for floor in range(6, -1, -1):
        await pulse(dut)
        check_leds(dut, floor, "Bajando P5 a S2")
