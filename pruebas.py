
import ht

# Define the temperatures
T1 = 70
T2 = 120
T3 = 240
T4 = 120

# Calculate the LMTD
LMTD = ht.LMTD(T3,T4,T1,T2)

# Calculate the correction factor
correction_factor = ht.F_LMTD_Fakheri(T3, T4, T1, T2,1)

# Print the results
print("LMTD:", LMTD)
print("Correction factor:", correction_factor)
