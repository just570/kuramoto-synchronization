# Kuramoto Synchronization

A visual simulation of the Kuramoto model using Python, showing how a system of initially independent oscillators can achieve collective synchronization through local interactions.

## About the project

The Kuramoto model is a mathematical model used to study synchronization in systems of coupled oscillators.

In this simulation, each cell represents an oscillator with:

- A random initial phase
- A different natural frequency
- Interactions with its four neighboring cells

At each step, the phase of each oscillator is updated according to its natural frequency and the influence of its neighbors.

As the simulation progresses, the oscillators can become increasingly synchronized.

## Synchronization parameter

The synchronization of the system is measured using the order parameter `R`:

R ≈ 0 → low synchronization

R ≈ 1 → high synchronization

The parameter is calculated from the phases of all oscillators and provides a measure of how aligned they are.

## Visualization

The phase of each oscillator is represented by its color, while its size changes periodically according to its phase.

The graph on the right shows the evolution of the synchronization parameter `R` over time.

![Kuramoto synchronization](kuramoto.gif)

## Technologies

- Python
- NumPy
- Matplotlib
- Pillow

## How to run

Clone the repository and install the required libraries:

```bash
pip install numpy matplotlib pillow
