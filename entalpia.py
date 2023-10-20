from thermo import ChemicalConstantsPackage, PRMIX, CEOSLiquid, CEOSGas, FlashPureVLS, EquilibriumState
from thermo.heat_capacity import POLING_POLY, HeatCapacityGas, HeatCapacityLiquid
CpObj = HeatCapacityGas('64-17-5')
CpObj.method = POLING_POLY
HeatCapacityGases = [CpObj]
constants, correlations = ChemicalConstantsPackage.from_IDs(['64-17-5'])
print(constants)
print("="*10)
print(correlations.__dict__)

eos_kwargs = dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas)
liquid = CEOSLiquid(PRMIX, HeatCapacityGases=HeatCapacityGases, eos_kwargs=eos_kwargs)
gas = CEOSGas(PRMIX, HeatCapacityGases=HeatCapacityGases, eos_kwargs=eos_kwargs)

flasher = FlashPureVLS(constants, correlations, gas=gas, liquids=[liquid], solids=[])
res = flasher.flash(T=298.15,P=101325)
res2 = flasher.flash(T=273.15+78.5,P=101325)

print(res.H_mass()/1000)
print(res2.H_mass()/1000)
print(abs(res.H_mass()-res2.H_mass())/1000)