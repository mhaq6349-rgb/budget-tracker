# Budget Tracker

A premium dark-finance personal budget tracker. Single-file HTML — download and open, or run with Python.

## Features

- **Income / Expense tracking** with 17 categories
- **Monthly budgeting** — set spending limits per category with progress bars
- **Month navigation** — view past budgets and spending
- **SVG donut breakdown** of expenses by category
- **Insights** — top spending category, savings rate, transaction count
- **Search** transactions by description or category
- **Export to CSV**
- **localStorage persistence** — works offline from `file://`
- **Optional Flask backend** for server-side persistence

## Usage

**No server needed:**
```
open index.html
```

**With Python server:**
```bash
pip install flask
py server.py
# → http://localhost:5000
```

## Categories

| Income | Expense |
|--------|---------|
| Salary, Freelance, Investments, Gifts, Refunds, Business | Food & Dining, Transportation, Shopping, Entertainment, Bills & Utilities, Health, Education, Groceries, Rent, Subscriptions, Travel |

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions` | List all transactions |
| POST | `/api/transactions` | Add transaction |
| DELETE | `/api/transactions/<id>` | Delete transaction |
| GET | `/api/budgets` | Get budget limits |
| PUT | `/api/budgets` | Set budget limits |
