interface VoiceCountSelectorProps {
  value: number;
  onChange: (count: number) => void;
  disabled?: boolean;
}

export const VoiceCountSelector: React.FC<VoiceCountSelectorProps> = ({ value, onChange, disabled = false }) => {
  return (
    <div className="voice-count-selector">
      <label>Number of Voices:</label>
      <div className="radio-group">
        {[2, 3, 4].map((count) => (
          <label key={count}>
            <input
              type="radio"
              name="voiceCount"
              value={count}
              checked={value === count}
              onChange={(e) => onChange(Number(e.target.value))}
              disabled={disabled}
            />
            {count} voices
          </label>
        ))}
      </div>
    </div>
  );
};
