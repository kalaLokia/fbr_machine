import datetime
import ftplib
import io
import os
from typing import Optional
import time

from dotenv import load_dotenv

from web_api import slack_api, webhook_request

load_dotenv()


class MachineData:
    """Model for machine data"""

    # Note that the production here means "pouring"

    def __init__(
        self, date, time, station, target, current, countdown, achieved
    ) -> None:
        self.date = datetime.datetime.strptime(date, "%y/%m/%d").date()
        self.time = datetime.datetime.strptime(time, "%H:%M:%S").time()
        self.station = int(station)
        self.prod_target = int(target)
        self.prod_current = int(current)
        self.prod_countdown = int(countdown)
        self.prod_achieved = int(achieved)

    @property
    def prod_time(self) -> str:  # Datetime formatted
        return f"{self.date.strftime('%b %d, %Y')} {self.time.strftime('%I:%M %p')}"

    @property
    def display_status(self) -> str:
        return f"{self.prod_time}  ->  {self.prod_achieved}"


def get_tienkang_data() -> Optional[bytes | None]:
    """Grasp data from Tienkang machine"""

    now = datetime.datetime.now()
    filename = os.environ.get("TIENKANG_FILE") + "_" + now.strftime("%y%m%d") + ".csv"
    data = io.BytesIO()

    check_min = now.minute % 10
    if check_min < 2 or check_min > 6:
        # Preventing reading data while hmi uses flash drive to write
        # 10 minutes gap till next file updation
        return None

    try:
        ftp = ftplib.FTP(os.environ.get("TIENKANG_HOST"))  # port is 21 by default
        ftp.login(
            user=os.environ.get("TIENKANG_USER"), passwd=os.environ.get("TIENKANG_PASS")
        )
        ftp.retrbinary("RETR " + filename, data.write)

        # Remove old Data collection files on every sunday 1pm
        if now.weekday() == 6 and now.hour == 13:
            # There are non-unicode character files exists in server
            ftp.encoding = "unicode_escape"
            dir_files = []  # to store all files in the root
            ftp.dir(dir_files.append)
            ftp.encoding = "utf-8"  # To delete, change file encoding back to utf-8
            for file_info in dir_files:
                if "DATA_collection" in file_info:
                    if filename not in file_info:
                        old_filename = file_info.split(" ")[-1]
                        if old_filename[-3:] == "csv":
                            # data can be exported to db if necessary before removing
                            ftp.delete(old_filename)

    except:
        return None

    finally:
        ftp.quit()

    return data.getvalue()


if __name__ == "__main__":

    start = time.time()
    data = get_tienkang_data()
    end = time.time()
    print(f"Time taken to finish: {end-start}")
    if data:
        data = data.decode("utf-16").split("\n")
        print(f"No. of lines: {len(data)}")
        last_data = data[-2].split("\t")
        # gets last data in the bytes
        tienkang = MachineData(*last_data)
        # print(tienkang.display_status)
        if tienkang.prod_achieved != 0:
            slack_api(tienkang.display_status)
            if datetime.datetime.today().weekday() != 6:
                webhook_request({"text": tienkang.display_status}, "google")
    # else:
    #     print("ERROR Occured")
