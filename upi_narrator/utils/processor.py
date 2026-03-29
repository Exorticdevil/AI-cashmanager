import pandas as pd
import re

# ── Category mapping ─────────────────────────────────────────────────────────
CATEGORY_MAP = {
    "swiggy":        "Food",
    "zomato":        "Food",
    "mcdonald":      "Food",
    "domino":        "Food",
    "pizza":         "Food",
    "kfc":           "Food",
    "cafe":          "Food",
    "restaurant":    "Food",
    "chai":          "Food",
    "food":          "Food",
    "uber":          "Transport",
    "ola":           "Transport",
    "rapido":        "Transport",
    "metro":         "Transport",
    "irctc":         "Transport",
    "makemytrip":    "Transport",
    "redbus":        "Transport",
    "amazon":        "Shopping",
    "flipkart":      "Shopping",
    "myntra":        "Shopping",
    "meesho":        "Shopping",
    "nykaa":         "Shopping",
    "bigbasket":     "Groceries",
    "blinkit":       "Groceries",
    "zepto":         "Groceries",
    "grofers":       "Groceries",
    "netflix":       "Entertainment",
    "spotify":       "Entertainment",
    "prime":         "Entertainment",
    "hotstar":       "Entertainment",
    "youtube":       "Entertainment",
    "electricity":   "Bills",
    "water":         "Bills",
    "gas":           "Bills",
    "broadband":     "Bills",
    "jio":           "Bills",
    "airtel":        "Bills",
    "bsnl":          "Bills",
    "vi ":           "Bills",
    "insurance":     "Bills",
    "hospital":      "Health",
    "pharmacy":      "Health",
    "medplus":       "Health",
    "apollo":        "Health",
    "doctor":        "Health",
    "clinic":        "Health",
    "college":       "Education",
    "school":        "Education",
    "tuition":       "Education",
    "fees":          "Education",
    "course":        "Education",
}

CATEGORY_COLORS = {
    "Food":          "#a78bfa",
    "Transport":     "#60a5fa",
    "Shopping":      "#4ade80",
    "Groceries":     "#34d399",
    "Entertainment": "#f472b6",
    "Bills":         "#fbbf24",
    "Health":        "#f87171",
    "Education":     "#38bdf8",
    "Others":        "#94a3b8",
}

def categorise(description: str) -> str:
    desc = str(description).lower()
    for keyword, category in CATEGORY_MAP.items():
        if keyword in desc:
            return category
    return "Others"

def parse_gpay_csv(df: pd.DataFrame) -> pd.DataFrame:
    """Handle Google Pay CSV column names."""
    col_map = {}
    for col in df.columns:
        c = col.strip().lower()
        if "date" in c:
            col_map[col] = "date"
        elif "description" in c or "narration" in c or "particular" in c or "note" in c:
            col_map[col] = "description"
        elif "debit" in c or "amount" in c or "withdrawal" in c:
            col_map[col] = "amount"
        elif "credit" in c:
            col_map[col] = "credit"
        elif "balance" in c:
            col_map[col] = "balance"
    df = df.rename(columns=col_map)
    if "amount" not in df.columns and "credit" in df.columns:
        df["amount"] = df.get("debit", 0).fillna(0)
    return df

def load_and_clean(uploaded_file) -> pd.DataFrame:
    """Load CSV, normalise columns, categorise transactions."""
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        return pd.DataFrame()

    df = parse_gpay_csv(df)

    required = {"date", "description", "amount"}
    if not required.issubset(set(df.columns)):
        for col in required - set(df.columns):
            df[col] = "Unknown" if col == "description" else (pd.Timestamp.now() if col == "date" else 0)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(
        df["amount"].astype(str).str.replace(",", "").str.replace("₹", "").str.strip(),
        errors="coerce"
    ).fillna(0).abs()

    df = df[df["amount"] > 0].copy()
    df["category"] = df["description"].apply(categorise)
    df["day_of_week"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["month"] = df["date"].dt.strftime("%B %Y")
    df["merchant"] = df["description"].apply(
        lambda x: str(x).split("@")[0].split("-")[0].strip()[:25]
    )
    return df

def get_summary(df: pd.DataFrame) -> dict:
    """Return key summary stats."""
    if df.empty:
        return {}
    by_cat    = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    by_merch  = df.groupby("merchant")["amount"].sum().sort_values(ascending=False).head(8)
    by_day    = df.groupby("day_of_week")["amount"].sum()
    top_cat   = by_cat.idxmax() if not by_cat.empty else "N/A"
    total     = df["amount"].sum()
    n_trans   = len(df)
    days      = max((df["date"].max() - df["date"].min()).days, 1)
    avg_day   = total / days

    late_night = df[df["hour"] >= 22]
    late_pct   = round(len(late_night) / n_trans * 100) if n_trans else 0

    day_order  = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    by_day     = by_day.reindex([d for d in day_order if d in by_day.index])
    busiest_day= by_day.idxmax() if not by_day.empty else "N/A"

    return {
        "total":        round(total, 2),
        "n_trans":      n_trans,
        "avg_day":      round(avg_day, 2),
        "top_cat":      top_cat,
        "top_cat_amt":  round(by_cat.get(top_cat, 0), 2),
        "top_cat_pct":  round(by_cat.get(top_cat, 0) / total * 100) if total else 0,
        "by_cat":       by_cat.round(2).to_dict(),
        "by_merch":     by_merch.round(2).to_dict(),
        "by_day":       by_day.round(2).to_dict(),
        "busiest_day":  busiest_day,
        "late_night_pct": late_pct,
        "late_night_n": len(late_night),
        "colors":       CATEGORY_COLORS,
    }
