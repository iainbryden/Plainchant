import { useEffect, useRef } from 'react';
import { Renderer, Stave, StaveNote, Voice, Formatter, Accidental } from 'vexflow';
import { midiToVexFlowNote, determineClef, getKeySignature } from '../utils/noteConverter';
import type { Mode } from '../types';

interface ScoreRendererProps {
  cfNotes: number[];
  cpNotes: number[];
  allVoices?: number[][];
  tonic: number;
  mode: Mode;
  violationIndices?: number[];
}

export const ScoreRenderer: React.FC<ScoreRendererProps> = ({ 
  cfNotes = [], 
  cpNotes = [], 
  allVoices = [],
  tonic, 
  mode,
  violationIndices = []
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || (cfNotes.length === 0 && allVoices.length === 0)) return;

    // Clear previous render
    containerRef.current.innerHTML = '';

    const numNotes = cfNotes.length || (allVoices.length > 0 ? allVoices[0].length : 0);
    const width = Math.max(800, numNotes * 80);
    const numStaves = allVoices.length > 0 ? allVoices.length : (cpNotes.length > 0 ? 2 : 1);
    const height = numStaves * 150 + 50;

    // Create renderer
    const renderer = new Renderer(containerRef.current, Renderer.Backends.SVG);
    renderer.resize(width, height);
    const context = renderer.getContext();

    const cfClef = determineClef(cfNotes);
    const cpClef = cpNotes.length > 0 ? determineClef(cpNotes) : 'treble';
    const keySignature = getKeySignature(tonic, mode);

    try {
      if (allVoices.length > 0) {
        // Multi-voice rendering
        allVoices.forEach((voice, idx) => {
          const yPos = 40 + idx * 150;
          const stave = new Stave(10, yPos, width - 20);
          const clef = determineClef(voice);
          stave.addClef(clef).addKeySignature(keySignature).addTimeSignature('4/4');
          stave.setContext(context).draw();

          const staveNotes = voice.map((midi) => {
            const note = new StaveNote({
              keys: [midiToVexFlowNote(midi)],
              duration: 'w',
            });
            const noteName = midiToVexFlowNote(midi);
            if (noteName.includes('#')) {
              note.addModifier(new Accidental('#'), 0);
            }
            return note;
          });

          const voiceObj = new Voice({ numBeats: voice.length * 4, beatValue: 4 });
          voiceObj.addTickables(staveNotes);
          new Formatter().joinVoices([voiceObj]).format([voiceObj], width - 40);
          voiceObj.draw(context, stave);
        });
      } else if (cpNotes.length > 0) {
        // Two staves (counterpoint + cantus firmus)
        const cpStave = new Stave(10, 40, width - 20);
        cpStave.addClef(cpClef).addKeySignature(keySignature).addTimeSignature('4/4');
        cpStave.setContext(context).draw();

        const cfStave = new Stave(10, 180, width - 20);
        cfStave.addClef(cfClef).addKeySignature(keySignature).addTimeSignature('4/4');
        cfStave.setContext(context).draw();

        // Create notes
        const cpStaveNotes = cpNotes.map((midi, i) => {
          const note = new StaveNote({
            keys: [midiToVexFlowNote(midi)],
            duration: 'w',
          });
          
          // Add accidentals for sharps/flats
          const noteName = midiToVexFlowNote(midi);
          if (noteName.includes('#')) {
            note.addModifier(new Accidental('#'), 0);
          }
          
          // Highlight violations
          if (violationIndices.includes(i)) {
            note.setStyle({ fillStyle: 'red', strokeStyle: 'red' });
          }
          
          return note;
        });

        const cfStaveNotes = cfNotes.map((midi) => {
          const note = new StaveNote({
            keys: [midiToVexFlowNote(midi)],
            duration: 'w',
          });
          
          const noteName = midiToVexFlowNote(midi);
          if (noteName.includes('#')) {
            note.addModifier(new Accidental('#'), 0);
          }
          
          return note;
        });

        // Create voices and format
        const cpVoice = new Voice({ numBeats: cfNotes.length * 4, beatValue: 4 });
        cpVoice.addTickables(cpStaveNotes);

        const cfVoice = new Voice({ numBeats: cfNotes.length * 4, beatValue: 4 });
        cfVoice.addTickables(cfStaveNotes);

        new Formatter().joinVoices([cpVoice]).joinVoices([cfVoice]).format([cpVoice, cfVoice], width - 40);

        cpVoice.draw(context, cpStave);
        cfVoice.draw(context, cfStave);
      } else {
        // Single stave (cantus firmus only)
        const cfStave = new Stave(10, 40, width - 20);
        cfStave.addClef(cfClef).addKeySignature(keySignature).addTimeSignature('4/4');
        cfStave.setContext(context).draw();

        const cfStaveNotes = cfNotes.map((midi) => {
          const note = new StaveNote({
            keys: [midiToVexFlowNote(midi)],
            duration: 'w',
          });
          
          const noteName = midiToVexFlowNote(midi);
          if (noteName.includes('#')) {
            note.addModifier(new Accidental('#'), 0);
          }
          
          return note;
        });

        const cfVoice = new Voice({ numBeats: cfNotes.length * 4, beatValue: 4 });
        cfVoice.addTickables(cfStaveNotes);

        new Formatter().joinVoices([cfVoice]).format([cfVoice], width - 40);
        cfVoice.draw(context, cfStave);
      }
    } catch (error) {
      console.error('VexFlow rendering error:', error);
    }
  }, [cfNotes, cpNotes, allVoices, tonic, mode, violationIndices]);

  if ((!cfNotes || cfNotes.length === 0) && allVoices.length === 0) return null;

  return (
    <div className="score-renderer">
      <h4>Musical Notation</h4>
      <div ref={containerRef} className="score-container" />
    </div>
  );
};
