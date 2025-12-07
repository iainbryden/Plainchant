interface NoteListProps {
  notes: number[];
  label: string;
}

const PITCH_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

const midiToNoteName = (midi: number): string => {
  const pitchClass = midi % 12;
  const octave = Math.floor(midi / 12) - 1;
  return `${PITCH_NAMES[pitchClass]}${octave}`;
};

export const NoteList: React.FC<NoteListProps> = ({ notes = [], label }) => {
  if (!notes || notes.length === 0) return null;

  return (
    <div className="note-list">
      <h4>{label}</h4>
      <div className="notes">
        {notes.map((midi, index) => (
          <span key={index} className="note">
            {midiToNoteName(midi)}
          </span>
        ))}
      </div>
      <p className="midi-values">MIDI: [{notes.join(', ')}]</p>
    </div>
  );
};
