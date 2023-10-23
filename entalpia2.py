from thermo.chemical import Chemical
from math import ceil

quimico = Chemical('water',T=273.15, P=1e5)
comp = 2695
temp_f = 85
tsat = 373.15
print(tsat-273.15)
h_liquido_subenfriado = ceil(quimico.HeatCapacityLiquid.T_dependent_property_integral(273.15,273.15+85)/quimico.MW  - quimico.calc_H_excess(T=tsat, P=1e5)/1000) 
quimico.calculate(tsat, P=1e5)
h_liquido_saturado = ceil(quimico.Hvap/1000 - quimico.calc_H_excess(T=tsat, P=1e5)/1000) 
quimico.calculate(273.15+temp_f)
h_vapor_sobrecalentado = ceil(quimico.HeatCapacityGas.T_dependent_property_integral(tsat,273.15+temp_f)/quimico.MW) 
print(tsat)
print(f"Entalpía de líquido subenfriado (0-100 Celsius): {h_liquido_subenfriado} J/g")
# print(f"Entalpía de Vaporización (100 Celsius): {h_liquido_saturado} J/g")
# print(f"Entalpía de Vapor Sobrecalentado (100-200 Celsius): {h_vapor_sobrecalentado} J/g")
dH = ceil(h_liquido_subenfriado)
print((comp-dH)/comp*100)

print(f"Delta H: {dH} J/g")
