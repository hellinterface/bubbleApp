const { defineConfig } = require('@vue/cli-service')
module.exports = {
  pages: {
    index: {
      entry: 'src/index/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'Main App',
      // chunks to include on this page, by default includes
      // extracted common chunks and vendor chunks.
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
    login: {
      entry: 'src/login/main.js',
      template: 'public/login.html',
      filename: 'login.html',
      title: 'Log In | Bubble'
    },
    signup: {
      entry: 'src/signup/main.js',
      template: 'public/signup.html',
      filename: 'signup.html',
      title: 'Sign Up | Bubble'
    },
  }
}