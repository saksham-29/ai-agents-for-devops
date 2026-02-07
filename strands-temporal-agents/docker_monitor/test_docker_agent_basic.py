import sys

def test_imports():
    print("Testing imports...")
    try:
        import docker_utils
        print("✓ docker_utils imported successfully")
        
        assert hasattr(docker_utils, 'ContainerInfo')
        assert hasattr(docker_utils, 'HealthStatus')
        assert hasattr(docker_utils, 'OperationResult')
        print("✓ Data models found")
        
        assert hasattr(docker_utils, 'DockerConnectionError')
        assert hasattr(docker_utils, 'ContainerNotFoundError')
        print("✓ Custom exceptions found")
        
        assert hasattr(docker_utils, 'DockerClientWrapper')
        print("✓ DockerClientWrapper class found")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_data_models():
    print("\nTesting data models...")
    try:
        from docker_utils import ContainerInfo, HealthStatus, OperationResult
        from datetime import datetime
        
        container = ContainerInfo(
            id="abc123",
            name="test-container",
            status="running",
            image="nginx:latest",
            created=datetime.now()
        )
        assert container.to_dict() is not None
        assert container.format_summary() is not None
        print("✓ ContainerInfo works")
        
        health = HealthStatus(
            container_name="test-container",
            is_healthy=True,
            status="running"
        )
        assert health.to_dict() is not None
        assert health.format_summary() is not None
        print("✓ HealthStatus works")
        
        result = OperationResult(
            operation="test",
            success=True,
            data="test data"
        )
        assert result.to_dict() is not None
        assert result.format_summary() is not None
        print("✓ OperationResult works")
        
        return True
    except Exception as e:
        print(f"✗ Data model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_structure():
    print("\nTesting agent structure...")
    try:
        import docker_agent
        
        assert hasattr(docker_agent, 'get_container_status')
        assert hasattr(docker_agent, 'check_container_health')
        assert hasattr(docker_agent, 'get_container_logs')
        assert hasattr(docker_agent, 'restart_container')
        print("✓ All tools defined")
        
        assert hasattr(docker_agent, 'create_agent')
        assert hasattr(docker_agent, 'main')
        print("✓ Agent creation and main functions found")
        
        return True
    except Exception as e:
        print(f"✗ Agent structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Docker Agent Basic Validation Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Data Models", test_data_models()))
    results.append(("Agent Structure", test_agent_structure()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! Code structure is valid.")
        print("\nNote: Docker daemon is not running, so the agent cannot")
        print("connect to Docker. To test with real containers:")
        print("  1. Start Docker Desktop")
        print("  2. Run: python docker_agent.py")
        return 0
    else:
        print("\n✗ Some tests failed. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
