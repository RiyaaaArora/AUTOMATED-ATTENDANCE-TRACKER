from datetime import datetime
from database import load_lectures
# --- Public Holidays (Customize this list as needed for the current year) ---
# Example: Common Indian holidays (adjust dates/years as needed)
current_year = datetime.now().year
public_holidays = [
    f"{current_year}-08-15",  # Independence Day (example, adjust if needed)
    f"{current_year}-10-02",  # Gandhi Jayanti
    f"{current_year}-12-25",  # Christmas
    # Add more as needed, e.g., f"{current_year}-01-26" for Republic Day
]

# --- Generate Valid Dates (Exclude Sundays, 2nd/4th Saturdays, and Public Holidays) ---
def get_valid_dates():
    valid_dates = []
    months_days = [
        (11, range(26, 31)),  # Nov 26-30 (November has 30 days, so up to 30)
        (12, range(1, 32))    # Dec 1-31
    ]
    
    for month, days in months_days:
        saturdays = []
        for day in days:
            date_str = f"{current_year}-{month:02d}-{day:02d}"
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            weekday = date_obj.weekday()  # 0=Monday, 5=Saturday, 6=Sunday
            
            if weekday == 5:  # Saturday
                saturdays.append(date_str)
            if weekday == 6:
                continue
            elif date_str in public_holidays:  # Exclude public holidays
                continue
            else:  # Weekdays (Mon-Fri)
                valid_dates.append(date_str)
        
        # For Saturdays, exclude 2nd and 4th (if they exist)
        if len(saturdays) >= 1:
            valid_saturdays = [saturdays[i] for i in range(len(saturdays)) if i not in [1, 3]]  # 0-based: 1=2nd, 3=4th
            valid_dates.extend(valid_saturdays)
    
    return valid_dates

dates = get_valid_dates()

# --- Get Current Lecture ---
def get_current_lecture():
    # RELOAD DATA: Load fresh data every time we check for a lecture
    lecture_schedule, _ = load_lectures()

    current_time = datetime.now().strftime('%H:%M')
    current_day = datetime.now().strftime('%A')
    current_dt = datetime.strptime(current_time, '%H:%M')
    
    if current_day in lecture_schedule:
        for lec, time_str in lecture_schedule[current_day].items():
            scheduled_dt = datetime.strptime(time_str, '%H:%M')
            time_diff = abs((current_dt - scheduled_dt).total_seconds() / 60)
            if time_diff <= 10:
                return lec
    return None