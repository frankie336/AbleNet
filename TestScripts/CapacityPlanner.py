

def factors_of(line_rate):

    factors = []

    for whole_number in range(1, line_rate + 1):
        if line_rate % whole_number == 0:
            factors.append(whole_number)

    return factors


GigE=944#https://www.gigabit-wireless.com/gigabit-wireless/actual-maximum-throughput-gigabit-ethernet/
TenGigE=8000#https://fmad.io/blog-what-is-10g-line-rate.html
print(factors_of(line_rate= GigE))


16777216