const path = require('path');
const webpack = require('webpack');
const jquery = require('jquery');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'webpack.js',
    path: path.resolve(__dirname, 'static'),
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: require.resolve('jquery'),
      jQuery: require.resolve('jquery')
  }),
  ],
  module: {
    rules: [
      { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
    ]
  }
};
