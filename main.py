import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
sim_len = 20  # [s] Total simulation time
tps = 60  # Steps per second

# Rocket parameters
m = 0.2  # [kg] Rocket mass (without fuel)
r_rocket = 0.03  # [m] Rocket radius
r_parachute = 0.1  # [m] Parachute radius
t_parachute = 5  # [s] Parachute deploy time

# Thrust function
def thrust(t):
    peak = 5  # Peak thrust [N]
    avr = 3   # Average thrust [N]
    t_peak = 0.5  # Time to peak thrust [s]
    t_burn = 5  # Total burn time [s]
    m_motor_start = 0.05  # [kg] Initial fuel mass

    f_motor = 0
    m_motor = 0

    if t <= t_peak:
        f_motor = (t / t_peak) * peak
    elif t_peak < t <= 2 * t_peak:
        f_motor = peak - (t - t_peak) * (peak - avr) / t_peak
    elif 2 * t_peak < t <= t_burn - avr / 3:
        f_motor = avr
    elif t_burn - avr / 3 < t <= t_burn:
        f_motor = 3 * (t_burn - t)

    if t <= t_burn:
        m_motor = m_motor_start * (1 - t / t_burn)

    return f_motor, m_motor

# Drag force function
def drag(v, parachute=False):

    p = 1.293 # [kg/m^3] densety of air

    if parachute:
        cd = 1.75
        a = np.pi * r_parachute**2
    else:
        cd = 0.1
        a = np.pi * r_rocket**2

    return -0.5 * p * v**2 * cd * a * np.sign(v)

# Initialize simulation variables
alt = 0
v = 0

altitudes = []
velocities = []
thrusts = []
drags = []
masses = []

for step in range(sim_len * tps):
    t = step / tps

    f_motor, m_motor = thrust(t)

    # Check if the parachute is deployd
    parachute = t > t_parachute

    f_drag = drag(v, parachute)
    f_net = f_drag + f_motor

    a_gravity = -9.81
    a = a_gravity + f_net / (m + m_motor)

    # Update velocity
    v += a / tps

    # Update altitude after velocity change
    alt += v / tps

    # Prevent negative altitude
    if alt <= 0:
        alt = 0
        if v < 0:
            v = 0
    
    # Store data for plotting
    altitudes.append(alt)
    velocities.append(v)
    thrusts.append(f_motor)
    drags.append(f_drag)
    masses.append(m + m_motor)



time = np.linspace(0, sim_len, sim_len * tps)

# Create figure (without extra subplots)
fig = plt.figure(figsize=(12, 9.5))

# Altitude plot (takes 2/3 of the figure height)
ax_alt = plt.subplot2grid((4, 2), (0, 0), colspan=2, rowspan=2)
ax_alt.plot(time, altitudes, 'b', label="Altitude")
ax_alt.set_ylabel("Altitude (m)")
ax_alt.set_title("Rocket Flight Simulation")
ax_alt.grid()
ax_alt.legend()

# Velocity plot (bottom left)
ax_vel = plt.subplot2grid((4, 2), (2, 0))
ax_vel.plot(time, velocities, 'r', label="Velocity")
ax_vel.set_ylabel("Velocity (m/s)")
ax_vel.grid()
ax_vel.legend()

# Thrust plot (bottom right)
ax_thrust = plt.subplot2grid((4, 2), (2, 1))
ax_thrust.plot(time, thrusts, 'g', label="Thrust")
ax_thrust.set_ylabel("Thrust (N)")
ax_thrust.grid()
ax_thrust.legend()

# Drag force plot (bottom left)
ax_drag = plt.subplot2grid((4, 2), (3, 0))
ax_drag.plot(time, drags, 'purple', label="Drag")
ax_drag.set_xlabel("Time (s)")
ax_drag.set_ylabel("Drag (N)")
ax_drag.grid()
ax_drag.legend()

# Mass plot (bottom right)
ax_mass = plt.subplot2grid((4, 2), (3, 1))
ax_mass.plot(time, masses, 'orange', label="Mass")
ax_mass.set_xlabel("Time (s)")
ax_mass.set_ylabel("Mass (kg)")
ax_mass.grid()
ax_mass.legend()

# Adjust layout
plt.tight_layout()

# Center the plot window
manager = plt.get_current_fig_manager()
try:
    manager.window.wm_geometry("+{}+{}".format(
        (manager.window.winfo_screenwidth() // 2) - 600,
        (manager.window.winfo_screenheight() // 2) - 535
    ))
except AttributeError:
    pass

# Show the plot
plt.show()