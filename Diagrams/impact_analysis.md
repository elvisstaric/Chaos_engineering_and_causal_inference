%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
subgraph "High Traffic Tests"
HT1[Model 1: High Traffic → User Requests<br/>ATE = 161.27<br/>🔴 STRONG]
HT2[Model 3: High Traffic → Order Errors<br/>ATE = 103.59<br/>🔴 STRONG]
HT3[Model 17: High Traffic → Cart → Inventory → Order Errors<br/>ATE = 110.06<br/>🔴 STRONG]
end

    subgraph "Bandwidth Simulation Tests"
        BW1[Model 8: Cart bandwidth → Order latency<br/>ATE = 4.80<br/>🟢 WEAK]
        BW2[Model 9: User bandwidth → Order latency<br/>ATE = 80.31<br/>🔴 STRONG]
        BW3[Model 20: Inventory timeout → Inventory latency → Cart errors → Order requests<br/>ATE = -42.15<br/>🟡 MODERATE]
    end

    subgraph "Latency Injection Tests"
        LI1[Model 4: User latency → Cart requests<br/>ATE = -36.79<br/>🟡 MODERATE]
        LI2[Model 5: Inventory latency → Cart latency<br/>ATE = 5.93<br/>🟢 WEAK]
        LI3[Model 7: Cart latency → Cart requests<br/>ATE = -46.18<br/>🟡 MODERATE]
    end

    subgraph "Resource Stress Tests"
        RS1[Model 10: User CPU → Cart latency<br/>ATE = 828.24<br/>🔴 STRONG]
        RS2[Model 11: Inventory CPU → Cart requests<br/>ATE = -91.45<br/>🔴 STRONG]
        RS3[Model 12: User memory → Cart latency<br/>ATE = 0.90<br/>🟢 WEAK]
        RS4[Model 13: Cart memory → Order errors<br/>ATE = 44.58<br/>🟡 MODERATE]
        RS5[Model 14: Inventory I/O → Cart requests<br/>ATE = 1.21<br/>🟢 WEAK]
        RS6[Model 15: Order I/O → Order errors<br/>ATE = 46.59<br/>🟡 MODERATE]
    end

    subgraph "Key Insights"
        INSIGHT1[🔴 HIGHEST IMPACT: Resource CPU stress spike on latency]
        INSIGHT2[🔴 HIGH IMPACT: High Traffic increases user requests and order errors]
        INSIGHT3[🟡 MODERATE: Bandwidth changes cascade into order flow]
        INSIGHT4[🟡/🟢 MIXED: Latency injection shows moderate-to-weak effects]
    end

    %% Styling
    classDef strong fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef weak fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef insight fill:#e3f2fd,stroke:#1976d2,stroke-width:2px

    class HT1,HT2,HT3,BW2,RS1,RS2 strong
    class LI1,LI3,RS4,RS6,BW3 moderate
    class LI2,RS3,RS5,BW1 weak
    class INSIGHT1,INSIGHT2,INSIGHT3,INSIGHT4 insight
