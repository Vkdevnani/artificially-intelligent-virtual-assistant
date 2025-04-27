import time
import datetime
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_websites(host_path, website_list, redirect):
    with open(host_path, "r+") as file:
        content = file.read()
        for website in website_list:
            if website not in content:
                file.write(f"{redirect} {website}\n")
                print(f"Blocked: {website}")
        time.sleep(2)
        print("Focus mode turned on!")

def unblock_websites(host_path, website_list):
    with open(host_path, "r+") as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(website in line for website in website_list):
                file.write(line)
        file.truncate()
    print("Websites are unblocked!")

def main():
    if is_admin():
        try:
            current_time = datetime.datetime.now().strftime("%H:%M")
            Stop_time = input("Enter stop time (example: 10:10): ")
            current_time_obj = datetime.datetime.strptime(current_time, "%H:%M")
            stop_time_obj = datetime.datetime.strptime(Stop_time, "%H:%M")
            focus_duration = (stop_time_obj - current_time_obj).total_seconds() / 60.0

            host_path = r'C:\Windows\System32\drivers\etc\hosts'
            redirect = '127.0.0.1'
            website_list = ["www.facebook.com", "www.youtube.com", "www.instagram.com", "instagram.com"]

            print(f"Focus mode activated. Blocking websites until {Stop_time}.")

            if current_time_obj < stop_time_obj:
                block_websites(host_path, website_list, redirect)

            while True:
                current_time = datetime.datetime.now().strftime("%H:%M")
                current_time_obj = datetime.datetime.strptime(current_time, "%H:%M")
                if current_time_obj >= stop_time_obj:
                    unblock_websites(host_path, website_list)
                    with open("focus.txt", "a") as file:
                        file.write(f"{focus_duration} minutes\n")
                    break

        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
if __name__ == "__main__":
    main()