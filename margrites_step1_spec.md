# Margrites — Step 1 Simulator Spec (v2)

> **Board dimensions (clarified):** The game uses **9 columns × 8 rows** — files **a–i** (columns) and ranks **1–8** (rows). In code we’ll use 0-based indexing: rows **0–7** (top→bottom), columns **0–8** (left→right).

This is a beginner-friendly, implementation-ready spec for building a faithful, testable simulator. You can hand this straight to your coding assistant.

---

## Goals (Definition of Done)
A single Python package that can:
1. Represent any legal position and whose turn it is.
2. Generate all **legal single-steps** for the current side (including diagonals).
3. Apply one step, then **resolve instantaneous capture(s)** until stable.
4. Enforce **martyrdom** (you may not move a piece into capture), but allow moves that cause an **ally** to be captured.
5. Track a **turn** of up to **four moves** (and end early if remaining moves are illegal / you’re trapped).
6. Prevent returning a piece to its **start-of-turn square** and prevent **stalling** (begin & end in same square).
7. Handle **scoring** (step off the far edge; consumes one move; piece removed; cannot return).
8. Detect **terminal** (one side has no pieces) and compute **winner** (points; tie-break by captures).
9. Provide unit tests that replay at least one annotated game from the packet and spot-check tricky rules.

---

## Tech Choices (simple & novice-friendly)
- **Language:** Python 3.11+
- **Core libs:** `dataclasses`, `enum`, `typing` (optional later: `numpy` for speed)
- **Dev/test:** `pytest`
- **Coordinates:** 0-based rows 0–7, cols 0–8; helpers for algebraic notation `"a1".."i8"`.

---

## Package Layout
```
margrites/
  __init__.py
  types.py           # enums, dataclasses, coordinate helpers
  state.py           # GameState + cloning/serialization
  rules.py           # move gen, capture resolution, scoring
  engine.py          # step application & turn loop
  io_pgn.py          # (tiny) parser for packet-style notations e5>e6; ...; e8>B++
  tests/
    test_rules.py
    test_turnflow.py
    test_capture_chain.py
    test_scenarios_from_packet.py
```
*(If you prefer, start as a single file and split later.)*

---

## Data Model (`GameState`)
```python
from dataclasses import dataclass
from typing import Tuple, Dict, List

Coord = Tuple[int, int]  # (row, col)

@dataclass
class GameState:
    # 9x8 board stored as 8 rows × 9 columns
    board: List[List[int]]           # 8 rows × 9 cols; 0 empty, +1 current side, -1 opponent
    to_move: int                     # +1 (Black) or -1 (White), or vice versa — pick and be consistent
    moves_left: int                  # 4..0 within the current turn
    start_squares: Dict[Coord, Coord]  # for each moved piece: {current_coord_at_step: start_of_turn_coord}
    score: Dict[int, int]            # {+1: your points, -1: their points}
    captures: Dict[int, int]         # {+1: captured_by_you, -1: captured_by_them}

    def clone(self) -> "GameState": ...
    def serialize(self) -> dict: ...
```

### Invariants
- `moves_left` resets to **4** when `to_move` flips.
- `start_squares` records, per piece, the square it occupied **at the start of this turn**; that piece may **not** return there during the same turn.
- “Touching” means **8-neighbor** adjacency (orthogonal + diagonal).

---

## Rules Implementation Details

### Legal Single-Step Generation
For each of the current side’s pieces:
1. Enumerate up to **8 neighbors** (stay on-board; destination must be empty).
2. Tentatively move there and run **martyrdom**: if the moved piece would be captured **after** the step (see capture rule), **reject** the move.
3. Reject if it returns the piece to **its own start-of-turn square**.
4. If stepping **off the far edge** from your last rank, allow a **scoring step** (consumes one move; piece removed).

**Full movement / trapping:** if any legal step exists you **must** move; if none exist before using all 4 moves, your **turn ends** (forfeit).

### Capture Rule (resolve after each step; may chain)
For any occupied square:
- Let `opp = # of opposing pieces touching that square` and
- `ally = # of allied pieces touching that square + 1` (the piece itself).
- If `opp >= 2 * ally`, that piece is **captured** and removed. After each capture, re-check the board; **cascades** are possible.
- Increment capture counts for tie-breaks.

**Martyrdom edge-case:** a move that would both capture an enemy **and** leave the moving piece captured is **illegal**. (You may still make a move that causes an **ally** to be captured.)

### Scoring
- From your **last rank**, a step **off the board** scores **+1**, consumes **one move**, and **removes** the piece from play (it cannot return).

### Turn / Game End
- A turn ends when `moves_left == 0` **or** you have **no legal steps**.
- The game ends when a side has **no pieces** on the board (all captured or scored), or by **resignation**.
- **Winner**: most **points**; ties broken by **total captures**.

---

## Public API
```python
# types.py
Coord = tuple[int, int]  # (row, col)

# state.py
class GameState:
    def clone(self) -> "GameState": ...
    def serialize(self) -> dict: ...
    @staticmethod
    def from_setup(black: list[Coord], white: list[Coord], to_move=+1) -> "GameState": ...

# rules.py
def legal_steps(state: GameState) -> list[tuple[Coord, Coord] | tuple[Coord, str]]:
    """Return all legal (from,to) steps; scoring steps use to='B++'/'W++'."""

def apply_step(state: GameState, step) -> GameState:
    """Apply one step, resolve captures, update moves_left/turn, return new state."""

def resolve_captures(state: GameState) -> None: ...
def is_terminal(state: GameState) -> bool: ...
def result(state: GameState) -> dict[str, int]:
    """{'points_black':..., 'points_white':..., 'captures_black':..., 'captures_white':...}"""

# engine.py
def play_turn(state: GameState, step_sequence: list[tuple]) -> GameState: ...
def legal_turn_exists(state: GameState) -> bool: ...
```

---

## Testing Plan (pytest)

### Golden tests from the packet
- **Scoring in 4 moves** from `e5`: `e5>e6; e6>e7; e7>e8; e8>B++` (board labels a–i, 1–8).
- **Scoring in 1 move** from `e8`: `e8>B++`.
- **Chain capture** example where a single step eliminates two enemy pieces (capture cascades).
- **Martyrdom**: a tempting capturing step for the mover is illegal if the mover would be captured after the step.
- **Trapping**: construct a position with no legal steps; turn must forfeit.

### Unit tests
- `test_neighbors_allow_diagonals()`
- `test_no_return_to_start_square()`
- `test_no_stalling_same_start_end_square()`
- `test_scoring_consumes_move_and_removes_piece()`
- `test_terminal_and_winner_tie_break_by_captures()`

### Property tests (nice-to-have)
- Any legal step never leaves the **moved** piece immediately capturable.
- After `resolve_captures`, no remaining piece satisfies `opp >= 2*ally`.

---

## Milestone Checklist (build order)
1) **Board & coords**: helpers + initial position loader (8 rows × 9 cols; algebraic notation helpers).
2) **Capture math**: `touching_counts(coord)`, `would_be_captured(...)`.
3) **Single-step legality**: bounds, occupancy, martyrdom, start-square rule, scoring exits.
4) **Step application**: move → resolve capture chain → decrement `moves_left` (or score) → handle trap/full-movement.
5) **Turn logic**: flip `to_move` when needed; reset `moves_left` and `start_squares`.
6) **Endgame & result**: terminal + winner with capture tie-break.
7) **Tests**: implement the fixtures above (including packet examples).

---

### Notes
- Start with a plain **2D list** board for clarity. If/when you need speed, switch to **bitboards**; the logic stays the same.
- Write small, pure helpers (e.g., `neighbors(coord)`, `would_be_captured(state, coord)`).

