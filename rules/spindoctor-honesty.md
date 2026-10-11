# SpinDoctor honesty rule

SpinDoctor is a classical FP64 simulator running on this computer. It is not a quantum computer and gives no quantum
speed-up or advantage. Registers hold 1-298 logical qubits, but one entangled factor is limited to 59 qubits and dense
factors are limited by memory (2^n x 16 bytes); registers wider than 29 qubits sample in basis z only. Histogram counts
come from seeded Born sampling and fluctuate around the exact probabilities. Never present SpinDoctor results as coming
from quantum hardware or as a quantum advantage.
