"""Hybrid routing simulation: edge vs cloud decision."""
import json, random, numpy as np, argparse
from pathlib import Path
random.seed(42)

def route_query(query_complexity):
    if query_complexity < 0.4: return "edge", 65, 0.001
    elif query_complexity < 0.7: return "edge", 85, 0.001
    else: return "cloud", 800 + random.randint(0,400), 0.03

def main():
    p = argparse.ArgumentParser(); p.add_argument("--n_queries", type=int, default=1000)
    p.add_argument("--output_dir", default="outputs"); a = p.parse_args()
    out = Path(a.output_dir); out.mkdir(parents=True, exist_ok=True)
    results = []
    for i in range(a.n_queries):
        complexity = np.random.beta(2, 5)
        dest, latency, cost = route_query(complexity)
        accuracy = 0.95 if dest == "cloud" else max(0.7, 0.92 - complexity * 0.3)
        results.append({"query_id": i, "complexity": round(complexity,3), "route": dest,
                        "latency_ms": latency, "cost": cost, "accuracy": round(accuracy,3)})
    edge = [r for r in results if r["route"]=="edge"]; cloud = [r for r in results if r["route"]=="cloud"]
    with open(out / "routing_results.json", "w") as f: json.dump({"summary": {
        "total": len(results), "edge_pct": round(len(edge)/len(results)*100,1),
        "avg_latency": round(np.mean([r["latency_ms"] for r in results]),1),
        "avg_cost": round(np.mean([r["cost"] for r in results]),4),
        "avg_accuracy": round(np.mean([r["accuracy"] for r in results]),3)
    }}, f, indent=2)
    print(f"\u2705 Hybrid Routing ({len(results)} queries)")
    print(f"   Edge: {len(edge)} ({len(edge)/len(results)*100:.0f}%), Cloud: {len(cloud)} ({len(cloud)/len(results)*100:.0f}%)")
    print(f"   Avg latency: {np.mean([r['latency_ms'] for r in results]):.0f}ms")
    print(f"   Avg cost: ${np.mean([r['cost'] for r in results]):.4f}/query")

if __name__ == "__main__": main()
