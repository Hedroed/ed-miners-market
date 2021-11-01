module.exports = {
  publicPath: '/',
  pluginOptions: {
    moment: {
      locales: [
        'en'
      ]
    }
  },
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'ED Miners Market',
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
    about: {
        entry: 'src/about.js',
        template: 'public/about.html',
        filename: 'about.html',
        title: 'ED Miners Market | About',
        chunks: ['chunk-vendors', 'chunk-common', 'about']
    }
  }
}
