
# sample employee data
employees = [
    {"name": "Joe", "unavailable_shifts": [
        {"day": "Thursday", "shifts": ["7am-3pm", "3pm-11pm"]},
        {"day": "Saturday", "shifts": ["3pm-11pm"]},
    ]},
    {"name": "Trevor", "unavailable_shifts": [
        {"day": "Monday", "shifts": ["3pm-11pm"]},
        {"day": "Friday", "shifts": ["3pm-11pm"]}
    ]},
    {"name": "Leo", "unavailable_shifts": [
        {"day": "Friday", "shifts": ["3pm-11pm"]},
    ]},
    {"name": "Abby", "unavailable_shifts": [
        {"day": "Friday", "shifts": ["7am-3pm"]}]},
    {"name": "Carter", "unavailable_shifts": [
        {"day": "Friday", "shifts": ["7am-3pm", "3pm-11pm"]}
    ]},
    {"name": "Alex", "unavailable_shifts": []}
]


schedule = {"Monday": [], "Tuesday": [], "Wednesday": [],
            "Thursday": [], "Friday": [], "Saturday": []}
open_shift_times = {
    "Monday": ["7am-3pm", "3pm-11pm"],
    "Tuesday": ["7am-3pm", "3pm-11pm"],
    "Wednesday": ["7am-3pm", "3pm-11pm"],
    "Thursday": ["7am-3pm", "3pm-11pm"],
    "Friday": ["7am-3pm", "3pm-11pm"],
    "Saturday": ["7am-3pm", "3pm-11pm"]
}


def employee_num_total_shifts_scheduled(schedule, employee_name):
    count = 0
    for shifts in schedule.values():
        for shift in shifts:
            if shift["name"] == employee_name:
                count += 1
    return count


def employee_num_day_shifts_scheduled(schedule, employee_name, day):
    count = 0
    if day in schedule:
        for shift in schedule[day]:
            if shift["name"] == employee_name:
                count += 1
    return count


# create open shift time set for easy reading/updating open shifts
open_shift_times_set = set()
for open_shift_day, open_shift_times_list in open_shift_times.items():
    for open_shift_time in open_shift_times_list:
        open_shift_times_set.add((open_shift_day, open_shift_time))

# create unavailable shifts set containing employee unavailable shifts for easy reading
employee_unavailable_shifts_set = set()
for employee in employees:
    for shift_info in employee["unavailable_shifts"]:
        day = shift_info["day"]
        for shift_time in shift_info["shifts"]:
            employee_unavailable_shifts_set.add(
                (employee["name"], day, shift_time))


def is_schedule_valid(schedule, employees, employee, open_shift_times, employee_unavailable_shifts, day, shift_time):

    if (employee["name"], day, shift_time) in employee_unavailable_shifts:
        return False

    if (day, shift_time) not in open_shift_times:
        return False

    if employee_num_day_shifts_scheduled(schedule, employee["name"], day) == 1:
        return False

    if employee_num_total_shifts_scheduled(schedule, employee["name"]) == 2:
        return False

    schedule[day].append({"name": employee["name"], "shift": shift_time})
    open_shift_times.discard((day, shift_time))

    if len(open_shift_times) == 0:
        return True

    for emp in employees:
        for (openDay, openTime) in open_shift_times:
            open_shift_times_copy = open_shift_times.copy()
            res = is_schedule_valid(
                schedule, employees, emp, open_shift_times_copy, employee_unavailable_shifts, openDay, openTime)
            if res:
                return True

    schedule[day].pop()
    open_shift_times.add((day, shift_time))

    return False


def generate_shift_schedule(schedule, employees, open_shift_times, employee_unavailable_shifts):
    for employee in employees:
        for (day, time) in open_shift_times:
            res = is_schedule_valid(
                schedule, employees, employee, open_shift_times, employee_unavailable_shifts, day, time)
            if res == True:
                print(schedule)
                return True
    return False


res = generate_shift_schedule(
    schedule, employees, open_shift_times_set, employee_unavailable_shifts_set)
if res:
    print("Employee shifts successfully scheduled")
else:
    print("Couldn't successfully schedule employee shifts")
