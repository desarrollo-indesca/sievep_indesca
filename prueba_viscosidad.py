from thermo.chemical import Chemical
from thermo import VolumeLiquid
from CoolProp.CoolProp import PropsSI 


print(PropsSI("V","T",407.3888888888888888888888888888888888889,"P",565370,"water"))
print(PropsSI("D","T",407.3888888888888888888888888888888888889,"P",565370,"water"))

quimico = Chemical('water', 407.3888888888888888888888888888888888889, 565370)
print(quimico.mul)
print(quimico.rhol)