# Flight Navigation Optimization and Risk Mitigation
We are going to build a robust solution for aerospace industry as part of aerothon 6.0. Aerothon is a hackathon hosted by Airbus India to solve some challenges in aerospace industry.
## Problem Statement
The straight path from source airport to destination airport is always best route for aircrafts to fly. But, due to some obstructions (such as weather, air traffic) in the straight path, we have to find an alternate path.
We aim to maximize safety and minimize risk in finding the optimal flight route, while also minimizing total cost (extra fuel, API calls, etc.). Additionally, the solution provides alternate paths for pilots to choose from.
# Solution Overview
We convert the problem into a graph problem with a source, destination, and risk factors associated with each node that need to be minimized. Using a time-varying Dijkstra algorithm, we calculate the optimal path while considering these risk factors.
# How It Helps
By converting the problem into a graph problem, we can efficiently use well-established algorithms (like Dijkstra) to find the shortest and safest path. The inclusion of time-varying risk factors ensures that the solution adapts to changing conditions, enhancing safety.
# Impact Metrics
- Weather patterns over an area for a duration of an hour.
- Number of planes in the area, which can increase collision risks.
# Problem Representation
- Each node represents a waypoint. Each node in the four directions are at a distance of 10 km.
- Edges represent the possible 8 directional moves from each node.
- Nodes contain risk factors that need to be minimized (weather conditions, plane density).
# Technology Stack
- **Database:** SQL/Firebase for storing API call results to reduce costs.
- **Backend:** Python for implementing the risk calculation algorithm.
- **APIs:** Weather API, Plane data API.
- **Frontend:** HTML, CSS, JS
# Assumptions and Constraints
- Planes will not deviate more than 20% from the optimal route.
- The maximum flight length is 11,000 km, with a maximum width of 1,100 km.
- Risk increases quadratically with the number of planes in a node.
- Weather risk follows a sigmoid function.
- API calls are cached and reused to save costs.
- Maximum flight duration is 18 hours, with a 2-hour buffer for API calls.
# Solution Implementation
- The solution can be implemented with moderate difficulty, estimated at around 3,000 lines of code.
- Using the COCOMO model:
  - Effort: 2.4 * (3)^1.05 = 8 person-months.
  - Time: 5 months.
  - Team size: 2 people.
- The solution is effective with an estimated error rate of 10% for risk calculations.
# Scalability and Usability
- The solution is designed for the worst-case scenario, ensuring scalability.
- Cost scaling is proportional to the square of the distance.
# Installation and Setup
1. Clone the repository
##
    git clone https://github.com/bijeshkumarch/aerothon-6.0/map
    cd map
    python manage.py runserver
2. Configure the database connection and other settings in the configuration files.
3. Start the development server using "python manage.py runserver".
4. Access the platform through the provided URL or open it locally on your web browser.
