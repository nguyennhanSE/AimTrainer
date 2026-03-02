# Aim Trainer - Reflex & Precision Training

An interactive, Python-based aim training mini-game developed using the **Pygame** library. This project is designed to help players improve their mouse accuracy, reaction time, and tracking skills through dynamic difficulty progression and a rewarding combo system.

**Institution:** Ho Chi Minh City University of Technology (HCMUT)  
**Course:** Game Programming (SEM252)  

---

## 🚀 How to Run

### Prerequisites
- Python 3.x installed on your system.
- `pygame` library.

### Installation & Execution
1. Clone this repository to your local machine:
   ```bash
   git clone <your-github-repo-link>
   cd <repository-folder>
2. Install the required dependencies:

   ```bash
   pip install pygame
   Run the main application file to start the game:
   python app.py

## 🎮 Controls
The game is heavily mouse-dependent, with intuitive keyboard shortcuts for flow management:

### Left Mouse Click (LMB):

  - Shoot/destroy targets during gameplay.

  - Interact with menu buttons (Start, Settings, Pause, Exit,...).

### ESC Key: Pause the game during a live round, or resume from the Pause menu.

### SPACE Key: Quickly restart a new round from the Game Over / Results screen.

## 📜 Game Rules & Mechanics
### Objective
  - Click on the targets as quickly and accurately as possible before they disappear. The game runs for a fixed duration, and the goal is to achieve the highest score and accuracy possible.

### Core Mechanics
  - Spawn & Despawn: Targets appear at random locations. Each target has a Time-To-Live (TTL). If you fail to click it before the TTL expires, it counts as a Miss.

  - Hit Detection: Based on mathematical radius calculation (circle collision) rather than simple bounding boxes, ensuring precise hit registration.

  - Dynamic Difficulty: As the round progresses, the game becomes harder. The targets' TTL decreases (they disappear faster), and their radius shrinks (they become smaller).

### Scoring & Combo System (Bonus Features)
  - Base Score & Reflex Bonus: Hitting a target grants a base score of 100 points. An additional time bonus (up to 50 points) is awarded based on how fast you react.

  - Multiplier Combo: Consecutive hits build up your combo meter. Higher combos yield higher score multipliers.

  - Combo Break: Clicking on an empty space (Miss) or letting a target expire (Timeout) breaks your combo back to zero.
  
  - Persistent Statistics: At the end of each round, your performance (Hits, Misses, Accuracy, Score, Average/Best Reaction Times) is displayed and saved to a local stats.json file. You can view your historical data and recent score graphs in the Statistics menu.


### 📂 Asset Sources
  - The menu music is on Pixabay, the link: "https://pixabay.com/music/electronic-minimal-techno-background-loop-475852/"


