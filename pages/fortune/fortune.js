const app = getApp();  // 获取全局 app 实例

let isInitializing = false;  // 添加初始化锁

Page({
  data: {
    messages: [],
    inputMessage: '',
    scrollToView: '',
    isLoading: false
  },

  onLoad() {
    // 添加欢迎消息
    this.setData({
      messages: [{
        type: 'assistant',
        content: '✨ 你好呀！我是你的算命小助手，很高兴见到你！来问我点什么吧~ ✨'
      }]
    });
  },

  onInputChange(e) {
    this.setData({
      inputMessage: e.detail.value
    });
  },

  sendMessage() {
    const message = this.data.inputMessage.trim();
    if (!message || this.data.isLoading) return;

    // 添加用户消息
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
      url: 'http://your-backend-url/chat',
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