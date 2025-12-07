import { useState } from 'react';

interface PlaybackControlsProps {
  onPlay: () => Promise<void>;
  onStop: () => void;
  disabled: boolean;
  tempo: number;
  onTempoChange: (tempo: number) => void;
}

export const PlaybackControls: React.FC<PlaybackControlsProps> = ({
  onPlay,
  onStop,
  disabled,
  tempo,
  onTempoChange,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePlay = async () => {
    setIsPlaying(true);
    await onPlay();
    // Auto-stop after playback duration (approximate)
    setTimeout(() => setIsPlaying(false), 10000);
  };

  const handleStop = () => {
    setIsPlaying(false);
    onStop();
  };

  return (
    <div className="playback-controls">
      <h4>Audio Playback</h4>
      <div className="playback-buttons">
        <button onClick={handlePlay} disabled={disabled || isPlaying}>
          ▶ Play
        </button>
        <button onClick={handleStop} disabled={!isPlaying}>
          ⏹ Stop
        </button>
      </div>
      <div className="tempo-control">
        <label htmlFor="tempo">Tempo: {tempo} BPM</label>
        <input
          id="tempo"
          type="range"
          min="40"
          max="200"
          value={tempo}
          onChange={(e) => onTempoChange(Number(e.target.value))}
        />
      </div>
    </div>
  );
};
