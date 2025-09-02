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

   * As the orders are given in the input file, we check which of the idle drones are nearest.
   * We occupy the nearest idle drone for the travel and set its status to non-idle for the travel time.
   * If the nearest drone is not idle, we iterate to the next nearest until an idle drone is available.
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
For each turn t:
    Activate new orders
    For each idle drone d:
        If battery < safety_threshold:
            Send to nearest charging station
        Else:
            Assign nearest order with earliest deadline
            Plan path: Depot → Professor → Charging Station
            Execute next move in path
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
