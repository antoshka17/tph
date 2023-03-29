import time
import requests
from eco2ai.tools.tools_gpu import GPU, all_available_gpu
from eco2ai.tools.tools_cpu import CPU, all_available_cpu
from eco2ai.tools.tools_ram import RAM
import warnings
from eco2ai.utils import(
    is_file_opened,
    define_carbon_index,
    get_params,
    set_params,
    # calculate_money,
    # summary,
    encode,
    encode_dataframe,
    electricity_pricing_check,
    calculate_price,
    FileDoesNotExistsError,
    NotNeededExtensionError,
)

cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)

time_start = time.time()
curr_time = time.time()
while curr_time - time_start < 100:
    cpu_con = cpu.get_consumption()
    ram_con = ram.get_consumption()
    total_con = ram_con + cpu_con
    curr_time = time.time()
    req = requests.get('http://localhost:3306/db/log/1')
    print(req.headers)

