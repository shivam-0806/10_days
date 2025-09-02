# TAKNEEK PS – ZENITH
# Submission by Pool Peshwas

## 10 Days Over Kanpur

---

### 1. Introduction

IIT Kanpur, in collaboration with its faculty and the Programming Club, initiated the *“10 Days Over Kanpur”* project. The objective is to design dispatch algorithms for autonomous drones operating in a simulated environment. These drones operate over a 2D grid, interacting with depots, professors, and charging stations, while facing constraints like limited battery and single-package carrying capacity.

The challenge simulates a **10-day period**, represented as `T_max` discrete turns. During this time, the drones must deliver packages efficiently while avoiding operational failures. The success of any solution depends on balancing delivery speed, order prioritization, and energy management.

---

### 2. Problem Description

#### 2.1 Simulation Environment

The IIT Kanpur campus is modeled as a **W × W 2D grid**. Each grid cell `(r, c)` may contain one of the following:

* **Professors (C locations):** Destinations where packages must be delivered.
* **Depots (M locations):** Sources of packages, each maintaining an independent inventory. Depots stock `K` item types.
* **Charging Stations (P locations):** Safe spots where drones recharge their batteries. Multiple drones can use the same station simultaneously.
* **Empty Cells:** Traversable grid space.

Drones move only in four directions (up, down, left, right). Diagonal moves are not permitted. Each movement consumes **1 energy unit** and takes **1 turn**.

#### 2.2 Drones

A fleet of `D` identical drones is available. Each drone is defined by:

* Position `(r, c)`
* Current battery level `B` (max `B_max`)
* Current package (empty or item\_id)

Each drone can carry **one package at a time**. If a drone’s battery depletes to `0` outside a charging station, it is considered **lost**, which incurs heavy penalties.

#### 2.3 Actions per Turn

At each turn, every drone must perform exactly one action:

1. **MOVE U/D/L/R** -> Move one cell (cost: 1 energy)
2. **PICKUP item\_id password** -> Pick an item from a depot (cost: 5 energy)
3. **DROPOFF item\_id** -> Deliver to the correct professor (cost: 5 energy)
4. **CHARGE** -> Recharge battery at a charging station (+R units per turn)
5. **STAY** -> Idle (cost: 1 energy)

Invalid commands default to `STAY`.

#### 2.4 Orders

The simulation provides **N orders** at the start. Each order `i` has:

* Item type
* Origin depot
* Destination professor
* Appear turn
* Deadline turn
* Value (score if completed)

Orders appear dynamically during the simulation (`appear_turn`) and must be completed before their deadlines.

---

### 3. Algorithm Design

Our approach is a **Greedy Nearest-Drone Strategy with Battery Safety Checks**.

#### 3.1 Design Philosophy

* **Reliability over Complexity:** Losing drones incurs heavy penalties, so our algorithm always ensures drones recharge before battery-critical missions.
* **Greedy Allocation:** Orders are allocated to the nearest drone to reduce travel time and energy cost.
* **Safety Cycles:** Each order path ends at a charging station to prevent losses.

#### 3.2 Step-by-Step Algorithm

1. **Initialization:**

   * All drones first move to the nearest charging station and recharge to full.

2. **Order Assignment:**

   * As the orders are given in the input file, first the orders are started in decreasing order.
   * Then like if for the first order a drone A is the most feasible one. Then that drone is reserved for that travel path from t1 to t2.
   * Then we go to the next order, and suppose A was the most feasible in this too, but as it is reserved from t1 to t2, we go to the next feasible drone.
   * We occupy the most feasible drone for the travel and set its status to non-idle for the travel time.
   * If the most feasible drone is not idle, we iterate to the next most feasible until an feasible drone is available.
   * Next iteration is done according to the order with the highest value.
   * If multiple orders are within reach, choose the one with the **earliest deadline**.

3. **Path Computation:**

   * Compute Manhattan distance path:

     ```
     Drone -> Depot -> Professor -> Nearest Charging Station
     ```

4. **Battery Check:**

   * Ensure that battery ≥ (distance\_to\_depot + distance\_to\_professor + distance\_to\_station + action\_costs).
   * If insufficient, send the drone to **charge first**.

5. **Conflict Resolution:**

   * If two drones are assigned the same order, break ties by shortest path, else by drone ID.

6. **Execution:**

   * Drones follow assigned paths turn by turn.

#### 3.3 Pseudocode

```text
// Initialize a schedule for each drone
FOR EACH drone IN all_drones:
    drone.schedule = new List<Reservation>()
END FOR

BEGIN INITIALIZATION
    FOR EACH drone IN all_drones:
        find_path_to_nearest_charging_station(drone)
    END FOR
END INITIALIZATION

FOR t FROM 0 TO T_max-1:

    // --- Planning and Reservation Phase ---
    all_available_orders = get_all_unassigned_active_orders(t)
    
    // Sort orders: high value first, then earliest deadline
    sort all_available_orders by value (descending), then by deadline (ascending)

    FOR EACH order IN all_available_orders:
        // Find the most feasible drone that is available in the future
        potential_drones = find_all_drones()
        sort potential_drones by distance to order.origin_depot (ascending)

        FOR EACH drone IN potential_drones:
            // Calculate when the drone could start this mission
            estimated_start_turn = drone.is_idle ? t : drone.schedule.last_item.end_turn
            
            path = compute_manhattan_path(drone -> order.depot -> order.professor -> nearest_charging_station)
            mission_duration = calculate_path_duration(path)
            estimated_end_turn = estimated_start_turn + mission_duration

            // --- Feasibility Check ---
            has_time_conflict = check_schedule_for_overlap(drone, estimated_start_turn, estimated_end_turn)
            
            // For simplicity, we check current battery. A real system would predict future battery.
            required_battery = calculate_total_energy_cost(path)
            has_sufficient_battery = drone.battery >= required_battery
            
            IF NOT has_time_conflict AND has_sufficient_battery AND estimated_end_turn <= order.deadline:
                // Reserve the drone if it's feasible
                new_reservation = create_reservation(order.id, estimated_start_turn, estimated_end_turn)
                add_to_schedule(drone, new_reservation)
                
                assign_order_to_drone(drone, order, path)
                set_order_status(order, 'assigned')
                BREAK // Move to the next order
            END IF
        END FOR
    END FOR

    // --- Execution Phase ---
    FOR EACH drone IN all_drones:
        current_task = get_task_for_current_turn(drone, t)

        IF current_task is a delivery_mission:
            command = get_next_action_from_path(drone.path)
            issue_command(drone, command)
            
        ELSE IF NOT has_sufficient_battery AND is_idle:
            path_to_charge = find_path_to_nearest_charging_station(drone)
            command = get_next_action_from_path(path_to_charge)
            issue_command(drone, command)
            
        ELSE:
            issue_command(drone, "STAY")
        END IF
    END FOR
    
    print_all_drone_commands()

END FOR
```

---

### 4. Example Walkthrough

Suppose:

* Drone A at (2,2), Battery = 15
* Depot at (4,2) with item X
* Professor at (6,2)
* Charging Station at (7,2)

At turn 5, order X appears:

1. Drone A computes path → `(2,2) → (4,2) → (6,2) → (7,2)`
2. Battery check: Needs 1+2+2+1 moves + 10 energy (pickup + dropoff) = 16.

   * Since current battery = 15 < 16, Drone A goes to **charge first**.
3. After charging, Drone A executes the delivery cycle.

This ensures reliability without drone loss.

---

### 5. Results & Analysis

#### 5.1 Strengths

* **Drone Safety Guaranteed:** No drone is lost due to battery depletion.
* **Timely Deliveries:** Greedy nearest-drone assignment minimizes travel.
* **Simplicity:** Easy to implement and debug in a time-limited contest.

#### 5.2 Limitations

* **No Value Optimization:** Does not prioritize high-value orders.
* **Local Optimality:** Greedy allocation may miss globally better solutions.
* **Path Overlap:** Drones may travel overlapping paths without coordination.

#### 5.3 Complexity Analysis

* Order assignment per turn: `O(D × N_active)`
* Path computation (Manhattan distance): `O(1)` per drone
* Overall per turn: `O(D × N_active)`

Efficient for contest constraints.

---

### 6. Future Improvements

* **Value-Based Prioritization:** Factor in order value along with distance.
* **Multi-Drone Coordination:** Avoid overlapping paths.
* **Lookahead Scheduling:** Plan based on upcoming orders (`appear_turn`).
* **Battery Optimization:** Smarter recharge scheduling to avoid idle time.

---

### 7. Conclusion

The implemented algorithm provides a **baseline strategy** for the “10 Days Over Kanpur” challenge. By focusing on battery safety and nearest-drone delivery allocation, it ensures reliable performance while maintaining simplicity. Although not globally optimal, it establishes a strong foundation for future enhancements such as value optimization and multi-drone coordination.

---

## Decryption

The decryption algorithm can be simplified as follows:
```
from Crypto.Util.number import *
from functools import reduce
import random

def rI(b, mod):
    return getRandomNBitInteger(b) + mod

def cP(a, b, m):
    return a ** m + b

def gP():
    while True:
        a = rI(2048 // 4, 1)
        r = rI(16, random.randint(1, 3))
        p = a**4 + r
        if isPrime(p):
            return (p, r)

def sm():
    e = 65537
    p, a = gP(4)
    q, b = gP(4)
    n = p * q
    return e, n, p, q, a, b
# m=4
def encrypt():
    e, n, p, q, a, b = sm()
    with open("password.txt", "rb") as f:
        password = f.read().strip()
    mLng = bytes_to_long(password)
    c = pow(mLng, e, n)
    with open("out.txt", "w") as out:
        out.write(f"n = {n}\n")
        out.write(f"e = {e}\n")
        out.write(f"c = {c}\n")
        out.write(f"secret1 = {a}\n")
        out.write(f"secret2 = {b}\n")

encrypt()
```

What's happening here is that this RSA is implemented as follows:<br>

N = p * q<br>
p = a^4 + r_1<br>
q = b^4 + r_2<br>



So here a and b are 512 bit and r_1 and r_2 are 16 bit.<br>
What's being returned in the `out.txt` are the values of n, e, c, secret1 and secret 2. secret_1 and secret_2 that are being returned as a and b are actually r_1 and r_2. <br>
Ignoring the values of r_1 and r_2 compared to a^4 and b^4 (16 bit compared to 2048 bit integer), we can approximate N = (a\*b)^4.<br>
Taking S to be equal to the fourth root of N, i.e., `S=N^(1/4)`, and expanding N.<br>

We start with $N = p \cdot q = (a^4 + r_1)(b^4 + r_2)$.<br>

Expanding: $N = (ab)^4 + a^4 r_2 + b^4 r_1 + r_1 r_2$.<br>

Let $S = a \cdot b$.<br>

Then we can form the polynomial: $r_2 X^2 - \bigl(N - S^4 - r_1 r_2\bigr) X + r_1 S^4 = 0$<br>

Now we solve for X, and the fourth of the root as `X = a^4`. <br>
Then we have obtained a from which we can get p as `p = a^4 + r_1` and r_1 is already known. Then we obtain q from `N // p`. Then we get `phi(N) = (p-1)(q-1)`. From there we obtain d as `d\*e = 1 modulo(phi(N))`, from `d = e^-1 modulo(phi(N))`.<br>
Then we can obtain the decrypted message as `m = c^d modulo(N)`.<br>
Then convert the obtained long integer into ascii (utf-8).<br>

Attached in the `scripts` folder is the decryption script as `decrypt.txt`.<br>
