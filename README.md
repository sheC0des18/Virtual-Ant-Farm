# 🐜 Virtual Ant Farm Multi-Agent System

The Virtual Ant Farm Multi-Agent System simulates and analyses the behavior of ant colonies in a dynamic, grid-based environment. The project demonstrates how autonomous agents (ants) interact with their surroundings to collect resources, avoid obstacles, and collaborate effectively using shared memory.

---

## 📖 Project Overview

### **Goals**:
- Develop a dynamic 2D environment with resources and obstacles.
- Simulate ant-like behaviors, including resource collection and adaptive movement.
- Model colony-level collaboration through shared memory and pheromone trails.
- Provide a clear, dynamic visualization of ant movements and colony activities.

[Explore the Repository](https://github.com/sheC0des18/Virtual-Ant-Farm)

---

## 🚀 Features

### **Dynamic Environment**:
- **Grid-Based Setup**: The simulation environment is designed as a configurable 2D grid with:
  - **Nests**: Serving as home bases for ant colonies.
  - **Resources**: Food and water scattered randomly across the grid.
  - **Obstacles**: Randomly placed barriers.
- **Colour and Sprite Representation**:
  - White: Empty cells.
  - Green: Food resources.
  - Blue: Water resources.
  - Gray: Obstacles.
  - Yellow & Red: Colony nests.
  - Purple & Orange: Ants belonging to colonies.
  - Pale Brown/Pink: Pheromone trails.

### **Agent Behavior**:
- **Decision-Making Rules**:
  - Collect resources (food/water).
  - Return resources to nests for rewards.
  - Avoid obstacles.
  - Explore unvisited cells for higher rewards.
- **Reward System**:
  - Collect food: +10 points.
  - Collect water: +5 points.
  - Return to nest: +5 points.
  - Hit obstacle: -5 points.
  - Visit new cells: +2 points.
  - Revisit cells: -2 points.

### **Colony Collaboration**:
- Shared memory tracks visited cells to optimize exploration.
- Pheromone trails guide ants toward optimal paths, with trails decaying over time.

### **Simulation Enhancements**:
- **Pheromone Trails**: Dynamic, visual representation of paths.
- **Sprites for Ants and Nests**: Improved clarity and aesthetics.
- **Real-Time Stats**: Display of resources collected and colony scores.

---

## 🛠 Implementation Phases

### **Phase 1: Basic Environment Setup**
- Configurable 2D grid with nests, resources, and obstacles.
- Random initialization of ants and resources.

### **Phase 2: Agent Behavior**
- Movement and decision-making guided by the reward system.
- Collaborative memory to reduce redundant exploration.

### **Phase 3: Visual and Functional Enhancements**
- Visual pheromone trails for pathfinding.
- Adaptive reward systems for exploration and resource collection.

---

## 🎯 Experimental Results

- **Colony 0**: Collected 3 resources, scoring 15 points.
- **Colony 1**: Collected 11 resources, scoring 55 points.
- The inclusion of pheromone trails and shared memory significantly improved efficiency.

---

## 🌟 Challenges and Solutions

- **Boundary Errors**: Implemented boundary checks to prevent ants from moving outside the grid.
- **High Computational Demand**: Optimized grid updates and memory usage for large environments.
- **Reward Balancing**: Adjusted the system to encourage exploration and penalize redundancy.

---

## 📈 Future Enhancements

- **Visual Refinements**: Improve graphical representation of nests, resources, and obstacles.
- **Dynamic Obstacles**: Introduce obstacles that change positions during simulation.
- **Resource Prioritization**: Add multi-resource types with varying values.
- **User Interactivity**: Allow users to place resources, obstacles, or agents in real time.

---

## 📌 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/sheC0des18/Virtual-Ant-Farm.git
   cd Virtual-Ant-Farm
