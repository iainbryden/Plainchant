interface VoicingSelectorProps {
  value: boolean;
  onChange: (useBass: boolean) => void;
  disabled?: boolean;
}

export const VoicingSelector: React.FC<VoicingSelectorProps> = ({ value, onChange, disabled = false }) => {
  return (
    <div className="voicing-selector">
      <label>3-Voice Voicing:</label>
      <div className="radio-group">
        <label>
          <input
            type="radio"
            name="voicing"
            checked={!value}
            onChange={() => onChange(false)}
            disabled={disabled}
          />
          SAT (High)
        </label>
        <label>
          <input
            type="radio"
            name="voicing"
            checked={value}
            onChange={() => onChange(true)}
            disabled={disabled}
          />
          SAB (Low)
        </label>
      </div>
    </div>
  );
};
