const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
    transpileDependencies: true,
    configureWebpack: {
        module: {
            rules: [{
                    test: /worker-javascript\.js$/,
                    use: { loader: 'worker-loader' }
                }
                // Add other worker loaders if needed
            ]
        }
    }
});