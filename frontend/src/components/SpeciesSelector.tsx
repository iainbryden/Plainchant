import type { SpeciesType } from '../types';

interface SpeciesSelectorProps {
  value: SpeciesType;
  onChange: (species: SpeciesType) => void;
  disabled?: boolean;
}

export const SpeciesSelector: React.FC<SpeciesSelectorProps> = ({ 
  value, 
  onChange, 
  disabled = false 
}) => {
  return (
    <div className="control-group">
      <label htmlFor="species-select">Species:</label>
      <select
        id="species-select"
        value={value}
        onChange={(e) => onChange(e.target.value as SpeciesType)}
        disabled={disabled}
      >
        <option value="first">First (1:1)</option>
        <option value="second">Second (2:1)</option>
        <option value="third">Third (4:1)</option>
        <option value="fifth">Fifth (Florid)</option>
      </select>
    </div>
  );
};
