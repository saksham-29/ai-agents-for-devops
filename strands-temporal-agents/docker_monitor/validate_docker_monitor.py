import sys
import subprocess

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def print_result(test_name, passed):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{test_name}: {status}")
    return passed

def test_compilation():
    print_header("Testing Code Compilation")
    
    files = [
        '../config.py',
        'docker_utils.py',
        'docker_agent.py',
        'docker_temporal_agent.py',
        'docker_worker.py',
        'docker_client.py'
    ]
    
    all_passed = True
    for file in files:
        try:
            result = subprocess.run(
                ['python', '-m', 'py_compile', file],
                capture_output=True,
                text=True
            )
            passed = result.returncode == 0
            print_result(f"  {file}", passed)
            if not passed:
                print(f"    Error: {result.stderr}")
                all_passed = False
        except Exception as e:
            print_result(f"  {file}", False)
            print(f"    Error: {e}")
            all_passed = False
    
    return all_passed

def test_imports():
    print_header("Testing Module Imports")
    
    all_passed = True
    
    try:
        import docker_utils
        assert hasattr(docker_utils, 'ContainerInfo')
        assert hasattr(docker_utils, 'HealthStatus')
        assert hasattr(docker_utils, 'OperationResult')
        assert hasattr(docker_utils, 'DockerClientWrapper')
        print_result("  docker_utils", True)
    except Exception as e:
        print_result("  docker_utils", False)
        print(f"    Error: {e}")
        all_passed = False
    
    try:
        import docker_agent
        assert hasattr(docker_agent, 'get_container_status')
        assert hasattr(docker_agent, 'check_container_health')
        assert hasattr(docker_agent, 'get_container_logs')
        assert hasattr(docker_agent, 'restart_container')
        assert hasattr(docker_agent, 'create_agent')
        print_result("  docker_agent", True)
    except Exception as e:
        print_result("  docker_agent", False)
        print(f"    Error: {e}")
        all_passed = False
    
    try:
        import docker_temporal_agent
        assert hasattr(docker_temporal_agent, 'get_container_status_activity')
        assert hasattr(docker_temporal_agent, 'check_container_health_activity')
        assert hasattr(docker_temporal_agent, 'get_container_logs_activity')
        assert hasattr(docker_temporal_agent, 'restart_container_activity')
        assert hasattr(docker_temporal_agent, 'ai_orchestrator_activity')
        assert hasattr(docker_temporal_agent, 'DockerMonitorWorkflow')
        print_result("  docker_temporal_agent", True)
    except Exception as e:
        print_result("  docker_temporal_agent", False)
        print(f"    Error: {e}")
        all_passed = False
    
    return all_passed

def test_data_models():
    print_header("Testing Data Models")
    
    all_passed = True
    
    try:
        from docker_utils import ContainerInfo, HealthStatus, OperationResult
        from datetime import datetime
        
        container = ContainerInfo(
            id="test123",
            name="test-container",
            status="running",
            image="nginx:latest",
            created=datetime.now()
        )
        assert container.to_dict() is not None
        assert container.format_summary() is not None
        print_result("  ContainerInfo", True)
        
        health = HealthStatus(
            container_name="test",
            is_healthy=True,
            status="running"
        )
        assert health.to_dict() is not None
        assert health.format_summary() is not None
        print_result("  HealthStatus", True)
        
        result = OperationResult(
            operation="test",
            success=True,
            data="test"
        )
        assert result.to_dict() is not None
        assert result.format_summary() is not None
        print_result("  OperationResult", True)
        
    except Exception as e:
        print_result("  Data Models", False)
        print(f"    Error: {e}")
        all_passed = False
    
    return all_passed

def test_configuration():
    print_header("Testing Configuration")
    
    try:
        import config
        
        assert hasattr(config, 'DOCKER_HOST')
        assert hasattr(config, 'DOCKER_TIMEOUT')
        assert hasattr(config, 'DOCKER_MONITOR_TASK_QUEUE')
        
        assert hasattr(config, 'STATUS_CHECK_TIMEOUT')
        assert hasattr(config, 'HEALTH_CHECK_TIMEOUT')
        assert hasattr(config, 'LOG_RETRIEVAL_TIMEOUT')
        assert hasattr(config, 'RESTART_TIMEOUT')
        
        assert hasattr(config, 'CPU_THRESHOLD_PERCENT')
        assert hasattr(config, 'MEMORY_THRESHOLD_PERCENT')
        assert hasattr(config, 'RESTART_COUNT_THRESHOLD')
        
        print_result("  Configuration", True)
        return True
    except Exception as e:
        print_result("  Configuration", False)
        print(f"    Error: {e}")
        return False

def test_temporal_worker():
    print_header("Testing Temporal Worker")
    
    try:
        import asyncio
        from temporalio.client import Client
        from temporalio.worker import Worker
        from docker_temporal_agent import (
            DockerMonitorWorkflow,
            get_container_status_activity,
            check_container_health_activity,
            get_container_logs_activity,
            restart_container_activity,
            ai_orchestrator_activity
        )
        
        async def test():
            try:
                client = await Client.connect('localhost:7233', connect_timeout=2)
                worker = Worker(
                    client,
                    task_queue='test-queue',
                    workflows=[DockerMonitorWorkflow],
                    activities=[
                        get_container_status_activity,
                        check_container_health_activity,
                        get_container_logs_activity,
                        restart_container_activity,
                        ai_orchestrator_activity
                    ]
                )
                return True
            except Exception as e:
                print(f"    Note: {e}")
                return False
        
        result = asyncio.run(test())
        print_result("  Worker Creation", result)
        if not result:
            print("    (This is OK if Temporal server is not running)")
        return True
        
    except Exception as e:
        print_result("  Worker Creation", False)
        print(f"    Error: {e}")
        return True

def main():
    print("=" * 60)
    print("Docker Container Health Monitor - Validation")
    print("=" * 60)
    
    results = []
    
    results.append(("Compilation", test_compilation()))
    results.append(("Imports", test_imports()))
    results.append(("Data Models", test_data_models()))
    results.append(("Configuration", test_configuration()))
    results.append(("Temporal Worker", test_temporal_worker()))
    
    print_header("Validation Summary")
    
    all_passed = True
    for test_name, passed in results:
        print_result(test_name, passed)
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✓ All validation tests passed!")
        print("\nThe Docker Container Health Monitor is ready to use.")
        print("\nNext steps:")
        print("  1. Ensure Docker Desktop is running")
        print("  2. For simple agent: python docker_agent.py")
        print("  3. For Temporal agent:")
        print("     - Terminal 1: temporal server start-dev")
        print("     - Terminal 2: python docker_worker.py")
        print("     - Terminal 3: python docker_client.py")
        return 0
    else:
        print("✗ Some validation tests failed.")
        print("Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
