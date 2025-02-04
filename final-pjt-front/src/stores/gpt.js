import { defineStore } from "pinia";
import axios from "axios";

export const useGptStore = defineStore("gpt", {
  state: () => ({
    chatMessages: [],
    apiKey: "api_key",
    apiUrl: "https://api.openai.com/v1/chat/completions",
    // 학습 데이터 입력 칸
    preTrainedData: [
      {
        role: "system",
        content: `
          당신은 금융 회사에서 100년 일한 금융상품 추천 챗봇입니다.
          누구보다 친절하게 금융 상품에 대해 설명하는 챗봇으로 인기가 많습니다.
          사용자가 금융 상품에 대해 물어보면 친절하게 설명해주세요.
          예금, 적금, 대출 등 금융상품에 대한 전문적인 설명을 제공해주세요.
        `
      }
    ],
  }),
  actions: {
    addChat(type, content) {
      this.chatMessages.push({ type, content });
    },
    async sendChat(userMessage) {
      this.addChat("send", userMessage);

      const headers = {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      };

      // 사전 정의된 학습 데이터와 대화 내용을 결합
      const messages = [
        ...this.preTrainedData,
        ...this.chatMessages.map((msg) => ({
          role: msg.type === "send" ? "user" : "assistant",
          content: msg.content
        }))
      ];

      try {
        const response = await axios.post(this.apiUrl, {
          model: "gpt-4o-mini",
          messages,
        }, { headers });

        const assistantMessage = response.data.choices[0].message.content;
        this.addChat("receive", assistantMessage);
      } catch (error) {
        console.error(error.response?.data || error.message);
      }
    },
  },
});