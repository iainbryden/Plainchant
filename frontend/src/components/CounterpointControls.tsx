import { useState } from 'react';

interface CounterpointControlsProps {
  onGenerate: (seed?: number) => void;
  isLoading: boolean;
  disabled: boolean;
}

export const CounterpointControls: React.FC<CounterpointControlsProps> = ({ onGenerate, isLoading, disabled }) => {
  const [seed, setSeed] = useState('');

  const handleGenerate = () => {
    const seedValue = seed ? Number(seed) : undefined;
    onGenerate(seedValue);
  };

  return (
    <div className="counterpoint-controls">
      <h3>Counterpoint (First Species)</h3>
      <div className="control-group">
        <label htmlFor="cp-seed">Seed (optional):</label>
        <input
          id="cp-seed"
          type="number"
          value={seed}
          onChange={(e) => setSeed(e.target.value)}
          placeholder="Random"
          disabled={disabled}
        />
      </div>
      <button onClick={handleGenerate} disabled={isLoading || disabled}>
        {isLoading ? 'Generating...' : 'Generate Counterpoint'}
      </button>
      {disabled && <p className="hint">Generate a Cantus Firmus first</p>}
    </div>
  );
};
