import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import os

plt.style.use('dark_background')
COLORS = {
    'success': '#4a9eff',
    'fail': '#ff6b6b',
    'web_search': '#4a9eff',
    'code_execution': '#51cf66',
    'reasoning': '#ffd43b'
}


def load_latest_results(results_dir: str = "evaluation/results") -> pd.DataFrame:
    """
    Load the most recent benchmark CSV."""
    
    files = [f for f in os.listdir(results_dir) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No benchmark results found. Run benchmark.py first.")
    latest = sorted(files)[-1]
    print(f"loading: {latest}")
    return pd.read_csv(f"{results_dir}/{latest}")


def plot_overall_accuracy(df: pd.DataFrame, ax):
    """Pie chart -- overall pass/fail breakdown."""
    passed = df['success'].sum()
    failed = len(df) - passed
    accuracy = passed / len(df) * 100
    
    wedges, texts, autotexts = ax.pie(
        [passed, failed],
        labels=['Passed', 'Failed'],
        colors=[COLORS['success'], COLORS['fail']],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'color': 'white', 'fontsize': 14}
    )
    autotexts[0].set_fontsize(14)
    
    ax.set_title(
        f'Overall Accuracy: {accuracy:.1f}%\n({passed}/{len(df)} queries)',
        color = 'white',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    
def plot_category_accuracy(df: pd.DataFrame, ax):
    """Bar chart — accuracy broken down by category."""
    categories = df['category'].unique()
    accuracies = []
    colors = []

    for cat in categories:
        cat_df = df[df['category'] == cat]
        acc = (cat_df['success'].sum() / len(cat_df)) * 100
        accuracies.append(acc)
        colors.append(COLORS.get(cat, '#888'))

    bars = ax.bar(categories, accuracies, color=colors, alpha=0.85, width=0.5)

    # Add value labels on top of bars
    for bar, acc in zip(bars, accuracies):
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            bar.get_height() + 1,
            f'{acc:.1f}%',
            ha='center', va='bottom',
            color='white', fontsize=12, fontweight='bold'
        )

    ax.set_ylim(0, 110)
    ax.set_xlabel('Category', color='white', fontsize=12)
    ax.set_ylabel('Accuracy (%)', color='white', fontsize=12)
    ax.set_title('Accuracy by Category', color='white', fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def plot_latency_distribution(df: pd.DataFrame, ax):
    """Histogram — response time distribution."""
    ax.hist(
        df['latency_seconds'],
        bins=15,
        color=COLORS['success'],
        alpha=0.7,
        edgecolor='#333'
    )

    # Add P50 and P95 lines
    p50 = df['latency_seconds'].quantile(0.50)
    p95 = df['latency_seconds'].quantile(0.95)

    ax.axvline(p50, color='#ffd43b', linestyle='--', linewidth=2, label=f'P50: {p50:.1f}s')
    ax.axvline(p95, color='#ff6b6b', linestyle='--', linewidth=2, label=f'P95: {p95:.1f}s')

    ax.set_xlabel('Response Time (seconds)', color='white', fontsize=12)
    ax.set_ylabel('Number of Queries', color='white', fontsize=12)
    ax.set_title('Latency Distribution', color='white', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def plot_pass_fail_by_category(df: pd.DataFrame, ax):
    """Stacked bar — pass/fail count per category."""
    categories = df['category'].unique()
    passed = [df[(df['category'] == c) & (df['success'] == True)].shape[0] for c in categories]
    failed = [df[(df['category'] == c) & (df['success'] == False)].shape[0] for c in categories]

    x = range(len(categories))
    ax.bar(x, passed, color=COLORS['success'], alpha=0.85, label='Passed')
    ax.bar(x, failed, bottom=passed, color=COLORS['fail'], alpha=0.85, label='Failed')

    ax.set_xticks(x)
    ax.set_xticklabels(categories, color='white')
    ax.set_xlabel('Category', color='white', fontsize=12)
    ax.set_ylabel('Number of Queries', color='white', fontsize=12)
    ax.set_title('Pass/Fail Count by Category', color='white', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def generate_dashboard(results_dir: str = "evaluation/results"):
    """
    Generates a 2x2 dashboard of charts and saves as PNG.
    """
    df = load_latest_results(results_dir)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor('#0f0f0f')

    for ax in axes.flat:
        ax.set_facecolor('#1a1a1a')

    fig.suptitle(
        'Agentic Research Assistant — Benchmark Results',
        color='white',
        fontsize=16,
        fontweight='bold',
        y=1.02
    )

    plot_overall_accuracy(df, axes[0, 0])
    plot_category_accuracy(df, axes[0, 1])
    plot_latency_distribution(df, axes[1, 0])
    plot_pass_fail_by_category(df, axes[1, 1])

    plt.tight_layout()

    output_path = f"{results_dir}/dashboard.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0f0f0f')
    print(f"Dashboard saved to: {output_path}")
    plt.show()
    return output_path


if __name__ == "__main__":
    generate_dashboard()
    

