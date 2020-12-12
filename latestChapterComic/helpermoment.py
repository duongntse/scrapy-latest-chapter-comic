import moment
import re


class HelperMoment():

    def getRawTime(self, timefromnow):
        # timefromnow: an hour ago, a day ago, 34 hours ago, 2 days ago, etc
        regex_fromNow_pattern = r'(\d{1,2}|a|an)\s(minute(s)?|hour(s)?|day(s)?|year(s)?)\sago'
        time_now = moment.now()
        raw_time = time_now.clone()

        if(re.search(regex_fromNow_pattern, timefromnow) is not None):
            timelist = timefromnow.split(' ')

            numb = 0

            if(timelist[0] in ['a', 'an', 1]):
                numb = 1
            else:
                numb = int(timelist[0])

            if(timelist[1] in ['minute', 'minutes']):
                # raw_time.subtract(minutes=eval(f"{numb}"))
                raw_time.subtract(minutes=numb)
            elif(timelist[1] in ['hour', 'hours']):
                # raw_time.subtract(hours=numb)
                raw_time.subtract(hours=numb)
            elif(timelist[1] in ['day', 'days']):
                # raw_time.subtract(days=numb)
                raw_time.subtract(days=numb)
            elif(timelist[1] in ['month', 'months']):
                # raw_time.subtract(months=numb)
                raw_time.subtract(months=numb)
            else:
                # raw_time.subtract(years=numb)
                raw_time.subtract(years=numb)

        rawtimedata = raw_time.format('DD MMMM YYYY hh:mm:ss')

        return rawtimedata

    def fromNow(self, time):
        time = moment.date(time)
        time_now = moment.now()
        year = time_now.year - time.year
        month = time_now.month - time.month
        day = time_now.day - time.day
        hour = time_now.hour - time.hour
        minute = time_now.minute - time.minute
        second = time_now.second - time.second

        if(year > 0):
            txtYear = 'year'
            if(year == 1):
                year = 'a'
            if(year > 1):
                txtYear = 'years'
            return f"{year} {txtYear} ago"
        elif(year < 0):
            txtYear = 'year'
            if(year == -1):
                year = 'a'
            if(year < -1):
                txtYear = 'years'
            return f"in {year} {txtYear}"

        else:
            if(month > 0):
                txtMonth = 'month'
                if(month == 1):
                    month = 'a'
                if(month > 1):
                    txtMonth = 'months'
                return f"{month} {txtMonth} ago"
            elif(month < 0):
                txtMonth = 'month'
                if(month == -1):
                    month = 'a'
                if(month < -1):
                    txtMonth = 'months'
                return f"in {month} {txtMonth}"
            else:
                if(day > 0):
                    txtDay = 'day'
                    if(day == 1):
                        day = 'a'
                    if(day > 1):
                        txtDay = 'days'
                    return f"{day} {txtDay} ago"
                elif(day < 0):
                    txtDay = 'day'
                    if(day == -1):
                        day = 'a'
                    if(day < -1):
                        txtDay = 'days'
                    return f"in {day} {txtDay}"
                else:
                    if(hour > 0):
                        txtHour = 'hour'
                        if(hour == 1):
                            hour = 'an'
                        if(hour > 1):
                            txtHour = 'hours'
                        return f"{hour} {txtHour} ago"
                    elif(hour < 0):
                        txtHour = 'hour'
                        if(hour == -1):
                            hour = 'an'
                        if(hour < -1):
                            txtHour = 'hours'
                        return f"in {hour} {txtHour}"
                    else:
                        if(minute > 0):
                            txtMinute = 'minute'
                            if(minute == 1):
                                minute = 'a'
                            if(minute > 1):
                                txtMinute = 'minutes'
                            return f"{minute} {txtMinute} ago"
                        elif(minute < 0):
                            txtMinute = 'minute'
                            if(minute == -1):
                                minute = 'a'
                            if(minute < -1):
                                txtMinute = 'minutes'
                            return f"in {minute} {txtMinute}"
                        else:
                            if(second > 0):
                                txtSecond = 'second'
                                if(second == 1):
                                    second = 'a'
                                if(second > 1):
                                    txtSecond = 'seconds'
                                return f"{second} {txtSecond} ago"
                            elif(second < 0):
                                txtSecond = 'second'
                                if(second == -1):
                                    second = 'a'
                                if(second < -1):
                                    txtSecond = 'seconds'
                                return f"in {second} {txtSecond}"

    def timeFromVnToEn(self, time):
        hmsRepEn = 'hour'
        time_arr = time.split(' ')
        numb = int(time_arr[0])
        hmsRepVn = time_arr[1]
        # agoVn = time_arr[2]

        # time = '1 giờ trước'
        if(hmsRepVn == 'năm'):
            hmsRepEn = 'year'
        elif(hmsRepVn == 'tháng'):
            hmsRepEn = 'month'
        elif(hmsRepVn == 'tuần'):
            hmsRepEn = 'week'
        elif(hmsRepVn == 'ngày'):
            hmsRepEn = 'day'
        elif(hmsRepVn == 'giờ'):
            hmsRepEn = 'hour'
        elif(hmsRepVn == 'phút'):
            hmsRepEn = 'minute'
        else:
            hmsRepEn = 'second'

        if(int(numb) > 1):
            hmsRepEn += 's'

        timeFrom = f'{numb} {hmsRepEn} ago'
        return timeFrom

    def timeRawVnToEn(self, time):
        # time = 19:54 12/10
        match = re.search(
            r'(\d{1,2}):(\d{1,2}) (\d{1,2})\/(\d{1,2})\b', time)
        if (match is not None):
            return moment.date(time).format('DD MMMM YYYY hh:mm:ss')
