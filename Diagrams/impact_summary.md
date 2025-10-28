%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
subgraph "🔴 HIGHEST IMPACT"
CPU[CPU Stress<br/>Max ATE: 828.24<br/>Latency spike risk]
HT[High Traffic<br/>Max ATE: 161.27<br/>User & Order impact]
end

    subgraph "🟡 MODERATE / 🟢 WEAK"
        BW[Bandwidth Simulation<br/>Max ATE: 80.31<br/>User bandwidth → Order latency]
        LI[Latency Injection<br/>Max ATE: 46.18<br/>Service chain effects]
        RS[Other Resource Stress<br/>Max ATE: 46.59<br/>Memory/I/O/Errors]
    end

    subgraph "Key Findings"
        FINDING1[CPU stress has dominant effect on latency]
        FINDING2[High traffic raises user requests and order errors]
        FINDING3[Bandwidth throttling can strongly affect order latency]
        FINDING4[Latency injection shows moderate impacts]
    end

    CPU --> FINDING1
    HT --> FINDING2
    BW --> FINDING3
    LI --> FINDING4

    %% Styling
    classDef high fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef finding fill:#e3f2fd,stroke:#1976d2,stroke-width:2px

    class CPU,HT high
    class BW,LI,RS moderate
    class FINDING1,FINDING2,FINDING3,FINDING4 finding
