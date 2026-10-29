// SPDX-License-Identifier: Apache-2.0
// Elevador convertido de CircuitVerse (28/10/2026).
// Orden original: S2=0, S1=1, PB=2, P1=3, P2=4, P3=5, P4=6, P5=7.
// El subcircuito Next State calcula un unico paso hacia el destino
// en cada flanco positivo del reloj.
`default_nettype none

module tt_um_porras_elevador_cv (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    // ui_in[2:0] es el destino codificado como {T2,T1,T0}.
    // ui_in[7:3] no se usan, igual que en el proyecto original.
    wire [2:0] destino = ui_in[2:0];

    // Los 3 flip-flops Q2 Q1 Q0 representan el piso actual.
    // S2=000 es el estado que elegimos al activar reset externo.
    reg [2:0] piso_actual;
    reg [2:0] piso_siguiente;

    // Equivalente a las 64 filas del Next State del .cv:
    // Q < T -> Q + 1; Q > T -> Q - 1; Q == T -> Q.
    always @* begin
        piso_siguiente = piso_actual;
        if (piso_actual < destino)
            piso_siguiente = piso_actual + 3'd1;
        else if (piso_actual > destino)
            piso_siguiente = piso_actual - 3'd1;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            piso_actual <= 3'd0;
        else
            piso_actual <= piso_siguiente;
    end

    // Decoder 3 a 8, mismo cableado y orden que el .cv original:
    // uo_out[0]=S2, [1]=S1, [2]=PB, [3]=P1,
    // [4]=P2, [5]=P3, [6]=P4, [7]=P5.
    assign uo_out = (8'b0000_0001 << piso_actual);

    // Pines bidireccionales no utilizados: todos en modo entrada.
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;
    wire _unused = &{ena, uio_in, ui_in[7:3], 1'b0};
endmodule

`default_nettype wire
