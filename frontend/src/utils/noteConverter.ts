// Convert MIDI numbers to VexFlow note format

const PITCH_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

export const midiToVexFlowNote = (midi: number): string => {
  if (midi === undefined || midi === null) {
    console.error('Invalid MIDI value:', midi);
    return 'C/4'; // Default fallback
  }
  const pitchClass = midi % 12;
  const octave = Math.floor(midi / 12) - 1;
  const noteName = PITCH_NAMES[pitchClass];
  
  // VexFlow uses 'b' for flats, convert sharps to flats where appropriate
  const vexNote = noteName.replace('#', '#');
  
  return `${vexNote}/${octave}`;
};

export const midiToNoteName = (midi: number): string => {
  const pitchClass = midi % 12;
  const octave = Math.floor(midi / 12) - 1;
  return `${PITCH_NAMES[pitchClass]}${octave}`;
};

export const determineClef = (notes: number[]): 'treble' | 'bass' => {
  if (notes.length === 0) return 'treble';
  const avgMidi = notes.reduce((sum, n) => sum + n, 0) / notes.length;
  return avgMidi < 60 ? 'bass' : 'treble';
};

export const getKeySignature = (tonic: number, mode: string): string => {
  // Simplified key signature mapping for common keys
  const keyMap: Record<string, string> = {
    '0-ionian': 'C',
    '2-ionian': 'D',
    '4-ionian': 'E',
    '5-ionian': 'F',
    '7-ionian': 'G',
    '9-ionian': 'A',
    '11-ionian': 'B',
    '9-aeolian': 'Am',
  };
  
  return keyMap[`${tonic}-${mode}`] || 'C';
};
