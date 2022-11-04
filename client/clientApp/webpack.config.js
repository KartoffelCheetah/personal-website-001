const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = (env, options) => {
  const NE_DEV = 'development';
  const NE_PROD = 'production';
  const validNodeEnvs = new Set([NE_DEV, NE_PROD]);
  if (!validNodeEnvs.has(process.env.NODE_ENV)) {
    throw new Error(`process.env.NODE_ENV is not valid, expected one of: ${[...validNodeEnvs]}, received: ${process.env.NODE_ENV}`);
  }
  return {
    entry: [
      path.resolve(__dirname, 'index.ts'),
      path.resolve(__dirname, 'index.styl'),
    ],
    output: {
      filename: '[name].[contenthash:8].js',
      chunkFilename: '[name].[chunkhash:8].bundle.js',
      path: path.resolve(__dirname, '..', '..', 'static'),
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
          test: /\.(woff(2)?|ttf|otf|eot|svg)$/,
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
            process.env.NODE_ENV === NE_PROD ? MiniCssExtractPlugin.loader : 'style-loader',
            {
              loader: 'css-loader',
              options: {
                modules: false,
              },
            },
            'stylus-loader',
          ]
        },
      ],
    },
    plugins: [
      new VueLoaderPlugin(),
      ...(process.env.NODE_ENV === NE_PROD ? [new MiniCssExtractPlugin()] : []),
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
  };
};
