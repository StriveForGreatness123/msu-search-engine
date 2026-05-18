<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue';
import type { AudioFile } from './types';
import AudioLibrary from './components/AudioLibrary.vue';
import { audioFiles } from './data/audioFiles';

// Global state
const currentTrack = ref<AudioFile | null>(null);
const isPlaying = ref(false);
const audioRef = ref<HTMLAudioElement | null>(null);
const favoritedTracks = ref<Set<string>>(new Set());

// Playback controls
const handlePlay = (track: AudioFile) => {
  if (currentTrack.value?.id === track.id) {
    // Toggle play/pause if same track
    isPlaying.value = !isPlaying.value;
  } else {
    // Play new track
    currentTrack.value = track;
    isPlaying.value = true;
  }
};

// Favorites controls
const toggleFavorite = (trackId: string) => {
  if (favoritedTracks.value.has(trackId)) {
    favoritedTracks.value.delete(trackId);
  } else {
    favoritedTracks.value.add(trackId);
  }
  // Trigger reactivity
  favoritedTracks.value = new Set(favoritedTracks.value);
};

// Audio event handlers
const handleEnded = () => {
  isPlaying.value = false;
};

// Watch for isPlaying changes to play/pause the audio
watch(
  () => isPlaying.value,
  async (playing) => {
    // Wait for next tick if audioRef is null (first render)
    if (!audioRef.value) {
      await nextTick();
    }

    if (audioRef.value) {
      if (playing) {
        // Wait for audio to be ready before playing
        if (audioRef.value.readyState >= 2) {
          audioRef.value.play().catch((error) => {
            console.log('Play failed:', error);
          });
        } else {
          // Wait for canplay event
          const playWhenReady = () => {
            audioRef.value?.play().catch((error) => {
              console.log('Play failed:', error);
            });
            audioRef.value?.removeEventListener('canplay', playWhenReady);
          };
          audioRef.value.addEventListener('canplay', playWhenReady, { once: true });
        }
      } else {
        audioRef.value.pause();
      }
    } else {
      console.log('audioRef.value is still null after nextTick!');
    }
  }
);

// Watch for track changes
watch(
  () => currentTrack.value?.url,
  async () => {
    await nextTick();
    if (audioRef.value && currentTrack.value) {
      audioRef.value.load();
      // If already playing, start playing the new track
      if (isPlaying.value) {
        const playWhenReady = () => {
          audioRef.value?.play().catch((error) => {
            console.log('Play failed on track change:', error);
          });
        };
        if (audioRef.value.readyState >= 2) {
          playWhenReady();
        } else {
          audioRef.value.addEventListener('canplay', playWhenReady, { once: true });
        }
      }
    }
  }
);

onMounted(() => {
  if (audioRef.value) {
    audioRef.value.addEventListener('ended', handleEnded);
  }
});

onUnmounted(() => {
  if (audioRef.value) {
    audioRef.value.removeEventListener('ended', handleEnded);
  }
});
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50">
    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <AudioLibrary
        :current-track="currentTrack"
        :is-playing="isPlaying"
        :favorited-tracks="favoritedTracks"
        @play="handlePlay"
        @toggle-favorite="toggleFavorite"
      />
    </main>

    <!-- Hidden Audio Element -->
    <audio
      v-if="currentTrack"
      ref="audioRef"
      :src="currentTrack.url"
    />

    <!-- Preload all audio files -->
    <audio
      v-for="track in audioFiles"
      :key="'preload-' + track.id"
      :src="track.url"
      preload="auto"
      style="display: none"
    />
  </div>
</template>
