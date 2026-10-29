# Como llevar tu elevador de CircuitVerse a Tiny Tapeout

**Este ZIP es para COPIAR SUS ARCHIVOS ENCIMA de una plantilla oficial, no
es una plantilla completa** (no trae los GitHub Actions originales).

1. Abre https://github.com/TinyTapeout/ttsky-verilog-template
2. Presiona **Use this template** -> **Create a new repository**.
3. Dentro de tu repositorio, sube las rutas de este ZIP respetando las carpetas:
   - `src/project.v`
   - `info.yaml`
   - `docs/info.md`
   - `test/test.py`
   - `test/tb.v`
   - `test/Makefile`
   Puedes conservar `tools/verificar_next_state.py` y `referencia/original.cv`.
4. Cambia el nombre de autor en `info.yaml` por tu nombre.
5. Recomendado: renombra el módulo `tt_um_elevador_cv` en **los tres** lugares:
   `src/project.v`, `info.yaml` (`top_module`) y `test/tb.v`.
   Debe empezar con `tt_um_` y ser único, por ejemplo `tt_um_TUUSUARIO_elevador`.
6. Verifica que GitHub **Actions** pase los tests y el flujo de GDS.
7. Cuando todo esté correcto, usa el portal de Tiny Tapeout para registrar y enviar
   tu repositorio a un shuttle abierto; construir el GDS NO equivale a fabricar el chip.

## Uso de entradas y salidas
- `ui_in[2:0]`: destino binario, en orden T2 T1 T0.
- `ui_in[7:3]`: sin uso.
- `clk`: 1 flanco positivo = un piso (necesitaras reloj externo lento para observarlo).
- `rst_n`: activo bajo. Lleva a S2.
- `uo_out[0..7]`: luces S2,S1,PB,P1,P2,P3,P4,P5.
- No hay control de motor, protecciones de puerta ni sensores fisicos.

## Que se verifico
Se interpreto el netlist de compuertas del subcircuito `Next State` del
archivo original y se enumeraron 64 combinaciones Q/T. Todas coinciden con
`Q+1` si T>Q; `Q-1` si T<Q; `Q` si T=Q.
La nueva version usa comparadores HDL equivalentes, con reset externo adicional.
Se agrego un test Cocotb, pero requiere ejecutarlo con Icarus/Cocotb o GitHub
Actions; el archivo ZIP por si solo NO prueba la sintesis fisica ni el silicio.
