# 101 Okey Tile Arrangement Optimization System

An advanced combinatorial optimization system designed to automatically arrange a complex and disordered hand of 101 Okey tiles based on game rules (color and numerical harmony) to maximize the total score.

## Project Overview
In 101 Okey, the permutation possibilities of tiles on the rack are extremely high, making it a classic **NP-Hard combinatorial optimization problem**. This project implements meta-heuristic algorithms and mathematical modeling to solve this problem efficiently in real-time.

## Core Methods & Algorithms

### 1. Simulated Annealing (SA)
The primary optimization engine uses the **Simulated Annealing** algorithm inspired by metallurgy. It allows the system to accept worse solutions with a probability ($P=e^{\Delta/T}$) at high temperatures, enabling it to escape local optima and successfully converge on the **global optimum**.
* **Cooling Rate:** $0.9995$

### 2. Custom Advanced Techniques
* **Smart Neighbor Generation (Smart Magnet):** Instead of fully random swapping, the algorithm has a 70% probability to pick a tile and place it next to a compatible neighbor (same number or sequential). This drastically reduces the convergence time.
* **Dynamic Sorter (Smart Sorter):** Automatically sorts ongoing tile groups in ascending order (e.g., converting a messy `3-5-4` meld instantly into `3-4-5`), preventing score penalties during execution.

## Mathematical Model (0-1 Integer Programming)

### Decision Variables
$$X_{i,j} = \begin{cases} 1, & \text{if tile } i \text{ is assigned to slot } j \\ 0, & \text{otherwise} \end{cases}$$

### Objective Function
$$\text{Maximize } Z = \sum_{i=1}^{106} \sum_{j=1}^{24} (P_{ij} \cdot X_{ij}) - \sum_{i=1}^{106} \sum_{j=1}^{24} (C_{ij} \cdot X_{ij})$$
$$\text{Maximize } Z = \sum(\text{Meld Scores}) - \sum(\text{Penalty Costs})$$

### Constraints
* **Single Assignment:** $\sum_{i=1}^{106} X_{ij} \le 1 \quad \forall j$ (Max 1 tile per slot)
* **Tile Existence:** $\sum_{j=1}^{24} X_{ij} = 1 \quad \forall i$ (Every hand tile must be placed)
* **Integrity:** $X_{ij} \in \{0,1\}$

## Tech Stack
* **Language:** Python 3
* **Paradigm:** Object-Oriented Programming (OOP)
* **Libraries:** Tkinter / Custom GUI Components

## Features
* **Randomize:** Instantly distribute random tile sets to the rack.
* **Manual Intervention:** Users can dynamically add or delete tiles.
* **AI Optimization:** Triggering the "Optimize" button resolves the board within milliseconds.
