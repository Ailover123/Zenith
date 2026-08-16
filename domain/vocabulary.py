from enum import Enum


class Operation(str, Enum):
    READ = "read"
    CREATE = "create"
    MODIFY = "modify"
    EXECUTE = "execute"
    DELEGATE = "delegate"


class Interface(str, Enum):
    API = "api"
    MCP = "mcp"
    BROWSER = "browser"
    DEVICE = "device"
    A2A = "a2a"
