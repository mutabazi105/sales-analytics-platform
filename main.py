"""
Main entry point for Sales Analytics Platform
"""
from analyzer import SalesAnalyzer
from algorithms import compare_sorting, compare_searching


def main():
    print("=" * 50)
    print("SALES ANALYTICS PLATFORM")
    print("=" * 50)

    # Initialize analyzer
    analyzer = SalesAnalyzer("data/sales_data.csv")

    # 1. Load and clean data
    print("\n1. Loading and cleaning data...")
    analyzer.load_data()
    analyzer.clean_data()
    analyzer.export_clean_data()

    # 2. Business analysis
    print("\n2. Performing business analysis...")
    answers = analyzer.answer_business_questions()

    print("\n" + "="*50)
    print("BUSINESS INSIGHTS")
    print("="*50)

    for question, answer in answers.items():
        if isinstance(answer, dict):
            print(f"\n{question}:")
            for key, value in answer.items():
                print(f"  {key}: {value}")
        else:
            print(f"{question}: {answer}")

    # 3. Algorithm comparison
    print("\n" + "="*50)
    print("ALGORITHM PERFORMANCE")
    print("="*50)

    sample_data = list(range(10000, 0, -1))

    # Sorting comparison
    sort_results = compare_sorting(sample_data[:1000])
    print("\nSorting Performance (1000 elements):")
    for algo, time_taken in sort_results.items():
        print(f"  {algo}: {time_taken:.6f} seconds")

    # Searching comparison
    search_results = compare_searching(sample_data[:10000], 7500)
    print("\nSearching Performance (10000 elements):")
    for algo, time_taken in search_results.items():
        print(f"  {algo}: {time_taken:.6f} seconds")

    print("\n" + "="*50)
    print("✅ PROJECT COMPLETED SUCCESSFULLY!!")
    print("="*50)


if __name__ == "__main__":
    main()
