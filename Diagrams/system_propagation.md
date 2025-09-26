%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
subgraph "Service Architecture"
US[User Service<br/>:8000]
CS[Cart Service<br/>:8002]
IS[Inventory Service<br/>:8001]
OS[Order Service<br/>:8003]
end

    subgraph "Variable Propagation Paths"
        subgraph "Request Rate Propagation"
            R1[High Traffic → User Requests<br/>+164.46]
            R2[User Latency → Cart Requests<br/>-26.88]
            R3[User Timeout → Cart Requests<br/>-94.84]
            R4[Cart Latency → Cart Requests<br/>-50.38]
        end

        subgraph "Latency Propagation"
            L1[Inventory Latency → Cart Latency<br/>+18.46]
            L2[High Traffic → Cart Latency<br/>-0.009]
        end

        subgraph "Error Rate Propagation"
            E1[High Traffic → Order Errors<br/>+122.04]
            E2[User Latency → Cart Errors<br/>+3.27]
            E3[Inventory CPU → Cart Errors<br/>+0.36]
            E4[Cart Memory → Order Errors<br/>+26.92]
            E5[Order I/O → Order Errors<br/>+21.41]
        end

        subgraph "Cascading Effects"
            C1[High Traffic → User → Cart → Order → Inventory<br/>+38.82]
            C2[High Traffic → Cart → Inventory → Order Errors<br/>+152.14]
            C3[User Latency → User → Cart → Order<br/>-8.74]
            C4[Cart Latency → Cart → Inventory → Order<br/>-24.47]
            C5[Inventory Timeout → Inventory → Cart → Order<br/>-56.75]
        end
    end

    %% Service connections
    US --> CS
    CS --> IS
    CS --> OS
    OS --> IS

    %% Variable flows
    R1 --> US
    R2 --> CS
    R3 --> CS
    R4 --> CS

    L1 --> CS
    L2 --> CS

    E1 --> OS
    E2 --> CS
    E3 --> CS
    E4 --> OS
    E5 --> OS

    C1 --> IS
    C2 --> OS
    C3 --> OS
    C4 --> OS
    C5 --> OS

    %% Styling
    classDef service fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef strong fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef weak fill:#e8f5e8,stroke:#388e3c,stroke-width:2px

    class US,CS,IS,OS service
    class R1,R3,R4,E1,C2 strong
    class R2,L1,E4,E5,C1,C4,C5 moderate
    class L2,E2,E3,C3 weak
