console.log('Trying to require:', '../../config/experts');
const experts = require('../../config/experts');
const config = require('../../config/index');

const app = getApp();
let isPageLoaded = false;

Page({
  data: {
    experts: Object.values(experts),
    selectedExpert: null,
    skippedSelection: false,
    messages: [],
    inputMessage: '',
    scrollToView: '',
    isLoading: false
  },

  onLoad() {
    if (!isPageLoaded) {
      this.setData({
        messages: []  // 清空默认消息，等待选择专家
      });
      isPageLoaded = true;
    }
  },

  selectExpert(e) {
    const expert = e.currentTarget.dataset.expert;
    this.setData({
      selectedExpert: expert,
      messages: [
        ...this.data.messages,  // 保留现有消息
        {
          type: 'assistant',
          content: `您好，我是${expert.name}，${expert.description}。请问有什么想问的吗？`
        }
      ]
    });
  },

  skipExpertSelection() {
    this.setData({
      skippedSelection: true,
      messages: [
        ...this.data.messages,  // 保留现有消息
        {
          type: 'assistant',
          content: '✨ 你好呀！我是你的小助手，很高兴见到你！来问我点什么吧~ ✨'
        }
      ]
    });
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

    wx.request({
      url: `${config.apiBaseUrl}/chat`,
      method: 'POST',
      data: {
        message: message,
        expert: this.data.selectedExpert?.id || 'default',
        history: this.data.messages  // 发送所有历史消息
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
  },

  backToSelection() {
    this.setData({
      selectedExpert: null,
      skippedSelection: false,
      // 不清空消息记录
      inputMessage: ''
    });
  }
}); 