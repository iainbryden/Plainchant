import * as Tone from 'tone';

export class AudioEngine {
  private synth: Tone.PolySynth | null = null;
  private isInitialized = false;

  constructor() {
    // Don't create synth until user interaction
  }

  private createSynth() {
    if (!this.synth) {
      this.synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: 'sine' },
        envelope: {
          attack: 0.02,
          decay: 0.1,
          sustain: 0.3,
          release: 1,
        },
      }).toDestination();
    }
  }

  async initialize(): Promise<void> {
    if (!this.isInitialized) {
      this.createSynth();
      await Tone.start();
      this.isInitialized = true;
    }
  }

  midiToNote(midi: number): string {
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const octave = Math.floor(midi / 12) - 1;
    const note = notes[midi % 12];
    return `${note}${octave}`;
  }

  playNote(midi: number, duration: string = '1n'): void {
    if (!this.synth) return;
    const note = this.midiToNote(midi);
    this.synth.triggerAttackRelease(note, duration);
  }

  async playSequence(notes: number[], tempo: number = 120): Promise<void> {
    await this.initialize();
    if (!this.synth) return;
    
    Tone.Transport.bpm.value = tempo;
    const noteDuration = '1n';
    
    const now = Tone.now();
    notes.forEach((midi, index) => {
      const time = now + index * (240 / tempo);
      this.synth!.triggerAttackRelease(this.midiToNote(midi), noteDuration, time);
    });
  }

  async playTwoVoices(
    voice1: number[],
    voice2: number[],
    tempo: number = 120
  ): Promise<void> {
    await this.initialize();
    if (!this.synth) return;
    
    Tone.Transport.bpm.value = tempo;
    const noteDuration = '1n';
    
    const now = Tone.now();
    const maxLength = Math.max(voice1.length, voice2.length);
    
    for (let i = 0; i < maxLength; i++) {
      const time = now + i * (240 / tempo);
      
      if (i < voice1.length) {
        this.synth.triggerAttackRelease(this.midiToNote(voice1[i]), noteDuration, time);
      }
      if (i < voice2.length) {
        this.synth.triggerAttackRelease(this.midiToNote(voice2[i]), noteDuration, time);
      }
    }
  }

  async playMultipleVoices(
    voices: number[][],
    tempo: number = 120
  ): Promise<void> {
    await this.initialize();
    if (!this.synth) return;
    
    Tone.Transport.bpm.value = tempo;
    const noteDuration = '1n';
    
    const now = Tone.now();
    const maxLength = Math.max(...voices.map(v => v.length));
    
    for (let i = 0; i < maxLength; i++) {
      const time = now + i * (240 / tempo);
      
      voices.forEach(voice => {
        if (i < voice.length) {
          this.synth!.triggerAttackRelease(this.midiToNote(voice[i]), noteDuration, time);
        }
      });
    }
  }

  stop(): void {
    if (this.synth) {
      this.synth.releaseAll();
    }
  }

  setVolume(db: number): void {
    if (this.synth) {
      this.synth.volume.value = db;
    }
  }

  dispose(): void {
    if (this.synth) {
      this.synth.dispose();
    }
  }
}

export const audioEngine = new AudioEngine();
