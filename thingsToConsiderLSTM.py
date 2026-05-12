preds = (probs > 0.5).astype(int)

print("Pred up rate:", preds.mean())
print("Actual up rate:", nnyTest.numpy().mean())


results = pd.DataFrame({
    "prob": probs,
    "actual": nnyTest.numpy().flatten()
})

results["bucket"] = pd.qcut(results["prob"], 5, duplicates="drop")

print(results.groupby("bucket")["actual"].agg(["count", "mean"]))


for t in [0.50, 0.55, 0.60, 0.65, 0.70]:
    mask = results["prob"] > t
    print(t, "trades:", mask.sum(), "win rate:", results.loc[mask, "actual"].mean())


results["forwardRet"] = (
    technicalData["SPY"]["Close"]
    .pct_change()
    .shift(-1)
    .iloc[-len(results):]
    .values
)

for t in [0.5, 0.55, 0.6, 0.65, 0.7]:
    mask = results["prob"] > t

    avgRet = results.loc[mask, "forwardRet"].mean()
    sharpe = (
        results.loc[mask, "forwardRet"].mean() /
        results.loc[mask, "forwardRet"].std()
    ) * np.sqrt(252)

    print(
        t,
        "trades:", mask.sum(),
        "avgRet:", round(avgRet, 5),
        "sharpe:", round(sharpe, 2)
    )





    