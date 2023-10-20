from thermo.chemical import Chemical

quimico = Chemical('H2O')

quimico.phase = 'g'

print(quimico.calc_H(T=323.15,P=101325))
print(quimico.Hf)
print(quimico.calc_H(T=323.15,P=101325) + quimico.Hf)