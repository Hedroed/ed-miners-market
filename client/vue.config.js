module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/ed-miners-market/'
    : '/',
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
      title: 'ED Dealers',
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
    about: {
        entry: 'src/about.js',
        template: 'public/about.html',
        filename: 'about.html',
        title: 'ED Dealers | About',
        chunks: ['chunk-vendors', 'chunk-common', 'about']
    }
  }
}
