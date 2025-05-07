import math

def latlon_to_utm(lat, lon):
    # Constants
    a = 6378137.0  # Semi-major axis (WGS84)
    f = 1 / 298.257223563
    e2 = f * (2 - f)
    k0 = 0.9996

    zone_number = int((lon + 180) / 6) + 1
    lon_origin = (zone_number - 1) * 6 - 180 + 3
    lon_origin_rad = math.radians(lon_origin)

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    n = a / math.sqrt(1 - e2 * math.sin(lat_rad)**2)
    t = math.tan(lat_rad)**2
    c = e2 / (1 - e2) * math.cos(lat_rad)**2
    a_ = math.cos(lat_rad) * (lon_rad - lon_origin_rad)

    m = a * (
        (1 - e2 / 4 - 3 * e2**2 / 64 - 5 * e2**3 / 256) * lat_rad
        - (3 * e2 / 8 + 3 * e2**2 / 32 + 45 * e2**3 / 1024) * math.sin(2 * lat_rad)
        + (15 * e2**2 / 256 + 45 * e2**3 / 1024) * math.sin(4 * lat_rad)
        - (35 * e2**3 / 3072) * math.sin(6 * lat_rad)
    )

    easting = k0 * n * (
        a_ + (1 - t + c) * a_**3 / 6 + (5 - 18 * t + t**2 + 72 * c - 58 * e2 / (1 - e2)) * a_**5 / 120
    ) + 500000

    northing = k0 * (
        m + n * math.tan(lat_rad) * (
            a_**2 / 2 + (5 - t + 9 * c + 4 * c**2) * a_**4 / 24 +
            (61 - 58 * t + t**2 + 600 * c - 330 * e2 / (1 - e2)) * a_**6 / 720
        )
    )

    if lat < 0:
        northing += 10000000  # สำหรับซีกโลกใต้

    return easting, northing, zone_number

# รับค่าจากผู้ใช้
try:
    lat = float(input("Enter Latitude (Ex: 19.588960): "))
    lon = float(input("Enter Longitude (Ex: 100.610014): "))

    easting, northing, zone = latlon_to_utm(lat, lon)

    print(f"\nResult:")
    print(f"Easting: {easting:.3f} m")
    print(f"Northing: {northing:.3f} m")
    print(f"Zone: {zone}")
    print(f"Hemisphere: {'North' if lat >= 0 else 'South'}")

except ValueError:
    print("❌ Data is invalid. Try again")
