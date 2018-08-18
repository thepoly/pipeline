const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  mode: 'none',
  context: __dirname,
  entry: [
    './pipeline/static/js/pipeline.js',
    './pipeline/static/css/pipeline.scss',
  ],
  output: {
    path: path.resolve('./pipeline/static/webpack_bundles/'),
    filename: '[name]-[hash].js'
  },

  plugins: [
    new CleanWebpackPlugin(['./pipeline/static/webpack_bundles/']),
    new BundleTracker({ filename: './webpack-stats.json' }),
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css',
      chunkFilename: '[id].css'
    })
  ],
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {}
          }
        ]
      },
      {
        test: /\.(scss)$/,
        use: [
          'style-loader',
          {
            loader: MiniCssExtractPlugin.loader,
            options: {}
          },
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              config: {
                path: path.resolve('./postcss.config.js')
              }
            }
          },
          'sass-loader'
        ]
      }
    ]
  }
}
