import math
import argparse

def interest(i):
    return (i / 100) / 12

def count_of_months(principal, monthly_payment, i):
    n = math.ceil(math.log((monthly_payment / (monthly_payment - i * principal)), 1 + i))
    years = math.floor(n / 12)
    months = n - (years * 12)
    if months != 0:
        print("You need {} years and {} months to repay this credit!".format(int(years), int(months)))
    else:
        print("You need {} years to repay this credit!".format(int(years)))
    return n

def credit_principal(count_of_periods, monthly_payment, i):
    a = monthly_payment / ((i * pow((1 + i), count_of_periods)) / (pow((1 + i), count_of_periods) - 1))
    print("Your credit principal = {}!".format(int(a)))
    return a

def annuity_payment(credit_principal, i, count_of_periods):
    return math.ceil(credit_principal * ((i * pow((1 + i), count_of_periods)) / (pow((1 + i), count_of_periods) - 1)))

def differentiated_payment(credit_principal, number_of_months, interest_rate, current_period):
    return math.ceil(credit_principal / number_of_months + interest_rate * (credit_principal - ((credit_principal * (current_period - 1)) / number_of_months)))

possible_choices = ["diff", "annuity"]
all_payment = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str)
    parser.add_argument("--principal", type=int)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)
    parser.add_argument("--payment", type=int)

    args = parser.parse_args()
    params = [args.type, args.principal, args.periods, args.interest, args.payment]

    n_none = 0
    for t in params:
        if t is None:
            n_none += 1

    type = params[0]
    principal = params[1]
    periods = params[2]
    i = params[3]
    payment = params[4]
    if type not in possible_choices or n_none > 2:
        if principal is not None or periods is not None:
            if principal < 0 or periods < 0 or i < 0:
                print("Incorrect parameters")
            else:
                print("Incorrect parameters")
        else:
            print("Incorrect parameters")
    elif type == 'diff' and i is not None:
        i = interest(i)
        for m in range(1, periods + 1):
            d = differentiated_payment(principal, periods, i, m)
            all_payment += d
            print("Month {}: paid out {}".format(m, int(d)))
        print("\nOverpayment = %d" % (all_payment - principal))
    elif type == 'annuity' and i is not None:
        i = interest(i)
        if periods is not None and payment is not None:
            a = credit_principal(periods, payment, i)
            all_payment += periods * payment
            print("Overpayment = %d" % (all_payment - a))
        elif periods is not None:
            a = annuity_payment(principal, i, periods)
            all_payment += a
            print("Your annuity payment = {}!".format(a))
            print("Overpayment = %d" % ((all_payment * periods) - principal))
        else:
            n = count_of_months(principal, payment, i)
            all_payment += n * payment
            print("Overpayment = %d" % (all_payment - principal))
    else:
        print("Incorrect parameters")

