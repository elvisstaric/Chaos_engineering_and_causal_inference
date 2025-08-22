import pandas as pd
import json
import numpy as np
import os
import re
from graphviz import Digraph

import dowhy
from dowhy import CausalModel
def normalize_endpoint(endpoint):
    parts = endpoint.strip("/").split("/")
    if len(parts) == 2:
        parts[1] = ":id"
    return "/" + "/".join(parts)

def load_all_latency_jsons_from_folder(folder_path, files="", value_col="", treatment=""):
    all_dfs = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(f"{files}.json"):
            filepath = os.path.join(folder_path, filename)
            
            with open(filepath) as f:
                data = json.load(f)
            
            rows = []
            for entry in data["data"]["result"]:
                endpoint = entry["metric"].get("endpoint")
                normalized = normalize_endpoint(endpoint) if endpoint else None
                for timestamp, value in entry["values"]:
                    rows.append({
                        "timestamp": int(timestamp),
                        "endpoint": normalized,
                        value_col: float(value),
                        "treatment": treatment
                    })
            
            df = pd.DataFrame(rows)
            if df.empty or value_col not in df.columns:
                continue
            df[value_col] = df[value_col].replace([np.inf, -np.inf], np.nan)
            df = df.dropna(subset=[value_col])
            df = df[df["endpoint"] != "/metrics"]
            df = df.sort_values(by="timestamp").reset_index(drop=True)
            
            all_dfs.append(df)
   
    combined_df = pd.concat(all_dfs, ignore_index=True)
    return combined_df

#------------------------------------Load dataframes-----------------------------------------------


#Baseline
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_normal_test"
# Load all data
df_normal_lat_full = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=0)
df_normal_err_full = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=0)
df_normal_req_full = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=0)

# Extract only the first 5 minutes (300 seconds) of data
if not df_normal_lat_full.empty:
    min_time = df_normal_lat_full['timestamp'].min()
    df_normal_lat = df_normal_lat_full[df_normal_lat_full['timestamp'] < min_time + 300]
else:
    df_normal_lat = df_normal_lat_full

if not df_normal_err_full.empty:
    min_time = df_normal_err_full['timestamp'].min()
    df_normal_err = df_normal_err_full[df_normal_err_full['timestamp'] < min_time + 300]
else:
    df_normal_err = df_normal_err_full

if not df_normal_req_full.empty:
    min_time = df_normal_req_full['timestamp'].min()
    df_normal_req = df_normal_req_full[df_normal_req_full['timestamp'] < min_time + 300]
else:
    df_normal_req = df_normal_req_full

#High traffic
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_high_traffic_test"
df_high_trafic_lat_full = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_high_trafic_err_full = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_high_trafic_req_full = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

# Extract only the first 5 minutes (300 seconds) of data
if not df_high_trafic_lat_full.empty:
    min_time = df_high_trafic_lat_full['timestamp'].min()
    df_high_trafic_lat = df_high_trafic_lat_full[df_high_trafic_lat_full['timestamp'] < min_time + 300]
else:
    df_high_trafic_lat = df_high_trafic_lat_full

if not df_high_trafic_err_full.empty:
    min_time = df_high_trafic_err_full['timestamp'].min()
    df_high_trafic_err = df_high_trafic_err_full[df_high_trafic_err_full['timestamp'] < min_time + 300]
else:
    df_high_trafic_err = df_high_trafic_err_full

if not df_high_trafic_req_full.empty:
    min_time = df_high_trafic_req_full['timestamp'].min()
    df_high_trafic_req = df_high_trafic_req_full[df_high_trafic_req_full['timestamp'] < min_time + 300]
else:
    df_high_trafic_req = df_high_trafic_req_full

#Latency
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_latency_cart_test"
df_cart_lat_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_cart_lat_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_cart_lat_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_latency_inventory_test"
df_inv_lat_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_inv_lat_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_inv_lat_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_latency_order_test"
df_order_lat_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_order_lat_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_order_lat_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_latency_user_test"
df_user_lat_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_user_lat_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_user_lat_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

#timeouts
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_timeout_order_test"
df_timeout_order_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_timeout_order_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_timeout_order_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)


file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_timeout_user_test"
df_timeout_user_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_timeout_user_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_timeout_user_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_timeout_cart_test"
df_timeout_cart_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_timeout_cart_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_timeout_cart_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_timeout_inv_test"
df_timeout_inv_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_timeout_inv_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_timeout_inv_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

#cpu
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_cpu_order_test"
df_cpu_order_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_cpu_order_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_cpu_order_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_cpu_inv_test"
df_cpu_inv_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_cpu_inv_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_cpu_inv_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_cpu_user_test"
df_cpu_user_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_cpu_user_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_cpu_user_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_cpu_cart_test"
df_cpu_cart_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_cpu_cart_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_cpu_cart_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

#memory
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_memory_order_test"
df_memory_order_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_memory_order_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_memory_order_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_memory_inv_test"
df_memory_inv_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_memory_inv_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_memory_inv_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_memory_user_test"
df_memory_user_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_memory_user_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_memory_user_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_memory_cart_test"
df_memory_cart_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_memory_cart_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_memory_cart_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

#io
file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_io_order_test"
df_io_order_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_io_order_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_io_order_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_io_inv_test"
df_io_inv_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_io_inv_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_io_inv_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_io_user_test"
df_io_user_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_io_user_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_io_user_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

file_path = "/Users/elvisstaric/Desktop/FIPU/Diplomski/Znanstveni ljeto/chaos+causal/test_1/results_io_cart_test"
df_io_cart_lat = load_all_latency_jsons_from_folder(file_path,files="latency", value_col="latency", treatment=1)
df_io_cart_err = load_all_latency_jsons_from_folder(file_path,files="errors", value_col="errors", treatment=1)
df_io_cart_req = load_all_latency_jsons_from_folder(file_path,files="requests", value_col="requests", treatment=1)

#--------------------------------------------Models--------------------------------------------

#utjecaj high traffic na user req
user_endpoints = ["/login", "/register"]
df_user_normal = df_normal_req[df_normal_req["endpoint"].isin(user_endpoints)].rename(columns={"requests": "user_req"})
df_user_normal["timestamp"] = (df_user_normal["timestamp"] // 30) * 30

df_user_high_trafic = df_high_trafic_req[df_high_trafic_req["endpoint"].isin(user_endpoints)].rename(columns={"requests": "user_req"})
df_user_high_trafic["timestamp"] = (df_user_high_trafic["timestamp"] // 30) * 30

df_user_normal["treatment"] = 0
df_user_high_trafic["treatment"] = 1
df_final = pd.concat([df_user_normal, df_user_high_trafic], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="user_req",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#utjecaj high traffic na cart lat
cart_endpoints=["/cart"]
df_cart_normal = df_normal_lat[df_normal_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "cart_lat"})
df_cart_high_trafic = df_high_trafic_lat[df_high_trafic_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "cart_lat"})
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30
df_cart_high_trafic["timestamp"] = (df_cart_high_trafic["timestamp"] // 30) * 30

df_cart_normal["treatment"] = 0
df_cart_high_trafic["treatment"] = 1
df_final = pd.concat([df_cart_normal, df_cart_high_trafic], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_lat",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#utjecaj high traffic na order err
order_endpoints=["/orders"]
df_order_normal = df_normal_err[df_normal_err["endpoint"].isin(order_endpoints)].rename(columns={"errors": "order_err"})
df_order_high_trafic = df_high_trafic_err[df_high_trafic_err["endpoint"].isin(order_endpoints)].rename(columns={"errors": "order_err"})
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30
df_order_high_trafic["timestamp"] = (df_order_high_trafic["timestamp"] // 30) * 30

df_order_normal["treatment"] = 0
df_order_high_trafic["treatment"] = 1
df_final = pd.concat([df_order_normal, df_order_high_trafic], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="order_err",
    common_causes=[]
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#Utjecaj user lat na cart req
user_endpoints = ["/login", "/register"]
df_user_normal = df_normal_lat[df_normal_lat["endpoint"].isin(user_endpoints)].rename(columns={"latency": "latency_user"})
df_cart_normal = df_normal_req[df_normal_req["endpoint"] == "/cart"].rename(columns={"requests": "requests_cart"})
df_user_normal["timestamp"] = (df_user_normal["timestamp"] // 30) * 30
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_user_normal[["timestamp", "latency_user"]],
                     df_cart_normal[["timestamp", "requests_cart"]],
                     on="timestamp",
                     how="inner")
df_user_lat = df_user_lat_lat[df_user_lat_lat["endpoint"].isin(user_endpoints)].rename(columns={"latency": "latency_user"})
df_cart_lat = df_user_lat_req[df_user_lat_req["endpoint"] == "/cart"].rename(columns={"requests": "requests_cart"})
df_user_lat["timestamp"] = (df_user_lat["timestamp"] // 30) * 30
df_cart_lat["timestamp"] = (df_cart_lat["timestamp"] // 30) * 30

df_merged_user_lat = pd.merge(df_user_lat[["timestamp", "latency_user"]],
                     df_cart_lat[["timestamp", "requests_cart"]],
                     on="timestamp",
                     how="inner")

df_merged_normal["treatment"] = 0
df_merged_user_lat["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_user_lat], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",         
    outcome="requests_cart",       
    common_causes=["latency_user"],
    graph="""digraph {
        treatment->latency_user;
        latency_user->requests_cart;
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")

print(estimate)
print(refute)

#inv lat utjecaj na cart lat
inv_endpoints = ["/products", "/products/:id"]
cart_endpoints=["/cart", "/cart/:id"]
df_inv_normal = df_normal_lat[df_normal_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "latency_inv"})
df_cart_normal = df_normal_lat[df_normal_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "latency_cart"})
df_inv_normal["timestamp"] = (df_inv_normal["timestamp"] // 30) * 30
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30
df_merged_normal = pd.merge(df_inv_normal[["timestamp", "latency_inv"]],
                     df_cart_normal[["timestamp", "latency_cart"]],
                     on="timestamp",
                     how="inner")

df_inv_lat = df_inv_lat_lat[df_inv_lat_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "latency_inv"})
df_cart_lat = df_inv_lat_lat[df_inv_lat_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "latency_cart"})
df_inv_lat["timestamp"] = (df_inv_lat["timestamp"] // 30) * 30
df_cart_lat["timestamp"] = (df_cart_lat["timestamp"] // 30) * 30
df_merged_inv_lat_cart_lat = pd.merge(df_inv_lat[["timestamp", "latency_inv"]],
                     df_cart_lat[["timestamp", "latency_cart"]],
                     on="timestamp",
                     how="inner")

df_merged_normal["treatment"] = 0
df_merged_inv_lat_cart_lat["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_inv_lat_cart_lat], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",         
    outcome="latency_cart",       
    common_causes=["latency_inv"],
    graph="""digraph {
    treatment->latency_inv;
    latency_inv->latency_cart;
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")

print(estimate)
print(refute)

#user lat utjecaj na cart err
user_endpoints = ["/login", "/register"]
cart_endpoints=["/cart", "cart/:id"]
df_user_normal = df_normal_lat[df_normal_lat["endpoint"].isin(user_endpoints)].rename(columns={"latency": "latency_user"})
df_cart_err_normal = df_normal_err[df_normal_err["endpoint"].isin(cart_endpoints)].rename(columns={"errors": "err_cart"})
df_user_normal["timestamp"] = (df_user_normal["timestamp"] // 30) * 30
df_cart_err_normal["timestamp"] = (df_cart_err_normal["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_user_normal[["timestamp", "latency_user"]],
                     df_cart_err_normal[["timestamp", "err_cart"]],
                     on="timestamp",
                     how="inner")

df_user_lat = df_user_lat_lat[df_user_lat_lat["endpoint"].isin(user_endpoints)].rename(columns={"latency": "latency_user"})
df_cart_err_lat = df_user_lat_err[df_user_lat_err["endpoint"].isin(cart_endpoints)].rename(columns={"errors": "err_cart"})
df_user_lat["timestamp"] = (df_user_lat["timestamp"] // 30) * 30
df_cart_err_lat["timestamp"] = (df_cart_err_lat["timestamp"] // 30) * 30

df_merged_user_lat = pd.merge(df_user_lat[["timestamp", "latency_user"]],
                     df_cart_err_lat[["timestamp", "err_cart"]],
                     on="timestamp",
                     how="inner")

df_merged_normal["treatment"] = 0
df_merged_user_lat["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_user_lat], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",         
    outcome="err_cart",       
    common_causes=["latency_user"],
    graph="""digraph {
        treatment->latency_user;
        latency_user->err_cart;
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")

print(estimate)
print(refute) 

#cart lat utjecaj na cart req
cart_endpoints=["/cart"]
df_cart_normal = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30
df_cart_lat = df_cart_lat_req[df_cart_lat_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_lat["timestamp"] = (df_cart_lat["timestamp"] // 30) * 30

df_cart_normal["treatment"] = 0
df_cart_lat["treatment"] = 1
df_final = pd.concat([df_cart_normal, df_cart_lat], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_req",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#cart timeout utjecaj na orders req
order_endpoints = ["/orders"]
df_order_normal = df_normal_req[df_normal_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30

df_order_timeout = df_timeout_cart_req[df_timeout_cart_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})
df_order_timeout["timestamp"] = (df_order_timeout["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_order_normal[["timestamp", "order_req"]], df_order_timeout[["timestamp", "order_req"]], on="timestamp", how="inner")

df_order_normal["treatment"] = 0
df_order_timeout["treatment"] = 1

df_final = pd.concat([df_order_normal, df_order_timeout], ignore_index=True)


model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="order_req",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#user timeout utjecaj na cart req
cart_endpoints=["/cart"]
df_cart_normal = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30

df_cart_timeout = df_timeout_user_req[df_timeout_user_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_timeout["timestamp"] = (df_cart_timeout["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_cart_normal[["timestamp", "cart_req"]], df_cart_timeout[["timestamp", "cart_req"]], on="timestamp", how="inner")     

df_cart_normal["treatment"] = 0
df_cart_timeout["treatment"] = 1

df_final = pd.concat([df_cart_normal, df_cart_timeout], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_req",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#user cpu utjecaj na cart req
cart_endpoints=["/cart"]
df_user_normal = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_user_normal["timestamp"] = (df_user_normal["timestamp"] // 30) * 30

df_user_cpu = df_cpu_user_req[df_cpu_user_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_user_cpu["timestamp"] = (df_user_cpu["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_user_normal[["timestamp", "cart_req"]], df_user_cpu[["timestamp", "cart_req"]], on="timestamp", how="inner")

df_user_normal["treatment"] = 0
df_user_cpu["treatment"] = 1

df_final = pd.concat([df_user_normal, df_user_cpu], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_req",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#inv cpu utjecaj na cart err   
cart_endpoints=["/cart"]
df_cart_normal = df_normal_err[df_normal_err["endpoint"].isin(cart_endpoints)].rename(columns={"errors": "cart_err"})
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30

df_cart_inv = df_cpu_inv_err[df_cpu_inv_err["endpoint"].isin(cart_endpoints)].rename(columns={"errors": "cart_err"})
df_cart_inv["timestamp"] = (df_cart_inv["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_cart_normal[["timestamp", "cart_err"]], df_cart_inv[["timestamp", "cart_err"]], on="timestamp", how="inner")

df_cart_normal["treatment"] = 0
df_cart_inv["treatment"] = 1

df_final = pd.concat([df_cart_normal, df_cart_inv], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_err",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#user memory utjecaj na cart req
cart_endpoints=["/cart"]
df_user_normal = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_user_normal["timestamp"] = (df_user_normal["timestamp"] // 30) * 30

df_user_memory = df_memory_user_req[df_memory_user_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_user_memory["timestamp"] = (df_user_memory["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_user_normal[["timestamp", "cart_req"]], df_user_memory[["timestamp", "cart_req"]], on="timestamp", how="inner")

df_user_normal["treatment"] = 0
df_user_memory["treatment"] = 1

df_final = pd.concat([df_user_normal, df_user_memory], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_req",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#cart memory utjecaj na order err
order_endpoints=["/orders"]
df_order_normal = df_normal_err[df_normal_err["endpoint"].isin(order_endpoints)].rename(columns={"errors": "order_err"})
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30

df_order_memory = df_memory_order_req[df_memory_order_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_err"})
df_order_memory["timestamp"] = (df_order_memory["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_order_normal[["timestamp", "order_err"]], df_order_memory[["timestamp", "order_err"]], on="timestamp", how="inner")

df_order_normal["treatment"] = 0
df_order_memory["treatment"] = 1

df_final = pd.concat([df_order_normal, df_order_memory], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="order_err",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#inv io utjecaj na cart req
cart_endpoints=["/cart"]
df_cart_normal = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30

df_cart_inv = df_io_inv_req[df_io_inv_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_inv["timestamp"] = (df_cart_inv["timestamp"] // 30) * 30

df_cart_normal["treatment"] = 0
df_cart_inv["treatment"] = 1

df_merged_normal = pd.merge(df_cart_normal[["timestamp", "cart_req"]], df_cart_inv[["timestamp", "cart_req"]], on="timestamp", how="inner") 

df_final = pd.concat([df_cart_normal, df_cart_inv], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="cart_req",
    common_causes=[]
)   
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#order io utjecaj na order err
order_endpoints=["/orders"]
df_order_normal = df_normal_err[df_normal_err["endpoint"].isin(order_endpoints)].rename(columns={"errors": "order_err"})
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30

df_order_io = df_io_order_req[df_io_order_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_err"})
df_order_io["timestamp"] = (df_order_io["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_order_normal[["timestamp", "order_err"]], df_order_io[["timestamp", "order_err"]], on="timestamp", how="inner")
df_order_normal["treatment"] = 0    
df_order_io["treatment"] = 1

df_final = pd.concat([df_order_normal, df_order_io], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="order_err",
    common_causes=[]
)
model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#------------------------------------bigger models-----------------------------------------------

#high traffic utjecaj na cart latency, utjecaj na order req utjecaj na inv req

user_endpoints = ["/login", "/register"]
df_user_normal = df_normal_req[df_normal_req["endpoint"].isin(user_endpoints)].rename(columns={"requests": "high_users"})
df_user_high_trafic = df_high_trafic_req[df_high_trafic_req["endpoint"].isin(user_endpoints)].rename(columns={"requests": "high_users"})

cart_endpoints = ["/cart"]
df_cart_normal = df_normal_lat[df_normal_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "cart_latency"})
df_cart_high_trafic = df_high_trafic_lat[df_high_trafic_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "cart_latency"})


order_endpoints = ["/orders"]
df_order_normal = df_normal_req[df_normal_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})
df_order_high_trafic = df_high_trafic_req[df_high_trafic_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})

inv_endpoints = ["/products", "/products/:id"]
df_inv_normal = df_normal_req[df_normal_req["endpoint"].isin(inv_endpoints)].rename(columns={"requests": "inv_req"})
df_inv_high_trafic = df_high_trafic_req[df_high_trafic_req["endpoint"].isin(inv_endpoints)].rename(columns={"requests": "inv_req"})

df_user_normal["timestamp"] = (df_user_normal["timestamp"] // 30) * 30
df_user_high_trafic["timestamp"] = (df_user_high_trafic["timestamp"] // 30) * 30
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30
df_cart_high_trafic["timestamp"] = (df_cart_high_trafic["timestamp"] // 30) * 30
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30
df_order_high_trafic["timestamp"] = (df_order_high_trafic["timestamp"] // 30) * 30
df_inv_normal["timestamp"] = (df_inv_normal["timestamp"] // 30) * 30
df_inv_high_trafic["timestamp"] = (df_inv_high_trafic["timestamp"] // 30) * 30


df_merged_normal = pd.merge(
    df_user_normal[["timestamp", "high_users"]],
    df_cart_normal[["timestamp", "cart_latency"]],
    on="timestamp",
    how="inner"
)
df_merged_normal = pd.merge(
    df_merged_normal,
    df_order_normal[["timestamp", "order_req"]],
    on="timestamp",
    how="inner"
)
df_merged_normal = pd.merge(
    df_merged_normal,
    df_inv_normal[["timestamp", "inv_req"]],
    on="timestamp",
    how="inner"
)


df_merged_high_trafic = pd.merge(
    df_user_high_trafic[["timestamp", "high_users"]],
    df_cart_high_trafic[["timestamp", "cart_latency"]],
    on="timestamp",
    how="inner"
)
df_merged_high_trafic = pd.merge(
    df_merged_high_trafic,
    df_order_high_trafic[["timestamp", "order_req"]],
    on="timestamp",
    how="inner"
)
df_merged_high_trafic = pd.merge(
    df_merged_high_trafic,
    df_inv_high_trafic[["timestamp", "inv_req"]],
    on="timestamp",
    how="inner"
)


df_merged_normal["treatment"] = 0
df_merged_high_trafic["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_high_trafic], ignore_index=True)


model = CausalModel(
    data=df_final,
    treatment="treatment",         
    outcome="inv_req",       
    common_causes=["high_users", "cart_latency", "order_req"],
    graph="""digraph {
        treatment->high_users;
        high_users->cart_latency;
        cart_latency->order_req;
        order_req->inv_req
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#high traffic utjecaj na cart req utjecaj na inv latency utjecaj na order err

cart_endpoints = ["/cart"]
df_cart_normal = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_high_trafic = df_high_trafic_req[df_high_trafic_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})


inv_endpoints = ["/products", "/products/:id"]
df_inv_normal_lat = df_normal_lat[df_normal_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "inv_latency"})
df_inv_high_trafic_lat = df_high_trafic_lat[df_high_trafic_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "inv_latency"})

order_endpoints = ["/orders"]
df_order_normal = df_normal_err[df_normal_err["endpoint"].isin(order_endpoints)].rename(columns={"errors": "order_err"})
df_order_high_trafic = df_high_trafic_err[df_high_trafic_err["endpoint"].isin(order_endpoints)].rename(columns={"errors": "order_err"})

df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30
df_cart_high_trafic["timestamp"] = (df_cart_high_trafic["timestamp"] // 30) * 30
df_inv_normal_lat["timestamp"] = (df_inv_normal_lat["timestamp"] // 30) * 30
df_inv_high_trafic_lat["timestamp"] = (df_inv_high_trafic_lat["timestamp"] // 30) * 30
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30
df_order_high_trafic["timestamp"] = (df_order_high_trafic["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_cart_normal[["timestamp", "cart_req"]], df_inv_normal_lat[["timestamp", "inv_latency"]], on="timestamp", how="inner")
df_merged_normal = pd.merge(df_merged_normal, df_order_normal[["timestamp", "order_err"]], on="timestamp", how="inner")
df_merged_high_trafic = pd.merge(df_cart_high_trafic[["timestamp", "cart_req"]], df_inv_high_trafic_lat[["timestamp", "inv_latency"]], on="timestamp", how="inner")
df_merged_high_trafic = pd.merge(df_merged_high_trafic, df_order_high_trafic[["timestamp", "order_err"]], on="timestamp", how="inner")
df_merged_normal["treatment"] = 0
df_merged_high_trafic["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_high_trafic], ignore_index=True)

model = CausalModel(

    data=df_final,
    treatment="treatment",
    outcome="order_err",
    common_causes=["cart_req", "inv_latency"],
    graph="""digraph {
        treatment->cart_req;
        cart_req->inv_latency;
        inv_latency->order_err;
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)


#user latency utjecaj na user req utjecaj na cart req utjecaj na order req

user_endpoints = ["/login", "/register"]
df_user_normal_lat = df_normal_lat[df_normal_lat["endpoint"].isin(user_endpoints)].rename(columns={"latency": "user_latency"})
df_user_lat_lat = df_user_lat_lat[df_user_lat_lat["endpoint"].isin(user_endpoints)].rename(columns={"latency": "user_latency"})


df_user_normal_req = df_normal_req[df_normal_req["endpoint"].isin(user_endpoints)].rename(columns={"requests": "user_req"})
df_user_lat_user_req = df_user_lat_req[df_user_lat_req["endpoint"].isin(user_endpoints)].rename(columns={"requests": "user_req"})


cart_endpoints = ["/cart"]
df_cart_normal_req = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_lat_req = df_user_lat_req[df_user_lat_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})

order_endpoints = ["/orders"]
df_order_normal_req = df_normal_req[df_normal_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})
df_order_lat_req = df_user_lat_req[df_user_lat_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})

df_user_normal_lat["timestamp"] = (df_user_normal_lat["timestamp"] // 30) * 30
df_user_lat_lat["timestamp"] = (df_user_lat_lat["timestamp"] // 30) * 30
df_user_normal_req["timestamp"] = (df_user_normal_req["timestamp"] // 30) * 30
df_user_lat_user_req["timestamp"] = (df_user_lat_user_req["timestamp"] // 30) * 30
df_cart_normal_req["timestamp"] = (df_cart_normal_req["timestamp"] // 30) * 30
df_cart_lat_req["timestamp"] = (df_cart_lat_req["timestamp"] // 30) * 30
df_order_normal_req["timestamp"] = (df_order_normal_req["timestamp"] // 30) * 30
df_order_lat_req["timestamp"] = (df_order_lat_req["timestamp"] // 30) * 30


df_merged_normal = pd.merge(
    df_user_normal_lat[["timestamp", "user_latency"]],
    df_user_normal_req[["timestamp", "user_req"]],
    on="timestamp",
    how="inner"
)
df_merged_normal = pd.merge(
    df_merged_normal,
    df_cart_normal_req[["timestamp", "cart_req"]],
    on="timestamp",
    how="inner"
)
df_merged_normal = pd.merge(
    df_merged_normal,
    df_order_normal_req[["timestamp", "order_req"]],
    on="timestamp",
    how="inner"
)

df_merged_user_lat = pd.merge(
    df_user_lat_lat[["timestamp", "user_latency"]],
    df_user_lat_user_req[["timestamp", "user_req"]],
    on="timestamp",
    how="inner"
)
df_merged_user_lat = pd.merge(
    df_merged_user_lat,
    df_cart_lat_req[["timestamp", "cart_req"]],
    on="timestamp",
    how="inner"
)
df_merged_user_lat = pd.merge(
    df_merged_user_lat,
    df_order_lat_req[["timestamp", "order_req"]],
    on="timestamp",
    how="inner"
)


df_merged_normal["treatment"] = 0
df_merged_user_lat["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_user_lat], ignore_index=True)


model = CausalModel(
    data=df_final,
    treatment="treatment",         
    outcome="order_req",       
    common_causes=["user_latency", "user_req", "cart_req"],
    graph="""digraph {
        treatment->user_latency;
        user_latency->user_req;
        user_req->cart_req;
        cart_req->order_req
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#cart latency utjecaj na cart req utjecaj na inv latency utjecaj na order req

cart_endpoints = ["/cart"]
df_cart_normal_latency = df_normal_lat[df_normal_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "cart_latency"})
df_cart_lat_cart_lat = df_cart_lat_lat[df_cart_lat_lat["endpoint"].isin(cart_endpoints)].rename(columns={"latency": "cart_latency"})

df_cart_normal_req = df_normal_req[df_normal_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})
df_cart_lat_cart_req = df_cart_lat_req[df_cart_lat_req["endpoint"].isin(cart_endpoints)].rename(columns={"requests": "cart_req"})

inv_endpoints = ["/products", "/products/:id"]
df_inv_normal = df_normal_lat[df_normal_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "inv_latency"})
df_inv_lat_inv_lat = df_cart_lat_lat[df_cart_lat_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "inv_latency"})

order_endpoints = ["/orders"]
df_order_normal = df_normal_req[df_normal_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})
df_order_lat_order_req = df_cart_lat_req[df_cart_lat_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})

df_cart_normal_latency["timestamp"] = (df_cart_normal_latency["timestamp"] // 30) * 30
df_cart_lat_cart_lat["timestamp"] = (df_cart_lat_cart_lat["timestamp"] // 30) * 30
df_cart_normal_req["timestamp"] = (df_cart_normal_req["timestamp"] // 30) * 30
df_cart_lat_cart_req["timestamp"] = (df_cart_lat_cart_req["timestamp"] // 30) * 30
df_inv_normal["timestamp"] = (df_inv_normal["timestamp"] // 30) * 30
df_inv_lat_inv_lat["timestamp"] = (df_inv_lat_inv_lat["timestamp"] // 30) * 30
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30
df_order_lat_order_req["timestamp"] = (df_order_lat_order_req["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_cart_normal_latency[["timestamp", "cart_latency"]], df_cart_normal_req[["timestamp", "cart_req"]], on="timestamp", how="inner")
df_merged_normal = pd.merge(df_merged_normal, df_inv_normal[["timestamp", "inv_latency"]], on="timestamp", how="inner")
df_merged_normal = pd.merge(df_merged_normal, df_order_normal[["timestamp", "order_req"]], on="timestamp", how="inner")

df_merged_lat = pd.merge(df_cart_lat_cart_lat[["timestamp", "cart_latency"]], df_cart_lat_cart_req[["timestamp", "cart_req"]], on="timestamp", how="inner")
df_merged_lat = pd.merge(df_merged_lat, df_inv_lat_inv_lat[["timestamp", "inv_latency"]], on="timestamp", how="inner")
df_merged_lat = pd.merge(df_merged_lat, df_order_lat_order_req[["timestamp", "order_req"]], on="timestamp", how="inner")

df_merged_normal["treatment"] = 0
df_merged_lat["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_lat], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="order_req",
    common_causes=["cart_latency", "cart_req", "inv_latency"],
    graph="""digraph {
        treatment->cart_latency;
        cart_latency->cart_req;
        cart_req->inv_latency;
        inv_latency->order_req
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

#inv timeout utjecaj na inv latency utjecaj na cart err utjecaj na order req
inv_endpoints = ["/products", "/products/:id"]
df_inv_normal = df_normal_lat[df_normal_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "inv_latency"})
df_inv_timeout_lat = df_timeout_inv_lat[df_timeout_inv_lat["endpoint"].isin(inv_endpoints)].rename(columns={"latency": "inv_latency"})

cart_endpoints = ["/cart"]
df_cart_normal = df_normal_err[df_normal_err["endpoint"].isin(cart_endpoints)].rename(columns={"errors": "cart_err"})
df_cart_timeout_err = df_timeout_inv_err[df_timeout_inv_err["endpoint"].isin(cart_endpoints)].rename(columns={"errors": "cart_err"})

order_endpoints = ["/orders"]
df_order_normal = df_normal_req[df_normal_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})
df_order_timeout_req = df_timeout_inv_req[df_timeout_inv_req["endpoint"].isin(order_endpoints)].rename(columns={"requests": "order_req"})

df_inv_normal["timestamp"] = (df_inv_normal["timestamp"] // 30) * 30
df_inv_timeout_lat["timestamp"] = (df_inv_timeout_lat["timestamp"] // 30) * 30
df_cart_normal["timestamp"] = (df_cart_normal["timestamp"] // 30) * 30
df_cart_timeout_err["timestamp"] = (df_cart_timeout_err["timestamp"] // 30) * 30
df_order_normal["timestamp"] = (df_order_normal["timestamp"] // 30) * 30
df_order_timeout_req["timestamp"] = (df_order_timeout_req["timestamp"] // 30) * 30

df_merged_normal = pd.merge(df_inv_normal[["timestamp", "inv_latency"]], df_cart_normal[["timestamp", "cart_err"]], on="timestamp", how="inner")
df_merged_normal = pd.merge(df_merged_normal, df_order_normal[["timestamp", "order_req"]], on="timestamp", how="inner")

df_merged_timeout = pd.merge(df_inv_timeout_lat[["timestamp", "inv_latency"]], df_cart_timeout_err[["timestamp", "cart_err"]], on="timestamp", how="inner")
df_merged_timeout = pd.merge(df_merged_timeout, df_order_timeout_req[["timestamp", "order_req"]], on="timestamp", how="inner")

df_merged_normal["treatment"] = 0
df_merged_timeout["treatment"] = 1

df_final = pd.concat([df_merged_normal, df_merged_timeout], ignore_index=True)

model = CausalModel(
    data=df_final,
    treatment="treatment",
    outcome="order_req",
    common_causes=["inv_latency", "cart_err"],
    graph="""digraph {
        treatment->inv_latency;
        inv_latency->cart_err;
        cart_err->order_req
    }"""
)

model.view_model()
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
refute = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter")
print(estimate)
print(refute)

