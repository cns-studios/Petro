FROM node:18

# Set the working directory inside the container.
# All subsequent commands will be run from this directory.
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files first.
# This allows Docker to use layer caching, so these steps are
# only re-run if your dependencies change.
COPY package*.json ./

# Install application dependencies.
RUN npm install

# Copy the rest of the application source code into the container.
COPY . .

# Expose the port that your Node.js application is listening on.
# You can change this if your app uses a different port.
EXPOSE 3000

# Define the command to run your application when the container starts.
# Replace 'server.js' with the entry point of your application.
CMD ["node", "server.js"]
