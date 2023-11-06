const { defineConfig } = require('@vue/cli-service')
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
	},
	pages: {
		index: {
			entry: 'src/pages/index/main.js',
			template: 'public/index.html',
			filename: 'index.html',
			title: 'Main App',
			// chunks to include on this page, by default includes
			// extracted common chunks and vendor chunks.
			chunks: ['chunk-vendors', 'chunk-common', 'index']
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
		},
		admin: {
			entry: 'src/pages/admin/main.js',
			template: 'public/admin.html',
			filename: 'admin.html',
			title: 'Bubble Admin Panel'
		}
	}
}