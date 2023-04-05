import warnings

from eco2ai.tools.tools_cpu import CPU
from eco2ai.tools.tools_ram import RAM

warnings.filterwarnings('ignore')

cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)
CO2_CONST = 443.03
ELECTRICITY_CONST = 3.75


def calculate(cpu, ram, start_consumption_cpu, start_consumption_ram):
    val_cpu, val_ram = cpu.get_consumption(), ram.get_consumption()
    cpu_con = val_cpu - start_consumption_cpu
    ram_con = val_ram - start_consumption_ram
    total_con = ram_con + cpu_con
    co2 = total_con * CO2_CONST
    price = total_con * ELECTRICITY_CONST
    return cpu_con * 10000, ram_con * 10000, total_con * 10000, co2, price, val_cpu, val_ram
