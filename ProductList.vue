<script setup lang="ts">
import type { Product } from '../types';
import ProductCard from './ProductCard.vue';

interface Props {
  products: Product[];
  loading?: boolean;
}

defineProps<Props>();
</script>

<template>
  <div>
    <v-row v-if="loading">
      <v-col v-for="n in 6" :key="n" cols="12" sm="6" md="4">
        <v-skeleton-loader type="card" />
      </v-col>
    </v-row>

    <v-alert v-else-if="products.length === 0" type="info" variant="tonal">
      No products found matching your filters.
    </v-alert>

    <v-row v-else>
      <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
      >
        <ProductCard
          :product="product"
          :show-add-to-cart="true"
          :show-quantity-controls="false"
        />
      </v-col>
    </v-row>
  </div>
</template>
