# GitHub Actions Setup Guide

This guide will walk you through setting up automated Windows executable builds using GitHub Actions.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository

## Step-by-Step Setup

### Step 1: Push Your Code to GitHub

If you haven't already, push your code to GitHub:

```bash
# If this is a new repo
git init
git add .
git commit -m "Initial commit with WORM Settings feature"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ctools.git
git push -u origin main

# If you already have a repo
git add .
git commit -m "Add WORM Settings and GitHub Actions workflow"
git push
```

### Step 2: GitHub Actions Will Run Automatically

Once you push to GitHub:
1. Go to your repository on GitHub
2. Click the "Actions" tab at the top
3. You'll see your workflow running
4. Wait for it to complete (usually 3-5 minutes)

### Step 3: Download Your Executable

After the workflow completes successfully:

1. In the Actions tab, click on the latest workflow run
2. Scroll down to the "Artifacts" section
3. Click on "ctools-windows-exe" to download
4. Extract the zip file to get `ctools.exe`

## Manual Triggering

You can also trigger a build manually:

1. Go to Actions tab
2. Click "Build Windows Executable" in the left sidebar
3. Click "Run workflow" button on the right
4. Select the branch and click "Run workflow"

## Troubleshooting

### Build Fails

If the build fails, click on the failed workflow run to see error logs:
- Red X means it failed
- Click on the job name to see detailed logs
- Common issues:
  - Missing dependencies in requirements.txt
  - Python syntax errors
  - Missing files

### Icon/Logo Issues

If you see errors about missing icon.jpeg or logo.png:
- Make sure these files are committed to your repo
- Update the workflow file to remove the `--icon` flag if you don't have an icon

### Download the Build Logs

If you need to debug:
1. Click on the failed/completed workflow
2. Click on the job name
3. Each step shows detailed output
4. You can download the full log using the "..." menu

## Creating Releases

To create a tagged release with the executable:

```bash
# Create and push a tag
git tag -a v3.2.2 -m "Release version 3.2.2 with WORM Settings"
git push origin v3.2.2
```

This will:
1. Trigger the workflow
2. Build the executable
3. Automatically create a GitHub Release with the .exe attached

## Cost

- **Free for public repositories**
- **2,000 minutes/month free for private repositories**
- Windows builds use 2x minutes (3 min build = 6 mins consumed)
- You can build ~333 times per month on the free tier

## Next Steps

After your first successful build:
1. Download the .exe
2. Test it on a Windows machine
3. If it works, you're done!
4. Future builds happen automatically on every push
