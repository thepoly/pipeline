const merge = require('webpack-merge');
const common = require('./webpack.config.js');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = merge(common, {
    mode: 'development',
    plugins: [
        new CleanWebpackPlugin(['./pipeline/static/webpack_bundles/']),
    ]
});
