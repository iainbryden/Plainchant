import type { VoiceRange } from '../types';

interface VoiceRangeSelectorProps {
  value: VoiceRange;
  onChange: (range: VoiceRange) => void;
  label?: string;
}

const VOICE_RANGES: VoiceRange[] = ['soprano', 'alto', 'tenor', 'bass'];

export const VoiceRangeSelector: React.FC<VoiceRangeSelectorProps> = ({ value, onChange, label = 'Voice Range' }) => {
  return (
    <div className="voice-range-selector">
      <label>{label}:</label>
      <div className="radio-group">
        {VOICE_RANGES.map((range) => (
          <label key={range} className="radio-label">
            <input
              type="radio"
              name={`voice-range-${label}`}
              value={range}
              checked={value === range}
              onChange={(e) => onChange(e.target.value as VoiceRange)}
            />
            {range.charAt(0).toUpperCase() + range.slice(1)}
          </label>
        ))}
      </div>
    </div>
  );
};
