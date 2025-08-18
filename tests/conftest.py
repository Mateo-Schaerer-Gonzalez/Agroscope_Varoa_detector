"""
Pytest configuration for the test suite.
- Ensures the repository root is importable (so tests can import project modules).
- Sets a non-interactive matplotlib backend for headless/CI runs.
"""
import os
import sys

# Add repo root to sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Use headless matplotlib backend to avoid GUI requirements in tests
try:
    import matplotlib
    matplotlib.use("Agg", force=True)
except Exception:
    pass
