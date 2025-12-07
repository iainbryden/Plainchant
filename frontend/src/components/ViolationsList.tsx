import type { RuleViolation } from '../types';

interface ViolationsListProps {
  violations: RuleViolation[];
}

export const ViolationsList: React.FC<ViolationsListProps> = ({ violations = [] }) => {
  if (!violations || violations.length === 0) {
    return (
      <div className="violations-list success">
        <h4>✓ No Violations</h4>
        <p>The counterpoint follows all first species rules!</p>
      </div>
    );
  }

  const errorCount = violations.filter((v) => v.severity === 'error').length;
  const warningCount = violations.filter((v) => v.severity === 'warning').length;

  return (
    <div className="violations-list">
      <h4>Rule Violations ({violations.length})</h4>
      <p className="summary">
        {errorCount > 0 && <span className="error-count">{errorCount} errors</span>}
        {errorCount > 0 && warningCount > 0 && ', '}
        {warningCount > 0 && <span className="warning-count">{warningCount} warnings</span>}
      </p>
      <ul>
        {violations.map((violation, index) => (
          <li key={index} className={`violation ${violation.severity}`}>
            <strong>{violation.rule_code}</strong>: {violation.description}
            {violation.note_indices && violation.note_indices.length > 0 && (
              <span className="location"> (notes: {violation.note_indices.join(', ')})</span>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};
