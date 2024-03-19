from thermo.chemical import Chemical
from thermo import VolumeLiquid
from CoolProp.CoolProp import PropsSI 


print(PropsSI("V","T",409.261,"P",243380,"water"))
print(PropsSI("D","T",409.261,"P",243380,"water"))

quimico = Chemical('water', 409.261, 243380)
print(quimico.mul)
print(quimico.rhol)