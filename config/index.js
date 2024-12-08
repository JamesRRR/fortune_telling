const env = wx.getAccountInfoSync().miniProgram.envVersion;

// 根据环境选择对应的配置文件
let envConfig;
try {
  if (env === 'develop' && typeof __wxConfig !== 'undefined' && __wxConfig.platform === 'devtools') {
    // 本地开发环境 (.env.dev)
    envConfig = require('../.env.dev');
  } else if (env === 'develop' || env === 'trial') {
    // 开发版/体验版环境 (.env.test)
    envConfig = require('../.env.test');
  } else {
    // 正式环境 (.env.prod)
    envConfig = require('../.env.prod');
  }
} catch (error) {
  console.error('Failed to load environment config:', error);
  // 提供默认配置
  envConfig = {
    API_URL: 'https://lavish-insight-dev.up.railway.app'
  };
}

const config = {
  apiBaseUrl: envConfig.API_URL,
  debug: envConfig.DEBUG === 'True',
  // 其他从环境文件中读取的配置...
};

module.exports = config; 