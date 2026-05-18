<script setup lang="ts">
import { Heart } from 'lucide-vue-next';
import type { AudioFile } from '@/types';
import AudioTrack from './AudioTrack.vue';
import { audioFiles } from '@/data/audioFiles';

interface Props {
  currentTrack: AudioFile | null;
  isPlaying: boolean;
  favoritedTracks: Set<string>;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  play: [track: AudioFile];
  toggleFavorite: [trackId: string];
}>();

const handlePlay = (track: AudioFile) => {
  emit('play', track);
};

const handleToggleFavorite = (trackId: string) => {
  emit('toggleFavorite', trackId);
};
</script>

<template>
  <div class="mb-8 flex items-center justify-between">
    <div class="flex flex-col gap-y-2">
      <div class="text-3xl font-medium text-gray-900">Nature Soundscape</div>
      <div class="text-sm text-gray-500 mt-1">Immerse yourself in the sounds of the natural world</div>
    </div>
    <div class="flex items-center gap-2 text-gray-700">
      <Heart :size="20" fill="currentColor" class="text-green-600" />
      <span class="text-lg font-medium">{{ favoritedTracks.size }}</span>
    </div>
  </div>
  <v-card class="rounded-xl" elevation="1">
    <v-list>
      <AudioTrack v-for="(track, index) in audioFiles" :key="track.id" :track="track"
        :is-playing="props.isPlaying && currentTrack?.id === track.id" :is-favorited="favoritedTracks.has(track.id)"
        :is-last="index === audioFiles.length - 1" @play="handlePlay" @toggle-favorite="handleToggleFavorite" />
    </v-list>
  </v-card>
</template>
