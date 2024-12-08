const app = getApp();  // 获取全局 app 实例

let isPageLoaded = false;

Page({
  data: {
    messages: [],
    inputMessage: '',
    scrollToView: '',
    isLoading: false
  },

  onLoad() {
    if (!isPageLoaded) {
      this.setData({
        messages: [{
          type: 'assistant',
          content: '✨ 你好呀！我是你的算命小助手，很高兴见到你！来问我点什么吧~ ✨'
        }]
      });
      isPageLoaded = true;
    }
  },

  onUnload() {
    // 清理定时器
    if (this.sendMessageTimer) {
      clearTimeout(this.sendMessageTimer);
    }
    isPageLoaded = false;
  },

  onShow() {
    // 页面显示时的处理
  },

  bindinput(e) {
    this.setData({
      inputMessage: e.detail.value
    });
  },

  sendMessage() {
    const message = this.data.inputMessage.trim();
    if (!message || this.data.isLoading) return;

    // 添加防抖处理
    if (this.sendMessageTimer) {
      clearTimeout(this.sendMessageTimer);
    }

    this.sendMessageTimer = setTimeout(() => {
      this._sendMessageToServer(message);
    }, 300);
  },

  _sendMessageToServer(message) {
    // 原来的发送消息逻辑
    const messages = [...this.data.messages, {
      type: 'user',
      content: message
    }];

    this.setData({
      messages,
      inputMessage: '',
      isLoading: true,
      scrollToView: `msg-${messages.length - 1}`
    });

    // 发送请求到后端
    wx.request({
      url: 'http://localhost:5001/chat',
      method: 'POST',
      data: {
        message: message
      },
      success: (res) => {
        const response = res.data.response;
        const updatedMessages = [...this.data.messages, {
          type: 'assistant',
          content: response
        }];

        this.setData({
          messages: updatedMessages,
          scrollToView: `msg-${updatedMessages.length - 1}`
        });
      },
      fail: (error) => {
        console.error('请求失败：', error);
        wx.showToast({
          title: '啊哦，出错了~请重试',
          icon: 'none'
        });
      },
      complete: () => {
        this.setData({
          isLoading: false
        });
      }
    });
  }
}); 