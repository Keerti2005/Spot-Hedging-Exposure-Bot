def calculate_optimal_hedge_size(delta, target_delta=0, partial_hedge_pct=1.0):
    return (delta - target_delta) * partial_hedge_pct

def simulate_hedge(asset, hedge_size, est_price=None, slippage_pct=0.001, fixed_fee=2.0):
    if est_price is None:
        est_price = 100
    gross_cost = hedge_size * est_price
    slippage_cost = gross_cost * slippage_pct
    total_cost = gross_cost + slippage_cost + fixed_fee
    return (f"✅ Hedge executed for {hedge_size:.4f} {asset}.\n\n"
            f"• Gross cost: ${gross_cost:,.2f}\n"
            f"• Slippage: ${slippage_cost:,.2f}\n"
            f"• Fee: ${fixed_fee:,.2f}\n"
            f"• Total cost: ${total_cost:,.2f}")
