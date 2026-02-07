# Data Analysis Projekt

This repo contains a Python sales analytics pipeline and a Next.js frontend dashboard.

## Run Instructions

1) Generate the raw data:

```bash
python sales-analytics/generate_data.py
```

2) Run the backend pipeline (analytics + exports):

```bash
python sales-analytics/main.py
```

3) Install frontend dependencies:

```bash
cd frontend
pnpm install
```

4) Start the frontend:

```bash
pnpm run dev
```

## Notes

- The analytics pipeline writes outputs to `sales-analytics/output` and copies `analytics.json` into `frontend/public`.
- Output artifacts are ignored by git via `.gitignore`.
