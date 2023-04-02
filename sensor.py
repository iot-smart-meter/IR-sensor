import serial


def hex_to_int(hex):
    i = int(hex, 16)
    if i & 0x80000000:    # MSB set -> neg.
        return -((~i & 0xffffffff) + 1)
    else:
        return i


s = serial.Serial(
    port="/dev/ttyUSB0",
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    baudrate=9600
)

start = '1b1b1b1b01010101'
end = '1b1b1b1b1a'

data = ""
while True:
    data += (s.read().hex())

    pos = data.find(end)
    if (pos != -1):
        print("end")
        f = data.find("77078181c78203ff0101010104")
        print(f)
        search = '77078181c78203ff0101010104'

        pos = data.find(search)
        if (pos != -1):
            pos = pos + len(search)
            value = data[pos:pos + 6]
            print('Hersteller-ID:   ' + search + ': ' + value + ' = ')

        search = '77070100000009ff010101010b'
        pos = data.find(search)
        if (pos != -1):
            pos = pos + len(search)
            value = data[pos:pos + 20]
            print('Server-ID:       ' + search + ': ' + value)

        energy = 0
        search = '77070100010800ff64'
        pos = data.find(search)
        if (pos != -1):
            # skip 9 Bytes which may be different
            pos = pos + len(search) + 18
            value = data[pos:pos + 16]
            try:
                energy = float(int(value, 16)) / 10
            except:
                energy = 0.0
            print('Total Bezug:     ' + search + ': ' +
                  value + ' = ' + str(energy/1e6) + ' kWh')

        energy_feed = 0
        search = '77070100020800ff64'
        pos = data.find(search)
        if (pos != -1):
            # skip 9 Bytes which may be different
            pos = pos + len(search) + 18
            value = data[pos:pos + 16]
            try:
                energy_feed = float(int(value, 16)) / 10
            except:
                energy_feed = 0.0
            print('Total Lieferung: ' + search + ': ' +
                  value + ' = ' + str(energy_feed/1e6) + ' kWh')

        power = 0
        search = '77070100100700ff0101621b52fe59'
        pos = data.find(search)
        if (pos != -1):
            pos = pos + len(search)
            value = data[pos:pos + 16]
            try:
                power = float(hex_to_int(value)) / 100
            except:
                power = 0.0
            print('Leistung:        ' + search + ': ' +
                  value + ' = ' + str(power) + ' W')

        data = ""
