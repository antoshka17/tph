from eco2ai.tools.tools_cpu import CPU
from eco2ai.tools.tools_ram import RAM
import warnings
warnings.filterwarnings('ignore')

cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)


def calculate(cpu, ram):
    cpu_con = cpu.get_consumption()
    ram_con = ram.get_consumption()
    total_con = ram_con + cpu_con
    return cpu_con, ram_con, total_con
