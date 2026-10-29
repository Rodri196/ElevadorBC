# Elevador de ocho niveles

## How it works

Proyecto convertido desde la exportacion original `.cv` de CircuitVerse del
28 de octubre de 2026. La arquitectura original contiene tres flip-flops
`Q2/Q1/Q0`, un bloque combinacional `Next State` de seis entradas y tres
salidas, y un decoder 3 a 8 para indicar el piso actual.

Al llegar un flanco positivo de `clk`, el elevador recorre exactamente UN
nivel hacia el destino. Si ya esta en ese nivel, permanece alli. El destino
se lee continuamente; si cambia durante el movimiento, el elevador redirige
su siguiente paso. No hay memoria de solicitudes multiples ni tiempos de
espera: reproduce la logica del proyecto original, no un controlador fisico.

El reset externo `rst_n` es activo bajo y lleva al piso S2 (000). Esta
entrada se agrego para que un chip real arranque con estado conocido; en
CircuitVerse las basculas podian iniciar con valores impuestos por simulacion.

| Codigo (T2 T1 T0) | Piso | Luz de salida |
|---|---|---|
| 000 | S2 | uo_out[0] |
| 001 | S1 | uo_out[1] |
| 010 | PB | uo_out[2] |
| 011 | P1 | uo_out[3] |
| 100 | P2 | uo_out[4] |
| 101 | P3 | uo_out[5] |
| 110 | P4 | uo_out[6] |
| 111 | P5 | uo_out[7] |

## How to test

- Establezca `rst_n = 0`: LED S2 debe quedar encendido.
- Establezca `rst_n = 1` y `ui_in[2:0] = 3'b100` (P2).
- Pulse `clk` cuatro veces: S1, PB, P1 y finalmente P2.
- Vuelva a `ui_in[2:0] = 3'b000` y pulse cuatro veces: P1, PB, S1, S2.
- Con `ui_in[2:0] = Q actual`, los pulsos adicionales no cambian el piso.
- El test `test/test.py` prueba los 64 pares Q/T y las salidas one-hot.

## External hardware

Requiere un reloj externo para avanzar. Con 1 Hz se observa un piso por
segundo. No conecte botones mecanicos directamente como reloj sin
eliminar rebotes (debounce). Las salidas logicas necesitan conexiones
apropiadas y resistencias/driver para LEDs fisicos. El chip no maneja
motores ni cargas de potencia.
