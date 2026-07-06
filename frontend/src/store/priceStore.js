// store/priceStore.js
import { create } from "zustand";

export const usePriceStore = create((set) => ({
  livePrices: {},    // { NVDA: { price, change, changePercent, updatedAt }, TSLA: {...} }

  updatePrice: (ticker, priceData) =>
    set((state) => ({
      livePrices: { ...state.livePrices, [ticker]: priceData },
    })),
}));
