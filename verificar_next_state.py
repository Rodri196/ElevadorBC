# Verifica que los 64 resultados esperados de la tabla extraida de .cv
# coincidan con la expresion aritmetica usada en el RTL.
import json
from pathlib import Path
p = Path(__file__).with_name("tabla_verdad_extraida.json")
data = json.loads(p.read_text())
for q in range(8):
    for t in range(8):
        esperado = data['N_por_Q_T'][q][t]
        calculado = q + (t > q) - (t < q)
        assert esperado == calculado, (q,t,esperado,calculado)
        assert 0 <= calculado <= 7
        assert 1 << calculado in [1 << i for i in range(8)]
print("OK: los 64 pares Q/T coinciden con Next State del CV")
