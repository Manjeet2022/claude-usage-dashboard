# Claude utilization dashboard - GitHub free version

No n8n, no server, no cost. GitHub Actions fetches your usage/cost data
every hour and GitHub Pages hosts the dashboard that reads it.

## Step 1 - Create a repository
1. Go to https://github.com and sign in (or sign up, it's free).
2. Click "+" (top right) -> "New repository".
3. Name it something like `claude-usage-dashboard`.
4. Set it to **Private** (recommended, since it will contain cost data
   even though the actual API keys stay in Secrets, not in the code).
5. Click "Create repository".

## Step 2 - Upload these files
Upload all files from this folder, keeping the same structure:
```
claude-usage-dashboard/
├── .github/
│   └── workflows/
│       └── update_usage.yml
├── scripts/
│   └── fetch_usage.py
├── data.json
└── index.html
```
Easiest way: on the repo page, click "Add file" -> "Upload files", drag
the whole folder in (GitHub keeps the folder structure automatically).

## Step 3 - Add your Admin API keys as Secrets
1. In your repo: Settings -> Secrets and variables -> Actions.
2. Click "New repository secret" and add each one:
   - `ORG1_ADMIN_KEY` = sk-ant-admin-... (Antiersolutions-exchange)
   - `ORG2_ADMIN_KEY` = sk-ant-admin-... (Antiersolutions-DeFi)
   - `ORG3_ADMIN_KEY` = sk-ant-admin-... (Antier-QA)
   - `ORG4_ADMIN_KEY` = sk-ant-admin-... (Antier.Mobile.Ror)
   - `ORG5_ADMIN_KEY` = sk-ant-admin-... (3rd floor Antiersolutions)
   - `ORG6_ADMIN_KEY` = sk-ant-admin-... (Antier - Gaming and Metaverse)
   Get each key from that org's Console -> Settings -> Admin API keys
   (you need Owner/Admin role there).

## Step 4 - Turn on GitHub Pages
1. Repo -> Settings -> Pages.
2. Under "Build and deployment", Source = "Deploy from a branch".
3. Branch = `main`, folder = `/ (root)`. Save.
4. GitHub gives you a URL like:
   `https://<your-username>.github.io/claude-usage-dashboard/`
   That's your live dashboard link - bookmark it, open it anytime.

## Step 5 - Run it once manually (don't wait for the hourly clock)
1. Repo -> Actions tab -> "Update Claude usage data" workflow.
2. Click "Run workflow" -> "Run workflow" button.
3. Wait ~30 seconds, refresh, it should show green.
4. Open your Pages URL from Step 4 - numbers should now be real.

After that, it updates itself every hour automatically - no manual step
needed again.

## Notes
- Free tier limits: GitHub Actions gives 2,000 free minutes/month on
  private repos (this job takes seconds, so an hourly run costs
  nothing meaningful). Public repos are unlimited.
- "review" status badge = that org's 7-day cost crossed $500. Change
  `REVIEW_THRESHOLD_USD` in `scripts/fetch_usage.py` if you want a
  different limit.
- "no_key" status = that Secret isn't set yet for that org.
- If your repo is private, GitHub Pages on a private repo requires
  GitHub Pro/Team/Enterprise. If you're on a free personal account,
  either make the repo public (fine, since API keys live only in
  Secrets, never in the code or data.json) or upgrade your plan.
