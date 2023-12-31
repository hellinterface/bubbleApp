const { defineConfig } = require('@vue/cli-service');
const { readFileSync } = require('fs');
module.exports = {
	chainWebpack: config => {
		config.module
			.rule('vue')
			.use('vue-loader')
			.tap(options => {
				options.compilerOptions = {
					...options.compilerOptions,
					isCustomElement: tag => tag.startsWith('icon')
				}
				return options
			})
	},/*
	devServer: {
		port: 8080,
		https: {
			key: readFileSync("../localhost.key"),
			cert: readFileSync("../localhost.crt"),
			ca: readFileSync("../localhost_ca.pem"),
		},
	},*/
	pages: {
		app: {
			entry: 'src/pages/index/main.js',
			template: 'public/index.html',
			filename: 'app.html',
			title: 'Bubble',
			// chunks to include on this page, by default includes
			// extracted common chunks and vendor chunks.
			//chunks: ['chunk-vendors', 'chunk-common', 'index']
		},
		landing: {
			entry: 'src/pages/landing/landing.js',
			template: 'public/landing/landing.html',
			filename: 'index.html',
			title: 'Bubble'
		},
		login: {
			entry: 'src/pages/login/main.js',
			template: 'public/login.html',
			filename: 'login.html',
			title: 'Log In | Bubble'
		},
		signup: {
			entry: 'src/pages/signup/main.js',
			template: 'public/signup.html',
			filename: 'signup.html',
			title: 'Sign Up | Bubble'
		}
	}
}