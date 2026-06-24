from src.schemas.infrastructure_status import InfrastructureStatus


INFRASTRUCTURE = [

    {
        "resource_name": "GPU Server",
        "resource_type": "Hardware",
        "quantity": 2,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "Cloud Virtual Machine",
        "resource_type": "Cloud",
        "quantity": 5,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "Windows Server",
        "resource_type": "Server",
        "quantity": 2,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "Linux Server",
        "resource_type": "Server",
        "quantity": 3,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "NAS Storage",
        "resource_type": "Storage",
        "quantity": 1,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "Developer Workstations",
        "resource_type": "Hardware",
        "quantity": 25,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "Android Test Devices",
        "resource_type": "Testing Device",
        "quantity": 10,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "iOS Test Devices",
        "resource_type": "Testing Device",
        "quantity": 4,
        "availability_status": InfrastructureStatus.LIMITED
    },

    {
        "resource_name": "GitHub Enterprise",
        "resource_type": "Software",
        "quantity": 1,
        "availability_status": InfrastructureStatus.AVAILABLE
    },

    {
        "resource_name": "Docker Registry",
        "resource_type": "DevOps",
        "quantity": 1,
        "availability_status": InfrastructureStatus.AVAILABLE
    }

]