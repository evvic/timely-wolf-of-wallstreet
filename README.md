# timely-wolf-of-wallstreet
webapp to show relevant stock charts and news

> Note: for testing this webapp this project is deploying to GitHub pages

# Best Practices

## Feature Ticket
- Every feature/addition requires an [issue to be created](https://github.com/evvic/timely-wolf-of-wallstreet/issues)
  - Please link the issue to the GitHub project [Daily Charts Browser Extension](https://github.com/users/evvic/projects/3)
- The issue is then developed in a branch
  - Within the **issue page** of the created issue a branch can be generated that automatically links the issue with the beanch and the GitHub Project
  - This gives the branch an ID that matches the issues ID
> If unsure how to do any of this ask *[@evvic](https://github.com/evvic)*

## Branches
> Note: **NEVER COMMIT DIRECTLY TO MAIN BRANCH**
- To merge the feature branch to main a PR must be submitted
- The PR must pass a code review to be approved

## Tags
- Notable features should add a tag
- The tag should increment the correct decimal precision `x.x.x` depending on the size of the feature 
  - Tags are created on **main**
- Create a tag like so:
```
git tag -a 0.0.1 -m "Initialize Svelte project"
git push --tags
```
- Add the tag after perging your PR

# Setup

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
- Creates a directory named `dist` inside `webapp` containing built webapp to deploy

## First Time Setup

### Clone Repo To Local
- Simply run the following 
```
git clone git@github.com:evvic/timely-wolf-of-wallstreet.git
```

### Install Node
- **This project requires node version** `v18.0.0` **or higher**
- Run the following commands to update node:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm --version
nvm install --lts
node --version
```
- The commands above:
  - Install `nvm` (node version manager)
  - Have the new nvm actively running in the current terminal (~/.bashrc)
  - Check the nvm version
  - Install node **lts** (long term support) version
  - Check the node version
- Node version should now be `v20.11.1` or greater!

### Project Initialization
> **This step does not need to be done**, but shows how to initialize a new Vite + Svelte project
- This project uses [Vite](https://vitejs.dev/) to initialize and bundle the [Svelte](https://svelte.dev/) project
- This webapp was initialized with
```
npm init vite
```

