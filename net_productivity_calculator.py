"""
Net Productivity Calculator
Calculates empirical statistics from time_and_defect_logs.csv
"""
import csv

def calculate_stats():
    with open("time_and_defect_logs.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total_manual = sum(float(r["manual_time_min"]) for r in rows)
    total_gen = sum(float(r["ai_gen_time_min"]) for r in rows)
    total_review = sum(float(r["ai_review_time_min"]) for r in rows)
    total_fix = sum(float(r["ai_fix_time_min"]) for r in rows)
    total_assisted = sum(float(r["total_assisted_min"]) for r in rows)

    total_lines_gen = sum(int(r["lines_gen"]) for r in rows)
    total_lines_kept = sum(int(r["lines_kept"]) for r in rows)

    net_speedup = total_manual / total_assisted
    headline_speedup = total_manual / total_gen
    review_share = ((total_review + total_fix) / total_assisted) * 100
    overall_acceptance = (total_lines_kept / total_lines_gen) * 100

    print("=== ASSIGNMENT 4 PRODUCTIVITY RESULTS ===")
    print(f"Total Tasks: {len(rows)}")
    print(f"Manual Dev Time: {total_manual:.1f} min ({total_manual/60:.1f} hours)")
    print(f"Total AI Assisted Time: {total_assisted:.1f} min ({total_assisted/60:.1f} hours)")
    print(f"  - AI Generation Time: {total_gen:.1f} min")
    print(f"  - Review Time: {total_review:.1f} min")
    print(f"  - Fix/Debug Time: {total_fix:.1f} min")
    print(f"Review & Correction Proportion: {review_share:.1f}% of assisted time")
    print(f"Overall Code Acceptance Rate: {overall_acceptance:.1f}%")
    print(f"Headline Generation Speedup: {headline_speedup:.2f}x")
    print(f"REAL NET PRODUCTIVITY SPEEDUP: {net_speedup:.2f}x")

if __name__ == "__main__":
    calculate_stats()
