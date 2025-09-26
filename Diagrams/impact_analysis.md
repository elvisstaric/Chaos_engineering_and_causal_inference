%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
subgraph "High Traffic Tests"
HT1[Model 1: High Traffic → User Requests<br/>ATE = 164.46<br/>🔴 STRONG]
HT2[Model 3: High Traffic → Order Errors<br/>ATE = 122.04<br/>🔴 STRONG]
HT3[Model 17: High Traffic → Cart → Inventory → Order Errors<br/>ATE = 152.14<br/>🔴 STRONG]
end

    subgraph "Timeout Simulation Tests"
        TS1[Model 9: User Timeout → Cart Requests<br/>ATE = -94.84<br/>🔴 STRONG]
        TS2[Model 7: Cart Latency → Cart Requests<br/>ATE = -50.38<br/>🔴 STRONG]
        TS3[Model 20: Inventory Timeout → Cart Errors → Order Requests<br/>ATE = -56.75<br/>🔴 STRONG]
    end

    subgraph "Latency Injection Tests"
        LI1[Model 4: User Latency → Cart Requests<br/>ATE = -26.88<br/>🟡 MODERATE]
        LI2[Model 5: Inventory Latency → Cart Latency<br/>ATE = 18.46<br/>🟡 MODERATE]
        LI3[Model 19: Cart Latency → Cart Requests → Inventory → Order<br/>ATE = -24.47<br/>🟡 MODERATE]
    end

    subgraph "Resource Stress Tests"
        RS1[Model 13: Cart Memory → Order Errors<br/>ATE = 26.92<br/>🟡 MODERATE]
        RS2[Model 15: Order I/O → Order Errors<br/>ATE = 21.41<br/>🟡 MODERATE]
        RS3[Model 10: User CPU → Cart Requests<br/>ATE = -5.63<br/>🟢 WEAK]
        RS4[Model 12: User Memory → Cart Requests<br/>ATE = 8.82<br/>🟢 WEAK]
    end

    subgraph "Key Insights"
        INSIGHT1[🔴 HIGHEST IMPACT: High Traffic<br/>Strong effects on User & Order services]
        INSIGHT2[🔴 CRITICAL: Timeout Simulation<br/>Strong negative effects on Cart operations]
        INSIGHT3[🟡 MODERATE: Latency Injection<br/>Moderate effects on service chains]
        INSIGHT4[🟢 LOWEST: Resource Stress<br/>Weak to moderate effects overall]
    end

    %% Styling
    classDef strong fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef moderate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef weak fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef insight fill:#e3f2fd,stroke:#1976d2,stroke-width:2px

    class HT1,HT2,HT3,TS1,TS2,TS3 strong
    class LI1,LI2,LI3,RS1,RS2 moderate
    class RS3,RS4 weak
    class INSIGHT1,INSIGHT2,INSIGHT3,INSIGHT4 insight
