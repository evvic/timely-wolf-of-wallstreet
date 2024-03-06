# timely-wolf-of-wallstreet
webapp to show relevant stock charts and news

> Note: for testing this webapp this project is deploying to GitHub pages

# Best Practices
- Every feature/addition requires a GitHub projects ticket
- The feature/addition is then developed in a branch
  - The name of the branch is the exact name of the ticket number
> Note: NEVER COMMIT DIRECTLY TO MAIN BRANCH
- To merge the feature branch to main a PR must be submitted
- The PR must pass code review to be approved

# Setup

## Project Initialization
- This project uses [Vite](https://vitejs.dev/) to initialize and bundle the [Svelte](https://svelte.dev/) project

## Running Project
- For testing this project and viewing it in local browser (localhost)
- Supports **hot reloading**
```
cd webapp
npm install
npm run dev
```

## Building Project
- For building the project to deploy on a webserver
```
cd webapp
npm install
npm run build
```
