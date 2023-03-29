from database import *
from server import *
import warnings
from eco2ai.tools.tools_gpu import GPU, all_available_gpu
from eco2ai.tools.tools_cpu import CPU, all_available_cpu
from eco2ai.tools.tools_ram import RAM


warnings.filterwarnings('ignore')
cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)


