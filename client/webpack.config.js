const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = (env, options) => ({
  entry: [
    path.resolve(__dirname, 'index.ts'),
    path.resolve(__dirname, 'index.styl'),
  ],
  output: {
    filename: '[name].[contenthash:8].js',
    chunkFilename: '[name].[chunkhash:8].bundle.js',
    path: path.resolve(__dirname, '../static'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: 'babel-loader',
      },
      {
        test: /\.ts?$/,
        loader: 'ts-loader',
        options: {
          appendTsSuffixTo: [/\.vue$/],
        },
      },
      {
        test: /\.vue$/,
        use: 'vue-loader',
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)$/,
        include: /fonts/,
        use: {
          loader: 'file-loader',
          options: {
            name: 'fonts/[name].[contenthash:8].[ext]',
          },
        }
      },
      {
        test: /\.(png|jpg|jpeg|svg)$/,
        include: /images/,
        use: {
          loader: 'file-loader',
          options: {
            name: 'images/[name].[contenthash:8].[ext]',
          },
        }
      },
      {
        test: /\.pug$/,
        use: 'pug-plain-loader',
      },
      {
        test: /\.(css|styl)$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              modules: true,
            },
          },
          'stylus-loader',
        ]
      },
    ],
  },
  // resolve: { extensions: ['.js', '.json', '.vue', '.css' ] },
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, 'index.html'),
    }),
  ],
  devServer: {
    port: process.env.PORT_TEST_CLIENT,
    host: '0.0.0.0',
    hot: true,
    disableHostCheck: true,
  },
});
