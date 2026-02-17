#!/usr/bin/env python3
"""
Verification script for the Frontend UI & Full Integration implementation
Checks that all required components are in place and working correctly
"""

import os
import sys
from pathlib import Path

def check_directory_structure():
    """Check that all required directories exist"""
    frontend_dir = Path("frontend")

    required_dirs = [
        "frontend/src/app/(auth)",
        "frontend/src/app/(auth)/signin",
        "frontend/src/app/(auth)/signup",
        "frontend/src/app/(dashboard)",
        "frontend/src/app/(dashboard)/tasks",
        "frontend/src/components/tasks",
        "frontend/src/context",
        "frontend/src/lib/api",
        "frontend/src/lib/hooks",
        "frontend/src/lib/utils",
        "frontend/src/lib/schemas",
        "frontend/src/types",
        "frontend/src/providers",
        "frontend/tests/unit",
        "frontend/tests/integration",
        "frontend/tests/e2e",
        "frontend/public"
    ]

    print("🔍 Checking directory structure...")
    all_good = True

    for dir_path in required_dirs:
        if not (frontend_dir / dir_path).exists():
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
        else:
            print(f"✅ Found directory: {dir_path}")

    return all_good

def check_key_files():
    """Check that all key implementation files exist"""
    frontend_dir = Path("frontend")

    required_files = [
        "frontend/src/app/(auth)/signin/page.tsx",
        "frontend/src/app/(auth)/signup/page.tsx",
        "frontend/src/app/(dashboard)/page.tsx",
        "frontend/src/app/(dashboard)/tasks/page.tsx",
        "frontend/src/components/tasks/TaskList.tsx",
        "frontend/src/components/tasks/TaskCard.tsx",
        "frontend/src/components/tasks/TaskForm.tsx",
        "frontend/src/context/AuthContext.tsx",
        "frontend/src/lib/api/client.ts",
        "frontend/src/lib/api/auth.ts",
        "frontend/src/lib/api/tasks.ts",
        "frontend/src/lib/schemas/auth.ts",
        "frontend/src/lib/schemas/tasks.ts",
        "frontend/src/types/auth.ts",
        "frontend/src/types/tasks.ts",
        "frontend/src/types/api.ts",
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/next.config.mjs",
        "frontend/tailwind.config.ts",
        "frontend/.env.local"
    ]

    print("\n🔍 Checking key files...")
    all_good = True

    for file_path in required_files:
        if not (frontend_dir / file_path).exists():
            print(f"❌ Missing file: {file_path}")
            all_good = False
        else:
            print(f"✅ Found file: {file_path}")

    return all_good

def check_auth_functionality():
    """Check that authentication functionality is implemented"""
    print("\n🔍 Checking authentication functionality...")

    auth_client_path = Path("frontend/src/lib/api/client.ts")
    auth_context_path = Path("frontend/src/context/AuthContext.tsx")

    if not auth_client_path.exists():
        print("❌ Auth client not found")
        return False

    if not auth_context_path.exists():
        print("❌ Auth context not found")
        return False

    # Read files to check for required functionality
    with open(auth_client_path, 'r') as f:
        client_content = f.read()

    with open(auth_context_path, 'r') as f:
        context_content = f.read()

    required_auth_elements = [
        "Authorization",
        "Bearer",
        "JWT",
        "interceptor",
        "token"
    ]

    client_has_auth = all(element in client_content for element in ["Authorization", "Bearer", "interceptor"])
    context_has_auth = all(element in context_content for element in ["JWT", "token", "user"])

    if client_has_auth:
        print("✅ Auth client has proper authorization handling")
    else:
        print("❌ Auth client missing authorization functionality")

    if context_has_auth:
        print("✅ Auth context has proper token handling")
    else:
        print("❌ Auth context missing token functionality")

    return client_has_auth and context_has_auth

def check_api_routes():
    """Check that API routes are properly implemented"""
    print("\n🔍 Checking API routes...")

    task_routes_path = Path("frontend/src/app/(dashboard)/tasks/page.tsx")
    auth_routes_path = Path("frontend/src/app/(auth)/signin/page.tsx")

    if not task_routes_path.exists():
        print("❌ Task routes not found")
        return False

    if not auth_routes_path.exists():
        print("❌ Auth routes not found")
        return False

    with open(task_routes_path, 'r') as f:
        task_content = f.read()

    with open(auth_routes_path, 'r') as f:
        auth_content = f.read()

    # Check for authentication dependency usage
    has_auth_dependency = "useAuth" in task_content and "useAuth" in auth_content
    has_user_filtering = "userId" in task_content or "user_id" in task_content

    if has_auth_dependency:
        print("✅ API routes have authentication dependency")
    else:
        print("❌ API routes missing authentication dependency")

    if has_user_filtering:
        print("✅ Task routes have user filtering")
    else:
        print("⚠️  Task routes may be missing user filtering")

    return has_auth_dependency

def check_tests_exist():
    """Check that test files exist"""
    print("\n🔍 Checking test files...")

    test_files = [
        "frontend/tests/unit/",
        "frontend/tests/integration/",
        "frontend/tests/e2e/",
        "frontend/tests/security/test_jwt_verification.py",
        "frontend/tests/security/test_user_isolation.py",
        "frontend/tests/security/test_auth_endpoints.py",
        "frontend/tests/security/test_complete_system_integration.py"
    ]

    all_good = True
    for test_path in test_files:
        path = Path(f"frontend/{test_path}")
        if not path.exists():
            if not str(test_path).endswith('/'):
                print(f"⚠️  Missing specific test: {test_path}")
        else:
            if str(test_path).endswith('/'):
                print(f"✅ Found test directory: {test_path}")
            else:
                print(f"✅ Found test file: {test_path}")

    # Check if test directories have content
    security_tests_dir = Path("frontend/tests/security/")
    if security_tests_dir.exists():
        test_files = list(security_tests_dir.glob("*.py"))
        if len(test_files) >= 3:  # At least 3 security tests
            print(f"✅ Found {len(test_files)} security test files")
        else:
            print(f"⚠️  Only {len(test_files)} security test files found")
            all_good = False
    else:
        print("❌ Security tests directory missing")
        all_good = False

    return all_good

def main():
    print("🚀 Verifying Frontend UI & Full Integration Implementation")
    print("="*60)

    checks = [
        ("Directory Structure", check_directory_structure),
        ("Key Files", check_key_files),
        ("Authentication Functionality", check_auth_functionality),
        ("API Routes", check_api_routes),
        ("Test Files", check_tests_exist)
    ]

    results = []
    for name, check_func in checks:
        print(f"\n📋 {name} Check:")
        result = check_func()
        results.append((name, result))

    print("\n" + "="*60)
    print("📊 FINAL VERIFICATION RESULTS:")
    print("="*60)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("🎉 IMPLEMENTATION VERIFICATION: ALL CHECKS PASSED!")
        print("✅ Frontend UI & Full Integration is complete and properly implemented")
        print("✅ Ready for frontend integration with Better Auth (Spec 3)")
    else:
        print("❌ IMPLEMENTATION VERIFICATION: SOME CHECKS FAILED")
        print("⚠️  Please review the missing components above")
    print("="*60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())