const audio = document.getElementById("audio");
const playPauseBtn = document.getElementById("playPauseBtn");
const shuffleBtn = document.getElementById("shuffleBtn");
const volumeSlider = document.getElementById("volume");
const trackTitle = document.getElementById("trackTitle");

const playlist = [
  { title: "Forest", src: "music/forest.mp3" },
  { title: "Rain", src: "music/rain.mp3" },
  { title: "Space", src: "music/space.mp3" },
];

let currentTrackIndex = 0;

// Set initial volume
audio.volume = volumeSlider.value;

// Load track
function loadTrack(index) {
  const track = playlist[index];
  audio.src = track.src;
  trackTitle.textContent = "Track: " + track.title;
  audio.load();
}

// Shuffle and play
function shuffleAndPlay() {
  currentTrackIndex = Math.floor(Math.random() * playlist.length);
  loadTrack(currentTrackIndex);
  audio.play();
  playPauseBtn.textContent = "⏸ Pause";
}

// Play/pause logic
playPauseBtn.addEventListener("click", () => {
  if (audio.paused) {
    audio.play();
    playPauseBtn.textContent = "⏸ Pause";
  } else {
    audio.pause();
    playPauseBtn.textContent = "▶️ Play";
  }
});

// Shuffle logic
shuffleBtn.addEventListener("click", () => {
  shuffleAndPlay();
});

// Volume control
volumeSlider.addEventListener("input", () => {
  audio.volume = volumeSlider.value;
});

// Load first track on page load
loadTrack(currentTrackIndex);
