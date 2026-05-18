<script setup lang="ts">
import { Play, Pause, Heart } from 'lucide-vue-next';
import type { AudioFile } from '@/types';

interface Props {
  track: AudioFile;
  isPlaying?: boolean;
  isLast?: boolean;
  isFavorited?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  isPlaying: false,
  isLast: false,
  isFavorited: false,
});

const emit = defineEmits<{
  play: [track: AudioFile];
  toggleFavorite: [trackId: string];
}>();

const handlePlay = () => {
  emit('play', props.track);
};

const handleToggleFavorite = () => {
  emit('toggleFavorite', props.track.id);
};
</script>

<template>
  <v-list-item
    :class="[
      isPlaying ? 'bg-purple-50' : '',
      !isLast ? 'border-b border-gray-100' : '',
      'py-4'
    ]"
  >
    <v-list-item-title class="font-medium text-gray-900">
      {{ track.title }}
    </v-list-item-title>

    <v-list-item-subtitle class="text-sm text-gray-500">
      {{ track.artist }}
    </v-list-item-subtitle>

    <template #append>
      <div class="flex items-center gap-2 ml-2">
        <v-btn
          :icon="true"
          size="small"
          variant="text"
          color="grey-lighten-2"
          @click="handleToggleFavorite"
        >
          <Heart
            :size="20"
            :fill="isFavorited ? 'currentColor' : 'none'"
            :class="isFavorited ? 'text-green-600' : 'text-gray-400'"
          />
        </v-btn>

        <v-btn
          :icon="true"
          size="small"
          rounded="circle"
          :color="isPlaying ? 'primary' : 'grey-lighten-2'"
          @click="handlePlay"
        >
          <Pause v-if="isPlaying" :size="16" />
          <Play v-else :size="16" />
        </v-btn>
      </div>
    </template>
  </v-list-item>
</template>