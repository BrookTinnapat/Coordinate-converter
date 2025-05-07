from pyproj import Proj, Transformer

def utm_to_latlon():
    print("\n=== UTM → GPS ===")
    print("Enter'b'to return to the main menu")

    easting_input = input("Enter Easting (m): ")
    if easting_input.lower() == "b":
        return
    northing_input = input("Enter Northing (m): ")
    if northing_input.lower() == "b":
        return
    zone_input = input("Enter UTM Zone (e.g., 47): ")
    if zone_input.lower() == "b":
        return
    hemisphere_input = input("Hemisphere? (N/S): ")
    if hemisphere_input.lower() == "b":
        return

    try:
        easting = float(easting_input)
        northing = float(northing_input)
        zone_number = int(zone_input)
        hemisphere = hemisphere_input.strip().upper()
        northern = hemisphere == "N"

        proj_utm = Proj(proj='utm', zone=zone_number, ellps='WGS84', south=not northern)
        proj_latlon = Proj(proj='latlong', datum='WGS84')
        transformer = Transformer.from_proj(proj_utm, proj_latlon)
        lon, lat = transformer.transform(easting, northing)
        print(f"\nLatitude: {lat:.6f}, Longitude: {lon:.6f}")
    except:
        print("❗ Data is invalid. Try again")
    
    input("\nPress Enter to back to main menu...")

def latlon_to_utm():
    print("\n=== GPS → UTM ===")
    print("Type 'b' to return to the main menu")

    lat_input = input("Enter Latitude: ")
    if lat_input.lower() == "b":
        return
    lon_input = input("Enter Longitude: ")
    if lon_input.lower() == "b":
        return

    try:
        lat = float(lat_input)
        lon = float(lon_input)
        zone_number = int((lon + 180) / 6) + 1
        northern = lat >= 0

        proj_latlon = Proj(proj='latlong', datum='WGS84')
        proj_utm = Proj(proj='utm', zone=zone_number, ellps='WGS84', south=not northern)
        transformer = Transformer.from_proj(proj_latlon, proj_utm)
        easting, northing = transformer.transform(lon, lat)
        hemisphere = "N" if northern else "S"
        print(f"\nEasting: {easting:.3f}, Northing: {northing:.3f}, Zone: {zone_number}{hemisphere}")
    except:
        print("❗ Data is invalid. Try again")

    input("\nPress Enter to back to main menu...")

# ============ Main Menu ============
while True:
    print("\n============================")
    print(" Coordinate converter UTM ⇄ GPS ")
    print("============================")
    print("1 = Convert UTM → GPS")
    print("2 = Convert GPS → UTM")
    print("0 = Exit")
    choice = input("Select (0-2): ")

    if choice == "1":
        utm_to_latlon()
    elif choice == "2":
        latlon_to_utm()
    elif choice == "0":
        print("Exiting the program...")
        break
    else:
        print("❗ Select (0-2)\n")
