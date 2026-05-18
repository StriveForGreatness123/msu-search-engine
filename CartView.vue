<script setup lang="ts">
import { computed, ref } from 'vue';
import confetti from 'canvas-confetti';
import { useCart } from '../composables/useCart';
import ProductCard from '../components/ProductCard.vue';

const {
  cartItems,
  cartCount,
  updateQuantity,
  removeFromCart,
  cartTotal,
  clearCart,
} = useCart();

const showSuccessMessage = ref(false);

const cartProducts = computed(() => {
  return cartItems.value.map((item) => ({
    ...item.product,
    quantity: item.quantity,
  }));
});

const formattedTotal = computed(() => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(cartTotal.value);
});

const handleCheckout = () => {
  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 },
  });

  showSuccessMessage.value = true;
  clearCart();
};
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-6">Shopping Cart</h1>

    <v-alert
      v-if="cartItems.length === 0"
      type="info"
      variant="tonal"
      class="mb-4"
    >
      Your cart is empty. Start shopping to add items!
    </v-alert>

    <template v-else>
      <v-row>
        <v-col
          v-for="product in cartProducts"
          :key="product.id"
          cols="12"
          md="6"
          lg="3"
        >
          <ProductCard
            :product="product"
            :quantity="product.quantity"
            :show-add-to-cart="false"
            :show-quantity-controls="true"
            @update:quantity="(value) => updateQuantity(product.id, value)"
            @remove="removeFromCart(product.id)"
          />
        </v-col>
      </v-row>

      <v-card class="mt-6 pa-4" elevation="2">
        <v-card-title class="text-h5">Order Summary</v-card-title>

        <v-card-text>
          <div class="d-flex justify-space-between text-h6 mb-2">
            <span>Total Items:</span>
            <span class="font-weight-bold">{{ cartCount }}</span>
          </div>

          <div class="d-flex justify-space-between text-h6">
            <span>Total Cost:</span>
            <span class="text-primary font-weight-bold">{{ formattedTotal }}</span>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-btn color="error" variant="text" @click="clearCart">
            Clear Cart
          </v-btn>

          <v-spacer />

          <v-btn
            color="primary"
            variant="elevated"
            size="large"
            @click="handleCheckout"
          >
            Checkout
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <v-snackbar v-model="showSuccessMessage" color="success" :timeout="3000">
      Order placed successfully! Thank you for your purchase.
    </v-snackbar>
  </v-container>
</template>
