def read_file(filename):
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()

    data = []
    for line in lines[1:]:  # Skip the header
        parts = line.strip().split('\t')
        data.append(parts)
    return data

def get_best_and_worst(data):
    best = data[0]
    worst = data[0]
    for row in data:
        try:
            sold = int(row[5].strip())  # QtySold now at index 5
            if sold > int(best[5].strip()):
                best = row
            if sold < int(worst[5].strip()):
                worst = row
        except:
            continue
    return best, worst

def get_mean_std(prices):
    total = sum(prices)
    mean = total / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    std_dev = variance ** 0.5
    return mean, std_dev

def min_max_normalize(prices, new_min, new_max):
    old_min = min(prices)
    old_max = max(prices)
    result = []
    for p in prices:
        scaled = ((p - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
        result.append(scaled)
    return result

def z_score_normalize(prices, mean, std):
    return [(p - mean) / std for p in prices]

def decimal_scaling(prices):
    max_val = max(abs(p) for p in prices)
    j = len(str(int(max_val)))
    return [p / (10 ** j) for p in prices]

def get_percentiles(numbers):
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)

    def get_median(data):
        l = len(data)
        if l % 2 == 0:
            return (data[l//2 - 1] + data[l//2]) / 2
        else:
            return data[l//2]

    q1 = get_median(sorted_nums[:n//2])
    q3 = get_median(sorted_nums[(n+1)//2:])
    median = get_median(sorted_nums)

    return median, q1, q3

def main():
    filename = 'dataset.txt'
    data = read_file(filename)

    print("Sample Row:", data[0])

    best, worst = get_best_and_worst(data)
    print(f"\nBest Selling Item: {best[3].strip()} with QtySold = {best[5].strip()}")
    print(f"Worst Selling Item: {worst[3].strip()} with QtySold = {worst[5].strip()}")

    # Prices are now at index 4
    prices = []
    for row in data:
        try:
            price = float(row[4].strip())
            prices.append(price)
        except:
            continue

    mean, std = get_mean_std(prices)
    print("\nMean Price:", round(mean, 2))
    print("Std Dev of Price:", round(std, 2))

    norm_minmax = min_max_normalize(prices, 10, 20)
    print("Min-Max Normalized (first 5):", norm_minmax[:5])

    norm_zscore = z_score_normalize(prices, mean, std)
    print("Z-Score Normalized (first 5):", norm_zscore[:5])

    norm_decimal = decimal_scaling(prices)
    print("Decimal Scaled (first 5):", norm_decimal[:5])

    # QtySold is now at index 5
    qtys = []
    for row in data:
        try:
            qty = int(row[5].strip())
            qtys.append(qty)
        except:
            continue

    med, q1, q3 = get_percentiles(qtys)
    print("\nMedian QtySold:", med)
    print("Q1 (25%):", q1)
    print("Q3 (75%):", q3)

if __name__ == "__main__":
    main()
