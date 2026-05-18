import { ref, computed, watch } from 'vue';
import type { Product, CartItem } from '../types';

const STORAGE_KEY = 'calis-electronics-cart';

// Singleton state - shared across all component instances
const cartItems = ref<CartItem[]>([]);

// Load from localStorage on initialization
const loadCart = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      cartItems.value = JSON.parse(stored);
    }
  } catch (error) {
    console.error('Failed to load cart from localStorage:', error);
  }
};

// Initialize cart from storage
loadCart();

// Persist to localStorage on changes
watch(
  cartItems,
  (newItems) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newItems));
    } catch (error) {
      console.error('Failed to save cart to localStorage:', error);
    }
  },
  { deep: true }
);

export function useCart() {
  const cartCount = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + item.quantity, 0);
  });

  const cartTotal = computed(() => {
    return cartItems.value.reduce(
      (sum, item) => sum + item.product.price * item.quantity,
      0
    );
  });

  const addToCart = (product: Product, quantity = 1) => {
    const existingIndex = cartItems.value.findIndex(
      (item) => item.product.id === product.id
    );

    if (existingIndex >= 0) {
      const existingItem = cartItems.value[existingIndex];
      if (existingItem) {
        existingItem.quantity += quantity;
      }
    } else {
      cartItems.value.push({ product, quantity });
    }
  };

  const removeFromCart = (productId: number) => {
    const index = cartItems.value.findIndex(
      (item) => item.product.id === productId
    );
    if (index >= 0) {
      cartItems.value.splice(index, 1);
    }
  };

  const updateQuantity = (productId: number, quantity: number) => {
    const item = cartItems.value.find(
      (item) => item.product.id === productId
    );
    if (item) {
      if (quantity <= 0) {
        removeFromCart(productId);
      } else {
        item.quantity = quantity;
      }
    }
  };

  const clearCart = () => {
    cartItems.value = [];
  };

  const isInCart = (productId: number) => {
    return cartItems.value.some((item) => item.product.id === productId);
  };

  return {
    cartItems: computed(() => cartItems.value),
    cartCount,
    cartTotal,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    isInCart,
  };
}
