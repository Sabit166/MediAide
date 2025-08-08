"""
Comprehensive test runner for all medical tools in the MediAide project.
Run this file to test all tools at once.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def test_diabetes_tool():
    """Test the diabetes database tool."""
    print("\n" + "="*60)
    print("TESTING DIABETES DATABASE TOOL")
    print("="*60)
    
    try:
        from src.tool.DiabetesDBTool import main as diabetes_main
        diabetes_main()
    except Exception as e:
        print(f"❌ Failed to test diabetes tool: {e}")


def test_cancer_tool():
    """Test the cancer database tool."""
    print("\n" + "="*60)
    print("TESTING CANCER DATABASE TOOL")
    print("="*60)
    
    try:
        from src.tool.CancerDBTool import main as cancer_main
        cancer_main()
    except Exception as e:
        print(f"❌ Failed to test cancer tool: {e}")


def test_heart_disease_tool():
    """Test the heart disease database tool."""
    print("\n" + "="*60)
    print("TESTING HEART DISEASE DATABASE TOOL")
    print("="*60)
    
    try:
        from src.tool.HeartDiseaseDBTool import main as heart_main
        heart_main()
    except Exception as e:
        print(f"❌ Failed to test heart disease tool: {e}")


def test_web_search_tool():
    """Test the medical web search tool."""
    print("\n" + "="*60)
    print("TESTING MEDICAL WEB SEARCH TOOL")
    print("="*60)
    
    try:
        from src.tool.MedicalWebSearchTool import main as web_main
        web_main()
    except Exception as e:
        print(f"❌ Failed to test web search tool: {e}")


def main():
    """Run all tool tests."""
    print("🚀 STARTING MEDIAIDE TOOLS TEST SUITE")
    print("="*60)
    
    # Test each tool
    test_diabetes_tool()
    test_cancer_tool()
    test_heart_disease_tool()
    test_web_search_tool()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
    print("\nTo run individual tests:")
    print("python src/tool/DiabetesDBTool.py")
    print("python src/tool/CancerDBTool.py")
    print("python src/tool/HeartDiseaseDBTool.py")
    print("python src/tool/MedicalWebSearchTool.py")


if __name__ == "__main__":
    main()
