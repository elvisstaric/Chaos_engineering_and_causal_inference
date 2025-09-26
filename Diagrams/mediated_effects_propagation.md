%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
subgraph "Mediated Effects - Cascading Through Services"
subgraph "High Traffic Cascade"
HT[High Traffic<br/>Treatment]
UR[User Requests<br/>+164.46]
CL[Cart Latency<br/>Intermediate]
OR[Order Requests<br/>Intermediate]
IR[Inventory Requests<br/>+38.82]

            HT --> UR
            UR --> CL
            CL --> OR
            OR --> IR
        end

        subgraph "High Traffic Cart Chain"
            HT2[High Traffic<br/>Treatment]
            CR[Cart Requests<br/>Intermediate]
            IL[Inventory Latency<br/>Intermediate]
            OE[Order Errors<br/>+152.14]

            HT2 --> CR
            CR --> IL
            IL --> OE
        end

        subgraph "User Latency Cascade"
            UL[User Latency<br/>Treatment]
            UR2[User Requests<br/>Intermediate]
            CR2[Cart Requests<br/>Intermediate]
            OR2[Order Requests<br/>-8.74]

            UL --> UR2
            UR2 --> CR2
            CR2 --> OR2
        end

        subgraph "Cart Latency Cascade"
            CL2[Cart Latency<br/>Treatment]
            CR3[Cart Requests<br/>Intermediate]
            IL2[Inventory Latency<br/>Intermediate]
            OR3[Order Requests<br/>-24.47]

            CL2 --> CR3
            CR3 --> IL2
            IL2 --> OR3
        end

        subgraph "Inventory Timeout Cascade"
            IT[Inventory Timeout<br/>Treatment]
            IL3[Inventory Latency<br/>Intermediate]
            CE[Cart Errors<br/>Intermediate]
            OR4[Order Requests<br/>-56.75]

            IT --> IL3
            IL3 --> CE
            CE --> OR4
        end
    end

    %% Styling
    classDef strong fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef weak fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef treatment fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef intermediate fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px

    class IR,OE,OR4 strong
    class OR2,OR3 moderate
    class HT,HT2,UL,CL2,IT treatment
    class UR,CL,OR,CR,IL,UR2,CR2,CL2,CR3,IL2,IL3,CE intermediate
