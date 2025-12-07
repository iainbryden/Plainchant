import { useState } from 'react';

interface CantusFirmusControlsProps {
  onGenerate: (length: number, seed?: number) => void;
  isLoading: boolean;
}

export const CantusFirmusControls: React.FC<CantusFirmusControlsProps> = ({ onGenerate, isLoading }) => {
  const [length, setLength] = useState(8);
  const [seed, setSeed] = useState('');

  const handleGenerate = () => {
    const seedValue = seed ? Number(seed) : undefined;
    onGenerate(length, seedValue);
  };

  return (
    <div className="cantus-firmus-controls">
      <h3>Cantus Firmus</h3>
      <div className="control-group">
        <label htmlFor="cf-length">Length:</label>
        <input
          id="cf-length"
          type="number"
          min="4"
          max="16"
          value={length}
          onChange={(e) => setLength(Number(e.target.value))}
        />
      </div>
      <div className="control-group">
        <label htmlFor="cf-seed">Seed (optional):</label>
        <input
          id="cf-seed"
          type="number"
          value={seed}
          onChange={(e) => setSeed(e.target.value)}
          placeholder="Random"
        />
      </div>
      <button onClick={handleGenerate} disabled={isLoading}>
        {isLoading ? 'Generating...' : 'Generate CF'}
      </button>
    </div>
  );
};
