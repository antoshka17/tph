from eco2ai.tools.tools_cpu import CPU
from eco2ai.tools.tools_ram import RAM
import warnings
warnings.filterwarnings('ignore')

cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)

def calculate(cpu, ram, start_consumption_cpu, start_consumption_ram):
    val_cpu, val_ram = cpu.get_consumption(), ram.get_consumption()
    cpu_con = val_cpu - start_consumption_cpu
    ram_con = val_ram - start_consumption_ram
    total_con = ram_con + cpu_con
    return cpu_con*1000000, ram_con*1000000, total_con*1000000, val_cpu, val_ram
