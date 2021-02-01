# Tokugawa Atlas
Tokugawa Atlas is a Vue application that interacts with ArcGIS Online to display an interactive map of Japan during the Edo Period (1603-1868). 
For more information about the project, visit [Yale's Official Page](https://dtl.macmillan.yale.edu/digital-atlas-tokugawa-japan).

## Prerequisites
- [Node.js and Npm](https://nodejs.org/en/)

## Setup

### 1. Image Server Backend
First, start the image server by entering `backend/` directory. 

Install the dependencies with the following command 
```
npm install
```

Then, start the server with 
```
node server
```

### 2. Web Application
To run the app, in another window navigate to `frontend/`.

Install dependencies with:
```
npm install
```

Compile and run the Vue development server with:
```
npm run serve
```

## Notes
- Dependencies only need to be installed once
- Vue dev server automatically updates when files in project updated, no need to restart.

