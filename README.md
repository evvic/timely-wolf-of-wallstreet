# timely-wolf-of-wallstreet
webapp to show relevant stock charts and news

> Note: for testing this webapp this project is deploying to GitHub pages

# Best Practices
## Feature Ticket
- Every feature/addition requires a GitHub projects ticket
- The feature/addition is then developed in a branch
- The name of the branch is the exact name of the ticket number

## Branches
> Note: NEVER COMMIT DIRECTLY TO MAIN BRANCH
- To merge the feature branch to main a PR must be submitted
- The PR must pass code review to be approved

## Tags
- Notable features should add a tag
- The tag should increment the correct decimal precision `x.x.x` depending on the size of the feature
  - Tags are created on **main**
- Create a tag like so:
```
git tag -a 0.0.1 -m "Initialize Svelte project"
git push --tags
```

# Setup

## Project Initialization
- This project uses [Vite](https://vitejs.dev/) to initialize and bundle the [Svelte](https://svelte.dev/) project
- This webapp was initialized with
```
npm init vite
```

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
