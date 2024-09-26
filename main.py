import math
from decimal import Decimal, getcontext

# Set precision for decimal calculations
getcontext().prec = 10000

class CelestialBody:
    def __init__(self, name, mass, radius, angular_velocity):
        self.name = name
        self.mass = Decimal(mass)
        self.radius = Decimal(radius) * Decimal(1000)  # Convert radius from km to meters
        self.angular_velocity = Decimal(angular_velocity)  # Angular velocity in radians per second

# Constants
GRAVITATIONAL_CONSTANT = Decimal('6.67430e-11')
SPEED_OF_LIGHT = Decimal('299792458')

# Define preset celestial bodies with angular velocities
Sun = CelestialBody("Sun", "1.989e30", "696340", "2.865e-6")
Mercury = CelestialBody("Mercury", "3.3011e23", "2439.7", "1.240e-6")
Venus = CelestialBody("Venus", "4.8675e24", "6051.8", "2.99e-7")
Earth = CelestialBody("Earth", "5.972e24", "6371", "7.272e-5")
Mars = CelestialBody("Mars", "6.4171e23", "3389.5", "7.088e-5")
Jupiter = CelestialBody("Jupiter", "1.898e27", "69911", "1.758e-4")
Saturn = CelestialBody("Saturn", "5.683e26", "58232", "1.637e-4")
Uranus = CelestialBody("Uranus", "8.681e25", "25362", "1.012e-4")
Neptune = CelestialBody("Neptune", "1.024e26", "24622", "1.083e-4")
R136a1 = CelestialBody("R136a1", "2.15e32", "3500", "0")

celestial_bodies = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, R136a1]

def calculate_frame_dragging_factor(body, distance_from_center):
    angular_momentum = (Decimal(2 / 5) * body.mass * body.radius**2) * body.angular_velocity
    spin_parameter = angular_momentum / (body.mass * SPEED_OF_LIGHT)
    frame_dragging_angular_velocity = (2 * GRAVITATIONAL_CONSTANT * body.mass * spin_parameter) / (SPEED_OF_LIGHT**2 * (distance_from_center**3 + spin_parameter**2 * distance_from_center + (2 * GRAVITATIONAL_CONSTANT * body.mass * spin_parameter**2) / SPEED_OF_LIGHT**2))
    return Decimal(math.sqrt(Decimal(1) - ((frame_dragging_angular_velocity * body.radius / SPEED_OF_LIGHT)**2)))

# Function to calculate Schwarzschild radius
def calculate_schwarzschild_radius(body):
    return (2 * GRAVITATIONAL_CONSTANT * body.mass) / (SPEED_OF_LIGHT**2)

# First frame of reference
time_interval = Decimal(input("time interval (in hours): ")) * Decimal('3600')  # Convert hours to seconds

print("First frame of reference")
distance_from_surface_1 = Decimal(input("Distance from surface (in km): ")) * Decimal('1000')  # Convert to meters

print("\nPreset available:\nCustom [0]\nSun [1]\nMercury [2]\nVenus [3]\nEarth [4]\nMars [5]\nJupiter [6]\nSaturn [7]\nUranus [8]\nNeptune [9]\nR136a1 (Star) [10]\n")
celestial_body_choice = input("Enter '0' for Custom or choose a preset (1-10): ")

if celestial_body_choice == "0":
    custom_mass = input("Enter mass for Custom (in kg): ")
    custom_radius = input("Enter radius for Custom (in km): ")
    angular_velocity = input("Angular velocity (in radians per seconds): ")
    selected_body_1 = CelestialBody("Custom", custom_mass, custom_radius, angular_velocity)
else:
    selected_body_1 = celestial_bodies[int(celestial_body_choice) - 1]

total_distance_1 = selected_body_1.radius + distance_from_surface_1

# Check if within Schwarzschild radius
schwarzschild_radius_1 = calculate_schwarzschild_radius(selected_body_1)
if total_distance_1 <= schwarzschild_radius_1:
    print("Error: The total distance is within the Schwarzschild radius for the first frame of reference.")
    exit()

# Gravitational Time Dilation Factor
def gravitational_time_dilation_factor(mass, distance):
    return Decimal(math.sqrt(1 - (2 * GRAVITATIONAL_CONSTANT * mass) / (distance * SPEED_OF_LIGHT**2)))

gravitational_time_dilation_1 = gravitational_time_dilation_factor(selected_body_1.mass, total_distance_1)

# Calculate orbital velocity
if (distance_from_surface_1 / 1000) >= 100:
    orbital_velocity_1 = Decimal(math.sqrt(GRAVITATIONAL_CONSTANT * selected_body_1.mass / total_distance_1))
elif (distance_from_surface_1 / 1000) < 100:
    orbital_velocity_1 = selected_body_1.angular_velocity * selected_body_1.radius
else:
    print("Err: incorrect distance")
    orbital_velocity_1 = 0

# Orbital velocity time dilation factor
orbital_time_dilation_factor_1 = Decimal(math.sqrt(1 - (orbital_velocity_1**2 / SPEED_OF_LIGHT**2)))

# Frame dragging factor
frame_dragging_factor_1 = calculate_frame_dragging_factor(selected_body_1, total_distance_1)

# Second frame of reference
print("\nSecond frame of reference")
distance_from_surface_2 = Decimal(input("Distance from surface (in km): ")) * Decimal('1000')  # Convert to meters

celestial_body_choice = input("Enter '0' for Custom or choose a preset (1-9): ")

if celestial_body_choice == "0":
    custom_mass = input("Enter mass for Custom (in kg): ")
    custom_radius = input("Enter radius for Custom (in km): ")
    angular_velocity = input("Angular velocity (in radians per seconds): ")
    selected_body_2 = CelestialBody("Custom", custom_mass, custom_radius, angular_velocity)
else:
    selected_body_2 = celestial_bodies[int(celestial_body_choice) - 1]

total_distance_2 = selected_body_2.radius + distance_from_surface_2

# Check if within Schwarzschild radius
schwarzschild_radius_2 = calculate_schwarzschild_radius(selected_body_2)
if total_distance_2 <= schwarzschild_radius_2:
    print("Error: The total distance is within the Schwarzschild radius for the second frame of reference.")
    exit()

gravitational_time_dilation_2 = gravitational_time_dilation_factor(selected_body_2.mass, total_distance_2)

# Calculate orbital velocity
if (distance_from_surface_2 / 1000) >= 100:
    orbital_velocity_2 = Decimal(math.sqrt(GRAVITATIONAL_CONSTANT * selected_body_2.mass / total_distance_2))
elif (distance_from_surface_2 / 1000) < 100:
    orbital_velocity_2 = selected_body_2.angular_velocity * selected_body_2.radius
else:
    print("Err: incorrect distance")
    orbital_velocity_2 = 0

# Orbital velocity time dilation factor
orbital_time_dilation_factor_2 = Decimal(math.sqrt(1 - (orbital_velocity_2**2 / SPEED_OF_LIGHT**2)))

# Frame dragging factor
frame_dragging_factor_2 = calculate_frame_dragging_factor(selected_body_2, total_distance_2)

# Total Time Dilation Factor
total_time_dilation_1 = gravitational_time_dilation_1 * orbital_time_dilation_factor_1 * frame_dragging_factor_1
total_time_dilation_2 = gravitational_time_dilation_2 * orbital_time_dilation_factor_2 * frame_dragging_factor_2

# Time Difference
time_difference = time_interval * (total_time_dilation_1 - total_time_dilation_2)

# Format time difference in a human-readable format
def format_time_difference(time_diff):
    abs_diff = abs(time_diff)
    if abs_diff >= 86400:
        formatted = f"{abs(time_diff) / 86400:.6f} days"
    elif abs_diff >= 3600:
        formatted = f"{abs(time_diff) / 3600:.6f} hours"
    elif abs_diff >= 60:
        formatted = f"{abs(time_diff) / 60:.6f} minutes"
    elif abs_diff >= 1:
        formatted = f"{abs(time_diff):.6f} seconds"
    elif abs_diff >= Decimal('1e-3'):
        formatted = f"{abs(time_diff) * Decimal('1e3'):.6f} milliseconds"
    elif abs_diff >= Decimal('1e-6'):
        formatted = f"{abs(time_diff) * Decimal('1e6'):.6f} microseconds"
    elif abs_diff >= Decimal('1e-9'):
        formatted = f"{abs(time_diff) * Decimal('1e9'):.6f} nanoseconds"
    elif abs_diff >= Decimal('1e-12'):
        formatted = f"{abs(time_diff) * Decimal('1e12'):.6f} picoseconds"
    else:
        formatted = f"{abs(time_diff) * Decimal('1e12'):.6f} picoseconds"  # Catch-all for any extremely small values
    return formatted

# Print summary statement
time_diff_formatted = format_time_difference(time_difference)
print("")
print(f"{time_interval / Decimal('3600')} hours in the first frame of reference is  {time_diff_formatted} {'slower' if time_difference < 0 else 'faster'} in the second frame of reference.")
