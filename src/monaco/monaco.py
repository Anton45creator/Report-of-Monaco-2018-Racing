from datetime import datetime, timedelta

position_of_qualified = 15


def build_report(data, asc=None):
    """Return list of drivers results:
        [
         {'driver': 'Sebastian Vettel',
            'car': 'FERRARI',
            'start': Timestamp('2018-05-24 12:02:58.917000'),
            'end': Timestamp('2018-05-24 12:04:03.332000'),
            'time': Timedelta('0 days 00:01:04.415000'),
            'result': '1:04.415'
            'position': 1},
         {'driver': 'Valtteri Bottas',
             'car': 'MERCEDES',
             'start': Timestamp('2018-05-24 12:00:00'),
             'end': Timestamp('2018-05-24 12:01:12.434000'),
             'time': Timedelta('0 days 00:01:12.434000'),
             'result': '1:12.434'
             'position': 2},]"""

    # Reading data and columns filling

    empty_datetime = datetime(1, 1, 1, 0, 0)
    empty_timedelta = timedelta(0)

    drivers = {}

    for line in data['abb'].splitlines():
        values = line.split('_')
        if len(values) < 3:
            continue

        key = values[0]
        drivers[key] = {
            'driver': values[1],
            'car': values[2],
            'start': empty_datetime,
            'end': empty_datetime,
            'time': empty_timedelta,
            'position': 0,
            'disqualified': False}

    fill_driver_datetime(drivers, data['start'], 'start')

    fill_driver_datetime(drivers, data['end'], 'end')

    fill_driver_time_result(drivers)

    # Make report

    report = []

    for driver in drivers.values():
        report.append(driver)

    report = sorted(report, key=lambda k: k['time'])

    # Column Position filling

    result = ''
    position = 0

    for record in report:

        if not result == record['result']:
            position = position + 1
            result = record['result']

        record['position'] = position

    # Sorting by settings
    if asc == False:
        report = sorted(report, key=lambda k: k['position'], reverse=False)
    else:
        report = sorted(report, key=lambda k: k['position'], reverse=True)

    return report


def fill_driver_datetime(drivers, data_string, field_name):
    for line in data_string.splitlines():
        values = line.split('_')
        if len(values) < 3:
            continue

        value_date = values[1]
        value_time = ''.join((values[2], '000'))

        value = ' '.join((value_date, value_time))
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

        key = values[0]
        drivers[key][field_name] = value


def fill_driver_time_result(drivers):
    dis_time = timedelta(days=30)
    dis_result = 'Disqualified'

    for key, driver in drivers.items():

        if driver['end'] <= driver['start']:
            driver['time'] = dis_time
            driver['result'] = dis_result
            driver['disqualified'] = True
        else:
            time = driver['end'] - driver['start']
            driver['time'] = time

            minutes = (time.seconds // 60) % 60
            seconds = time.seconds % 60
            ms = time.microseconds

            driver[
                'result'] = f'{minutes}:{str(seconds).zfill(2)}.{str(ms)[:3]}'


def print_report(report, driver, show_line=False):
    """
    Output for "build_report" function
    """
    if driver is None:

        if len(report):

            print(
                f'{"N": <3} | {"DRIVER": <20} | '
                f'{"CAR": <30} | {"BEST LAP": <30}')
            print('-' * 70)

            for record in report:
                if show_line and record['position'] > position_of_qualified:
                    show_line = False
                    print('-' * 70)
                print(
                    f'{str(record["position"]) + ".": <3} | '
                    f'{record["driver"]: <20} | {record["car"]: <30} | '
                    f'{record["result"]}')
        else:
            print('Report is empty!')

    else:

        records = [x for x in report if x["driver"] == driver]
        if len(records):
            record = records[0]

            if record['disqualified']:
                race_result = 'Disqualified'
            else:
                race_result = str(record['time'])[:-3][11:]

            message = f"""
                Driver: {record["driver"]}
                Car: {record["car"]}
                Position: {record["position"]}

                Best lap:
                    start - {record["start"].strftime('%Y-%m-%d %H:%M:%S.%f')
                             [:-3]}
                    end   - {record["end"].strftime('%Y-%m-%d %H:%M:%S.%f')
                             [:-3]}
                    result: {record["result"]}"""

            print(message.replace('\t', ''))
        else:
            print('Driver not found!')
