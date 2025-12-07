import type { Mode } from '../types';

interface KeySelectorProps {
  tonic: number;
  mode: Mode;
  onTonicChange: (tonic: number) => void;
  onModeChange: (mode: Mode) => void;
}

const TONIC_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const MODES: Mode[] = ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'];

export const KeySelector: React.FC<KeySelectorProps> = ({ tonic, mode, onTonicChange, onModeChange }) => {
  return (
    <div className="key-selector">
      <div className="control-group">
        <label htmlFor="tonic">Tonic:</label>
        <select id="tonic" value={tonic} onChange={(e) => onTonicChange(Number(e.target.value))}>
          {TONIC_NAMES.map((name, index) => (
            <option key={index} value={index}>
              {name}
            </option>
          ))}
        </select>
      </div>
      <div className="control-group">
        <label htmlFor="mode">Mode:</label>
        <select id="mode" value={mode} onChange={(e) => onModeChange(e.target.value as Mode)}>
          {MODES.map((m) => (
            <option key={m} value={m}>
              {m.charAt(0).toUpperCase() + m.slice(1)}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};
