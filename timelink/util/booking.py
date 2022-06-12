from datetime import date, time

# data storage
# 每天更新一次
available_frag = [f for f in range(24)]
booked_frag = []
# 00:00 - 01:00 -> 0
# 01:00 - 02:00 -> 1

# 預約判斷
def booking(booking_frag, start_hr, finish_hr):
    if booking_frag < start_hr or booking_frag > finish_hr:
        return {"data": "此時段不在服務時間"}
    if booking_frag not in available_frag:
        return {"data": "此時段已被預約"}
    else:
        available_frag.remove(booking_frag)
        booked_frag.append(booking_frag)
    return {"data": "預約成功"}

# 時段轉換時間
def time_transform(time_list):
    time_period = {"data":[]}
    for period in sorted(time_list):
        start_time = time(hour=period)
        end_time = time(hour=period+1)
        time_period["data"].append({"booked_date": date.today(), "start_time": start_time, "end_time": end_time})
    return time_period

start_hr = 8
finish_hr = 21
resp = booking(11, start_hr, finish_hr)
print(resp)

# to database
print(time_transform(booked_frag))