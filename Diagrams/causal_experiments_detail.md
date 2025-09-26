graph LR
%% Experiment Types
subgraph "Chaos Experiments (20 Total)"
HT[High Traffic<br/>3 experiments]
LI[Latency Injection<br/>4 experiments]
TS[Timeout Simulation<br/>4 experiments]
RS[Resource Stress<br/>12 experiments]
end

    %% Metrics Collected
    subgraph "Metrics Per Service"
        REQ[Request Rate<br/>HTTP requests/endpoint]
        LAT[Response Latency<br/>Average response time]
        ERR[Error Rate<br/>Failed requests/endpoint]
    end

    %% Causal Models
    subgraph "Causal Models (20 Total)"
        DIRECT[Direct Effect Models<br/>15 models]
        MEDIATED[Mediated Effect Models<br/>5 models]
    end

    %% Model Examples
    subgraph "Example Models"
        M1[Model 1: High Traffic → User Requests<br/>ATE = 164.46]
        M2[Model 2: High Traffic → Cart Latency<br/>ATE = -0.009]
        M3[Model 3: User Latency → Cart Requests<br/>ATE = -26.88]
        M4[Model 16: High Traffic → User → Cart → Order → Inventory<br/>ATE = 38.82]
    end

    %% Analysis Process
    subgraph "Analysis Process"
        PREP[Data Preprocessing<br/>30-second windows]
        CAUSAL[CausalModel Creation<br/>Treatment + Outcome + DAG]
        BACKDOOR[Backdoor Adjustment<br/>Linear Regression]
        PLACEBO[Placebo Refutation<br/>p-value validation]
    end

    %% Results Classification
    subgraph "Effect Classification"
        STRONG[Strong Effect<br/>ATE > 50]
        MODERATE[Moderate Effect<br/>ATE 10-50]
        WEAK[Weak Effect<br/>ATE < 10]
    end

    %% Connections
    HT --> REQ
    LI --> LAT
    TS --> ERR
    RS --> REQ

    REQ --> DIRECT
    LAT --> DIRECT
    ERR --> DIRECT

    REQ --> MEDIATED
    LAT --> MEDIATED
    ERR --> MEDIATED

    DIRECT --> M1
    DIRECT --> M2
    DIRECT --> M3
    MEDIATED --> M4

    M1 --> PREP
    M2 --> PREP
    M3 --> PREP
    M4 --> PREP

    PREP --> CAUSAL
    CAUSAL --> BACKDOOR
    BACKDOOR --> PLACEBO

    PLACEBO --> STRONG
    PLACEBO --> MODERATE
    PLACEBO --> WEAK

    %% Styling
    classDef experiment fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef metric fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef model fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef example fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef process fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef result fill:#e0f2f1,stroke:#00695c,stroke-width:2px

    class HT,LI,TS,RS experiment
    class REQ,LAT,ERR metric
    class DIRECT,MEDIATED model
    class M1,M2,M3,M4 example
    class PREP,CAUSAL,BACKDOOR,PLACEBO process
    class STRONG,MODERATE,WEAK result
