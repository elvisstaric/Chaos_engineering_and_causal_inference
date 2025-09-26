%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
subgraph "Data Collection & Processing"
PROM[Prometheus<br/>Metrics Collection]
EXP[Chaos Experiments<br/>20 Tests]
JSON[JSON Files<br/>Latency/Errors/Requests]
LOAD[Data Loading<br/>load_all_latency_jsons]
NORM[Endpoint<br/>Normalization]
CLEAN[Data Cleaning<br/>Remove outliers]
AGG[Time Windows<br/>30-second aggregation]

        PROM --> LOAD
        EXP --> LOAD
        JSON --> LOAD
        LOAD --> NORM
        NORM --> CLEAN
        CLEAN --> AGG
    end

    subgraph "Data Preparation"
        MERGE[Data Merging<br/>Timestamp alignment]
        TREAT[Treatment Assignment<br/>0=baseline, 1=chaos]
        COMBINE[Combine Datasets<br/>Baseline + Chaos]

        MERGE --> TREAT
        TREAT --> COMBINE
    end

    subgraph "Causal Analysis"
        MODEL[CausalModel<br/>DoWhy Framework]
        DAG[DAG Definition<br/>Causal Graph]
        IDENTIFY[Identify Effect<br/>Backdoor Criterion]
        ESTIMATE[Estimate Effect<br/>Linear Regression]
        REFUTE[Refutation Test<br/>Placebo Treatment]

        MODEL --> DAG
        DAG --> IDENTIFY
        IDENTIFY --> ESTIMATE
        ESTIMATE --> REFUTE
    end

    subgraph "Results"
        ATE[Average Treatment<br/>Effect ATE]
        P_VAL[p-values<br/>Validation]
        CLASSIFY[Effect Classification<br/>Strong/Moderate/Weak]

        ATE --> P_VAL
        P_VAL --> CLASSIFY
    end

    %% Cross-subgraph connections
    AGG --> MERGE
    COMBINE --> MODEL
    REFUTE --> ATE

    %% Styling
    classDef collection fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef processing fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef preparation fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef modeling fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef results fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class PROM,EXP,JSON collection
    class LOAD,NORM,CLEAN,AGG processing
    class MERGE,TREAT,COMBINE preparation
    class MODEL,DAG,IDENTIFY,ESTIMATE,REFUTE modeling
    class ATE,P_VAL,CLASSIFY results
