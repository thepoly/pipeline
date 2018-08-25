const merge = require('webpack-merge');
const common = require('./webpack.config.js');

module.exports = merge(common, {
    mode: 'development',
    plugins: [
        new CleanWebpackPlugin(['./pipeline/static/webpack_bundles/']),
    ]
});
