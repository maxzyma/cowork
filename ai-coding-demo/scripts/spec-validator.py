"""
规范验证器

用于验证规范文档的格式和一致性
实现 CI/CS 管道中的规范验证逻辑
"""

import os
import re
import yaml
import markdown
from pathlib import Path
from typing import Dict, List, Set, Tuple


class SpecValidator:
    """规范文档验证器"""

    def __init__(self, specs_dir: str):
        self.specs_dir = Path(specs_dir)
        self.errors = []
        self.warnings = []

    def validate_all(self) -> bool:
        """验证所有规范"""
        print(f"开始验证规范目录: {self.specs_dir}")

        # 检查目录结构
        self._validate_directory_structure()

        # 验证功能规范
        feature_specs = list(self.specs_dir.glob("features/*.md"))
        print(f"找到 {len(feature_specs)} 个功能规范")
        for spec_file in feature_specs:
            self._validate_feature_spec(spec_file)

        # 验证API规范
        api_specs = list(self.specs_dir.glob("apis/*.md"))
        print(f"找到 {len(api_specs)} 个API规范")
        for spec_file in api_specs:
            self._validate_api_spec(spec_file)

        # 验证数据模型规范
        data_specs = list(self.specs_dir.glob("data-models/*.md"))
        print(f"找到 {len(data_specs)} 个数据模型规范")
        for spec_file in data_specs:
            self._validate_data_model_spec(spec_file)

        # 输出结果
        self._print_results()

        return len(self.errors) == 0

    def _validate_directory_structure(self):
        """验证目录结构"""
        required_dirs = ["features", "apis", "data-models", "templates"]
        for dir_name in required_dirs:
            dir_path = self.specs_dir / dir_name
            if not dir_path.exists():
                self.errors.append(f"缺少必需目录: {dir_name}")

    def _validate_feature_spec(self, spec_file: Path):
        """验证功能规范"""
        content = spec_file.read_text()

        # 检查必需的章节
        required_sections = [
            "## 1. 需求概述",
            "## 2. 功能描述",
            "## 3. 技术规范",
            "## 4. 非功能需求",
            "## 5. 验收标准"
        ]

        for section in required_sections:
            if section not in content:
                self.errors.append(
                    f"{spec_file.name}: 缺少章节 {section}"
                )

        # 检查元数据
        if not re.search(r'\*\*ID\*\*:', content):
            self.warnings.append(
                f"{spec_file.name}: 缺少规范ID"
            )

        if not re.search(r'\*\*状态\*\*:', content):
            self.warnings.append(
                f"{spec_file.name}: 缺少状态"
            )

    def _validate_api_spec(self, spec_file: Path):
        """验证API规范"""
        content = spec_file.read_text()

        # 检查API端点定义
        if not re.search(r'POST|GET|PUT|DELETE|PATCH', content):
            self.errors.append(
                f"{spec_file.name}: 未定义API端点"
            )

        # 检查请求/响应示例
        if "请求格式" not in content:
            self.errors.append(
                f"{spec_file.name}: 缺少请求格式定义"
            )

        if "响应格式" not in content:
            self.errors.append(
                f"{spec_file.name}: 缺少响应格式定义"
            )

    def _validate_data_model_spec(self, spec_file: Path):
        """验证数据模型规范"""
        content = spec_file.read_text()

        # 检查实体定义
        if "Entity:" not in content and "实体:" not in content:
            self.errors.append(
                f"{spec_file.name}: 未定义数据实体"
            )

        # 检查字段定义
        if "字段" not in content and "Fields:" not in content:
            self.errors.append(
                f"{spec_file.name}: 缺少字段定义"
            )

    def _print_results(self):
        """打印验证结果"""
        print("\n" + "="*50)
        print("验证结果")
        print("="*50)

        if self.errors:
            print(f"\n❌ 发现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ 所有规范验证通过！")

        print("="*50)


class SpecCodeSyncChecker:
    """规范-代码同步检查器"""

    def __init__(self, specs_dir: str, src_dir: str):
        self.specs_dir = Path(specs_dir)
        self.src_dir = Path(src_dir)
        self.issues = []

    def check_sync(self) -> bool:
        """检查规范和代码是否同步"""
        print(f"检查规范和代码同步...")

        # 提取所有规范中提到的功能
        spec_features = self._extract_spec_features()

        # 检查实现是否存在
        for feature_id, spec_file in spec_features:
            self._check_feature_implementation(feature_id, spec_file)

        # 输出结果
        self._print_results()

        return len(self.issues) == 0

    def _extract_spec_features(self) -> List[Tuple[str, Path]]:
        """提取规范中定义的功能"""
        features = []
        for spec_file in self.specs_dir.rglob("*.md"):
            content = spec_file.read_text()
            # 提取规范ID
            match = re.search(r'\*\*ID\*\*:\s*([A-Z]+-\d+)', content)
            if match:
                spec_id = match.group(1)
                features.append((spec_id, spec_file))
        return features

    def _check_feature_implementation(self, feature_id: str, spec_file: Path):
        """检查功能是否已实现"""
        # 简化检查：查找对应的测试文件
        test_dir = self.src_dir.parent / "tests"

        # 检查是否有对应的测试文件
        feature_name = feature_id.split("-")[-1].lower()
        test_files = list(test_dir.rglob(f"*{feature_name}*.py"))

        if not test_files:
            self.issues.append(
                f"{feature_id}: 未找到对应的测试文件"
            )

        # 检查是否有实现文件
        impl_files = list(self.src_dir.rglob(f"*{feature_name}*.py"))

        if not impl_files:
            self.issues.append(
                f"{feature_id}: 未找到对应的实现文件"
            )

    def _print_results(self):
        """打印检查结果"""
        print("\n" + "="*50)
        print("同步检查结果")
        print("="*50)

        if self.issues:
            print(f"\n⚠️  发现 {len(self.issues)} 个同步问题:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✅ 规范和代码完全同步！")

        print("="*50)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="规范验证工具")
    parser.add_argument(
        "action",
        choices=["validate", "check-sync", "check-coverage"],
        help="验证操作"
    )
    parser.add_argument(
        "specs_dir",
        help="规范目录路径"
    )
    parser.add_argument(
        "--src-dir",
        default="src/",
        help="源代码目录路径"
    )

    args = parser.parse_args()

    if args.action == "validate":
        validator = SpecValidator(args.specs_dir)
        success = validator.validate_all()
        exit(0 if success else 1)

    elif args.action == "check-sync":
        checker = SpecCodeSyncChecker(args.specs_dir, args.src_dir)
        success = checker.check_sync()
        exit(0 if success else 1)

    elif args.action == "check-coverage":
        # TODO: 实现覆盖率检查
        print("覆盖率检查功能待实现")
        exit(0)


if __name__ == "__main__":
    main()
