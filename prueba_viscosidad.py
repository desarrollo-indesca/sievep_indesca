from thermo.chemical import Chemical
from CoolProp.CoolProp import PropsSI 

agua = Chemical('water', 273.15 + 21.11, 101325 + 2966.12)

print(agua.rho, agua.mu, agua.Psat)

print(PropsSI("D","T",273.15 + 21.11,"P",101325 + 2966.12,"water"))