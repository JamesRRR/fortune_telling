const env = wx.getAccountInfoSync().miniProgram.envVersion;
console.log('Current environment:', env);
console.log('Is devtools?', typeof __wxConfig !== 'undefined' && __wxConfig.platform === 'devtools');

// 根据环境选择对应的配置文件
let envConfig;
try {
  if (env === 'develop' && typeof __wxConfig !== 'undefined' && __wxConfig.platform === 'devtools') {
    // 本地开发环境 (.env.dev.js)
    envConfig = require('./../.env.dev.js');
  } else if (env === 'develop' || env === 'trial') {
    // 开发版/体验版环境 (.env.test.js)
    envConfig = require('./../.env.test.js');
  } else {
    // 正式环境 (.env.prod.js)
    envConfig = require('./../.env.prod.js');
  }
} catch (error) {
  console.error('Failed to load environment config:', error);
  // 提供默认配置
  envConfig = {
    API_URL: 'https://lavish-insight-dev.up.railway.app',
    DEBUG: true
  };
}

const config = {
  apiBaseUrl: envConfig.API_URL,
  debug: typeof envConfig.DEBUG === 'string' ? envConfig.DEBUG === 'True' : !!envConfig.DEBUG,
  // 其他从环境文件中读取的配置...
};

module.exports = config; 