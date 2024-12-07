let isAppInitializing = false;

App({
  globalData: {
    pageLoaded: false
  },

  onLaunch: function() {
    if (isAppInitializing) {
      console.log('App already initializing, skipping');
      return;
    }
    isAppInitializing = true;
    
    console.log('App Launch');
    this.globalData.pageLoaded = false;
    
    isAppInitializing = false;
  },

  onShow: function() {
    console.log('App Show');
  },

  onHide: function() {
    console.log('App Hide');
    // 保存状态
    this.globalData.pageLoaded = true;
  },

  onError: function(err) {
    console.error('App Error:', err);
    wx.showToast({
      title: '应用出现错误',
      icon: 'none'
    });
  },

  onPageNotFound: function(res) {
    console.error('Page Not Found:', res);
    wx.redirectTo({
      url: '/pages/fortune/fortune'
    }).catch(err => {
      console.error('Redirect failed:', err);
    });
  }
}); 