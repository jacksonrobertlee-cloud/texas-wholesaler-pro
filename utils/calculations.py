def calculate_mao(arv, repairs, fee, rule_percent):
    arv = float(arv)
    repairs = float(repairs)
    fee = float(fee)

    return (arv * rule_percent) - repairs - fee
