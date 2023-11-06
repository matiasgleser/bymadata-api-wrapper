"""
    bymadata_api_wrapper._enums

    Defines all API parameter enumerations
"""
from enum import Enum, unique


"""
Equity
"""

@unique
class EquityGroupEnum(Enum):
	Acciones = "ACCIONES"
	Cedears = "CEDEARS"
	FondosInversion = "FONDOSINVERSION"

@unique
class EquitySubGroupEnum(Enum):
	General = "GENERAL"
	Lider = "LIDER"

@unique
class EquityOperativeFormEnum(Enum):
	Contado = "CONTADO"
	Gris = "GRIS"

@unique
class EquityCurrencyEnum(Enum):
	Ars = "ARS"
	Usd = "USD"
	Ext = "EXT"

@unique
class EquitySettlPeriodEnum(Enum):
	Zero = "0000"
	One = "0001"
	Two = "0002"
	Three = "0003"

class EquityParameters:
	
	Required = {
		"group" : EquityGroupEnum,
		"operative_form" : EquityOperativeFormEnum
	}

	NotRequired = {
		"subgroup" : EquitySubGroupEnum,
		"currency" : EquityCurrencyEnum,
		"settle_period" : EquitySettlPeriodEnum
	}


"""
Fixed Income
"""

@unique
class FixedIncomeGroupEnum(Enum):
	TitulosPublicos = "TITULOSPUBLICOS"
	BonosConsolidacion = "BONOSCONSOLIDACION"
	Letras = "LETRAS"
	LetrasTesoro = "LETRASTESORO"
	TitulosDeuda = "TITULOSDEUDA"
	CertificadosParticipacion = "CERTPARTICIPACION"
	ObligacionesNegociables = "OBLIGACIONESNEGOC"
	ObligacionesNegociablesPYME = "ONPYMES"

@unique
class FixedIncomeMarketEnum(Enum):
	Ppt = "PPT"
	Senebi = "SENEBI"

@unique
class FixedIncomeOperativeFormEnum(Enum):
	Contado = "CONTADO"
	Gris = "GRIS"

@unique
class FixedIncomeCurrencyEnum(Enum):
	Ars = "ARS"
	Usd = "USD"
	Ext = "EXT"

@unique
class FixedIncomeSettlPeriodEnum(Enum):
	Zero = "0000"
	One = "0001"
	Two = "0002"
	Three = "0003"


class FixedIncomeParameters:
	
	Required = {
		"group" : FixedIncomeGroupEnum,
		"market" : FixedIncomeMarketEnum,
		"operative_form" : FixedIncomeOperativeFormEnum
	}

	NotRequired = {
		"currency" : FixedIncomeCurrencyEnum,
		"settle_period" : FixedIncomeSettlPeriodEnum
	}


"""
Futures
"""

@unique
class FuturesGroupEnum(Enum):
	FuturosMoneda = "FUTMONEDAS"
	FuturosIndiceTitulos = "FUTINDyTIT"

class FuturesParameters:
	
	Required = {
		"group" : FuturesGroupEnum
	}


"""
Options
"""

@unique
class OptionsGroupEnum(Enum):
	Opciones = "OPCIONES"

@unique
class OptionsCurrencyEnum(Enum):
	Ars = "ARS"
	Usd = "USD"
	Ext = "EXT"


class OptionsParameters:

	Required = {
		"group" : OptionsGroupEnum,
		"currency" : OptionsCurrencyEnum
	}


"""
Collateralized Repos
"""

@unique
class ReposGroupEnum(Enum):
	Cauciones = "CAUCIONES"


class ReposParameters:

	Required = {
		"group" : ReposGroupEnum
	}


"""
Trading Lots
"""

@unique
class TradingLotsGroupEnum(Enum):
	PlazoPorLotes = "PXL"

@unique
class TradingLotsCurrencyEnum(Enum):
	Ars = "ARS"
	Usd = "USD"
	Ext = "EXT"


class TradingLotsParameters:

	Required = {
		"group" : TradingLotsGroupEnum,
		"currency" : TradingLotsCurrencyEnum
	}


"""
Loans
"""

@unique
class LoansGroupEnum(Enum):
	VentaDescubierto : "PRESTAMOSV"
	FallaLiquidacion : "PRESTAMOSL"


@unique
class LoansCurrencyEnum(Enum):
	Ars = "ARS"
	Usd = "USD"
	Ext = "EXT"


class LoansParameters:

	Required = {
		"group" : LoansGroupEnum,
		"currency" : LoansCurrencyEnum
	}

