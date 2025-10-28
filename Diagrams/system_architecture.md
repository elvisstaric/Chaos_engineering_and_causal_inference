graph LR
%% Load Testing Layer
LT[Locust<br/>Load Testing]

    %% Chaos Tools Layer
    TP[ToxiProxy<br/>Latency Injection]
    ST[stress-ng<br/>Resource Stress]

    %% Microservices Layer (left to right flow)
    US[User Service<br/>:8000]
    CS[Cart Service<br/>:8002]
    IS[Inventory Service<br/>:8001]
    OS[Order Service<br/>:8003]

    %% Data Layer
    DATA[Data Storage<br/>CSV/JSON]

    %% Monitoring Layer
    MON[Monitoring<br/>Prometheus + cAdvisor]

    %% Main flow (clean horizontal)
    LT --> TP
    TP --> US
    US --> CS
    CS --> IS
    CS --> OS
    OS --> IS

    %% Data connections
    IS --> DATA
    OS --> DATA

    %% Monitoring (vertical, no overlaps)
    MON --> US
    MON --> CS
    MON --> IS
    MON --> OS

    %% Chaos injection (separate, dotted)
    ST -.-> US
    ST -.-> CS
    ST -.-> IS
    ST -.-> OS

    %% Styling
    classDef service fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef tool fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef monitor fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef storage fill:#fff3e0,stroke:#e65100,stroke-width:2px

    class US,CS,IS,OS service
    class LT,TP,ST tool
    class MON monitor
    class DATA storage
