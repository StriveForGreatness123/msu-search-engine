<script setup lang="ts">
import { computed } from 'vue';
import type { Product } from '../types';
import { useCart } from '../composables/useCart';

interface Props {
  product: Product;
  showAddToCart?: boolean;
  showQuantityControls?: boolean;
  quantity?: number;
}

const props = withDefaults(defineProps<Props>(), {
  showAddToCart: true,
  showQuantityControls: false,
  quantity: 0,
});

const emit = defineEmits<{
  (e: 'remove'): void;
  (e: 'update:quantity', value: number): void;
}>();

const { addToCart, isInCart } = useCart();

const typeColor = computed(() => {
  const colors: Record<string, string> = {
    CPU: '#1976D2',
    GPU: '#4CAF50',
    Motherboard: '#9C27B0',
    Case: '#FF9800',
    PowerSupply: '#F44336',
    RAM: '#009688',
  };

  return colors[props.product.type] || '#757575';
});

const formattedPrice = computed(() => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(props.product.price);
});

const specsList = computed(() => {
  return Object.entries(props.product.specs)
    .filter(([, value]) => value !== undefined)
    .slice(0, 4);
});

const handleAddToCart = () => {
  addToCart(props.product);
};

const incrementQuantity = () => {
  emit('update:quantity', props.quantity + 1);
};

const decrementQuantity = () => {
  if (props.quantity > 1) {
    emit('update:quantity', props.quantity - 1);
  } else {
    emit('remove');
  }
};
</script>

<template>
  <v-card class="h-100 d-flex flex-column" elevation="2">
    <div
      class="d-flex align-center justify-center position-relative"
      :style="{ backgroundColor: typeColor, height: '200px' }"
    >
      <span class="text-h6 text-white text-center px-4">
        {{ product.name }}
      </span>

      <v-chip
        color="white"
        class="ma-2 position-absolute"
        style="top: 0; left: 0"
        size="small"
      >
        {{ product.type }}
      </v-chip>
    </div>

    <v-card-title class="text-h6">
      {{ product.name }}
    </v-card-title>

    <v-card-subtitle class="text-h5 font-weight-bold text-primary">
      {{ formattedPrice }}
    </v-card-subtitle>

    <v-card-text class="flex-grow-1">
      <p class="text-body-2 mb-2">
        {{ product.description }}
      </p>

      <v-divider class="my-2" />

      <div class="d-flex flex-wrap">
        <v-chip
          v-for="[key, value] in specsList"
          :key="key"
          size="x-small"
          variant="outlined"
          class="ma-1"
        >
          {{ key }}: {{ value }}
        </v-chip>
      </div>
    </v-card-text>

    <v-card-actions v-if="showAddToCart">
      <v-btn
        color="primary"
        variant="elevated"
        block
        :disabled="isInCart(product.id)"
        @click="handleAddToCart"
      >
        <v-icon start>mdi-cart-plus</v-icon>
        {{ isInCart(product.id) ? 'In Cart' : 'Add to Cart' }}
      </v-btn>
    </v-card-actions>

    <v-card-actions v-if="showQuantityControls">
      <div class="d-flex align-center w-100 justify-center">
        <v-btn
          icon="mdi-minus"
          size="small"
          variant="outlined"
          @click="decrementQuantity"
        />

        <span class="mx-4 text-h6">
          {{ quantity }}
        </span>

        <v-btn
          icon="mdi-plus"
          size="small"
          variant="outlined"
          @click="incrementQuantity"
        />

        <v-spacer />

        <v-btn
          icon="mdi-delete"
          color="error"
          variant="text"
          @click="emit('remove')"
        />
      </div>
    </v-card-actions>
  </v-card>
</template>
