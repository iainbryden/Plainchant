import { useState } from 'react';
import { generateCantusFirmus, generateCounterpoint, evaluateCounterpoint, generateMultiVoice, generateSecondSpecies, generateThirdSpecies, generateFifthSpecies } from './services/apiClient';
import { KeySelector } from './components/KeySelector';
import { VoiceRangeSelector } from './components/VoiceRangeSelector';
import { VoiceCountSelector } from './components/VoiceCountSelector';
import { VoicingSelector } from './components/VoicingSelector';
import { SpeciesSelector } from './components/SpeciesSelector';
import { CantusFirmusControls } from './components/CantusFirmusControls';
import { CounterpointControls } from './components/CounterpointControls';
import { NoteList } from './components/NoteList';
import { ViolationsList } from './components/ViolationsList';
import { ScoreRenderer } from './components/ScoreRenderer';
import { PlaybackControls } from './components/PlaybackControls';
import { audioEngine } from './utils/audioEngine';
import type { Mode, VoiceRange, RuleViolation, SpeciesType } from './types';
import './App.css';

function App() {
  const [tonic, setTonic] = useState(0);
  const [mode, setMode] = useState<Mode>('ionian');
  const [cfVoiceRange, setCfVoiceRange] = useState<VoiceRange>('alto');
  const [species, setSpecies] = useState<SpeciesType>('first');
  
  const [cfNotes, setCfNotes] = useState<number[]>([]);
  const [cpNotes, setCpNotes] = useState<number[]>([]);
  const [allVoices, setAllVoices] = useState<any[][]>([]);
  const [voiceRanges, setVoiceRanges] = useState<string[]>([]);
  const [voiceCount, setVoiceCount] = useState(2);
  const [useBass, setUseBass] = useState(false);
  const [violations, setViolations] = useState<RuleViolation[]>([]);
  
  const [loadingCf, setLoadingCf] = useState(false);
  const [loadingCp, setLoadingCp] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tempo, setTempo] = useState(120);

  const handleGenerateCf = async (length: number, seed?: number) => {
    setLoadingCf(true);
    setError(null);
    setCpNotes([]);
    setViolations([]);
    
    try {
      const result = await generateCantusFirmus({ tonic, mode, length, voice_range: cfVoiceRange, seed });
      const pitches = result.notes.map((note: any) => note.midi);
      setCfNotes(pitches);
    } catch (err) {
      console.error('Failed to generate Cantus Firmus:', err);
      setError('Failed to generate Cantus Firmus. Please try again.');
    } finally {
      setLoadingCf(false);
    }
  };

  const handleGenerateCp = async (seed?: number) => {
    setLoadingCp(true);
    setError(null);
    
    try {
      if (voiceCount === 2) {
        let result;
        const params = { tonic, mode, cf_notes: cfNotes, cf_voice_range: cfVoiceRange, seed };
        
        switch (species) {
          case 'second':
            result = await generateSecondSpecies(params);
            break;
          case 'third':
            result = await generateThirdSpecies(params);
            break;
          case 'fifth':
            result = await generateFifthSpecies(params);
            break;
          default:
            result = await generateCounterpoint(params);
        }
        
        setCpNotes(result.cp_notes.map((n: any) => n.midi));
        setAllVoices([]);
        setViolations(result.violations || []);
      } else {
        const result = await generateMultiVoice({
          tonic,
          mode,
          cf_notes: cfNotes,
          cf_voice_range: cfVoiceRange,
          num_voices: voiceCount,
          use_bass: useBass,
          seed,
        });
        const voices = result.voices.map(v => v.notes);
        const ranges = result.voices.map(v => v.voice_range);
        setAllVoices(voices);
        setVoiceRanges(ranges);
        setCpNotes([]);
        setViolations(result.violations || []);
      }
    } catch (err) {
      console.error('Failed to generate Counterpoint:', err);
      setError('Failed to generate Counterpoint. Please try again.');
    } finally {
      setLoadingCp(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Species Counterpoint Generator</h1>
        <p className="subtitle">First Species - Two Voice Counterpoint</p>
      </header>

      <main>
        {error && <div className="error-message">{error}</div>}

        <section className="controls-panel">
          <KeySelector tonic={tonic} mode={mode} onTonicChange={setTonic} onModeChange={setMode} />
          <VoiceRangeSelector value={cfVoiceRange} onChange={setCfVoiceRange} label="CF Voice" />
          <VoiceCountSelector value={voiceCount} onChange={setVoiceCount} disabled={loadingCf || loadingCp} />
          {voiceCount === 3 && <VoicingSelector value={useBass} onChange={setUseBass} disabled={loadingCf || loadingCp} />}
          {voiceCount === 2 && <SpeciesSelector value={species} onChange={setSpecies} disabled={loadingCf || loadingCp} />}
          <CantusFirmusControls onGenerate={handleGenerateCf} isLoading={loadingCf} />
          <CounterpointControls onGenerate={handleGenerateCp} isLoading={loadingCp} disabled={!cfNotes || cfNotes.length === 0} />
        </section>

        <section className="results-panel">
          <ScoreRenderer 
            cfNotes={cfNotes} 
            cpNotes={voiceCount === 2 ? cpNotes : []} 
            allVoices={allVoices}
            voiceRanges={voiceRanges}
            tonic={tonic} 
            mode={mode}
            violationIndices={violations?.map(v => v.note_indices).flat() || []}
          />
          {cfNotes && cfNotes.length > 0 && (
            <PlaybackControls
              onPlay={async () => {
                if (allVoices.length > 0) {
                  const midiVoices = allVoices.map(v => v.map((n: any) => typeof n === 'number' ? n : n.midi));
                  await audioEngine.playMultipleVoices(midiVoices, tempo);
                } else if (cpNotes && cpNotes.length > 0) {
                  await audioEngine.playTwoVoices(cpNotes, cfNotes, tempo);
                } else {
                  await audioEngine.playSequence(cfNotes, tempo);
                }
              }}
              onStop={() => audioEngine.stop()}
              disabled={!cfNotes || cfNotes.length === 0}
              tempo={tempo}
              onTempoChange={setTempo}
            />
          )}
          {allVoices.length > 0 ? (
            allVoices.map((voice, idx) => (
              <NoteList key={idx} notes={voice.map((n: any) => typeof n === 'number' ? n : n.midi)} label={`Voice ${idx + 1}`} />
            ))
          ) : (
            <>
              <NoteList notes={cfNotes} label="Cantus Firmus" />
              <NoteList notes={cpNotes} label="Counterpoint" />
            </>
          )}
          {(cpNotes.length > 0 || allVoices.length > 0) && <ViolationsList violations={violations} />}
        </section>
      </main>
    </div>
  );
}

export default App;
