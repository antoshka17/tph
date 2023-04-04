import time
from server import Content, create_comp, create_comp_con, session, get_vals_for_graphic
from datetime import datetime
from calculations import cpu, ram, calculate
import platform
time_start = time.time()
curr_time = time.time()
iterations = 1
computer = create_comp(platform.node(), session())
start_consumption_cpu = cpu.get_consumption()
start_consumption_ram = ram.get_consumption()
while curr_time - time_start < 30:
    if iterations % 10 == 0:
        content = get_vals_for_graphic('minutes', session())
        # print('for graphic: -----------------')
        # print(content[0], content[1], content[2])
    cpu_con, ram_con, total_con, val_cpu, val_ram = calculate(cpu, ram, start_consumption_cpu, start_consumption_ram)
    start_consumption_cpu, start_consumption_ram = val_cpu, val_ram
    content_obj = Content(comp_id=1, time=datetime.now(), cpu_consumption=cpu_con, ram_consumption=ram_con,
                          total_consumption=total_con)
    data = create_comp_con(content_obj.comp_id,content_obj, session())
    curr_time = time.time()
    time.sleep(1)
    iterations+=1

print(iterations)
