#!/usr/bin/env python3
"""
运行测试脚本
"""
import sys
import subprocess
from pathlib import Path


def run_tests(test_type: str = "all"):
    """运行测试

    Args:
        test_type: 测试类型 (all, unit, integration, e2e)
    """
    project_root = Path(__file__).parent

    if test_type == "all":
        cmd = ["pytest", "-v"]
    elif test_type == "unit":
        cmd = ["pytest", "-v", "-m", "unit"]
    elif test_type == "integration":
        cmd = ["pytest", "-v", "-m", "integration"]
    elif test_type == "e2e":
        cmd = ["pytest", "-v", "-m", "e2e"]
    else:
        print(f"Unknown test type: {test_type}")
        sys.exit(1)

    subprocess.run(cmd, cwd=project_root)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="运行测试")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration", "e2e"],
        default="all",
        help="测试类型"
    )

    args = parser.parse_args()
    run_tests(args.type)
