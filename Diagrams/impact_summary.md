%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
subgraph "🔴 HIGHEST IMPACT"
HT[High Traffic<br/>Max ATE: 164.46<br/>User Service Vulnerability]
TS[Timeout Simulation<br/>Max ATE: -94.84<br/>Cart Service Critical]
end

    subgraph "🟡 MODERATE IMPACT"
        LI[Latency Injection<br/>Max ATE: -26.88<br/>Service Chain Effects]
        RS[Resource Stress<br/>Max ATE: 26.92<br/>Memory/I/O Effects]
    end

    subgraph "Key Findings"
        FINDING1[High Traffic = Biggest Risk<br/>Strong effects on core services]
        FINDING2[Timeouts = Critical Failure<br/>Strong negative impact on user flow]
        FINDING3[Latency = Moderate Risk<br/>Service dependency issues]
        FINDING4[Resource Stress = Lowest Risk<br/>Limited operational impact]
    end

    HT --> FINDING1
    TS --> FINDING2
    LI --> FINDING3
    RS --> FINDING4

    %% Styling
    classDef high fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef finding fill:#e3f2fd,stroke:#1976d2,stroke-width:2px

    class HT,TS high
    class LI,RS moderate
    class FINDING1,FINDING2,FINDING3,FINDING4 finding
