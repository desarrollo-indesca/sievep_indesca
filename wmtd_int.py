from ht import LMTD, F_LMTD_Fakheri
from thermo.chemical import Chemical

def wtd_caso_tdd(flujo_interes, t1i, t2i, tsi, t1c, cp_interes1, cp_interes2, calor_latente_interes) -> float:
    '''
    Resumen:
        Función para calcular el WTD en el caso de que el intercambiador sea de tipo DD de un lado, TOTAL del otro.
    '''

    calores = [
        cp_interes1*flujo_interes*abs(tsi - t1i),
        calor_latente_interes*flujo_interes,
        cp_interes2*flujo_interes*abs(t2i - tsi)
    ]

    temps_interes = [t1i,tsi,tsi,t2i]
    temps_complementarias = [t1c,t1c,t1c,t1c]

    print(f"Temps. Interés: {temps_interes}")

    qlmtds = []

    for i in range(len(calores)):
        t1,t2,t3,t4 = temps_interes[i],temps_interes[i+1],temps_complementarias[i],temps_complementarias[i+1]
        try:
            lmtd = abs(LMTD(t1,t2,t3,t4)) * F_LMTD_Fakheri(t1,t2,t3,t4)
        except:
            lmtd = abs(LMTD(t1,t2,t3,t4))

        qlmtds.append(calores[i]/lmtd)

    print(f"QLMTDs: {qlmtds}")
    print(f"Suma: {sum(qlmtds)}")
   
    return round(sum(calores)/sum(qlmtds), 3)

def calcular_pendiente(q1,q2,t1,t2):
    return (t2-t1)/(q2-q1)

def wtd_caso_sp(flujo_interes, t1i, t2i, t1c, t2c, cp_interes, calor_latente_interes, cambio_fase, calidad) -> float:
    '''
    Resumen:
        Función para calcular el WTD en el caso de que el intercambiador sea de tipo DL,LD,DV y VD de un lado, y sin cambio de fase en el otro.
    '''

    if(cambio_fase[0] == 'D'):
        calores = [
            calor_latente_interes*flujo_interes*calidad,
            cp_interes*flujo_interes*abs(t2i - t1i)
        ]

        temps_interes = [t1i,t1i,t2i]
    else:
        calores = [
            cp_interes*flujo_interes*abs(t1i - t2i),
            calor_latente_interes*flujo_interes*calidad,
        ]

        temps_interes = [t1i,t2i,t2i]

    pendiente = calcular_pendiente(0,sum(calores),t1c,t2c)
    temps_complementarias = [t1c,t1c + pendiente*calores[0], t2c]
    print(f"Calor: {sum(calores)}")
    print(f"Calores: {calores}")
    print(f"Temps. Interés: {temps_interes}")
    print(f"Temps. Complementarias: {temps_complementarias}")

    qlmtds = []

    for i in range(len(calores)):
        t1,t2,t3,t4 = temps_interes[i],temps_interes[i+1], temps_complementarias[i],temps_complementarias[i+1]
        try:
            lmtd = abs(LMTD(t1,t2,t3,t4)) * F_LMTD_Fakheri(t1,t2,t3,t4)
        except:
            lmtd = abs(LMTD(t1,t2,t3,t4))

        qlmtds.append(calores[i]/lmtd)

    return round(sum(calores)/sum(qlmtds), 3)

def wtd_caso_ts(flujo_interes, t1i, t2i, tsi, t1c, t2c, cp_interes1, cp_interes2, calor_latente_interes) -> float:
    '''
    Resumen:
        Función para calcular el WTD en el caso de que el intercambiador sea de tipo DD de un lado, TOTAL del otro.
    '''

    calores = [
        cp_interes1*flujo_interes*abs(tsi - t1i),
        calor_latente_interes*flujo_interes,
        cp_interes2*flujo_interes*abs(t2i - tsi)
    ]

    temps_interes = [t1i,tsi,tsi,t2i]
    pendiente = calcular_pendiente(0,sum(calores),t1c,t2c)
    temps_complementarias = [t1c,t1c + pendiente*calores[0],t1c + pendiente*sum(calores[:2]),t2c]

    print(f"Temps. Interés: {temps_interes}")
    print(f"Temps. Complementarias: {temps_complementarias}")

    qlmtds = []

    for i in range(len(calores)):
        t1,t2,t3,t4 = temps_interes[i],temps_interes[i+1],temps_complementarias[i],temps_complementarias[i+1]
        try:
            lmtd = abs(LMTD(t1,t2,t3,t4)) * F_LMTD_Fakheri(t1,t2,t3,t4)
        except:
            lmtd = abs(LMTD(t1,t2,t3,t4))

        qlmtds.append(calores[i]/lmtd)
   
    return round(sum(calores)/sum(qlmtds), 3)

# # 186-C
# print(LMTD(46.7,45.8,33.3,40.3) * F_LMTD_Fakheri(46.7,45.8,33.3,40.3))
# print(wtd_caso_ts(198937/3600,46.7,45.8,45.8*1.005,33.3,40.3,2357,2870,Chemical('propylene', 273.15 + 45.8*1.005).Hvap))
# print("-"*10)

# # 143 - C
# print(LMTD(46.7,45.8,33.3,40.3) * F_LMTD_Fakheri(46.7,45.8,33.3,40.3))
# print(wtd_caso_ts(284196/3600,46.7,45.8,45.8*1.005,33.3,40.3,2357,2870,Chemical('propylene', 273.15 + 45.8*1.005).Hvap))
# print("-"*10)

# # 314-C
# print(LMTD(55.6,46,33.3,40.3) * F_LMTD_Fakheri(55.6,46,33.3,40.3))
# print(wtd_caso_ts(285808/3600,55.6,46,47.1,33.3,40.3,2423.5,3205,Chemical('propylene', 273.15 + 46*1.005).Hvap))
# print("-"*10)

# # 181-C
# print("181-C")
# print(LMTD(95.5,40.6,33.3,40.3) * F_LMTD_Fakheri(95.5,40.6,33.3,40.3))
# print(wtd_caso_sp(114311/3600,95.5,40.6,33.3,40.3,(2181+1981)/2,1815604.8588,'LD',0.0122))
# print("-"*10)

# # 182-C
# print("182-C")
# print(LMTD(96.8,40.6,33.3,40.3) * F_LMTD_Fakheri(96.8,40.6,33.3,40.3))
# print(wtd_caso_sp(114311/3600,96.8,40.6,33.3,40.3,2106.5,1529601.3426,'LD',0.00985))
# print("-"*10)

# # 183-C
# print("183-C")
# print(LMTD(66.1,68.2,110.9,74.6) * F_LMTD_Fakheri(66.1,68.2,110.9,74.6))
# print(wtd_caso_sp(593160/3600,66.1,68.2,110.9,74.6,2106.5,260000,'DV',0.35))
# print("-"*10)

# # 193-C
# print("193-C")
# print(LMTD(-40.5,-40.6,-20,-26) * F_LMTD_Fakheri(-40.5,-40.6,-20,-26))
# print(wtd_caso_sp(11615/3600,-40.5,-40.6,-20,-26,1300,432400,'DV',0.9270770555))
# print("-"*10)

# # 196-C
# print("196-C")
# print(LMTD(-40,-40,46.3,-37))
# print(wtd_caso_sp(10040/3600,-40,-40,46.3,-37,1300,438000,'DV',0.88))
# print("-"*10)

# # 203-C
# print("203-C")
# print(LMTD(-0.2,0.9,47.3,41) * F_LMTD_Fakheri(-0.2,0.9,47.3,41))
# print(wtd_caso_sp(75910/3600,-0.2,0.9,47.3,41,4615,224288,'LD',0.50703))
# print("-"*10)

# # 208-C
# print("208-C")
# print(LMTD(98.2,40.5,33.3,40.6) * F_LMTD_Fakheri(98.2,40.5,33.3,40.6))
# print(wtd_caso_sp(113392/3600,98.2,40.5,33.3,40.6,2180,975780,'VD',0.00921))
# print('-'*10)