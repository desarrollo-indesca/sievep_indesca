# Cambio parcial y total: se escoge el total
from thermo import Chemical
from ht import LMTD, F_LMTD_Fakheri

cp_carcasa_gas = 2423.5
cp_tubo_gas = 0
cp_carcasa_liquido = 3205
cp_tubo_liquido = 0
calor_latente_tubo = 282000 
flujo_carcasa = 79.3911111
flujo_tubo = 0

t1c = 55.6
t2c = 46
tsc = 46

t1t = 33.3
t2t = 40.3

qs = []
temps_carcasa = [t1c]
temps_tubo = [t1t]

q1 = cp_carcasa_gas*abs(t1c-tsc)*flujo_carcasa

qs.append(q1)
temps_carcasa.append(tsc)
temps_tubo.append(52.4)

q2 = calor_latente_tubo*flujo_carcasa
qs.append(q2)
temps_carcasa.append(tsc)
temps_tubo.append(49.2)

lmtds = [
    abs(LMTD(temps_carcasa[0], temps_carcasa[1], temps_tubo[0], temps_tubo[1])),
    abs(LMTD(temps_carcasa[1], temps_carcasa[2], temps_tubo[1], temps_tubo[2])),
] # C

qlmtds = []
for i in range(len(lmtds)):
    q = qs[i]
    lmtd = lmtds[i]
    qlmtds.append(q/lmtd)

wmtd = 1/(sum(qlmtds)/(q1+q2))

print(temps_carcasa)
print(temps_tubo)
print(qs)
print(lmtds)
print(qlmtds)
print(wmtd)