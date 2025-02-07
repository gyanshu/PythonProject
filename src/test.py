def subset_sum_possible(arr, target):
    n = len(arr)
    # Create a table with (n+1) rows and (target+1) columns
    dp = [[False] * (target + 1) for _ in range(n + 1)]

    # Base case: A sum of 0 is always possible (empty subset)
    for i in range(n + 1):
        dp[i][0] = True

    # With 0 elements, no positive sum can be formed.
    for j in range(1, target + 1):
        dp[0][j] = False

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if arr[i - 1] > j:
                dp[i][j] = dp[i - 1][j]  # cannot include arr[i-1]
            else:
                # Either exclude arr[i-1] or include it if possible
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - arr[i - 1]]

    return dp[n][target]


# Example usage:
if __name__ == "__main__":
    arr = [3, 21, 7, 9, 5]
    target = 3
    if subset_sum_possible(arr, target):
        print("It is possible to form the target sum.")
    else:
        print("It is not possible to form the target sum.")
