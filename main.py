import datetime
import ftplib
import io
import os
from typing import Optional

from dotenv import load_dotenv


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
        return f"{self.date.strftime('%b %d, %Y')} {self.time.strftime('%I:%M:%S %p')}"

    @property
    def display_status(self) -> str:
        return f"{self.prod_time}  :  {self.prod_achieved}"


def get_tienkang_data() -> Optional[bytes | None]:
    """Grasp data from Tienkang machine"""

    filename = (
        os.environ.get("TIENKANG_FILE") + "_" + datetime.date.today().strftime("%y%m%d")
    )
    data = io.BytesIO()

    try:
        ftp = ftplib.FTP(os.environ.get("TIENKANG_HOST"))  # port is 21 by default
        ftp.login(
            user=os.environ.get("TIENKANG_USER"), passwd=os.environ.get("TIENKANG_PASS")
        )
        ftp.retrbinary("RETR " + filename, data.write)
    except:
        return None

    finally:
        ftp.quit()

    return data.getvalue()


if __name__ == "__main__":
    pass

    # data.decode("utf-16").split("\n")[-2].split("\t")  # gets last data in the bytes