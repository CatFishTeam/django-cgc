var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './assets/scripts/index',
    output: {
        path: path.resolve('./assets/webpack_bundles/'),
        filename: "[name].js"
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ]
}
