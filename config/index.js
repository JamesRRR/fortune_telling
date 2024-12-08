const env = wx.getAccountInfoSync().miniProgram.envVersion;

const config = {
  development: {
    apiBaseUrl: 'https://lavish-insight-dev.up.railway.app'  // 开发环境
  },
  release: {
    apiBaseUrl: 'https://fortunetelling-production.up.railway.app'  // 生产环境
  }
};

module.exports = config[env] || config.development; 