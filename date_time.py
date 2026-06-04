import datetime as dt


# build an alarm system.
def Alarm_set():
    alarm_sound = input("Alarm (Hour/Min): ")
    alarm_ring = dt.datetime.strptime(alarm_sound, "%H/%M")

    alarm_label = input("What do you want to name alarm: ")
    snooze_dur = int(input("Set Snooze duration: "))

    now = dt.datetime.now()

    while True:
        now.hour == alarm_ring.hour and now.hour == alarm_ring.minute

        Alarm_on()


def Alarm_on():
    print(f"""
        It's Time!!!
        {alarm_label}

        Do you want to:
        1. Snooze Alarm
        2. Stop Alarm
    """)

    user = input("Input 1 or 2: ")

    if user == "1":
        Snooze()

    elif user == "2":
        print("Alarm stopped")
        Alarm_set()

    else:
        print("Invalid Input")


def Snooze():
    snooze_set = now.minute + dt.timedelta(minute=snooze_dur)

    while True:
        now.minute == snooze_set.minute

        Alarm_on()
