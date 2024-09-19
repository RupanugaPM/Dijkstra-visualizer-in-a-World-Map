from django.shortcuts import render
import math
import random
from heapq import heappush, heappop

def homepage(request):
    
    # Define the Earth's radius in kilometers
    EARTH_RADIUS = 6371.0

    # Define the spacing in kilometers
    spacing_km = 10.0

    # Convert spacing to radians
    def km_to_radians(km):
        return km / EARTH_RADIUS

    #===================
    #way 3 start here ||
    #===================
    # Function to calculate the distance between two points on the Earth
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Earth radius in kilometers
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    # Function to calculate the initial bearing from point A to B
    def calculate_initial_compass_bearing(lat1, lon1, lat2, lon2):
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_lambda = math.radians(lon2 - lon1)

        x = math.sin(delta_lambda) * math.cos(phi2)
        y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
        
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    # Function to calculate destination point given start point, bearing, and distance
    def destination_point(lat, lon, bearing, distance_km):
        R = 6371.0  # Earth radius in kilometers
        bearing = math.radians(bearing)

        lat = math.radians(lat)
        lon = math.radians(lon)

        lat2 = math.asin(math.sin(lat) * math.cos(distance_km / R) + 
                        math.cos(lat) * math.sin(distance_km / R) * math.cos(bearing))

        lon2 = lon + math.atan2(math.sin(bearing) * math.sin(distance_km / R) * math.cos(lat), 
                                math.cos(distance_km / R) - math.sin(lat) * math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)

        return (lat2, lon2)

    # Function to generate waypoints along the path
    def generate_waypoints(source, destination, distance_interval_km, extend):
        waypoints = []

        lat1, lon1 = source
        lat2, lon2 = destination



        total_distance_km = haversine(lat1, lon1, lat2, lon2) + extend
        num_waypoints = int(total_distance_km // distance_interval_km)
        print("distance points", num_waypoints)
        width = min(num_waypoints//10, 100)
        initial_bearing = calculate_initial_compass_bearing(lat1, lon1, lat2, lon2)

        dp = [[[0, 0, random.randint(0, 101)] for i in range(width*2+1)] for j in range(num_waypoints + (extend//10)*2 )]  # (extend//10)*2 for extending the route
        dp_source = [4, width]
        dp[4][width][0],  dp[4][width][1] = source
        dp_destination = [num_waypoints-8+(extend//10)*2, width]
        dp[num_waypoints-4][width][0], dp[num_waypoints-4][width][1] = destination
        print("dp dim", len(dp), len(dp[0]))


        # extend prev to source
        num_prev_waypoints = extend//10
        for i in range(1, num_prev_waypoints + 1):
            main_point = destination_point(lat1, lon1, initial_bearing + 180, i * distance_interval_km)
            waypoints.append({'latitude': main_point[0], 'longitude': main_point[1]})
            dp[4-i][width][0], dp[4-i][width][1] = main_point[0], main_point[1]

            d = 10
            while d <= (width * 10):
                left_point = destination_point(main_point[0], main_point[1], initial_bearing - 90, d)
                right_point = destination_point(main_point[0], main_point[1], initial_bearing + 90, d)
                waypoints.append({'latitude': left_point[0], 'longitude': left_point[1]})
                dp[4-i][width-d//10][0], dp[4-i][width-d//10][1] = left_point[0], left_point[1]
                waypoints.append({'latitude': right_point[0], 'longitude': right_point[1]})
                dp[4-i][width+d//10][0], dp[4-i][width+d//10][1] = right_point[0], right_point[1]
                d += 10


        for i in range(num_waypoints + 1):
            main_point = destination_point(lat1, lon1, initial_bearing, i * distance_interval_km)
            if main_point != source and main_point != destination:
                waypoints.append({'latitude': main_point[0], 'longitude': main_point[1]})
                dp[4+i][width][0], dp[4+i][width][1] = main_point[0], main_point[1]

            d = 10
            while d <= (width * 10):
                left_point = destination_point(main_point[0], main_point[1], initial_bearing - 90, d)
                right_point = destination_point(main_point[0], main_point[1], initial_bearing + 90, d)
                waypoints.append({'latitude': left_point[0], 'longitude': left_point[1]})
                dp[4+i][width-d//10][0], dp[4+i][width-d//10][1] = left_point[0], left_point[1]
                waypoints.append({'latitude': right_point[0], 'longitude': right_point[1]})
                dp[4+i][width+d//10][0], dp[4+i][width+d//10][1] = right_point[0], right_point[1]
                
                d += 10


        dp2 = [[[-1, -1] for i in range(width*2+1)] for j in range(num_waypoints + (extend//10)*2 )]
        def findPath():
            print("source, dest", dp_source, dp_destination)
            print("source lat lon", dp[dp_source[0]][dp_source[1]])
            heap = []
            heappush(heap, [0, dp_source[0], dp_source[1]])

            rs = [1, 1, 1, -1, -1, -1, 0, 0]
            cs = [0, -1, 1, 0, 1, -1, -1, 1]

            while heap:
                dist, row, col = heappop(heap)
                for i in range(8):
                    new_row = row + rs[i]
                    new_col = col + cs[i]
                    if 0 <= new_row < num_waypoints + (extend//10)*2 and 0 <= new_col < width*2 and dp2[new_row][new_col][0]==-1:
                        dp2[new_row][new_col][0], dp2[new_row][new_col][1] = row, col
                        heappush(heap, [dist+dp[row][col][2], new_row, new_col])
            
            start = dp_destination
            path = []
            while start[0]!=dp_source[0] or start[1]!=dp_source[1]:
                path.append(start)
                start = dp2[start[0]][start[1]]
            path.append(start)
            path.reverse()

            pat_with_lat_lon = []
            for i, j in path:
                pat_with_lat_lon.append({"latitude":dp[i][j][0], "longitude":dp[i][j][1]})
            
            return pat_with_lat_lon
        return (waypoints, findPath())

    #===================
    #way 3 ends here  ||
    #===================
    



    
    source = (12.8379468, 77.6479789)
    destination = (17.4065, 78.4772)
    distance_interval_km = 10 #km
    extend = 40 #km
    waypoints, path = generate_waypoints(source, destination, distance_interval_km, extend)

    param = {"waypoints": waypoints, "source": source, "destination": destination, "path": path}
    

    return render(request,'index.html', param)