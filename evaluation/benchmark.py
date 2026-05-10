import time
import pandas as pd
from datetime import datetime
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.runner import AgentRunner
from evaluation.queries import BENCHMARK_QUERIES

def evaluate_response(response: str, expected_keywords: list) -> bool:
    """
    Simple keyword-based evaluation.
    Response is considered successful if it contains
    at least 60% of expected keywords.
    
    This mirrors how LLM-as-judge works at a basic level
    checking if key concepts appear in the answer.
    """
    
    response_lower = response.lower()
    matched = sum(
        1 for keyword in expected_keywords
        if keyword.lower() in response_lower
    )
    match_rate = matched / len(expected_keywords)
    return match_rate >= 0.6

def run_benchmark(sample_size: int = 50):
    """
    Runs the full benchmark suite and saves results  to CSV.
   
    Args:
        sample_size: Number of queries to test from the benchmark set(max 50)
    """
    
    print(f"Starting benchmark - {sample_size} queries")
    print("=" * 50)
    
    agent = AgentRunner()
    results = []
    queries = BENCHMARK_QUERIES[:sample_size]
    
    for item in queries:
        print(f"\n[{item['id']}/50] {item['query'][:60]}...")
        
        start_time = time.time()
        success = False
        error = None
        response = ""
        
        try:
            agent.clear_memory()
            response = agent.run(item["query"])
            latency = time.time() - start_time
            
            #Evaluate
            success = evaluate_response(response, item["expected_keywords"])
            status = "PASS" if success else "FAIL"
            print(f" → {status} ({latency:.1f}s)")
            
        except Exception as e:
            latency = time.time() - start_time
            error = str(e)
            print(f" → ERROR: {error[:50]} ({latency:.1f}s)")

        results.append({
            "id": item["id"],
            "category": item["category"],
            "query": item["query"],
            "success": success,
            "latency_seconds": round(latency, 2),
            "response_length": len(response),
            "error": error
        })
        
    df = pd.DataFrame(results)
    
    total = len(df)
    passed = df["success"].sum()
    accuracy = (passed / total) * 100
    
    
    print("\n" + "=" * 50)
    print("BENCHMARK RESULTS")
    print("=" * 50)
    print(f"Total queries:     {total}")
    print(f"Passed:            {passed}")
    print(f"Failed:            {total - passed}")
    print(f"Accuracy:          {accuracy:.1f}%")
    print(f"Avg latency:       {df['latency_seconds'].mean():.2f}s")
    print(f"P95 latency:       {df['latency_seconds'].quantile(0.95):.2f}s")

    # Per-category breakdown
    print("\nBy category:")
    for category in df["category"].unique():
        cat_df = df[df["category"] == category]
        cat_accuracy = (cat_df["success"].sum() / len(cat_df)) * 100
        print(f"  {category}: {cat_accuracy:.1f}% ({len(cat_df)} queries)")

    # ── Save results ───────────────────────────────────────────────
    os.makedirs("evaluation/results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"evaluation/results/benchmark_{timestamp}.csv"
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

    return accuracy, df


if __name__ == "__main__":
    accuracy, df = run_benchmark(sample_size=50)