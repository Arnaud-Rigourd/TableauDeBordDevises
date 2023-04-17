from django.shortcuts import render, redirect
import api


def redirect_index(request):
    return redirect("devise-dashboard", days_range=30, chosen_currencies="USD")


def dashboard(request, days_range=30, chosen_currencies="USD"):
    days, rates = api.get_rates(chosen_currencies, days_range)
    currencies = [currency for currency, rates in rates.items()]
    rate_per_currency = [rates for currency, rates in rates.items()]
    days_as_string = ",".join(days)
    period = {7: "Week", 30: "Month", 365: "Year"}.get(days_range, f"Custom: {days_range} days")
    return render(request, "devise/dashboard.html", context={
                                                            "days": days,
                                                            "days_as_string": days_as_string,
                                                            "rates": rate_per_currency,
                                                            "currencies": currencies,
                                                            "chosen_currencies": chosen_currencies,
                                                            "period": period
                                                    })


