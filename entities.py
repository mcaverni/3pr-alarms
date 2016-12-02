from excel import *

xml_file_template = """<?xml version="1.0" encoding="UTF-8" ?>\n<ALARMS>%s\n</ALARMS>"""

xml_alarm_template = """
  <ALARM>
    <ID>%(identifier)s</ID>
    <NAME>%(name)s</NAME>
    <DESCRIPTION>%(description)s</DESCRIPTION>
    <HELP>%(help)s</HELP>
    <GROUP>%(group)s</GROUP>
    <CONDITION>%(condition)s</CONDITION>
    <TYPE>%(what)s</TYPE>
    <RESET>%(reset)s</RESET>
    <REGTYPE>%(regtype)s</REGTYPE>
    <PAGE>%(page)s</PAGE>
  </ALARM>"""


class Alarm:
    def XML(self, lang):
        # applies all methods on class' attributes
        # so, if a sublcass wants to modify the behavior
        # it will take effect here
        self.identifier = self.get_identifier()
        self.name = self.get_name(lang)
        self.description = self.get_description(lang)
        self.help = self.get_help(lang)
        self.group = self.get_group()
        self.condition = self.get_condition()
        self.what = self.get_what()
        self.reset = self.get_reset()
        self.regtype = self.get_regtype()
        self.page = self.get_page()
        # return the complete XML calling class' methods
        return xml_alarm_template % self.__dict__

    def get_identifier(self):
        return self.identifier

    def get_name(self, lang):
        return value_at(self.name_row, lang)

    def get_description(self, lang):
        return value_at(self.desc_row, lang)

    def get_help(self, lang):
        return value_at(self.help_row, lang)

    def get_group(self):
        return self.group

    def get_condition(self):
        return self.condition

    def get_what(self):
        return self.what

    def get_reset(self):
        return self.reset

    def get_regtype(self):
        return self.regtype

    def get_page(self):
        return self.page


# =================
# GENERIC
# =================
class NonserialAlarm(Alarm):
    def __init__(self, ident, name, desc, help, group, reset, what, page, cond, regtype='COIL'):
        self.identifier = ident
        # from translation file...
        self.name_row = name
        self.desc_row = desc
        self.help_row = help
        # ........................
        self.group = group
        self.condition = cond
        self.what = what
        self.reset = reset
        self.regtype = regtype
        self.page = page


# =================
# ECODRY
# =================
class RowAlarm(Alarm):
    def __init__(self, row, fan=-1):
        self.row = row
        self.fan = fan  # only if used...
        self.group = "ECODRY ROW %d" % row
        self.condition = 'LOGIC'
        self.reset = 'AUTO'  # most of the cases

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(row=self.row, fan=self.fan)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(row=self.row, fan=self.fan)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(row=self.row, fan=self.fan)


class Row3PRComAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_COM" % (row + 8)
        self.name_row = 32
        self.desc_row = 33
        self.help_row = 34
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.regtype = 'COIL'


class RowTB9ComAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_COM" % (row + 8)
        self.name_row = 29
        self.desc_row = 30
        self.help_row = 31
        self.what = 'WARNING'
        self.page = '_none_'
        self.regtype = 'COIL'


class RowSerialComAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "E%02d_COM" % (row + 8)
        self.name_row = 35
        self.desc_row = 36
        self.help_row = 37
        self.what = 'WARNING'
        self.page = '_none_'
        self.regtype = 'HOLDING_REGISTER'


class RowFanBreakerAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_BRK" % (row + 8)
        self.name_row = 38
        self.desc_row = 39
        self.help_row = 40
        self.what = 'WARNING'
        self.page = '_none_'
        self.regtype = 'COIL'


class RowFanErrorAlarm(RowAlarm):
    def __init__(self, row, fan):
        RowAlarm.__init__(self, row, fan)
        self.identifier = "W%02d_SL%d" % (row + 8, fan - 1)
        self.name_row = 41
        self.desc_row = 42
        self.help_row = -1
        self.what = 'WARNING'
        self.page = '_none_'
        self.regtype = 'HOLDING_REGISTER'

    def get_help(self, lang):
        return "_autogenerated_"


class RowHighTSEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_TSE" % (row + 8)
        self.name_row = 43
        self.desc_row = 44
        self.help_row = 45
        self.what = 'WARNING'
        self.page = '_none_'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowTAEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_TAE" % (row + 8)
        self.name_row = 46
        self.desc_row = 47
        self.help_row = 48
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowTSEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_TSE" % (row + 8)
        self.name_row = 49
        self.desc_row = 50
        self.help_row = 51
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowTREAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_TRE" % (row + 8)
        self.name_row = 52
        self.desc_row = 53
        self.help_row = 54
        self.what = 'WARNING'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowPINEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_PIE" % (row + 8)
        self.name_row = 55
        self.desc_row = 56
        self.help_row = 57
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'


class RowPOUTEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_POE" % (row + 8)
        self.name_row = 58
        self.desc_row = 59
        self.help_row = 60
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'


class RowLTEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_LTE" % (row + 8)
        self.name_row = 61
        self.desc_row = 62
        self.help_row = 63
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowPSEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_PSE" % (row + 8)
        self.name_row = 64
        self.desc_row = 65
        self.help_row = 66
        self.what = 'ALARM'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowPBE1Alarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_PB1" % (row + 8)
        self.name_row = 67
        self.desc_row = 68
        self.help_row = 69
        self.what = 'WARNING'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowPBE2Alarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_PB2" % (row + 8)
        self.name_row = 70
        self.desc_row = 71
        self.help_row = 72
        self.what = 'WARNING'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowPBE3Alarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_PB3" % (row + 8)
        self.name_row = 73
        self.desc_row = 74
        self.help_row = 75
        self.what = 'WARNING'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowPAEAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "W%02d_PAE" % (row + 8)
        self.name_row = 76
        self.desc_row = 77
        self.help_row = 78
        self.what = 'WARNING'
        self.page = 'ecodry_pid.qml'
        self.condition = 'PROBE'
        self.regtype = 'COIL'


class RowBWRAlarm(RowAlarm):
    def __init__(self, row):
        RowAlarm.__init__(self, row)
        self.identifier = "A%02d_PMP" % (row + 8)
        self.name_row = 79
        self.desc_row = 80
        self.help_row = 81
        self.what = 'ALARM'
        self.page = 'ecodry_spray_page.qml'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'


# =================
# SDP PUMPS
# =================
class SDPumpAlarm(Alarm):
    def __init__(self, pump):
        self.pump = pump
        self.identifier = "A05_PP%d" % (pump)
        self.name_row = 193
        self.desc_row = 194
        self.help_row = 195
        self.what = 'ALARM'
        self.condition = 'DIGITAL'
        self.group = 'CIRCUIT SDP'
        self.page = 'ecodry_selfdrain_page.qml'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(pump=self.pump)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(pump=self.pump)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(pump=self.pump)


# =================
# CM from PLC
# =================
class PLCCMAlarm(Alarm):
    def __init__(self, module):
        self.module = module
        self.identifier = "PLC_CM%d" % (module)
        self.name_row = 257
        self.desc_row = 258
        self.help_row = 259
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.group = 'PLC'
        self.page = '_none_'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(module=self.module)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(module=self.module)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(module=self.module)


# =================
# AUXILIARY P/T
# =================
class TAUXAlarm(Alarm):
    def __init__(self, slave):
        self.identifier = "A%02d_TAX" % (slave)
        self.name_row = 263
        self.desc_row = 264
        self.help_row = 265
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.group = 'AUXILIARY'
        self.page = 'aux_page.qml'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'
        if slave == 1:
            self.tb9 = "CIRCUIT A"
        elif slave == 2:
            self.tb9 = "CIRCUIT B"
        elif slave == 3:
            self.tb9 = "CIRCUIT C"
        elif slave == 7:
            self.tb9 = "CENTRAL CHILLER"
        else:
            self.tb9 = "[wrong TB9]"

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(tb9=self.tb9)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(tb9=self.tb9)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(tb9=self.tb9)


class PAUXAlarm(Alarm):
    def __init__(self, slave):
        self.identifier = "A%02d_PAX" % (slave)
        self.name_row = 263
        self.desc_row = 264
        self.help_row = 265
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.group = 'AUXILIARY'
        self.page = 'aux_page.qml'
        self.reset = 'MANUAL'
        self.regtype = 'COIL'
        if slave == 1:
            self.tb9 = "CIRCUIT A"
        elif slave == 2:
            self.tb9 = "CIRCUIT B"
        elif slave == 3:
            self.tb9 = "CIRCUIT C"
        elif slave == 7:
            self.tb9 = "CENTRAL CHILLER"
        else:
            self.tb9 = "[wrong TB9]"

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(tb9=self.tb9)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(tb9=self.tb9)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(tb9=self.tb9)


# =================
# CIRCUITS
# =================
class CircuitAlarm(Alarm):
    def __init__(self, circuit, pump=-1):
        self.circuit = circuit
        self.pump = pump
        self.group = 'CIRCUIT %c' % circuit
        self.page = 'circuit_%c_page.qml' % circuit

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(circuit=self.circuit, pump=self.pump)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(circuit=self.circuit, pump=self.pump)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(circuit=self.circuit, pump=self.pump)

    def get_number(self):
        if self.circuit == 'A':
            return 1
        elif self.circuit == 'B':
            return 2
        elif self.circuit == 'C':
            return 3
        elif self.circuit == 'D':
            return 4


class Circuit3PRComAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_COM" % self.get_number()
        self.name_row = 82
        self.desc_row = 83
        self.help_row = 84
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.page = '_none_'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitTB9ComAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_COM" % self.get_number()
        self.name_row = 85
        self.desc_row = 86
        self.help_row = 87
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.page = '_none_'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitSerialComAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "E%02d_COM" % self.get_number()
        self.name_row = 88
        self.desc_row = 89
        self.help_row = 90
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.page = '_none_'
        self.regtype = 'HOLDING_REGISTER'
        self.reset = 'AUTO'


class WaterOnAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_LWL" % self.get_number()
        self.name_row = 91
        self.desc_row = 92
        self.help_row = 93
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class WaterOffAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_LWS" % self.get_number()
        self.name_row = 94
        self.desc_row = 95
        self.help_row = 96
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class WaterResetAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_LWR" % self.get_number()
        self.name_row = 97
        self.desc_row = 98
        self.help_row = 99
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitRefillAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_REF" % self.get_number()
        self.name_row = 100
        self.desc_row = 101
        self.help_row = 102
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitHTSAAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_TSA" % self.get_number()
        self.name_row = 103
        self.desc_row = 104
        self.help_row = 105
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitPumpsDeltaPWAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_LPD" % self.get_number()
        self.name_row = 106
        self.desc_row = 107
        self.help_row = 108
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitPumpsDeltaPAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_LPD" % self.get_number()
        self.name_row = 109
        self.desc_row = 110
        self.help_row = 111
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitPumpsHPSAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_HPS" % self.get_number()
        self.name_row = 112
        self.desc_row = 113
        self.help_row = 114
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitFilterDropWAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_FPD" % self.get_number()
        self.name_row = 115
        self.desc_row = 116
        self.help_row = 117
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitFilterDropAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_FPD" % self.get_number()
        self.name_row = 118
        self.desc_row = 119
        self.help_row = 120
        self.what = 'ALARM'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitPumpServAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_PSR" % self.get_number()
        self.name_row = 121
        self.desc_row = 122
        self.help_row = 123
        self.what = 'WARNING'
        self.condition = 'LOGIC'
        self.regtype = 'COIL'
        self.reset = 'PASSWORD'


class CircuitTSAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_TS%c" % (self.get_number(), self.circuit)
        self.name_row = 124
        self.desc_row = 125
        self.help_row = 126
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitTRAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "W%02d_TR%c" % (self.get_number(), self.circuit)
        self.name_row = 127
        self.desc_row = 128
        self.help_row = 129
        self.what = 'WARNING'
        self.condition = 'PROBE'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitPSAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_PS%c" % (self.get_number(), self.circuit)
        self.name_row = 130
        self.desc_row = 131
        self.help_row = 132
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitLTAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_LT%c" % (self.get_number(), self.circuit)
        self.name_row = 133
        self.desc_row = 134
        self.help_row = 135
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitFINAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_FI%c" % (self.get_number(), self.circuit)
        self.name_row = 136
        self.desc_row = 137
        self.help_row = 138
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitFOUTAlarm(CircuitAlarm):
    def __init__(self, circuit):
        CircuitAlarm.__init__(self, circuit)
        self.identifier = "A%02d_FO%c" % (self.get_number(), self.circuit)
        self.name_row = 139
        self.desc_row = 140
        self.help_row = 141
        self.what = 'ALARM'
        self.condition = 'PROBE'
        self.regtype = 'COIL'
        self.reset = 'MANUAL'


class CircuitONOFFAlarm(CircuitAlarm):
    def __init__(self, circuit, pump):
        CircuitAlarm.__init__(self, circuit, pump)
        self.identifier = "A%02d_PP%d" % (self.get_number(), self.pump)
        self.name_row = 142
        self.desc_row = 143
        self.help_row = 144
        self.what = 'ALARM'
        self.condition = 'DIGITAL'
        self.regtype = 'COIL'
        self.reset = 'AUTO'


class CircuitVFDAlarm(CircuitAlarm):
    def __init__(self, circuit, pump, number):
        CircuitAlarm.__init__(self, circuit, pump)
        self.identifier = "A%02d_G%d%d" % (self.get_number(), self.pump, number)
        self.name_row = 145
        self.desc_row = 146
        self.help_row = -1
        self.what = 'ALARM'
        self.condition = 'DIGITAL'
        self.regtype = 'HOLDING_REGISTER'
        self.reset = 'MANUAL'

    def get_help(self, lang):
        return "_autogenerated_"


class CircuitVFDWarning(CircuitAlarm):
    def __init__(self, circuit, pump, number):
        CircuitAlarm.__init__(self, circuit, pump)
        self.identifier = "W%02d_G%d%d" % (self.get_number(), self.pump, number)
        self.name_row = 145
        self.desc_row = 147
        self.help_row = -1
        self.what = 'WARNING'
        self.condition = 'DIGITAL'
        self.regtype = 'HOLDING_REGISTER'
        self.reset = 'MANUAL'

    def get_help(self, lang):
        return "_autogenerated_"


# =================
# CENTRAL CHILLER
# =================	
class ChillerDigitalAlarm(Alarm):
    def __init__(self, chiller):
        self.chiller = chiller
        self.name_row = 217
        self.desc_row = 218
        self.help_row = 219
        self.condition = 'DIGITAL'
        self.group = 'CENTRAL CHILLER'
        self.page = 'home_page.qml'
        self.what = 'ALARM'
        self.reset = 'AUTO'
        self.regtype = 'COIL'
        self.identifier = "A07_DC%d" % (self.chiller)

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(chiller=self.chiller)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(chiller=self.chiller)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(chiller=self.chiller)


class ChillerAlarm(Alarm):
    def __init__(self, chiller, alarm):
        self.alarm = alarm
        self.chiller = chiller
        self.name_row = 220
        self.desc_row = 221
        self.help_row = -1
        self.condition = 'DIGITAL'
        self.group = 'CENTRAL CHILLER'
        self.page = 'chiller_pid.qml'
        self.what = 'ALARM'
        self.reset = 'AUTO'
        self.regtype = 'HOLDING_REGISTER'
        self.identifier = "A07_C%d%d" % (self.chiller, self.alarm)

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(chiller=self.chiller)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(chiller=self.chiller, alarm=self.alarm)

    def get_help(self, lang):
        return "_autogenerated_"


# =================
# MULTISTAGE
# =================
class MultistageAlarm(Alarm):
    def __init__(self, chiller, alarm):
        self.alarm = alarm
        self.chiller = chiller
        self.name_row = 255
        self.desc_row = 256
        self.help_row = -1
        self.condition = 'DIGITAL'
        self.group = 'MULTISTAGE'
        self.page = 'multistage_pid.qml'
        self.what = 'ALARM'
        self.reset = 'AUTO'
        self.regtype = 'HOLDING_REGISTER'
        self.identifier = "A08_C%d%d" % (self.chiller, self.alarm)

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(chiller=self.chiller)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(chiller=self.chiller, alarm=self.alarm)

    def get_help(self, lang):
        return "_autogenerated_"


# =================
# FLOWMETER
# =================
class FlowmeterAlarm(Alarm):
    def __init__(self, slave):
        self.identifier = "A0%d_FMT" % slave
        if slave == 1:
            self.page = 'circuit_a_page.qml'
            self.group = 'CIRCUIT A'
            self.shortname = "A"
        elif slave == 2:
            self.page = 'circuit_b_page.qml'
            self.group = 'CIRCUIT B'
            self.shortname = "B"
        elif slave == 3:
            self.page = 'circuit_c_page.qml'
            self.group = 'CIRCUIT C'
            self.shortname = "C"
        elif slave == 4:
            self.page = 'circuit_d_page.qml'
            self.group = 'CIRCUIT D'
            self.shortname = "D"
        elif slave == 8:
            self.page = 'circuit_d_page.qml'
            self.group = 'MULTISTAGE'
            self.shortname = "M"
        self.condition = 'PROBE'
        self.reset = 'AUTO'
        self.regtype = 'COIL'
        self.what = 'ALARM'
        self.name_row = 269
        self.desc_row = 270
        self.help_row = 271

    def get_name(self, lang):
        return value_at(self.name_row, lang).format(slave=self.shortname)

    def get_description(self, lang):
        return value_at(self.desc_row, lang).format(slave=self.shortname)

    def get_help(self, lang):
        return value_at(self.help_row, lang).format(group=self.group)


# =================
# RCS
# =================
class RCSAlarm(Alarm):
    def __init__(self, ident_number, name, desc, help, group='GENERAL', reset='MANUAL', what='WARNING', page='_none_',
                 cond='LOGIC', regtype='NULL'):


        self.identifier = "1:alarm:%d" % (ident_number)
        self.name_row = name
        self.desc_row = desc
        self.help_row = help
        # ........................
        self.group = group
        self.condition = cond
        self.what = what
        self.reset = reset
        self.page = page
        self.regtype = regtype


class RCSAlarmProbe(Alarm):
    def __init__(self, number,  starting_ident_number, name, desc, help, group='GENERAL', reset='MANUAL', what='WARNING', page='_none_',
                 cond='LOGIC', regtype='NULL'):

        self.number = number
        self.identifier = "1:alarm:%d" % (self.number+starting_ident_number)
        self.name_row = name
        self.desc_row = desc
        self.help_row = help
        # ........................
        self.group = group
        self.condition = cond
        self.what = what
        self.reset = reset
        self.page = page
        self.regtype = regtype

    def get_name(self, lang):
        return value_at(self.name_row, lang).replace("(row)", str(self.number))

    def get_description(self, lang):
        return value_at(self.desc_row, lang).replace("(row)", str(self.number))

    def get_help(self, lang):
        return value_at(self.help_row, lang).replace("(row)", str(self.number))