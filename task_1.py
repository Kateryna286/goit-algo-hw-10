import time
import statistics as stats

def find_coins_greedy(amount):
    coins = [50, 25, 10, 5, 2, 1]
    result = {}
    
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount -= coin * count
            
    return result

# Приклад використання
amount = 113
change = find_coins_greedy(amount)
print("Жадібний алгоритм:", change)  

def find_min_coins(amount):
    coins = [50, 25, 10, 5, 2, 1]
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    coin_used = [-1] * (amount + 1)
    
    for coin in coins:
        for x in range(coin, amount + 1):
            if dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
                coin_used[x] = coin
                
    if dp[amount] == float('inf'):
        return {}
    
    result = {}
    while amount > 0:
        coin = coin_used[amount]
        if coin in result:
            result[coin] += 1
        else:
            result[coin] = 1
        amount -= coin
        
    return result

# Приклад використання
amount = 113
change = find_min_coins(amount)
print("Динамічне програмування:", change)  

# Функція для вимірювання часу виконання
def bench(fn, amount, repeats=5):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(amount)
        times.append(time.perf_counter() - t0)
    return stats.median(times)

amounts = [10, 10**2, 10**3, 5*10**3, 10**4]  
print("Порівняльна таблиця:")
print(f"{'amount':>8} | {'greedy, ms':>10} | {'dp, ms':>8} | {'coins(g)':>8} | {'coins(dp)':>10}")
print("-"*56)

for a in amounts:
    tg = bench(find_coins_greedy, a) * 1000
    td = bench(find_min_coins, a) * 1000
    g = find_coins_greedy(a)
    d = find_min_coins(a)
    print(f"{a:8d} | {tg:10.3f} | {td:8.3f} | {sum(g.values()):8d} | {sum(d.values()):10d}")

