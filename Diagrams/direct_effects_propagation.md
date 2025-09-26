%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
subgraph "Direct Effects Propagation"
subgraph "High Traffic Effects"
HT[High Traffic<br/>Treatment]
UR[User Requests<br/>+164.46]
CL[Cart Latency<br/>-0.009]
OE[Order Errors<br/>+122.04]

            HT --> UR
            HT --> CL
            HT --> OE
        end

        subgraph "Timeout Effects"
            UT[User Timeout<br/>Treatment]
            CR1[Cart Requests<br/>-94.84]

            CT[Cart Timeout<br/>Treatment]
            OR1[Order Requests<br/>-40.54]

            CLT[Cart Latency<br/>Treatment]
            CR2[Cart Requests<br/>-50.38]

            UT --> CR1
            CT --> OR1
            CLT --> CR2
        end

        subgraph "Latency Injection Effects"
            UL[User Latency<br/>Treatment]
            CR3[Cart Requests<br/>-26.88]
            CE1[Cart Errors<br/>+3.27]

            IL[Inventory Latency<br/>Treatment]
            CL2[Cart Latency<br/>+18.46]

            UL --> CR3
            UL --> CE1
            IL --> CL2
        end

        subgraph "Resource Stress Effects"
            UC[User CPU<br/>Treatment]
            CR4[Cart Requests<br/>-5.63]

            IC[Inventory CPU<br/>Treatment]
            CE2[Cart Errors<br/>+0.36]

            UM[User Memory<br/>Treatment]
            CR5[Cart Requests<br/>+8.82]

            CM[Cart Memory<br/>Treatment]
            OE2[Order Errors<br/>+26.92]

            UC --> CR4
            IC --> CE2
            UM --> CR5
            CM --> OE2
        end
    end

    %% Styling
    classDef strong fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef weak fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef treatment fill:#e3f2fd,stroke:#1976d2,stroke-width:2px

    class UR,OE,CR1,OR1,CR2 strong
    class CR3,CL2,OE2 moderate
    class CL,CE1,CR4,CE2,CR5 weak
    class HT,UT,CT,CLT,UL,IL,UC,IC,UM,CM treatment
