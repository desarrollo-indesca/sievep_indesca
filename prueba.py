from thermo.chemical import Chemical

quimico = Chemical('propylene')

quimico.calculate(P=10.77e5)
print(quimico.Tsat(10.77e5) - 273.15)