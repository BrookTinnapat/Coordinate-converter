import math

def utm_to_latlon(easting, northing, zone_number, northern_hemisphere=True):
    a = 6378137.0
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    x = easting - 500000.0
    y = northing
    if not northern_hemisphere:
        y -= 10000000.0

    zone_cm = 6 * zone_number - 183.0

    m = y / k0
    mu = m / (a * (1 - e**2 / 4 - 3 * e**4 / 64 - 5 * e**6 / 256))

    e1 = (1 - math.sqrt(1 - e**2)) / (1 + math.sqrt(1 - e**2))
    j1 = 3 * e1 / 2 - 27 * e1**3 / 32
    j2 = 21 * e1**2 / 16 - 55 * e1**4 / 32
    j3 = 151 * e1**3 / 96
    j4 = 1097 * e1**4 / 512

    fp = mu + j1 * math.sin(2 * mu) + j2 * math.sin(4 * mu) + j3 * math.sin(6 * mu) + j4 * math.sin(8 * mu)

    c1 = e1sq * math.cos(fp)**2
    t1 = math.tan(fp)**2
    r1 = a * (1 - e**2) / ((1 - (e * math.sin(fp))**2)**1.5)
    n1 = a / math.sqrt(1 - (e * math.sin(fp))**2)
    d = x / (n1 * k0)

    q1 = n1 * math.tan(fp) / r1
    q2 = d**2 / 2
    q3 = (5 + 3 * t1 + 10 * c1 - 4 * c1**2 - 9 * e1sq) * d**4 / 24
    q4 = (61 + 90 * t1 + 298 * c1 + 45 * t1**2 - 252 * e1sq - 3 * c1**2) * d**6 / 720

    lat = fp - q1 * (q2 - q3 + q4)

    q5 = d
    q6 = (1 + 2 * t1 + c1) * d**3 / 6
    q7 = (5 - 2 * c1 + 28 * t1 - 3 * c1**2 + 8 * e1sq + 24 * t1**2) * d**5 / 120

    lon = zone_cm + (q5 - q6 + q7) / math.cos(fp)

    latitude = math.degrees(lat)
    longitude = lon  # already in degrees

    return latitude, longitude

# รับค่าจากผู้ใช้
try:
    easting = float(input("Enter Easting (Ex: 691393.880): "))
    northing = float(input("Enter Northing (Ex: 2166400.150): "))
    zone = int(input("Enter Zone (Ex: 47): "))
    hemisphere_input = input("Hemisphere? (1 = N/2 = S): ").strip().upper()
    is_northern = hemisphere_input == 'N' or hemisphere_input == '1'
    if hemisphere_input == '2':
        is_northern = False
    elif hemisphere_input != '1':
        is_northern = True

    lat, lon = utm_to_latlon(easting, northing, zone, is_northern)

    print(f"\nResult:")
    print(f"Latitude: {lat:.6f}")
    print(f"Longitude: {lon:.6f}")

except ValueError:
    print("❌ Data is invalid. Try again")
